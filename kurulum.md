# YangınRiski.com Otomasyon ve Yayın Kurulumu
Güncelleme tarihi: 30 Temmuz 2026 (durum taşıyan mimari)

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
      data/skorlar.json                    (panelin okuduğu günlük skor; botun yazdığı)
      data/fwi_durum.json                  (FWI kodlarının dünkü hali; soğuk başlangıçta üretilir)
      .gitignore                           (ara çıktılar için, aşağıda)

Ara çıktılar repoda tutulmasa da olur, `.gitignore` içeriği şu kadar yeterli:

    operasyonel_tahmin.json
    skor_bu_hafta.json

Not: workflow dosyasının yolu birebir `.github/workflows/gunluk_skor.yml` olmalı, GitHub başka yerde aramaz.

## 2. Betik uyarlamaları (tamamlandı)

operasyonel_hava.py: durum taşıyan sürüm. Her sabah 60 günlük geçmişi yeniden çekmek yerine FWI kodlarının dünkü halini `data/fwi_durum.json` dosyasından okur, sadece yeni günleri işleyip ilerletir ve durumu geri yazar. İstek penceresi 67 günden 14 güne (7 geçmiş + 7 tahmin) iner; günlük ağırlıklı Open-Meteo maliyeti yaklaşık 25.100'den 5.254'e düşer, yani ücretsiz günlük sınırın (10.000) yarısına.

Geçmiş 7 gün bedavaya gelir, çünkü ağırlık formülünde gün sayısının asgarisi 14'tür. Faydası: koşu birkaç gün patlarsa eksik günler ertesi koşuda kendiliğinden tamamlanır. Boşluk 7 günü aşarsa, durum dosyası bozulursa ya da ızgaraya yeni nokta eklenirse betik kendiliğinden soğuk başlangıca (60 gün ısınma) düşer. `OM_SOGUK=1` ile elle de zorlanabilir.

Zaman aşımı, bağlantı hatası, 429 ve 5xx kademeli beklemeyle tekrar denenir; bir batch yine de alınamazsa o noktalar atlanır ve durumları dokunulmadan kalır. Kayıp yüzde 10'u aşarsa betik hata koduyla durur, durum yazılmaz ve skorlama adımına hiç geçilmez. Ayarlar ortam değişkenleriyle değiştirilebilir: `OM_BATCH`, `OM_SLEEP`, `OM_TIMEOUT`, `OM_TRIES`, `OM_MAX_KAYIP`, `OM_PAST_DAYS`, `OM_ISINMA`, `OM_MAX_BOSLUK`, `OM_SOGUK`.

Çıktısı `operasyonel_tahmin.json`, şeması değişmedi.

operasyonel_hafta.py: yeni sürüm iki dosya yazar. `data/skorlar.json` panelin okuduğu dosyadır ve şu alanları taşır: `uretim` (koşu anının Türkiye saatiyle ISO damgası), `hafta` (gün aralığı metni), `tarihler` (7 gün), `yer` (il ve ilçe etiketleri listesi), `harita` (hücre başına `[lat, lon, tepe_risk, yer_indeksi, ortalama_risk, tepe_gün, ffmc, dmc, dc, isi]`), `top` (en riskli 30 hücre, yedi günlük seyriyle). `skor_bu_hafta.json` ise ayrıntılı insan okur çıktı olarak korunur, hata ayıklama ve arşiv içindir. Boyut yaklaşık 330 KB.

`noktalar_idari.json` bulunamazsa betik durmaz, yer etiketlerini koordinat olarak yazar ve konsola uyarı basar. Dosya varsa hem liste (`il` ve `ilce` alanlı kayıtlar) hem sözlük (`"lat,lon" : "İl / İlçe"`) biçimini tanır, eşleştirmeyi üç haneye yuvarlanmış koordinat üzerinden yapar.

index.html (panel): Bu Hafta verisini gömülü sabitten değil `data/skorlar.json` adresinden fetch eder ve haritanın sağ alt köşesinde "Son güncelleme: <tarih>" gösterir. Koşu bir gün başarısız olursa panel son başarılı günün dosyasını göstermeye devam eder; damga 36 saatten eskiyse ibare turuncuya döner ve "son başarılı koşu" notu eklenir, yani tarih ibaresi durumu kullanıcıya dürüstçe söyler.

## 3. API anahtarı (ticari plan)

Open-Meteo Standard planı alındı: aylık 1 milyon çağrı, ticari kullanım lisansı, özel sunucu ve günlük/saatlik sınır yok. Durum taşıyan mimariyle günlük ihtiyaç yaklaşık 5.254 çağrı, yani ayda 158.000; bütçenin altıda biri.

