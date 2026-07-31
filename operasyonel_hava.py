#!/usr/bin/env python3
"""
operasyonel_hava.py  ·  YangınRiski.com  (durum tasiyan surum)

Her sabah 60 gunluk gecmisi yeniden cekmek yerine, FWI kodlarinin dunku halini
data/fwi_durum.json dosyasindan okur, yalnizca yeni gunleri isleyip ilerletir ve
yeni durumu geri yazar. Boylece istek basina gun sayisi 67'den 14'e iner ve
gunluk agirlikli Open-Meteo maliyeti yaklasik 25.100'den 5.254'e duser
(ucretsiz gunluk sinir 10.000).

Neden 7 gun gecmis isteniyor: agirlik formulunde gun sayisinin asgarisi 14
(7 gecmis + 7 tahmin). Yani gecmis 7 gun bedavaya geliyor. Faydasi: kosu
birkac gun patlarsa eksik gunler kendiliginden tamamlanir.

Modlar:
  ILIK  (varsayilan)  durum dosyasi varsa: past_days=7, durumu ilerletir.
  SOGUK (ilk kurulum) durum yoksa, bozuksa ya da bosluk 7 gunu asarsa:
        past_days=60 ile tam isinma yapar ve durumu sifirdan kurar.
        Bu kosu pahalidir (yaklasik 25.100 agirlikli cagri), bir kez ve
        tercihen kendi bilgisayarinda calistirilmalidir.
  OM_SOGUK=1 ile soguk baslangic elle zorlanabilir.
  Izgaraya yeni nokta eklenirse eskiler ILIK kalir, yalnizca yeniler 60 gunluk
  pencereyle isinir (kismi isinma). Eksik oran OM_KISMI_UST'u (varsayilan 0,50)
  asarsa tam soguk baslangica dusulur.

Calistir:  python operasyonel_hava.py
Cikti:     operasyonel_tahmin.json   (operasyonel_hafta.py'ye girdi, semasi degismedi)
           data/fwi_durum.json       (ertesi gunun baslangic durumu)

Dayaniklilik: zaman asimi, baglanti hatasi, 429 ve 5xx kademeli beklemeyle
tekrar denenir. Obekler arasi tempoyu yalnizca 429 (kota) yukseltir; zaman asimi
yukseltmez, cunku beklemek zaman asimini cozmez, sadece kosuyu uzatir. bir batch yine de alinamazsa o noktalar atlanir ve durumlari
dokunulmadan kalir (ertesi gun bosluk kapanir). Kayip esigi asilirsa betik
hata koduyla durur, panel son basarili gunun dosyasinda kalir.
"""
import requests, json, time, os, sys, datetime
import fwi

UCRETSIZ_URL = "https://api.open-meteo.com/v1/forecast"
MUSTERI_URL = "https://customer-api.open-meteo.com/v1/forecast"
# Anahtar ortam degiskeninden gelir, koda yazilmaz. Yoksa ucretsiz uca duser.
OM_APIKEY = os.environ.get("OM_APIKEY", "").strip()
FORECAST_URL = MUSTERI_URL if OM_APIKEY else UCRETSIZ_URL
BAZ_FILE = "noktalar_baz_grid.json"
CIKTI = "operasyonel_tahmin.json"
DURUM = os.path.join("data", "fwi_durum.json")
DAILY = "temperature_2m_max,relative_humidity_2m_mean,wind_speed_10m_max,precipitation_sum"


def ayar(ad, vars_, tip=int):
    try:
        return tip(os.environ.get(ad, vars_))
    except (TypeError, ValueError):
        return tip(vars_)


