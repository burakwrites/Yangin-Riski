# YangınRiski.com Otomasyon ve Yayın Kurulumu
Güncelleme tarihi: 30 Temmuz 2026

Hedef: her sabah 07:00'de kendi kendine dönen skorlama zinciri ve GitHub Pages üzerinden yayınlanan canlı panel. Sunucu yok, maliyet sıfır.

Betik ve panel uyarlamaları tamamlandı; bu sürüm artık uçtan uca hazır bir kurulum listesidir.

## 1. Repo yapısı

GitHub'da yeni bir repo aç (öneri: `yanginriski`, public ya da private fark etmez; Pages için public daha kolay). İçine şu yapıyla dosyaları koy:

    yanginriski/
      .github/workflows/gunluk_skor.yml    (workflow dosyası)
      operasyonel_hava.py                  (canlı 7 günlük hava çekimi + FWI, değişmedi)
      operasyonel_hafta.py                 (JSON çıktı uyarlamalı yeni sürüm)
      fwi.py                               (FWI motoru, operasyonel_hava.py kullanır)
      model_v3.json                        (dondurulmuş birleşik model, 12 özellik)
      noktalar_baz_grid.json               (ulusal ızgara: 5.254 hücre, nüfus, yakıt, tarım kenarı)
      noktalar_idari.json                  (hücre başına il ve ilçe etiketi)
      index.html                           (panel, fetch uyarlamalı)
      data/skorlar.json                    (ilk elle koşunun çıktısı; sonrasını bot yazar)
      .gitignore                           (ara çıktılar için, aşağıda)

Ara çıktılar repoda tutulmasa da olur, `.gitignore` içeriği şu kadar yeterli:

    operasyonel_tahmin.json
    skor_bu_hafta.json

Not: workflow dosyasının yolu birebir `.github/workflows/gunluk_skor.yml` olmalı, GitHub başka yerde aramaz.

## 2. Betik uyarlamaları (tamamlandı)

operasyonel_hava.py: değişiklik gerekmedi; kesinti toleransı ve batch yapısı Actions içinde aynen çalışır. Çıktısı `operasyonel_tahmin.json`.

operasyonel_hafta.py: yeni sürüm iki dosya yazar. `data/skorlar.json` panelin okuduğu dosyadır ve şu alanları taşır: `uretim` (koşu anının Türkiye saatiyle ISO damgası), `hafta` (gün aralığı metni), `tarihler` (7 gün), `yer` (il ve ilçe etiketleri listesi), `harita` (hücre başına `[lat, lon, tepe_risk, yer_indeksi, ortalama_risk, tepe_gün, ffmc, dmc, dc, isi]`), `top` (en riskli 30 hücre, yedi günlük seyriyle). `skor_bu_hafta.json` ise ayrıntılı insan okur çıktı olarak korunur, hata ayıklama ve arşiv içindir. Boyut yaklaşık 330 KB.

`noktalar_idari.json` bulunamazsa betik durmaz, yer etiketlerini koordinat olarak yazar ve konsola uyarı basar. Dosya varsa hem liste (`il` ve `ilce` alanlı kayıtlar) hem sözlük (`"lat,lon" : "İl / İlçe"`) biçimini tanır, eşleştirmeyi üç haneye yuvarlanmış koordinat üzerinden yapar.

index.html (panel): Bu Hafta verisini gömülü sabitten değil `data/skorlar.json` adresinden fetch eder ve haritanın sağ alt köşesinde "Son güncelleme: <tarih>" gösterir. Koşu bir gün başarısız olursa panel son başarılı günün dosyasını göstermeye devam eder; damga 36 saatten eskiyse ibare turuncuya döner ve "son başarılı koşu" notu eklenir, yani tarih ibaresi durumu kullanıcıya dürüstçe söyler.

## 3. Yerel deneme

`fetch` yerelden `file://` ile açıldığında tarayıcı engeller, panel Bu Hafta sekmesinde hata kartı gösterir. Lokalde denemek için repo kökünde küçük bir sunucu çalıştır:

    python3 -m http.server 8000

sonra `http://localhost:8000/index.html` adresini aç. Pages'te bu sorun yoktur.

## 4. Actions'ı etkinleştirme

Dosyalar push edildikten sonra repo > Actions sekmesi > "Gunluk risk skorlama" workflow'u görünür. İlk denemeyi beklemeden yapmak için "Run workflow" düğmesiyle elle tetikle. Koşu yaklaşık 25 ile 45 dakika sürer (106 batch, aralarda bekleme). Bittiğinde `data/skorlar.json` güncellenmiş ve commit edilmiş olmalı.

Zamanlama notu: GitHub cron'u dakika hassasiyeti garanti etmez, 07:00 hedefi bazen 07:15'e sarkar; günlük bir sistem için önemsizdir.

429 notu: GitHub koşucuları ortak IP kullandığından Open-Meteo nadiren daha sık 429 dönebilir; betikteki bekleme ve tekrar mantığı bunu zaten emiyor. Sorun süreklileşirse batch boyutunu düşürmek (B=50 yerine 30) yeterli olur.

## 5. GitHub Pages ile yayın

Repo > Settings > Pages > Source: "Deploy from a branch", Branch: main, klasör: / (root). Birkaç dakika içinde panel şu adreste yayında olur:

    https://<kullanici_adin>.github.io/yanginriski/

Panel ve data/ aynı repoda olduğu için fetch göreli yolla (`data/skorlar.json`) çalışır, ek ayar gerekmez.

## 6. Alan adı bağlama (istenirse, sonraki adım)

yanginriski.com alınmışsa Pages ayarlarında Custom domain alanına yazılır ve DNS'te CNAME kaydı `<kullanici_adin>.github.io` adresine yönlendirilir. GitHub SSL sertifikasını kendisi üretir.

## 7. Güzel yan ürün: skor arşivi

Bot her gün `data/skorlar.json` dosyasını commit ettiği için her günün ulusal risk haritası commit geçmişinde saklanır. Bu, ileride "geçmiş tahminler gerçek yangın tespitleriyle ne kadar örtüştü" (hindcast) analizi için bedava ve kendiliğinden biriken bir arşivdir; belediye pilotunda isabet doğrulamasının veri tabanı hazır olur.
