"""
operasyonel_hafta.py  ·  YangınRiski.com
Haftalik kosucu: dondurulmus modeli (model_v3.json), statik nokta tabani
(noktalar_baz_grid.json: nufus + yakit + tarim kenari), idari etiketleri
(noktalar_idari.json: il / ilce) ve bu haftanin tahminini (operasyonel_hava.py
ciktisi: operasyonel_tahmin.json) birlestirir, her nokta icin 7 gunluk riski
hesaplar ve haftanin tepe riskine gore siralar.

Gunluk akis (GitHub Actions):
    python operasyonel_hava.py      # operasyonel_tahmin.json  (canli 7 gun hava + FWI)
    python operasyonel_hafta.py     # data/skorlar.json        (panelin okudugu dosya)
    panel (index.html) data/skorlar.json'u fetch eder.

Cikti iki dosya:
    data/skorlar.json   panel semasi (uretim, hafta, tarihler, yer, harita, top)
                        harita satiri 15 alanlidir: konum, riskler, tepe gun,
                        FWI kodlari ve tepe gunun ham hava degiskenleri
    skor_bu_hafta.json  ayrintili insan-okur cikti (arsiv / hata ayiklama)

Skorlama saf aritmetik, sklearn gerekmez.
"""
import json, math, os, datetime

TOP_N = 30            # panelde listelenen en riskli hucre sayisi
PANEL_YOL = os.path.join("data", "skorlar.json")


# ----------------------------------------------------------------------
# girdi yukleme
# ----------------------------------------------------------------------
def yukle(ad):
    here = os.path.dirname(os.path.abspath(__file__))
    for base in [os.getcwd(), here]:
        p = os.path.join(base, ad)
        if os.path.exists(p):
            return json.load(open(p, encoding="utf-8"))
    raise FileNotFoundError(ad + " bulunamadi")


def yukle_ops(ad):
    try:
        return yukle(ad)
    except FileNotFoundError:
        return None


try:
    M = yukle("model_v3.json")     # birlesik model (FWI + tarim kenari)
except FileNotFoundError:
    M = yukle("model_v2.json")
try:
    BAZ = yukle("noktalar_baz_grid.json")   # ulusal izgara
except FileNotFoundError:
    BAZ = yukle("noktalar_baz.json")        # 20 bolgelik yedek
TAHM = yukle("operasyonel_tahmin.json")
IDARI = yukle_ops("noktalar_idari.json")     # il / ilce etiketleri (opsiyonel)

FEATS = M["feature_order"]
baz_by_ad = {b["ad"]: b for b in BAZ}


# ----------------------------------------------------------------------
# idari etiketler: hangi semada gelirse gelsin koordinat anahtarina indir
# ----------------------------------------------------------------------
def koord_anahtar(lat, lon):
    return "%.3f,%.3f" % (round(float(lat), 3), round(float(lon), 3))


def etiket_cikar(d):
    for k in ("yer", "etiket", "label"):
        if d.get(k):
            return str(d[k])
    il = d.get("il") or d.get("province") or d.get("sehir")
    ilce = d.get("ilce") or d.get("district")
    if il and ilce:
        return "%s / %s" % (il, ilce)
    return il or ilce or None


def idari_harita(veri):
    """noktalar_idari.json'u {koordinat_anahtari: 'Il / Ilce'} sozlugune cevirir."""
    h = {}
    if veri is None:
        return h
    if isinstance(veri, dict):
        for k, v in veri.items():
            et = v if isinstance(v, str) else etiket_cikar(v) if isinstance(v, dict) else None
            if not et:
                continue
            h[k] = et
            if isinstance(v, dict) and v.get("lat") is not None and v.get("lon") is not None:
                h[koord_anahtar(v["lat"], v["lon"])] = et
            else:
                parca = str(k).split(",")
                if len(parca) == 2:
                    try:
                        h[koord_anahtar(parca[0], parca[1])] = et
                    except ValueError:
                        pass
    elif isinstance(veri, list):
        for d in veri:
            if not isinstance(d, dict):
                continue
            et = etiket_cikar(d)
            if not et:
                continue
            if d.get("ad"):
                h[str(d["ad"])] = et
            if d.get("lat") is not None and d.get("lon") is not None:
                h[koord_anahtar(d["lat"], d["lon"])] = et
    return h