FCST_DAYS = 7
ILIK_GECMIS = ayar("OM_PAST_DAYS", 7)       # gunluk kosuda gecmis pencere
SOGUK_GECMIS = ayar("OM_ISINMA", 60)        # tam isinmada gecmis pencere
MAX_BOSLUK = ayar("OM_MAX_BOSLUK", 7)       # bu kadar gunden uzun boslukta soguk baslangic
KISMI_UST = ayar("OM_KISMI_UST", 0.50, float)  # bu orandan cok nokta eksikse tam soguk baslangic
# Ucretli uctaki gunluk ve saatlik sinir kalktigi icin tempo hizlandirilabilir.
B = ayar("OM_BATCH", 100 if OM_APIKEY else 25)
SLEEP = ayar("OM_SLEEP", 1 if OM_APIKEY else 13, float)
# 30 saniye ticari ucta fazla dardi: 100 noktalik istekler zaman zaman daha uzun
# suruyor, erken birakilan istek hem bosa gidiyor hem tekrar denemeyi getiriyordu.
# Istek yine de uzarsa OM_BATCH=50 ile obek kucultulebilir, toplam maliyet degismez.
TIMEOUT = ayar("OM_TIMEOUT", 60, float)
DENEME = ayar("OM_TRIES", 6)
MAX_KAYIP = ayar("OM_MAX_KAYIP", 0.10, float)
BEKLE = [5, 15, 45, 90, 180]
SLEEP_UST = 45.0
DSR_UST = 67        # yagissiz gun sayaci tavani; eski 67 gunluk pencerenin dogal siniri
RING = 30           # precip_30d icin tasinan gun sayisi

GECICI_HATALAR = (requests.exceptions.Timeout,
                  requests.exceptions.ConnectionError,
                  requests.exceptions.ChunkedEncodingError)


class Alinamadi(Exception):
    """Bir batch butun denemelerden sonra da alinamadi."""


# ----------------------------------------------------------------------
# girdi ve durum
# ----------------------------------------------------------------------
def simdi_tr():
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("Europe/Istanbul")
    except Exception:
        tz = datetime.timezone(datetime.timedelta(hours=3))
    return datetime.datetime.now(tz).replace(microsecond=0).isoformat()


def gun(s):
    return datetime.date.fromisoformat(str(s)[:10])


def yukle_baz():
    for f in [BAZ_FILE, "noktalar_baz.json"]:
        if os.path.exists(f):
            d = json.load(open(f, encoding="utf-8"))
            print("Baz: %s (%d)" % (f, len(d)))
            return [(p["ad"], p["lat"], p["lon"]) for p in d]
    raise FileNotFoundError(BAZ_FILE)


def durum_oku():
    """data/fwi_durum.json -> (son_tarih, {ad: [ffmc, dmc, dc, dsr, yagis]})"""
    if not os.path.exists(DURUM):
        return None, {}
    try:
        d = json.load(open(DURUM, encoding="utf-8"))
        h = {}
        for i, ad in enumerate(d["ad"]):
            h[ad] = [d["ffmc"][i], d["dmc"][i], d["dc"][i], d["dsr"][i], list(d["yagis"][i])]
        return d.get("son_tarih"), h
    except Exception as e:
        print("UYARI: durum dosyasi okunamadi (%s), soguk baslangica dusuluyor." % e)
        return None, {}


def durum_yaz(son_tarih, h):
    adlar = sorted(h)
    d = {"guncelleme": simdi_tr(), "son_tarih": son_tarih, "ad": adlar,
         "ffmc": [round(h[a][0], 2) for a in adlar],
         "dmc": [round(h[a][1], 2) for a in adlar],
         "dc": [round(h[a][2], 2) for a in adlar],
         "dsr": [int(h[a][3]) for a in adlar],
         "yagis": [[round(x, 1) for x in h[a][4]] for a in adlar]}
    if os.path.dirname(DURUM):
        os.makedirs(os.path.dirname(DURUM), exist_ok=True)
    with open(DURUM, "w", encoding="utf-8") as fh:
        json.dump(d, fh, ensure_ascii=False, separators=(",", ":"))
    return os.path.getsize(DURUM)


# ----------------------------------------------------------------------
# cekim
# ----------------------------------------------------------------------
def bekleme(i):
    return BEKLE[i] if i < len(BEKLE) else BEKLE[-1]


