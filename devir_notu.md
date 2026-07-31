# YangınRiski.com devir notu
Hazırlanma tarihi: 30 Temmuz 2026

Bu dosya bir sonraki sohbete yüklenmek için hazırlandı. Projenin bulunduğu nokta, biten işler, açık işler ve tekrar eden sorunlar burada.

## Kısaca durum

Otomasyon kuruldu ve çalışıyor. GitHub Actions her sabah 07:00'de dönüyor, skorları üretiyor, bot repoya commit ediyor, panel GitHub Pages üzerinden yayında. Open-Meteo ticari planı alındı. CEMS doğrulaması tamamlandı ve yöntem dokümanına işlendi.

Repo: `burakwrites/Yangin-Riski` (public)
Panel: https://burakwrites.github.io/Yangin-Riski/

## Repo yapısı

    .github/workflows/gunluk_skor.yml    günlük koşu (cron 04:00 UTC = 07:00 TR)
                                         actions/checkout@v7, actions/setup-python@v6 (Node 24)
    operasyonel_hava.py                  Open-Meteo çekimi + FWI, durum taşıyan sürüm
    operasyonel_hafta.py                 skorlama, data/skorlar.json yazar
    fwi.py                               FWI motoru (Van Wagner)
    model_v3.json                        dondurulmuş birleşik model, 12 özellik
    noktalar_baz_grid.json               5254 hücre, ad alanı "lat,lon" biçiminde koordinat
    noktalar_idari.json                  hücre başına il, ilce ve hazır "yer" etiketi
    index.html                           panel, data/skorlar.json'u fetch eder
    data/skorlar.json                    panelin okuduğu günlük skor (bot yazar)
    data/fwi_durum.json                  FWI kodlarının dünkü hali (bot yazar)
    .gitignore                           operasyonel_tahmin.json, skor_bu_hafta.json, __pycache__/

## Mimari kararlar ve nedenleri

**Durum taşıyan zincir.** FWI özyinelemeli olduğu için her sabah 60 günlük geçmişi yeniden çekmek gereksiz. `data/fwi_durum.json` hücre başına FFMC, DMC, DC, yağışsız gün sayacı ve son 30 günün yağışını taşır; günlük istek penceresi 7 geçmiş artı 7 tahmin. Günlük ağırlıklı Open-Meteo maliyeti 25.100'den 5.254'e indi.

**Neden 7 geçmiş gün.** Ağırlık formülünde gün sayısının asgarisi 14, yani geçmiş 7 gün bedavaya geliyor. Karşılığında koşu birkaç gün patlarsa eksik günler kendiliğinden kapanıyor.

**Otomatik soğuk başlangıç.** Boşluk 7 günü aşarsa, durum dosyası bozulursa ya da ızgaraya yeni nokta eklenirse betik 60 günlük ısınmaya düşer. `OM_SOGUK=1` ile elle zorlanabilir. Soğuk başlangıç bir kerelik yaklaşık 25.100 çağrı harcar, tercihen yerelde koşturulur.

**Yağışsız gün sayacı 67'de sabit.** Durum taşıyınca sayaç sınırsız büyüyebilirdi ve model eğitim dağılımının dışına çıkardı. Eski 67 günlük pencerenin doğal sınırı korundu.

**Kısmi kayıp toleransı.** Bir batch alınamazsa o noktalar atlanır ve durumları dokunulmadan kalır, ertesi gün boşluk kapanır. Kayıp yüzde 10'u aşarsa betik hata koduyla durur, durum yazılmaz, skorlama adımına hiç geçilmez ve panel son başarılı günde kalır.

**API anahtarı.** Open-Meteo Standard planı, aylık 1 milyon çağrı, ticari kullanım lisansı. Anahtar `OM_APIKEY` adıyla repo Secrets'ında; kodda yazılı değil, ortam değişkeninden okunur. Anahtar varsa `customer-api.open-meteo.com` ucuna geçilir, batch 100 ve bekleme 1 saniye olur; yoksa ücretsiz uca düşer ve çalışmaya devam eder. Plana tarihsel hava API'si dahil değil, ama günlük zincir `forecast` ucundaki `past_days` ile çalıştığı için sorun değil.

## data/skorlar.json şeması

    uretim     koşu anının Türkiye saatiyle ISO damgası
    hafta      "31.05.2026 ile 06.06.2026" biçiminde metin
    tarihler   7 gün
    yer        812 tekil "İl / İlçe" etiketi (il merkezleri "Karaman Merkez" biçiminde)
    harita     hücre başına 15 alan: [lat, lon, tepe_risk, yer_indeksi, ortalama_risk, tepe_gün,
               ffmc, dmc, dc, isi, tmax, nem, rüzgar, yağışsız_gün, yağış_30g]
               10'dan sonraki alanlar da tepe güne aittir; panel bunları popup'ta gösterir
    top        en riskli 30 hücre, yedi günlük seyriyle

