# YangınRiski.com devir notu
Son güncelleme: 6 Ağustos 2026

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

**İl/ilçe etiketleri doğu ve güneyde yanlıştı (6 Ağustos 2026).** "Bu Hafta" popup'ında bazı hücreler yanlış il/ilçe gösteriyordu (Siirt'e "Bitlis Merkez", Diyarbakır Lice'ye "Bingöl / Genç"). İki katmanlı hata: (1) WorldCover'la eklenen yeni hücreler, ilçe poligonunda etiketli eski hücre bulamayınca `idari_worldcover.py`'nin `nearest` yedeğiyle en yakın eski hücrenin ilini devralıyordu; eski ızgarada boş olan illerde (Siirt gibi) bu sınırı aşıyordu. (2) Eski il etiketlemesinde de yaygın sessiz hata vardı (Finike "Burdur", Anamur "Antalya", Ermenek "Mersin"). Çözüm: il ve ilçe resmi mülki idare sınırlarından (`İl_Sınırı`, `İlçe_Sınırı`, `Yerlesim_Noktas`) yetkili biçimde yeniden türetildi; ikisi de aynı kaynaktan geldiği için tutarlı, imkansız çift kalmadı. 887 il + 844 ilçe düzeldi. `noktalar_idari.json` (Deploy + arşiv) yeniden yazıldı, panel hemen düzelsin diye `data/skorlar.json`'un `yer`, harita indeksleri ve `top` alanları yamalandı. Kanonik yöntem artık `idari_resmi.py` (arşiv); `idari_worldcover.py`'nin nearest etiketlemesinin yerini alır ve ileride ızgara değişirse bu kullanılmalı. Not: OSM `network` plakası bazı illerde (Mersin, Zonguldak ilçeleri) yanlış olduğundan il yalnızca resmi poligondan alınır; OSM plakası sadece güneydoğuda birleşen 5 ilin (Gaziantep, Kilis, Mardin, Şanlıurfa, Şırnak) ada göre yedeğidir.

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

## 15 Ağustos 2026'da yapılanlar

Tetikleyici: Edirne Enez Büyükevren yangınının (11-12 Ağustos 2025) Geçmiş Yangınlar katmanında görünmemesi. İnceleme, hedef tanımında üç ayrı açık ortaya çıkardı ve üçü de kapatıldı. Ayrıntı yöntem dokümanı bölüm 12, İtiraz 3, 4 ve 5.