def fetch(points, past_days, tempo):
    params = {"latitude": ",".join(str(p[1]) for p in points),
              "longitude": ",".join(str(p[2]) for p in points),
              "daily": DAILY, "past_days": past_days, "forecast_days": FCST_DAYS,
              "timezone": "Europe/Istanbul"}
    if OM_APIKEY:
        params["apikey"] = OM_APIKEY
    son_hata = None
    for i in range(DENEME):
        try:
            r = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT)
        except GECICI_HATALAR as e:
            # Zaman asimi bir kota isareti degil, ag ya da sunucu yavasligidir.
            # Bu yuzden yalnizca bu istek icin kademeli beklenir; obekler arasi
            # genel tempo YUKSELTILMEZ. (Eskiden yukseltiliyordu ve tek bir
            # yavas sabah butun kosuyu 45 saniyelik tempoda kilitliyordu.)
            son_hata = "zaman asimi / baglanti (%s)" % type(e).__name__
            w = bekleme(i)
            print("    %s; %d sn bekle (deneme %d/%d, tempo %.0f sn, degismedi)"
                  % (son_hata, w, i + 1, DENEME, tempo))
            time.sleep(w); continue
        if r.status_code == 429:
            ra = r.headers.get("Retry-After", "")
            w = int(ra) if str(ra).isdigit() else bekleme(i) * 3
            tempo = min(tempo * 1.5, SLEEP_UST)
            son_hata = "429 (kota / tempo)"
            print("    429; %d sn bekle (deneme %d/%d, tempo %.0f sn)" % (w, i + 1, DENEME, tempo))
            time.sleep(w); continue
        if r.status_code >= 500:
            son_hata = "sunucu hatasi %d" % r.status_code
            w = bekleme(i)
            print("    %s; %d sn bekle (deneme %d/%d)" % (son_hata, w, i + 1, DENEME))
            time.sleep(w); continue
        try:
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            raise Alinamadi("kalici hata: %s" % e)
        # Ilk denemede temiz gecen her istek tempoyu tabana dogru geri ceker.
        # Yarilayarak: 429 sonrasi yukselen tempo birkac basarili istekte tabana doner.
        if i == 0:
            tempo = max(SLEEP, tempo * 0.5)
        return (j if isinstance(j, list) else [j]), tempo
    raise Alinamadi(son_hata or "bilinmeyen")


# ----------------------------------------------------------------------
# hesap
# ----------------------------------------------------------------------
def satirlar(daily):
    """Open-Meteo gunluk blogunu duz listeye cevirir."""
    t = daily["time"]
    nem = daily.get("relative_humidity_2m_mean") or [None] * len(t)
    yagis = daily.get("precipitation_sum") or [0.0] * len(t)
    return [{"date": dt, "tmax": daily["temperature_2m_max"][i], "humidity": nem[i],
             "wind": daily["wind_speed_10m_max"][i],
             "precip": (yagis[i] if yagis[i] is not None else 0.0)}
            for i, dt in enumerate(t)]


def fwi_satir(g):
    return {"date": g["date"], "temp": (g["tmax"] or 0.0),
            "rh": (g["humidity"] if g["humidity"] is not None else 50.0),
            "wind": (g["wind"] or 0.0), "precip": g["precip"]}


def dsr_ilerlet(dsr, precip):
    return 0 if precip > 1.0 else min(dsr + 1, DSR_UST)