## Yaşanan sorunlar ve çözümleri

**ReadTimeout ile koşu düşüyordu.** Betikte yalnızca 429 yakalanıyordu. Zaman aşımı, bağlantı hatası ve 5xx de kademeli beklemeyle tekrar denenecek şekilde eklendi.

**Tempo bir kere yavaşlayınca geri hızlanmıyordu.** Adaptif bekleme yalnızca yukarı yönlüydü; tek bir aksaklık bütün koşuyu kalıcı yavaşlatıyordu. İlk düzeltmede temiz geçen istek tempoyu yüzde 20 aşağı çekmeye başladı, ama bu yetmedi (aşağıya bakınız).

**Zaman aşımı tempoyu yükseltmemeli.** 31 Temmuz koşusu 52 dakika sürdü. Log'da anahtar görünüyordu, öbek 100 ve tempo 1 saniyeydi; sorun ReadTimeout'lardı. Her zaman aşımı öbekler arası tempoyu 1,5 katına çıkarıyor, buna karşılık her başarılı istek yalnızca yüzde 20 geri çekiyordu. Bir öbek üç kez düşünce tempo 3,4 katına çıkıyor, arada bir iki başarılı istek bunu kapatamıyordu; tempo tavana (45 saniye) tırmanıp orada kilitleniyordu. Kalan otuz küsur öbek yalnızca beklemeyle yarım saat harcadı. Mantık hatası şuydu: kademeli yavaşlama kota (429) için tasarlanmıştı, oysa zaman aşımı kota işareti değil ağ ya da sunucu yavaşlığıdır ve beklemek onu çözmez. Artık tempoyu yalnızca 429 yükseltiyor; zaman aşımında yalnızca o istek için kademeli bekleniyor. Temiz geçen istek de tempoyu yüzde 20 değil yarı yarıya geri çekiyor. Aynı hata deseniyle yapılan hesapta koşu 35 dakikadan 9 dakikaya iniyor.

**Ticari uçta zaman aşımı 30 saniye dardı.** 100 noktalık istekler zaman zaman daha uzun sürüyor; erken bırakılan istek hem boşa gidiyor hem tekrar denemeyi getiriyordu. Varsayılan 60 saniyeye çıkarıldı. Zaman aşımı yine de sürerse `OM_BATCH: "50"` ile öbek küçültülebilir, toplam maliyet değişmez.

**Actions log'u boş görünüyordu.** Python çıktısı tamponluyordu. Workflow'a `PYTHONUNBUFFERED: "1"` eklendi.

**Ücretli planda da beklenen hız gelmedi.** Darboğaz kota değil ağ turu. Yukarıdaki iki düzeltmeden sonra beklenen koşu süresi 5 ile 10 dakika.

**Panel yerelden açılınca Bu Hafta sekmesi hata veriyor.** `fetch` dosya protokolünde engelleniyor. Yerel deneme için repo kökünde `python3 -m http.server 8000`.

## Ayarlanabilir ortam değişkenleri

`OM_APIKEY`, `OM_BATCH`, `OM_SLEEP`, `OM_TIMEOUT` (varsayılan 60), `OM_TRIES`, `OM_MAX_KAYIP`, `OM_PAST_DAYS`, `OM_ISINMA`, `OM_MAX_BOSLUK`, `OM_SOGUK`

## Açık işler

1. **Yöntem dokümanına durum taşıyan mimariyi işlemek.** Bölüm 10'daki DC notu ve bölüm 11 güncellenmeli. Önemli nokta: DC artık kesintisiz biriktiği için CEMS doğrulamasında bulunan 63 puanlık sistematik aşağı kayma iki üç ay içinde kendiliğinden kapanacak. Panelin mutlak sayıları bu süreçte bir miktar yükselecek, sıralama etkilenmiyor. Dokümanın sonuna o günün tarihiyle yeni bir "Son güncelleme" satırı eklenmeli.
2. **Birkaç gün koşuyu izlemek.** Süre, kayıp oranı ve durum dosyasının boyut seyri.
3. **Belediye pilotu.** Sahada isabet doğrulaması ve ilk gelir. Bot her gün skorları commit ettiği için hindcast arşivi kendiliğinden birikiyor.
4. **Yangın yayılım modülü.** Ayrı ürün, OGM iş birliği.
5. **İsteğe bağlı.** yanginriski.com alan adının Pages'e bağlanması, repoya README, durum dosyasının küçültülmesi (yağışların tam sayı olarak saklanması).

## Çalışma notları

Burak GitHub'ı bu projede ilk kez kullanıyor. Akış VS Code Source Control üzerinden: Pull, değiştir, mesaj yaz, Commit, Sync Changes. Sync adımı sık atlanıyor, hatırlatmakta fayda var.

Yanıtlarda tire ve kısa çizgi noktalama işareti olarak kullanılmıyor; bileşik teknik terimlerdeki tireler (Low-Code, S-NPP gibi) serbest.
