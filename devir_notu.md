# YangınRiski.com devir notu
Son güncelleme: 31 Temmuz 2026

Projenin bulunduğu nokta, biten işler, açık işler ve tekrar eden sorunlar burada. Bozulmaması gereken kurallar ve dosya haritası için `CLAUDE.md` dosyasına bakınız.

## Kısaca durum

Otomasyon kuruldu ve çalışıyor. GitHub Actions her sabah 07:00'de dönüyor, skorları üretiyor, bot repoya commit ediyor, panel GitHub Pages üzerinden yayında. Open-Meteo ticari planı alındı. CEMS doğrulaması tamamlandı ve yöntem dokümanına işlendi. Panel 31 Temmuz'da elden geçirildi: iki dilli oldu, görsel dil sadeleşti, bayat sayılar düzeltildi.

Operasyonel orman maskesi 31 Temmuz'da OpenStreetMap'ten ESA WorldCover'a taşındı: ızgara 5.254'ten 9.472 hücreye çıktı (eski hücreler ad, nüfus ve kuraklık birikimiyle birebir korundu, WorldCover'ın orman gördüğü 4.218 yeni hücre eklendi), durum dosyası kısmi ısınmayla 9.472 hücreye genişletildi. Ayrıntı yöntem dokümanı bölüm 9 ve 10.

Repo: `burakwrites/Yangin-Riski` (public)
Panel: https://burakwrites.github.io/Yangin-Riski/

## Repo yapısı

    .github/workflows/gunluk_skor.yml    günlük koşu (cron 04:00 UTC = 07:00 TR)
                                         actions/checkout@v7, actions/setup-python@v6 (Node 24)
    operasyonel_hava.py                  Open-Meteo çekimi + FWI, durum taşıyan sürüm
    operasyonel_hafta.py                 skorlama, data/skorlar.json yazar
    fwi.py                               FWI motoru (Van Wagner)
    model_v3.json                        dondurulmuş birleşik model, 12 özellik
    noktalar_baz_grid.json               9472 hücre (WorldCover maskesi), ad alanı "lat,lon" biçiminde koordinat
    noktalar_idari.json                  hücre başına il, ilce ve hazır "yer" etiketi
    index.html                           panel, data/skorlar.json'u fetch eder
    data/skorlar.json                    panelin okuduğu günlük skor (bot yazar)
    data/fwi_durum.json                  FWI kodlarının dünkü hali (bot yazar)
    .gitignore                           operasyonel_tahmin.json, skor_bu_hafta.json, __pycache__/

## Mimari kararlar ve nedenleri

**Durum taşıyan zincir.** FWI özyinelemeli olduğu için her sabah 60 günlük geçmişi yeniden çekmek gereksiz. `data/fwi_durum.json` hücre başına FFMC, DMC, DC, yağışsız gün sayacı ve son 30 günün yağışını taşır; günlük istek penceresi 7 geçmiş artı 7 tahmin. Günlük ağırlıklı Open-Meteo maliyeti 25.100'den 5.254'e indi.

**Neden 7 geçmiş gün.** Ağırlık formülünde gün sayısının asgarisi 14, yani geçmiş 7 gün bedavaya geliyor. Karşılığında koşu birkaç gün patlarsa eksik günler kendiliğinden kapanıyor.

**Kısmi ısınma.** Izgaraya yeni nokta eklendiğinde eski hücreler ILIK kalır ve yalnızca yeni hücreler 60 günlük pencereyle ısınır; böylece maske genişletilirken mevcut hücrelerin DC birikimi sıfırlanmaz. Eksik oran `OM_KISMI_UST` değerini (varsayılan 0,50) aşarsa tam soğuk başlangıca düşülür.

**Otomatik soğuk başlangıç.** Boşluk 7 günü aşarsa ya da durum dosyası bozulursa betik 60 günlük ısınmaya düşer. `OM_SOGUK=1` ile elle zorlanabilir. Soğuk başlangıç bir kerelik yaklaşık 25.100 çağrı harcar, tercihen yerelde koşturulur.

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

`OM_APIKEY`, `OM_BATCH`, `OM_SLEEP`, `OM_TIMEOUT` (varsayılan 60), `OM_TRIES`, `OM_MAX_KAYIP`, `OM_PAST_DAYS`, `OM_ISINMA`, `OM_MAX_BOSLUK`, `OM_KISMI_UST` (varsayılan 0,50), `OM_SOGUK`

## 31 Temmuz 2026'da yapılanlar

**Panel iki dilli oldu.** Bütün metinler `const METIN={tr,en}` sözlüğünde toplandı, koda `T.anahtar` diye giriyor. Başlıkta TR ve EN bayraklı düğme var, dil adres satırında `?lang=en` ile taşınıyor, yani İngilizce bağlantı paylaşılabiliyor. Yeni metin eklerken iki dile birden eklemek gerek.

**Görsel dil sadeleştirildi.** Renk veriye ayrıldı: doygun renk yalnızca haritada, risk çubuklarında ve lejantta kaldı, arayüz kontrolleri nötr krem oldu. Arayüz yazı tipi sans oldu, serif yalnızca marka ve kart başlıklarında. Mobilde zaman şeridinin taştığı hata giderildi (şerit iki satıra ayrıldı, altına on yılın tik işaretleri eklendi). Sekmeler mobilde yatay kayan şeride dönüştü. Başlık şeridi sabitlendi. Favicon ve logo piksel alev ikonuna geçti, base64 olarak dosyaya gömülü, ayrı dosya yok.

**Bayat sayılar düzeltildi.** Yıllar arası AUC iki yerde 0.86 yazıyordu; doğrusu temel sürümde 0.83, birleşik modelde 0.84. Yöntem Özeti'nde orman olayı sayısı 2.702 yazıyordu, doğrusu 3.397. İki eksen kartındaki 0.83'ün "tam model" değil "iki eksen" olduğu netleştirildi, güncel birleşik modelin 0.84'ü ayrıca yazıldı.

**Terminoloji kuralı yerleşti.** Sayılan nesne yangın, modellenen olgu tutuşma. Sekme adı "Geçmiş Yangınlar" oldu; tutuşma kelimesi marka satırından ve sayfa başlığından da çıktı, yalnızca Yöntem Özeti'ndeki tez ve sınır cümlelerinde kaldı.

**FWI kartı eklendi.** Sistemin yapısı (girdi, üç nem kodu ve kuruma hızları, ISI, BUI, FWI bileşim kuralları), Van Wagner ve Pickett 1985 kaynağı, EFFIS ve Copernicus'un aynı sistemi kullandığı, bir de dürüst not: FWI ham değişkenlerin yerine konduğunda modeli geçmemişti.

**Bu Hafta popup'ına ham hava eklendi.** `data/skorlar.json` harita satırı 10 alandan 15'e çıktı, tepe günün sıcaklık, nem, rüzgar, yağışsız gün ve 30 günlük yağış değerleri taşınıyor. Ek boyut yaklaşık 100 KB.

**Panelde hata göstericisi var.** Harita katmanlarındaki bir hata eskiden bütün React ağacını düşürüyor ve siyah ekran bırakıyordu. Katmanlar yalıtıldı; ayrıca panel açılamazsa siyah ekran yerine hatanın metni yazılıyor.

## Açık işler

1. **Operasyonel orman maskesini WorldCover'a taşımak. TAMAMLANDI (31 Temmuz 2026).** Izgara 5.254'ten 9.472 hücreye çıktı, eski hücreler ve kuraklık birikimi korundu, durum dosyası kısmi ısınmayla genişletildi, yöntem dokümanı bölüm 9 ve 10 güncellendi. İzlenecek: yeni hücrelerin ilk ısınması nedeniyle sonraki günlük koşuların süresi ve dosya boyutu (`data/skorlar.json` 455 KB'den ~800 KB'ye çıktı, panel her açılışta indiriyor).
2. **Birkaç gün koşuyu izlemek.** Süre (5 ile 10 dakika beklenir), kayıp oranı ve durum dosyasının boyut seyri. Tempo düzeltmesinin tuttuğunu görmek için log'da tempo değerinin 1 saniyede kalıp kalmadığına bakılmalı.
3. **DC yakınsamasını ölçmek.** DC kesintisiz biriktiğine göre CEMS'e karşı ölçülen sistematik kaymanın iki üç ay içinde kapanması bekleniyor. Sezon sonunda aynı karşılaştırma tekrarlanıp sonuç yöntem dokümanının 7.10 bölümüne işlenmeli.
4. **Belediye pilotu.** Sahada isabet doğrulaması ve ilk gelir. Bot her gün skorları commit ettiği için hindcast arşivi kendiliğinden birikiyor.
5. **Mesire ve orman parkı noktalarını skorlamak.** Izgarayı sıklaştırmak yerine önerilen yol. Belediyeye satılan bilgi ızgara noktası değil, hafta sonu insan giden piknik alanı. Ulusal ölçekte birkaç bin nokta eder.
6. **Yangın yayılım modülü.** Ayrı ürün, OGM iş birliği.
7. **İsteğe bağlı.** yanginriski.com alan adının Pages'e bağlanması, repoya README, durum dosyasının küçültülmesi.

## Izgara hakkında bilinenler

Aralık 0,05 derece. Türkiye enlemlerinde kuzey güney 5,6 km, doğu batı 4,1 ile 4,5 km; hücre yaklaşık 24 kilometrekare.

Izgarayı sıklaştırmak değerlendirildi ve **önerilmedi**. Sebep maliyet değil, kazancın olmaması: Open-Meteo yüksek çözünürlüklü 1 ile 2 km'lik bölgesel modelleri Türkiye'de kullanmıyor, bize gelen hava alanı 7 ile 11 km bandında. Yani ızgara zaten hava verisinden daha sıkı; sıklaştırmak zamansal eksene sıfır bilgi ekler. Mekansal eksende (nüfus) kazanç var ama 2 km yarıçaplı toplama yüzünden hızla azalıyor. Asıl kayıp çözünürlük değil kapsamaydı; bu yüzden maske OSM'den WorldCover'a taşındı (31 Temmuz 2026, yukarıda).

## Çalışma notları

Burak GitHub'ı bu projede ilk kez kullanıyor. Akış VS Code Source Control üzerinden: Pull, değiştir, mesaj yaz, Commit, Sync Changes. Sync adımı sık atlanıyor, hatırlatmakta fayda var.

Yanıtlarda tire ve kısa çizgi noktalama işareti olarak kullanılmıyor; bileşik teknik terimlerdeki tireler (Low-Code, S-NPP gibi) serbest.