IDARI_H = idari_harita(IDARI)


def yer_adi(st):
    """Once idari etiket, sonra baz'daki ad, en son koordinat."""
    for k in (st.get("ad"), koord_anahtar(st["lat"], st["lon"])):
        if k and k in IDARI_H:
            return IDARI_H[k]
    ad = str(st.get("ad") or "")
    if ad and not ad.replace(".", "").replace(",", "").replace("-", "").isdigit():
        return ad
    return "%.2f, %.2f" % (st["lat"], st["lon"])


# ----------------------------------------------------------------------
# model
# ----------------------------------------------------------------------
def donustur(name, x):
    return math.log1p(x) if M["transform"].get(name) == "log1p" else x


def risk(rec):
    z = M["intercept"]
    for i, f in enumerate(FEATS):
        if rec.get(f) is None:
            return None
        t = donustur(f, rec[f])
        z += M["coef"][i] * ((t - M["scaler_mean"][i]) / M["scaler_scale"][i])
    return 1.0 / (1.0 + math.exp(-z))


def yuvarla(x, n=1):
    return round(float(x), n) if x is not None else None


def tamsayi(x):
    """Nem ve gun sayaci gibi alanlar tam sayi yazilir; dosya boyutu kucuk kalir."""
    return int(round(float(x))) if x is not None else None


# ----------------------------------------------------------------------
# skorlama
# ----------------------------------------------------------------------
out = []
eksik = []
for reg in TAHM:
    st = baz_by_ad.get(reg.get("name")) or baz_by_ad.get(reg.get("ad"))
    if not st:
        eksik.append(reg.get("name") or reg.get("ad"))
        continue
    gunluk = []
    for f in reg.get("forecast", []):
        rec = {"human": st["human"], "fuel": st["fuel"], "farm_dist": st.get("farm_dist"),
               "tmax": f.get("tmax"), "humidity": f.get("humidity"), "wind": f.get("wind"),
               "days_since_rain": f.get("days_since_rain"), "precip_30d": f.get("precip_30d"),
               "ffmc": f.get("ffmc"), "dmc": f.get("dmc"), "dc": f.get("dc"), "isi": f.get("isi")}
        s = risk(rec)
        if s is not None:
            gunluk.append({"date": f.get("date"), "risk": round(s, 4),
                           "ffmc": f.get("ffmc"), "dmc": f.get("dmc"),
                           "dc": f.get("dc"), "isi": f.get("isi"),
                           "tmax": f.get("tmax"), "humidity": f.get("humidity"),
                           "wind": f.get("wind"),
                           "days_since_rain": f.get("days_since_rain"),
                           "precip_30d": f.get("precip_30d")})
    if not gunluk:
        continue
    tepe = max(gunluk, key=lambda x: x["risk"])
    out.append({"ad": st["ad"], "yer": yer_adi(st), "lat": st["lat"], "lon": st["lon"],
                "risk_tepe": tepe["risk"], "tepe_gun": tepe["date"],
                "tepe_fwi": {"ffmc": tepe["ffmc"], "dmc": tepe["dmc"],
                             "dc": tepe["dc"], "isi": tepe["isi"]},
                "tepe_hava": {"tmax": tepe["tmax"], "humidity": tepe["humidity"],
                              "wind": tepe["wind"],
                              "days_since_rain": tepe["days_since_rain"],
                              "precip_30d": tepe["precip_30d"]},
                "risk_ort": round(sum(g["risk"] for g in gunluk) / len(gunluk), 4),
                "gunluk": gunluk})

if not out:
    raise SystemExit("HATA: hic nokta skorlanamadi, operasyonel_tahmin.json bos ya da uyumsuz")

out.sort(key=lambda x: -x["risk_tepe"])
for i, o in enumerate(out):
    o["sira"] = i + 1


# ----------------------------------------------------------------------
# panel dosyasi: data/skorlar.json
# ----------------------------------------------------------------------
def simdi_tr():
    """Uretim damgasi, Turkiye saatiyle ISO 8601."""
    try:
        from zoneinfo import ZoneInfo
        tz = ZoneInfo("Europe/Istanbul")
    except Exception:
        tz = datetime.timezone(datetime.timedelta(hours=3))
    return datetime.datetime.now(tz).replace(microsecond=0).isoformat()


