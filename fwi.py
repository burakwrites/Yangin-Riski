"""
fwi.py  ·  Kanada Orman Yangini Hava Indeksi (FWI) sistemi + KBDI
Van Wagner & Pickett (1985) denklemleri; cffdrs ile ayni formulasyon.

Girdi gunluk dizi: [{date, temp(C), rh(%), wind(km/h), precip(mm)}, ...]
Cikti her gun: ffmc, dmc, dc, isi, bui, fwi (+ istege bagli kbdi)

Not: FWI ideal olarak ogle (12:00) degerleriyle hesaplanir. Gunluk
tmax / ortalama nem / max ruzgar ile yaklasik hesaplanir; goreli indeks
icin yeterli, daha hassasiyet icin ogle saatlik degerler cekilebilir.
"""
import math

# kuzey yarimkure gun uzunlugu faktorleri (ay 1..12)
LE = [6.5, 7.5, 9.0, 12.8, 13.9, 13.9, 12.4, 10.9, 9.4, 8.0, 7.0, 6.0]   # DMC
LF = [-1.6,-1.6,-1.6, 0.9, 3.8, 5.8, 6.4, 5.0, 2.4, 0.4,-1.6,-1.6]       # DC

def _ffmc(t, h, w, r, f0):
    h = min(h, 100.0)
    wmo = 147.2*(101.0-f0)/(59.5+f0)
    if r > 0.5:
        rf = r - 0.5
        if wmo > 150.0:
            wmo = (wmo + 42.5*rf*math.exp(-100.0/(251.0-wmo))*(1.0-math.exp(-6.93/rf))
                   + 0.0015*(wmo-150.0)**2*math.sqrt(rf))
        else:
            wmo = wmo + 42.5*rf*math.exp(-100.0/(251.0-wmo))*(1.0-math.exp(-6.93/rf))
        wmo = min(wmo, 250.0)
    ed = 0.942*h**0.679 + 11.0*math.exp((h-100.0)/10.0) + 0.18*(21.1-t)*(1.0-math.exp(-0.115*h))
    if wmo > ed:
        ko = 0.424*(1.0-(h/100.0)**1.7) + 0.0694*math.sqrt(w)*(1.0-(h/100.0)**8)
        kd = ko*0.581*math.exp(0.0365*t)
        wm = ed + (wmo-ed)*10.0**(-kd)
    else:
        ew = 0.618*h**0.753 + 10.0*math.exp((h-100.0)/10.0) + 0.18*(21.1-t)*(1.0-math.exp(-0.115*h))
        if wmo < ew:
            kl = 0.424*(1.0-((100.0-h)/100.0)**1.7) + 0.0694*math.sqrt(w)*(1.0-((100.0-h)/100.0)**8)
            kw = kl*0.581*math.exp(0.0365*t)
            wm = ew - (ew-wmo)*10.0**(-kw)
        else:
            wm = wmo
    f = 59.5*(250.0-wm)/(147.2+wm)
    return max(0.0, min(f, 101.0))

def _dmc(t, h, r, p0, month):
    h = min(h, 100.0)
    if t < -1.1: t = -1.1
    rk = 1.894*(t+1.1)*(100.0-h)*LE[month-1]*1e-4
    if r > 1.5:
        rw = 0.92*r - 1.27
        wmi = 20.0 + 280.0/math.exp(0.023*p0)
        if p0 <= 33.0: b = 100.0/(0.5+0.3*p0)
        elif p0 <= 65.0: b = 14.0 - 1.3*math.log(p0)
        else: b = 6.2*math.log(p0) - 17.2
        wmr = wmi + 1000.0*rw/(48.77+b*rw)
        pr = 43.43*(5.6348 - math.log(wmr-20.0))
        pr = max(pr, 0.0)
    else:
        pr = p0
    return max(pr + rk, 0.0)

def _dc(t, r, d0, month):
    if t < -2.8: t = -2.8
    pe = (0.36*(t+2.8) + LF[month-1])/2.0
    if pe < 0.0: pe = 0.0
    if r > 2.8:
        rw = 0.83*r - 1.27
        smi = 800.0*math.exp(-d0/400.0)
        dr = d0 - 400.0*math.log(1.0 + 3.937*rw/smi)
        dr = max(dr, 0.0)
    else:
        dr = d0
    return max(dr + pe, 0.0)

def _isi(ffmc, w):
    fm = 147.2*(101.0-ffmc)/(59.5+ffmc)
    fw = math.exp(0.05039*w)
    ff = 91.9*math.exp(-0.1386*fm)*(1.0 + fm**5.31/4.93e7)
    return 0.208*fw*ff

def _bui(dmc, dc):
    if dmc == 0 and dc == 0: return 0.0
    if dmc <= 0.4*dc:
        bui = 0.8*dmc*dc/(dmc+0.4*dc)
    else:
        bui = dmc - (1.0 - 0.8*dc/(dmc+0.4*dc))*(0.92 + (0.0114*dmc)**1.7)
    return max(bui, 0.0)

def _fwi(isi, bui):
    fd = 0.626*bui**0.809 + 2.0 if bui <= 80.0 else 1000.0/(25.0+108.64*math.exp(-0.023*bui))
    b = 0.1*isi*fd
    return math.exp(2.72*(0.434*math.log(b))**0.647) if b > 1.0 else b

def fwi_series(rows, ffmc0=85.0, dmc0=6.0, dc0=15.0):
    """rows: date,temp,rh,wind,precip sirali gunluk. Onceki gun degerlerinden iterasyon."""
    f, p, d = ffmc0, dmc0, dc0
    out = []
    for r in rows:
        t = r["temp"]; h = r["rh"]; w = r["wind"]; pr = r["precip"]
        month = int(r["date"][5:7])
        f = _ffmc(t, h, w, pr, f)
        p = _dmc(t, h, pr, p, month)
        d = _dc(t, pr, d, month)
        isi = _isi(f, w); bui = _bui(p, d); fwi = _fwi(isi, bui)
        out.append({"date": r["date"], "ffmc": round(f,2), "dmc": round(p,2), "dc": round(d,2),
                    "isi": round(isi,2), "bui": round(bui,2), "fwi": round(fwi,2)})
    return out

def kbdi_series(rows, annual_rain_mm, q0=0.0):
    """Keetch-Byram Kuraklik Indeksi (0..800). annual_rain_mm: yillik ort yagis."""
    R = annual_rain_mm/25.4  # inch
    q = q0
    out = []
    net = 0.0; wet = 0.0
    for r in rows:
        tF = r["temp"]*9.0/5.0 + 32.0
        p = r["precip"]
        # yagis: ardisik yagisin ilk 0.2 inch'i tutulur (interception)
        if p > 0:
            wet += p
            eff = max(0.0, p - max(0.0, 5.1 - (wet - p)))  # 0.2 inch = 5.1 mm esigi
            q = max(0.0, q - eff/25.4*100.0)
        else:
            wet = 0.0
        dq = ((800.0 - q)*(0.968*math.exp(0.0486*tF) - 8.30)*1.0) / (1.0 + 10.88*math.exp(-0.0441*R)) * 1e-3
        if dq < 0: dq = 0
        q = min(800.0, q + dq)
        out.append({"date": r["date"], "kbdi": round(q,1)})
    return out