def nokta_isle(gunler, durum_kaydi, son_tarih):
    """Bir noktanin penceresini isler.
    Doner: (tahmin_kayitlari, yeni_durum, gecmisin_son_gunu)"""
    tahmin = gunler[-FCST_DAYS:]
    gecmis = gunler[:-FCST_DAYS]
    if not gecmis:
        raise ValueError("gecmis pencere bos")

    if durum_kaydi is None:
        ilerlenecek = gecmis                      # soguk baslangic: tum pencereyle isin
        f0, p0, d0, dsr, ring = 85.0, 6.0, 15.0, 0, []
    else:
        f0, p0, d0, dsr, ring = durum_kaydi
        ring = list(ring)
        ilerlenecek = [g for g in gecmis if gun(g["date"]) > gun(son_tarih)] if son_tarih else gecmis

    if ilerlenecek:
        seri = fwi.fwi_series([fwi_satir(g) for g in ilerlenecek], f0, p0, d0)
        f0, p0, d0 = seri[-1]["ffmc"], seri[-1]["dmc"], seri[-1]["dc"]
        for g in ilerlenecek:
            dsr = dsr_ilerlet(dsr, g["precip"])
            ring.append(g["precip"])
        ring = ring[-RING:]

    seri = fwi.fwi_series([fwi_satir(g) for g in tahmin], f0, p0, d0)
    kayitlar = []
    d = dsr
    for k, (g, s) in enumerate(zip(tahmin, seri), start=1):
        d = dsr_ilerlet(d, g["precip"])
        onceki = ring[-(RING - k):] if RING - k > 0 else []
        p30 = sum(onceki) + sum(x["precip"] for x in tahmin[:k])
        kayitlar.append({"date": g["date"], "tmax": g["tmax"], "humidity": g["humidity"],
                         "wind": g["wind"], "days_since_rain": d, "precip_30d": round(p30, 1),
                         "ffmc": s["ffmc"], "dmc": s["dmc"], "dc": s["dc"], "isi": s["isi"]})
    return kayitlar, [f0, p0, d0, dsr, ring], gecmis[-1]["date"]


# ----------------------------------------------------------------------
# akis
# ----------------------------------------------------------------------
PTS = yukle_baz()
son_tarih, DURUM_H = durum_oku()

zorla = bool(ayar("OM_SOGUK", 0))
soguk = zorla or not DURUM_H
sebep = "elle zorlandi" if zorla else "durum dosyasi yok"
if DURUM_H and son_tarih and not soguk:
    bosluk = (datetime.date.today() - gun(son_tarih)).days
    eksik = sum(1 for p in PTS if p[0] not in DURUM_H)
    if bosluk > MAX_BOSLUK:
        soguk, sebep = True, "son durum %d gun eski (esik %d)" % (bosluk, MAX_BOSLUK)
    elif eksik > len(PTS) * KISMI_UST:
        # Noktalarin cogu durumda yoksa kismi isinmanin anlami kalmiyor,
        # dogrudan tam soguk baslangic daha ucuz ve daha basit.
        soguk, sebep = True, "%d nokta durumda yok (yarisindan cok)" % eksik

# Izgaraya yeni nokta eklendiginde eskiler sicak kalir, yalnizca yeniler isinir.
# Boylece orman maskesi genisletildiginde mevcut 5.254 hucrenin DC birikimi
# sifirlanmaz; sadece yeni hucreler 60 gunluk pencereyle devreye girer.
if soguk:
    GRUPLAR = [("ISINMA", SOGUK_GECMIS, list(PTS))]
else:
    _ilik = [p for p in PTS if p[0] in DURUM_H]
    _yeni = [p for p in PTS if p[0] not in DURUM_H]
    GRUPLAR = [("ILIK", ILIK_GECMIS, _ilik)]
    if _yeni:
        GRUPLAR.append(("YENI NOKTA ISINMASI", SOGUK_GECMIS, _yeni))

agirlik = sum(len(g[2]) * (max(g[1] + FCST_DAYS, 14) / 14.0) for g in GRUPLAR)
print("Mod: %s (%s)" % ("SOGUK BASLANGIC" if soguk else "ILIK",
                        sebep if soguk else "son durum: %s" % son_tarih))
for ad, gec, pts in GRUPLAR:
    print("  %-22s %5d nokta, pencere %d gecmis + %d tahmin" % (ad, len(pts), gec, FCST_DAYS))
if OM_APIKEY:
    print("Uc: musteri (ticari plan, anahtar ...%s)" % OM_APIKEY[-4:])
    print("Tahmini agirlikli cagri: %.0f (aylik butce 1.000.000; her gun bu pencereyle ~%.0f/ay)"
          % (agirlik, agirlik * 30))
