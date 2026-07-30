#!/usr/bin/env python3
"""
operasyonel_hava.py  ·  YangınRiski.com  (FWI'li, dayanikli surum)
Ulusal orman izgarasinin her noktasi icin Open-Meteo'dan canli tahmin ceker,
gecmis pencereyle FWI sistemini (FFMC, DMC, DC, ISI) hesaplar ve her tahmin
gunune ekler. Cikti operasyonel_hafta.py'ye beslenir. fwi.py ayni klasorde olmali.

Calistir:  python operasyonel_hava.py
Cikti:     operasyonel_tahmin.json
Devam edebilir; kesilirse tekrar calistir (cikti dosyasi duruyorsa kaldigi yerden).

Bu surumdeki dayaniklilik degisiklikleri:
  1. Zaman asimi ve baglanti hatasi da tekrar denenir (once yalnizca 429 deneniyordu;
     GitHub kosucularinda kosuyu dusuren tam buydu).
  2. Batch kucultuldu (50 -> 25) ve istekler arasi bekleme uzatildi; toplam agirlikli
     cagri sayisi degismez, tek istegin yuku yariya iner.
  3. Bir batch tum denemelerden sonra da alinamazsa betik durmaz, o noktalari atlar.
     Kayip esigi (varsayilan yuzde 10) asilirsa hata koduyla durur, boylece panel
     yarim veriyle guncellenmez.
  4. 429 ya da zaman asimi gorulurse bekleme kendiliginden uzar (adaptif tempo).
  5. Ayarlar ortam degiskeniyle degistirilebilir: OM_BATCH, OM_SLEEP, OM_TIMEOUT,
     OM_TRIES, OM_MAX_KAYIP, OM_PAST_DAYS.
"""
import requests, json, time, os, sys
import fwi

FORECAST_URL = "https://api.open-meteo.com/v1/forecast"
BAZ_FILE = "noktalar_baz_grid.json"
CIKTI = "operasyonel_tahmin.json"
DAILY = "temperature_2m_max,relative_humidity_2m_mean,wind_speed_10m_max,precipitation_sum"

def ayar(ad, vars_, tip=int):
    try:
        return tip(os.environ.get(ad, vars_))
    except (TypeError, ValueError):
        return tip(vars_)

PAST_DAYS = ayar("OM_PAST_DAYS", 60)      # DC tohumlama icin gecmis pencere
FCST_DAYS = 7
B = ayar("OM_BATCH", 25)                  # istek basina nokta
SLEEP = ayar("OM_SLEEP", 13, float)       # istekler arasi bekleme (sn)
TIMEOUT = ayar("OM_TIMEOUT", 60, float)   # tek istek zaman asimi (sn)
DENEME = ayar("OM_TRIES", 6)              # batch basina deneme sayisi
MAX_KAYIP = ayar("OM_MAX_KAYIP", 0.10, float)   # kabul edilebilir nokta kaybi orani
BEKLE = [5, 15, 45, 90, 180]              # kademeli bekleme merdiveni
SLEEP_UST = 45.0                          # adaptif temponun ust siniri

GECICI_HATALAR = (requests.exceptions.Timeout,
                  requests.exceptions.ConnectionError,
                  requests.exceptions.ChunkedEncodingError)


class Alinamadi(Exception):
    """Bir batch butun denemelerden sonra da alinamadi."""


def yukle_baz():
    for f in [BAZ_FILE, "noktalar_baz.json"]:
        if os.path.exists(f):
            d = json.load(open(f, encoding="utf-8"))
            print("Baz: %s (%d)" % (f, len(d)))
            return [(p["ad"], p["lat"], p["lon"]) for p in d]
    raise FileNotFoundError(BAZ_FILE)


def bekleme(i):
    return BEKLE[i] if i < len(BEKLE) else BEKLE[-1]


def fetch(points, tempo):
    """Bir batch ceker. Gecici hatalarda kademeli bekleyip tekrar dener.
    Doner: (sonuc_listesi, yeni_tempo). Basarisizsa Alinamadi firlatir."""
    params = {"latitude": ",".join(str(p[1]) for p in points),
              "longitude": ",".join(str(p[2]) for p in points),
              "daily": DAILY, "past_days": PAST_DAYS, "forecast_days": FCST_DAYS,
              "timezone": "Europe/Istanbul"}
    son_hata = None
    for i in range(DENEME):
        try:
            r = requests.get(FORECAST_URL, params=params, timeout=TIMEOUT)
        except GECICI_HATALAR as e:
            son_hata = "zaman asimi / baglanti (%s)" % type(e).__name__
            tempo = min(tempo * 1.5, SLEEP_UST)
            w = bekleme(i)
            print("    %s; %d sn bekle (deneme %d/%d, tempo %.0f sn)"
                  % (son_hata, w, i + 1, DENEME, tempo))
            time.sleep(w)
            continue
        if r.status_code == 429:
            ra = r.headers.get("Retry-After", "")
            w = int(ra) if str(ra).isdigit() else bekleme(i) * 3
            tempo = min(tempo * 1.5, SLEEP_UST)
            son_hata = "429 (kota / tempo)"
            print("    429; %d sn bekle (deneme %d/%d, tempo %.0f sn)"
                  % (w, i + 1, DENEME, tempo))
            time.sleep(w)
            continue
        if r.status_code >= 500:
            son_hata = "sunucu hatasi %d" % r.status_code
            w = bekleme(i)
            print("    %s; %d sn bekle (deneme %d/%d)" % (son_hata, w, i + 1, DENEME))
            time.sleep(w)
            continue
        try:
            r.raise_for_status()
            j = r.json()
        except Exception as e:
            # 4xx ya da bozuk govde: tekrar denemek ise yaramaz, batch'i atla
            raise Alinamadi("kalici hata: %s" % e)
        return (j if isinstance(j, list) else [j]), tempo
    raise Alinamadi(son_hata or "bilinmeyen")