Anahtar hiçbir dosyada yazılı değildir, ortam değişkeninden okunur. Betik anahtar görürse `customer-api.open-meteo.com` ucuna geçer, isteğe `apikey` parametresi ekler ve tempoyu hızlandırır (batch 100, bekleme 1 saniye). Anahtar yoksa ücretsiz uca düşer ve yavaş tempoyla çalışmaya devam eder, yani hiçbir şey kırılmaz.

**GitHub tarafı**: Repo > Settings > Secrets and variables > Actions > New repository secret. Ad `OM_APIKEY`, değer anahtarın. Workflow bunu ilgili adıma ortam değişkeni olarak geçirir; GitHub secret değerini log çıktısında otomatik gizler.

**Kendi bilgisayarında**: terminalde anahtarı ver, dosyaya yazma.

    # Windows PowerShell
    $env:OM_APIKEY="anahtarin"

    # Mac ve Linux
    export OM_APIKEY=anahtarin

Anahtar bir şekilde sızarsa Open-Meteo müşteri panelinden yenile; kurulumda değişecek tek şey Secrets'taki değer olur.

## 4. İlk kurulum: soğuk başlangıç

Durum dosyası bir kez üretilmeli. Bunu GitHub'da değil kendi bilgisayarında çalıştır, çünkü soğuk başlangıç yaklaşık 25.100 ağırlıklı çağrı harcar ve ortak IP kullanan koşucularda hız sınırına takılır. Klasörde:

    python operasyonel_hava.py

Betik durum dosyası olmadığını görüp soğuk başlangıç moduna geçer, 60 günlük ısınmayla `data/fwi_durum.json` dosyasını üretir. Sonra:

    python operasyonel_hafta.py

`data/skorlar.json` güncellenir. İki dosyayı da commit edip gönder. Bundan sonra bot her sabah ılık modda dönecek, soğuk başlangıç bir daha gerekmeyecek (durum bozulmadıkça).

Not: soğuk başlangıç yaklaşık 25.100 ağırlıklı çağrı harcar. Ticari planın aylık bütçesinde bu bir yuvarlama hatası, ücretsiz uçta ise günlük sınırın 2,5 katıdır. Yarıda kesilirse çıktı dosyası duruyorsa betik kaldığı yerden devam eder, yeniden çalıştırman yeterli.

## 5. Yerel deneme

`fetch` yerelden `file://` ile açıldığında tarayıcı engeller, panel Bu Hafta sekmesinde hata kartı gösterir. Lokalde denemek için repo kökünde küçük bir sunucu çalıştır:

    python3 -m http.server 8000

sonra `http://localhost:8000/index.html` adresini aç. Pages'te bu sorun yoktur.

## 6. Actions'ı etkinleştirme

Dosyalar push edildikten sonra repo > Actions sekmesi > "Gunluk risk skorlama" workflow'u görünür. İlk denemeyi beklemeden yapmak için "Run workflow" düğmesiyle elle tetikle. Anahtar tanımlıysa koşu yaklaşık 3 ile 8 dakika sürer (53 istek, batch 100, aralarda 1 saniye). Anahtarsız ücretsiz uçta 45 ile 75 dakikaya çıkar, çünkü tempo dakikalık sınıra göre yavaşlatılır. Bittiğinde `data/skorlar.json` güncellenmiş ve commit edilmiş olmalı.

Zamanlama notu: GitHub cron'u dakika hassasiyeti garanti etmez, 07:00 hedefi bazen 07:15'e sarkar; günlük bir sistem için önemsizdir.

429 notu: ticari uçta günlük ve saatlik sınır olmadığı için 429 beklenmiyor. Yine de kademeli bekleme ve adaptif tempo mantığı yerinde duruyor; anahtar bir sebeple devre dışı kalırsa betik ücretsiz uca düşüp yavaş tempoyla tamamlar.

## 7. GitHub Pages ile yayın

Repo > Settings > Pages > Source: "Deploy from a branch", Branch: main, klasör: / (root). Birkaç dakika içinde panel şu adreste yayında olur:

    https://<kullanici_adin>.github.io/yanginriski/

Panel ve data/ aynı repoda olduğu için fetch göreli yolla (`data/skorlar.json`) çalışır, ek ayar gerekmez.

## 8. Alan adı bağlama (istenirse, sonraki adım)

yanginriski.com alınmışsa Pages ayarlarında Custom domain alanına yazılır ve DNS'te CNAME kaydı `<kullanici_adin>.github.io` adresine yönlendirilir. GitHub SSL sertifikasını kendisi üretir.

## 9. Güzel yan ürün: skor arşivi

Bot her gün `data/skorlar.json` ve `data/fwi_durum.json` dosyalarını commit ettiği için her günün ulusal risk haritası commit geçmişinde saklanır. Bu, ileride "geçmiş tahminler gerçek yangın tespitleriyle ne kadar örtüştü" (hindcast) analizi için bedava ve kendiliğinden biriken bir arşivdir; belediye pilotunda isabet doğrulamasının veri tabanı hazır olur.
