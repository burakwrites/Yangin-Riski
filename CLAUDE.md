# YangınRiski.com · çalışma kılavuzu

Bu dosya, bu klasörde açılan her Claude oturumunun ilk okuduğu yerdir.
Projenin ne olduğunu, dosyaların ne işe yaradığını ve bozulmaması gereken
kuralları anlatır. Ayrıntılı durum `devir_notu.md` dosyasındadır.

## Proje nedir

Türkiye geneli orman yangını tutuşma riski tahmin platformu. Tez şu: orman
yangınının birincil tetikleyicisi kuraklık değil, ormana insan erişimidir.
Kuraklık zemini hazırlar, kıvılcımı insan çakar.

Ürün yangın söndürmez, tutuşmayı önler. Hedef müşteri orman ile yerleşim
sınırındaki belediyeler. Sattığı bilgi şu: "Bu hafta sonu hangi ormana denetim
ekibi göndermeliyim."

Model, on iki özellikli dondurulmuş bir lojistik regresyondur (beş katlı
AUC 0,840). Panel ve zincir sunucusuz çalışır; GitHub Actions her sabah 07:00'de
skorları üretir, bot depoya işler, GitHub Pages yayınlar.

Canlı panel: https://burakwrites.github.io/Yangin-Riski/

## Dosyalar

    .github/workflows/gunluk_skor.yml  günlük koşu (cron 04:00 UTC = 07:00 TR)
    operasyonel_hava.py                Open-Meteo çekimi + FWI, durum taşıyan
    operasyonel_hafta.py               skorlama, data/skorlar.json yazar
    fwi.py                             FWI motoru (Van Wagner denklemleri)
    model_v3.json                      dondurulmuş model, 12 özellik
    noktalar_baz_grid.json             ulusal ızgara, 9.472 hücre (ESA WorldCover maskesi) + statik özellikler
    noktalar_idari.json                hücre başına il ve ilçe etiketi
    index.html                         panel (tek dosya, React + Leaflet + Babel)
    data/skorlar.json                  panelin okuduğu günlük skor (bot yazar)
    data/fwi_durum.json                FWI kodlarının dünkü hali (bot yazar)
    yontem_dokumani.md                 metodoloji dokümanı, dışarıya gösterilen kayıt
    devir_notu.md                      projenin güncel durumu ve açık işler

## Bozulmaması gereken kurallar

**Izgara kafesi oynatılmaz.** Hücreler 0,05 derecelik bir kafeste durur ve
adları `"enlem,boylam"` biçimindedir (üç ondalık). Kafesin başlangıcı ya da
adımı değişirse bütün hücre adları değişir, `data/fwi_durum.json` içindeki
kuraklık birikimi eşleşemez ve zincir tam soğuk başlangıca düşer.

**Nüfus tanımı eğitimle birebir aynı olmalı.** İnsan baskısı, noktanın
çevresindeki 2 km yarıçaplı dairenin WorldPop toplamıdır ve 1,11 kalibrasyon
bölenine sahiptir. Model bu değişkeni eğitimdeki ölçeğe göre standardize eder;
farklı bir yarıçap ya da bölen skorları **sessizce** bozar, yani panel çalışmaya
devam eder ama sıralama yanlış olur. Ayrıntı: yöntem dokümanı bölüm 4.4.

**`data/skorlar.json` içindeki harita satırı 15 alanlıdır.** Sıra:
`[lat, lon, tepe_risk, yer_indeksi, ort_risk, tepe_gün, ffmc, dmc, dc, isi,
tmax, nem, rüzgar, yağışsız_gün, yağış_30g]`. Şema değişirse `index.html`
içindeki popup indeksleri de aynı anda değişmeli, yoksa popup sessizce boşalır.

**Panel iki dillidir.** Bütün metinler dosyanın başındaki tek bir
`const METIN={tr:{...},en:{...}}` sözlüğünde durur ve koda `T.anahtar` diye
girer. Yeni metin eklerken iki dile birden eklenmeli. Sözlük adı `METIN`, `L`
değil; `L` Leaflet'in genel değişkeni.

**Terminoloji.** Sayılan nesne "yangın" (sayaçlar, katman etiketleri, kart
başlıkları). Modellenen olgu "tutuşma" ve artık yalnızca Yöntem Özeti'ndeki tez
ve sınır cümlelerinde geçer.

**Yöntem dokümanı güncellenince** dosyanın sonuna o günün tarihiyle yeni bir
"Son güncelleme" satırı eklenir, eskisi silinmez.

**Anahtar kodda yazmaz.** Open-Meteo anahtarı `OM_APIKEY` ortam değişkeninden
okunur, depo Secrets'ında durur. Depo public'tir; hiçbir dosyaya anahtar,
parola ya da kişisel veri yazılmamalı.

## Değişiklikten sonra yapılacak kontroller

Python betiği değiştiyse en az `python -m py_compile <dosya>`.

`index.html` değiştiyse JSX'in derlendiğini doğrula. Panel Babel'i tarayıcıda
çalıştırır, yani sözdizimi hatası siyah ekran demektir. Dosyada bir hata
göstericisi var: panel açılmazsa siyah ekran yerine hatanın metnini yazar.

Zincirin tamamı değiştiyse sahte girdiyle uçtan uca koştur; gerçek API'ye
gitmeden `requests` modülünü taklit etmek yeterlidir.

## Yazışma tercihi

Yanıtlarda tire ve kısa çizgi noktalama işareti olarak kullanılmıyor. Bileşik
teknik terimlerdeki tireler (Low-Code, S-NPP, Ro-Ro gibi) serbest.

Burak yazılımcı değil, GitHub'ı ilk kez bu projede kullanıyor. Akış VS Code
Source Control üzerinden: Pull, değiştir, mesaj yaz, Commit, Sync Changes.
Sync adımı sık atlanıyor, hatırlatmakta fayda var.
