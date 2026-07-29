#!/usr/bin/env python3
"""
operasyonel_hava.py  ·  YangınRiski.com  (FWI'li surum)
Ulusal orman izgarasinin her noktasi icin Open-Meteo'dan canli tahmin ceker,
60 gunluk gecmisle FWI sistemini (FFMC, DMC, DC, ISI) hesaplar ve her tahmin
gunune ekler. Cikti operasyonel_hafta.py'ye beslenir. fwi.py ayni klasorde olmali.

Calistir:  python operasyonel_hava.py
Cikti:     operasyonel_tahmin.json
Devam edebilir; kesilirse tekrar calistir.
"""
import requests, json, time, os
import fwi

FORECAST_URL="https://api.open-meteo.com/v1/forecast"
BAZ_FILE="noktalar_baz_grid.json"; CIKTI="operasyonel_tahmin.json"
DAILY="temperature_2m_max,relative_humidity_2m_mean,wind_speed_10m_max,precipitation_sum"
PAST_DAYS=60      # DC tohumlama icin
FCST_DAYS=7
B=50; SLEEP=10; BACKOFF=65

def yukle_baz():
    for f in [BAZ_FILE,"noktalar_baz.json"]:
        if os.path.exists(f):
            d=json.load(open(f,encoding="utf-8")); print(f"Baz: {f} ({len(d)})")
            return [(p["ad"],p["lat"],p["lon"]) for p in d]
    raise FileNotFoundError(BAZ_FILE)

def fetch(points):
    params={"latitude":",".join(str(p[1]) for p in points),"longitude":",".join(str(p[2]) for p in points),
            "daily":DAILY,"past_days":PAST_DAYS,"forecast_days":FCST_DAYS,"timezone":"Europe/Istanbul"}
    for _ in range(8):
        r=requests.get(FORECAST_URL,params=params,timeout=120)
        if r.status_code==429:
            w=int(r.headers.get("Retry-After",BACKOFF)) if r.headers.get("Retry-After","").isdigit() else BACKOFF
            print(f"    429; {w} sn bekle"); time.sleep(w); continue
        r.raise_for_status(); j=r.json(); return j if isinstance(j,list) else [j]
    raise RuntimeError("429 surekli; sonra tekrar calistir")

def derive(daily):
    dates=daily["time"]; precip=daily.get("precipitation_sum") or [0]*len(dates)
    out=[]; dsr=0
    for i,dt in enumerate(dates):
        p=precip[i] if precip[i] is not None else 0.0
        dsr=0 if p>1.0 else dsr+1
        p30=sum((precip[j] or 0) for j in range(max(0,i-29),i+1))
        out.append({"date":dt,"tmax":daily["temperature_2m_max"][i],
                    "humidity":(daily.get("relative_humidity_2m_mean") or [None]*len(dates))[i],
                    "wind":daily["wind_speed_10m_max"][i],"precip":p,
                    "days_since_rain":dsr,"precip_30d":round(p30,1)})
    return out

def fwi_ekle(days):
    rows=[{"date":d["date"],"temp":(d["tmax"] or 0.0),
           "rh":(d["humidity"] if d["humidity"] is not None else 50.0),
           "wind":(d["wind"] or 0.0),"precip":d["precip"]} for d in days]
    fs=fwi.fwi_series(rows)
    for d,f in zip(days,fs):
        d["ffmc"]=f["ffmc"]; d["dmc"]=f["dmc"]; d["dc"]=f["dc"]; d["isi"]=f["isi"]
    return days

PTS=yukle_baz()
results,done=[],set()
if os.path.exists(CIKTI):
    try:
        results=json.load(open(CIKTI,encoding="utf-8")); done={r["name"] for r in results}
        print(f"Devam: {len(done)} nokta hazir")
    except Exception: results,done=[],set()
kalan=[p for p in PTS if p[0] not in done]
print(f"Cekilecek: {len(kalan)}\n")
t0=time.time()
for bi,k in enumerate(range(0,len(kalan),B)):
    batch=kalan[k:k+B]; locs=fetch(batch)
    for (name,lat,lon),loc in zip(batch,locs):
        days=fwi_ekle(derive(loc["daily"]))
        fc=days[-FCST_DAYS:]
        for d in fc: d.pop("precip",None)   # precip artik gerekmez
        results.append({"name":name,"lat":lat,"lon":lon,"forecast":fc})
    y=k+len(batch); hiz=y/max(1,time.time()-t0)
    print(f"  {len(done)+y}/{len(PTS)}  (~{(len(kalan)-y)/max(0.1,hiz)/60:.0f} dk)")
    if (bi+1)%10==0: json.dump(results,open(CIKTI,"w",encoding="utf-8"),ensure_ascii=False)
    time.sleep(SLEEP)
json.dump(results,open(CIKTI,"w",encoding="utf-8"),ensure_ascii=False)
print(f"\nCikti: {CIKTI} ({len(results)} nokta, FWI kodlari eklendi)")
print("Sirada: python operasyonel_hafta.py")