def derive(daily):
    dates = daily["time"]
    precip = daily.get("precipitation_sum") or [0] * len(dates)
    out = []
    dsr = 0
    for i, dt in enumerate(dates):
        p = precip[i] if precip[i] is not None else 0.0
        dsr = 0 if p > 1.0 else dsr + 1
        p30 = sum((precip[j] or 0) for j in range(max(0, i - 29), i + 1))
        out.append({"date": dt, "tmax": daily["temperature_2m_max"][i],
                    "humidity": (daily.get("relative_humidity_2m_mean") or [None] * len(dates))[i],
                    "wind": daily["wind_speed_10m_max"][i], "precip": p,
                    "days_since_rain": dsr, "precip_30d": round(p30, 1)})
    return out


def fwi_ekle(days):
    rows = [{"date": d["date"], "temp": (d["tmax"] or 0.0),
             "rh": (d["humidity"] if d["humidity"] is not None else 50.0),
             "wind": (d["wind"] or 0.0), "precip": d["precip"]} for d in days]
    fs = fwi.fwi_series(rows)
    for d, f in zip(days, fs):
        d["ffmc"] = f["ffmc"]; d["dmc"] = f["dmc"]; d["dc"] = f["dc"]; d["isi"] = f["isi"]
    return days


def kaydet(results):
    with open(CIKTI, "w", encoding="utf-8") as fh:
        json.dump(results, fh, ensure_ascii=False)


# ----------------------------------------------------------------------
PTS = yukle_baz()
agirlik = len(PTS) * (max(PAST_DAYS + FCST_DAYS, 14) / 14.0)
print("Tahmini agirlikli Open-Meteo cagrisi: %.0f (ucretsiz gunluk sinir 10.000)" % agirlik)
print("Ayar: batch=%d, tempo=%.0f sn, zaman asimi=%.0f sn, deneme=%d, kayip esigi=%.0f%%"
      % (B, SLEEP, TIMEOUT, DENEME, MAX_KAYIP * 100))

results, done = [], set()
if os.path.exists(CIKTI):
    try:
        results = json.load(open(CIKTI, encoding="utf-8"))
        done = {r["name"] for r in results}
        print("Devam: %d nokta hazir" % len(done))
    except Exception:
        results, done = [], set()

kalan = [p for p in PTS if p[0] not in done]
print("Cekilecek: %d\n" % len(kalan))

t0 = time.time()
tempo = SLEEP
kayip = []
basarisiz_batch = 0
for bi, k in enumerate(range(0, len(kalan), B)):
    batch = kalan[k:k + B]
    try:
        locs, tempo = fetch(batch, tempo)
    except Alinamadi as e:
        basarisiz_batch += 1
        kayip.extend(p[0] for p in batch)
        print("  ATLANDI: %d nokta alinamadi (%s)" % (len(batch), e))
        time.sleep(tempo)
        continue
    for (name, lat, lon), loc in zip(batch, locs):
        try:
            days = fwi_ekle(derive(loc["daily"]))
        except Exception as e:
            kayip.append(name)
            print("  ATLANDI: %s hesaplanamadi (%s)" % (name, e))
            continue
        fc = days[-FCST_DAYS:]
        for d in fc:
            d.pop("precip", None)   # precip artik gerekmez
        results.append({"name": name, "lat": lat, "lon": lon, "forecast": fc})
    y = k + len(batch)
    hiz = y / max(1, time.time() - t0)
    print("  %d/%d  (~%.0f dk, kayip %d)"
          % (len(done) + y, len(PTS), (len(kalan) - y) / max(0.1, hiz) / 60, len(kayip)))
    if (bi + 1) % 10 == 0:
        kaydet(results)
    time.sleep(tempo)

kaydet(results)
oran = len(kayip) / max(1, len(PTS))
print("\nCikti: %s (%d nokta, FWI kodlari eklendi)" % (CIKTI, len(results)))
print("Kayip: %d nokta (%.1f%%), basarisiz batch: %d, sure: %.0f dk"
      % (len(kayip), oran * 100, basarisiz_batch, (time.time() - t0) / 60))

if oran > MAX_KAYIP:
    print("\nHATA: kayip orani esigi (%.0f%%) asti, skorlama yapilmayacak." % (MAX_KAYIP * 100))
    print("Panel son basarili gunun dosyasini gostermeye devam eder.")
    sys.exit(1)
if not results:
    print("\nHATA: hic nokta alinamadi.")
    sys.exit(1)
print("Sirada: python operasyonel_hafta.py")