**Hedef kümesi artık yeniden üretilebilir.** Önceki 3.397 olaylık küme betiksiz duruyordu ve yöntem dokümanındaki tarif onu yeniden üretmiyordu (dört ayak izi tanımıyla denendi, uyum Cohen kappa 0,72 tavanında kaldı; korunan olayların yüzde 49'u dokümandaki eşiği sağlamıyordu). Kümeleme adımının sadık olduğu doğrulandı (225.856 tespit birebir, kümelerin boyutları yüzde 99,6 aynı), sapma filtre adımındaydı. `atolye/uretim/hedef_kur.py` yazıldı: parametreli, sabit tohumlu, her adımın sayısını manifeste yazan, önbelleği parametre değişince geçersizleyen. Yeni küme 2.054 pozitif ve 2.054 referans; betik iki koşuda birebir aynı sayıyı verdi.

**Pozitif ve referans sınıfı artık aynı kuralla tanımlanıyor.** Eskiden pozitifler ayak izi alan çoğunluğuyla, referanslar tek nokta testiyle taniniyordu. Yeni betikte her referans noktasına rastgele bir pozitif olayın tespit deseni giydiriliyor, yani iki sınıf aynı şekil ve alan üzerinden ölçülüyor. Referanslar ayrıca ilçe poligonlarıyla Türkiye kara sınırına kırpılıyor.

**model_v4, on üç özellik.** Tarım kenarına ikinci bir ölçüm eklendi: ESA WorldCover sınıf 40'a uzaklık. OSM'in yerine konduğunda kazanç yok (p 0,24), ama ikisi birlikte kullanıldığında beş katlı AUC 0,8424'ten 0,8480'e çıkıyor (eşleştirilmiş fark artı 0,0056, yüzde 95 aralık artı 0,0012 ile artı 0,0089). Sebep ikisinin farklı şey ölçmesi: log korelasyon yalnızca 0,456. Ayrıntı bölüm 7.9b. `noktalar_baz_grid.json` içine `farm_dist_wc` alanı eklendi (9.472 hücrenin hepsi dolu, ızgara kafesi ve mevcut alanlar değişmedi), `operasyonel_hafta.py` model_v4'ü yüklüyor.

Zincir uçtan uca sınandı: mevcut `operasyonel_tahmin.json` ile v3 ve v4 ayrı ayrı koşturuldu. İkisi de 9.472 hücrenin tamamını skorluyor, harita satırı 15 alanda kalıyor, hiçbir hücre düşmüyor. Tepe risk korelasyonu Pearson 0,969, Spearman 0,964; ilk 20 riskli ilçenin 14'ü ortak. Test sonrası `data/skorlar.json` botun sürümüne geri alındı.

## 17 Ağustos 2026'da yapılanlar

Hedef kümesi baştan kuruldu ve model yeniden dondurularak model_v5 üretildi. Ayrıntı yöntem dokümanı bölüm 7.11.

Üç değişiklik: temsil noktası ayak izi merkezinden **en erken tespite** çekildi (merkez, yangının yayıldığı yeri gösterir ve yayılım söndürmeye bağlıdır; eski boru hattının da bu sözleşmede olduğu, yeni noktaların eski indeksle yüzde 99.8 oranında yüz metre içinde örtüşmesiyle doğrulandı). Ölçüm operatörü iki sınıfta eşitlendi. Orman payı ikili kapı yerine iki sınıfa da uygulanan ağırlığa çevrildi. Bütün hava ve FWI özellikleri baştan çekildi (5.496 nokta), çünkü eski tablonun DC ve KBDI değerleri arşivdeki betikle yeniden üretilemiyordu.

**Manşet rakam düştü ve bu beklenen bir sonuçtur.** Beş katlı AUC 0.848'den 0.795'e indi. Sebep model değil örnekleme çerçevesi: eski kurulumda pozitiflerin çevre nüfus ortancası 551, referanslarınki 83'tü; yenide 479'a karşı 98. Tek başına nüfusun AUC'si 0.766'dan 0.721'e iniyor. Buna karşılık eşik duyarlılığı neredeyse yok oldu (eşiği yüzde 50'den 70'e çekmenin bedeli 0.049'dan 0.013'e indi) ve tezin katsayı sıralaması korundu; en güçlü ayraç hâlâ insan baskısı.

Enez yangını artık eğitim kümesinin içinde, 0.474 ağırlıkla.

Yeni betikler `atolye/uretim/` altında: `hedef_kur.py`, `egitim_noktalari_kur.py`, `egitim_hava_cek.py`, `model_v5_dondur.py`, `farmdist_wc_cek.py`, `model_v4_dondur.py`.

## Açık işler

1. **Operasyonel orman maskesini WorldCover'a taşımak. TAMAMLANDI (31 Temmuz 2026).** Izgara 5.254'ten 9.472 hücreye çıktı, eski hücreler ve kuraklık birikimi korundu, durum dosyası kısmi ısınmayla genişletildi, yöntem dokümanı bölüm 9 ve 10 güncellendi. İzlenecek: yeni hücrelerin ilk ısınması nedeniyle sonraki günlük koşuların süresi ve dosya boyutu (`data/skorlar.json` 455 KB'den ~800 KB'ye çıktı, panel her açılışta indiriyor).
2. **Birkaç gün koşuyu izlemek.** Süre (5 ile 10 dakika beklenir), kayıp oranı ve durum dosyasının boyut seyri. Tempo düzeltmesinin tuttuğunu görmek için log'da tempo değerinin 1 saniyede kalıp kalmadığına bakılmalı.
3. **DC yakınsamasını ölçmek.** DC kesintisiz biriktiğine göre CEMS'e karşı ölçülen sistematik kaymanın iki üç ay içinde kapanması bekleniyor. Sezon sonunda aynı karşılaştırma tekrarlanıp sonuç yöntem dokümanının 7.10 bölümüne işlenmeli.
4. **Belediye pilotu.** Sahada isabet doğrulaması ve ilk gelir. Bot her gün skorları commit ettiği için hindcast arşivi kendiliğinden birikiyor.
5. **Mesire ve orman parkı noktalarını skorlamak.** Izgarayı sıklaştırmak yerine önerilen yol. Belediyeye satılan bilgi ızgara noktası değil, hafta sonu insan giden piknik alanı. Ulusal ölçekte birkaç bin nokta eder.
6. **Yangın yayılım modülü.** Ayrı ürün, OGM iş birliği.
7. **İsteğe bağlı.** yanginriski.com alan adının Pages'e bağlanması, repoya README, durum dosyasının küçültülmesi.
8. **Yeni hedef kümesiyle modeli eğitmek.** `hedef_kur.py` 2.054 pozitif üretti ama bunların bir kısmı eski eğitim tablosunda yok, dolayısıyla hava ve FWI özellikleri elde değil. Open-Meteo arşivinden çekim gerekiyor. Bu yapılmadan model_v4 eski (kaynağı belgesiz) hedef kümesiyle eğitilmiş durumdadır; bu, bölüm 12 İtiraz 4'te açıkça yazılıdır.
9. **Hedef ölçütünü maruziyete taşımak.** Mevcut ölçüt yanmış alan bileşimine, yani bir sonuca bakıyor; sonuç söndürme başarısına bağlı olduğu için hedef kısmen söndürmeden kaçabilmiş yangınlara yanlı. Önerilen yön: tutuşma noktasının en yakın ormana uzaklığı, yani tutuşmadan önce var olan ve sağlam ölçülebilen bir büyüklük. Ayrıntı bölüm 12, İtiraz 3.
10. **Panelin Geçmiş Yangınlar katmanı.** Olaylar `index.html` içine gömülü (`const DATA={"events":[...],"n":3397,...}`, her kayıt `lat, lon, y, d, t, h, dsr, p30, lc, sz, i, il, ilce`). Doküman artık 2.748 olaydan söz ediyor, panel hâlâ 3.397 gösteriyor. Paneli güncellemek için yeni olaylara model skoru ve resmi il/ilçe etiketi üretilip `DATA` bloğu yeniden yazılmalı.
11. **model_v5'i canlıya almak.** Bekliyor, çünkü operasyonel ızgaranın hücreleri WorldCover orman maskesiyle tanımlı, eğitimdeki yüzde 40'lık ayak izi kuralıyla değil. Modeli değiştirmeden önce ızgara aynı kuralla yeniden türetilmeli, yoksa eğitim ile operasyon arasında yeni bir tanım farkı doğar. Ayrıca eğitimdeki `fuel` artık ayak izinden türeyen sürekli bir değer, ızgaradaki ise sınıf tabanlı; katsayısı küçük (eksi 0.07) ama tanım farkı kapatılmalı.
12. **`atolye/uretim/` sürüm kontrolünde değil.** İtiraz 4'ün tamamı "üreten betik arşivde yok" sorunuydu ve çözümü betikleri yazmaktı; ama o betikler şu an yalnızca yerel diskte duruyor, git'te değil. Bu haliyle aynı sorun tekrar edebilir. Ya `uretim/` deponun altına taşınıp izlenmeli ya da ayrı bir depo açılmalı. Ham veri ve ara ürünler `.gitignore`'da kalır.

## Izgara hakkında bilinenler

Aralık 0,05 derece. Türkiye enlemlerinde kuzey güney 5,6 km, doğu batı 4,1 ile 4,5 km; hücre yaklaşık 24 kilometrekare.

Izgarayı sıklaştırmak değerlendirildi ve **önerilmedi**. Sebep maliyet değil, kazancın olmaması: Open-Meteo yüksek çözünürlüklü 1 ile 2 km'lik bölgesel modelleri Türkiye'de kullanmıyor, bize gelen hava alanı 7 ile 11 km bandında. Yani ızgara zaten hava verisinden daha sıkı; sıklaştırmak zamansal eksene sıfır bilgi ekler. Mekansal eksende (nüfus) kazanç var ama 2 km yarıçaplı toplama yüzünden hızla azalıyor. Asıl kayıp çözünürlük değil kapsamaydı; bu yüzden maske OSM'den WorldCover'a taşındı (31 Temmuz 2026, yukarıda).

## Çalışma notları

Burak GitHub'ı bu projede ilk kez kullanıyor. Akış VS Code Source Control üzerinden: Pull, değiştir, mesaj yaz, Commit, Sync Changes. Sync adımı sık atlanıyor, hatırlatmakta fayda var.

Yanıtlarda tire ve kısa çizgi noktalama işareti olarak kullanılmıyor; bileşik teknik terimlerdeki tireler (Low-Code, S-NPP gibi) serbest.