def gun_tr(iso):
    p = str(iso).split("-")
    return "%s.%s.%s" % (p[2], p[1], p[0]) if len(p) == 3 else str(iso)


tarihler = sorted({g["date"] for o in out for g in o["gunluk"] if g["date"]})
hafta = "%s ile %s" % (gun_tr(tarihler[0]), gun_tr(tarihler[-1])) if tarihler else ""

yer_listesi = sorted({o["yer"] for o in out})
yer_idx = {y: i for i, y in enumerate(yer_listesi)}

# harita satiri (15 alan):
#   0 lat          1 lon           2 tepe_risk     3 yer_indeksi   4 ort_risk
#   5 tepe_gun     6 ffmc          7 dmc           8 dc            9 isi
#  10 tmax (C)    11 nem (%)      12 ruzgar (km/sa)
#  13 yagissiz_gun            14 son 30 gun yagis (mm)
# 10'dan sonraki alanlar tepe gune aittir, tipki FWI kodlari gibi.
harita = [[round(o["lat"], 3), round(o["lon"], 3), round(o["risk_tepe"], 3),
           yer_idx[o["yer"]], round(o["risk_ort"], 3), o["tepe_gun"],
           yuvarla(o["tepe_fwi"]["ffmc"]), yuvarla(o["tepe_fwi"]["dmc"]),
           yuvarla(o["tepe_fwi"]["dc"]), yuvarla(o["tepe_fwi"]["isi"]),
           yuvarla(o["tepe_hava"]["tmax"]), tamsayi(o["tepe_hava"]["humidity"]),
           yuvarla(o["tepe_hava"]["wind"]), tamsayi(o["tepe_hava"]["days_since_rain"]),
           yuvarla(o["tepe_hava"]["precip_30d"])] for o in out]

# top listesi: gunluk seyir tarih sirasinda, eksik gun 0 ile doldurulur
top = []
for o in out[:TOP_N]:
    gunluk_map = {g["date"]: g["risk"] for g in o["gunluk"]}
    top.append({"yer": o["yer"], "lat": round(o["lat"], 3), "lon": round(o["lon"], 3),
                "rt": round(o["risk_tepe"], 3),
                "g": [round(gunluk_map.get(d, 0.0), 3) for d in tarihler]})

panel = {"uretim": simdi_tr(), "hafta": hafta, "tarihler": tarihler,
         "yer": yer_listesi, "harita": harita, "top": top}

if os.path.dirname(PANEL_YOL):
    os.makedirs(os.path.dirname(PANEL_YOL), exist_ok=True)
with open(PANEL_YOL, "w", encoding="utf-8") as fh:
    json.dump(panel, fh, ensure_ascii=False, separators=(",", ":"))

with open("skor_bu_hafta.json", "w", encoding="utf-8") as fh:
    json.dump(out, fh, ensure_ascii=False, indent=1)


# ----------------------------------------------------------------------
# ozet
# ----------------------------------------------------------------------
print("Skorlanan nokta: %d" % len(out) + ("  | baz'da bulunamayan: %d" % len(eksik) if eksik else ""))
if eksik:
    print("  ornek eksikler: %s" % ", ".join(str(e) for e in eksik[:5]))
if not IDARI_H:
    print("UYARI: noktalar_idari.json bulunamadi, yer etiketleri koordinat olarak yazildi.")
else:
    kayip = sum(1 for o in out if "," in o["yer"] and "/" not in o["yer"])
    print("Idari etiket: %d ayri il/ilce" % len(yer_listesi) + (", etiketsiz %d nokta" % kayip if kayip else ""))
print("Yazildi: %s (%.1f KB)  ve  skor_bu_hafta.json" % (PANEL_YOL, os.path.getsize(PANEL_YOL) / 1024))
print("Uretim damgasi: %s  |  hafta: %s" % (panel["uretim"], hafta))
print("\nBU HAFTA EN RISKLI (tepe risk):")
for o in out[:20]:
    bar = "#" * int(o["risk_tepe"] * 30)
    print("  %2d. %-24s tepe %.3f (%s) ort %.3f %s"
          % (o["sira"], o["yer"][:24], o["risk_tepe"], o["tepe_gun"], o["risk_ort"], bar))