else:
    print("Uc: ucretsiz (anahtar yok)")
    print("Tahmini agirlikli cagri: %.0f (ucretsiz gunluk sinir 10.000)" % agirlik)
print("Ayar: batch=%d, tempo=%.0f sn, zaman asimi=%.0f sn, deneme=%d, kayip esigi=%.0f%%\n"
      % (B, SLEEP, TIMEOUT, DENEME, MAX_KAYIP * 100))

results, done = [], set()
if os.path.exists(CIKTI):
    try:
        results = json.load(open(CIKTI, encoding="utf-8"))
        done = {r["name"] for r in results}
        print("Devam: %d nokta hazir" % len(done))
    except Exception:
        results, done = [], set()

ISLER = [(ad, gec, [p for p in pts if p[0] not in done]) for ad, gec, pts in GRUPLAR]
ISLER = [x for x in ISLER if x[2]]
print("Cekilecek: %d\n" % sum(len(x[2]) for x in ISLER))

t0 = time.time()
tempo = SLEEP
kayip = []
yeni_durum = {} if soguk else dict(DURUM_H)
yeni_son_tarih = None

bi = 0
bitti = 0
toplam_kalan = sum(len(x[2]) for x in ISLER)
for grup_ad, GEC, kalan in ISLER:
    print("\n-- %s: %d nokta, pencere %d gun --" % (grup_ad, len(kalan), GEC))
    for k in range(0, len(kalan), B):
        batch = kalan[k:k + B]
        try:
            locs, tempo = fetch(batch, GEC, tempo)
        except Alinamadi as e:
            kayip.extend(p[0] for p in batch)
            bitti += len(batch)
            print("  ATLANDI: %d nokta alinamadi (%s)" % (len(batch), e))
            time.sleep(tempo)
            continue
        for (name, lat, lon), loc in zip(batch, locs):
            try:
                gunler = satirlar(loc["daily"])
                # Durumda olmayan nokta (yeni hucre) None alir ve tum pencereyle isinir.
                kayitlar, dur, st = nokta_isle(gunler, None if soguk else DURUM_H.get(name), son_tarih)
            except Exception as e:
                kayip.append(name)
                print("  ATLANDI: %s hesaplanamadi (%s)" % (name, e))
                continue
            results.append({"name": name, "lat": lat, "lon": lon, "forecast": kayitlar})
            yeni_durum[name] = dur
            yeni_son_tarih = st
        bi += 1
        bitti += len(batch)
        hiz = bitti / max(1, time.time() - t0)
        print("  %d/%d  (~%.0f dk, kayip %d)"
              % (len(done) + bitti, len(PTS), (toplam_kalan - bitti) / max(0.1, hiz) / 60, len(kayip)))
        if bi % 10 == 0:
            json.dump(results, open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False)
        time.sleep(tempo)

json.dump(results, open(CIKTI, "w", encoding="utf-8"), ensure_ascii=False)
oran = len(kayip) / max(1, len(PTS))
print("\nCikti: %s (%d nokta)" % (CIKTI, len(results)))
print("Kayip: %d nokta (%.1f%%), sure: %.0f dk" % (len(kayip), oran * 100, (time.time() - t0) / 60))

if oran > MAX_KAYIP or not results:
    print("\nHATA: kayip orani esigi (%.0f%%) asti, durum yazilmadi ve skorlama yapilmayacak."
          % (MAX_KAYIP * 100))
    print("Panel son basarili gunun dosyasini gostermeye devam eder.")
    sys.exit(1)

boy = durum_yaz(yeni_son_tarih, yeni_durum)
print("Durum: %s (%d nokta, son tarih %s, %.0f KB)" % (DURUM, len(yeni_durum), yeni_son_tarih, boy / 1024))
if kayip:
    print("  not: %d noktanin durumu ilerletilmedi, ertesi gun kendiliginden kapanir." % len(kayip))
print("Sirada: python operasyonel_hafta.py")
