# YangınRiski.com
# Metodoloji Dokümanı (ulusal sürüm)

Bu doküman, Türkiye geneli orman yangını tutuşma riski tahmin projesinin yöntemini, kullanılan veriyi, çıkan bulguları, sınırları ve mevcut durumu detaylarıyla kaydeder. Amaç hem ileride referans olmak hem de teknik bir muhataba (yatırımcı, OGM, belediye) sürecin nasıl yürüdüğünü dürüstçe göstermektir.

---

## 1. Çıkış Noktası ve Hipotez

Türkiye'de yaz orman yangınlarının asıl tetikleyicisi kuraklığın kendisi değil, ormana giden insanın davranışıdır. Ateş, mangal közü, sigara izmariti gibi insan kaynaklı kıvılcımlar tutuşmayı başlatır; kuraklık yalnızca zemini hazırlar. Kuru orman tek başına yanmaz, bir kıvılcım gerekir ve o kıvılcımı ezici çoğunlukla insan çakar.

Hipotez iki ölçülebilir iddiaya ayrıldı:
Birincisi, sıcaklık ve kuraklık zemini hazırlar (literatürde ve resmi veride yerleşik).
İkincisi, ormana insan erişimi tutuşmayı tetikler. Bu, başlangıçta "ormana atılan çöp" biçiminde düşünülmüştü; ancak çöpün kendisi tutuşturucu değildir (cam şişenin yangın başlatması fiziksel olarak nadirdir, plastik yalnızca yanan malzemedir). Asıl etken çöple birlikte gelen insan davranışıdır. Bu yüzden "insan erişimi" doğrudan ölçülebilir değişken olarak benimsendi.

---

## 2. Ürün Konumlandırması

Açık ve kamuya açık veriyle çalışan bir girişim. İlk hedef müşteri, orman ile yerleşim sınırındaki belediyeler. Değer önerisi: "Bu hafta sonu hangi mesire alanına denetim ekibi göndermeliyim." Ürün yangın söndürmez; tutuşmayı önler. Böylece OGM'nin makro yangın yönetimiyle rekabet etmek yerine onun altındaki yerel önleyici denetim katmanını doldurur.

---

## 3. Yaklaşımın Ölçeği: Türkiye Geneli

Proje doğrudan ulusal ölçekte kurulmuştur. Yöntem önce tek bir bölgede prototiplendi; ancak tek bölgede yıl başına düşen bağımsız yangın olayı sayısının istatistiksel bir tahmin modeli için çok az olduğu görüldü (tek bölgede on yılda yalnızca yaklaşık dokuz bağımsız orman yangını olayı çıkıyordu, ve model tek bir felaket yılını ezberleme eğilimindeydi). Bu ders, ulusal ölçeğin zorunlu olduğunu netleştirdi. Bütün doğrulama ve sonuçlar Türkiye geneli veriyle üretilmiştir.

---

## 4. Veri Katmanları

### 4.1 Geçmiş yangınlar: NASA FIRMS
Uydu tabanlı aktif yangın (active fire) tespitleri; FIRMS'in sunduğu sıcak nokta arşivinin VIIRS S-NPP 375 metre ürünü (Collection 2, bilim kalitesi), 2012'den bugüne kesintisiz. Tüm Türkiye için 2016'dan itibaren yaklaşık 420 bin tespit; yaz aylarına (Haziran ile Eylül) ait 225.856 tespit kullanıldı.

Sensör seçimi (neden S-NPP): FIRMS aktif yangın kapısı birden çok ürün sunar (MODIS 1 kilometre, VIIRS S-NPP 375 metre, VIIRS NOAA-20 ve NOAA-21, Landsat OLI 30 metre). Üç gerekçeyle S-NPP seçildi. Birincisi çözünürlük: orman ile tarlayı, hatta bahçe ile ormanı ayırmak ve tespitleri olaylara kümelemek için MODIS'in 1 kilometresi çok kaba kalır; 375 metre bu ayrımı mümkün kılar. İkincisi ve en önemlisi tek sensör tutarlılığı: NOAA-20 yalnızca Nisan 2018'den, NOAA-21 ise Ocak 2024'ten beri veri verir; bunları eklemek, yeni uydunun devreye girdiği yıl tespit sayısını yapay olarak sıçratır ve 2016 ile 2025 arası yıl yıl karşılaştırmayı bozardı. S-NPP tek başına tüm pencereyi tutarlı bir geçiş sıklığı ve tespit karakteriyle kaplar. Üçüncüsü zamansal sıklık: Landsat OLI 30 metre daha da keskindir ama yalnızca Haziran 2022'den beri vardır ve 16 günde bir geçer, günlük tutuşma tespiti için fazla seyrektir.

Dürüstçe vazgeçilenler: MODIS seçilseydi 2000'e uzanan daha uzun bir tarihsel kayıt olurdu; NOAA-20 ve NOAA-21 eklenseydi daha yoğun tespit elde edilirdi. Bu ikincisi operasyonel katman için (canlı, 7 günlük tahmin tarafı) mantıklı olabilir, çünkü orada amaç hızlı tespittir, tutarlı tarihsel karşılaştırma değil. Eğitim verisinde önceliğimiz tutarlılıktı.

Bir ayrım daha: FIRMS'te "yanan alan" (burned area, MODIS MCD64) adlı ayrı bir ürün de vardır; o, yangının yanıp bitirdiği alanı, yani yayılımı haritalar. Yayılım bu ürünün değil, ayrı bir modülün ve OGM'nin konusudur. Bizim kullandığımız aktif yangın tespiti ise önleme için gereken tutuşma noktasıdır.

### 4.2 Hava: Open-Meteo arşivi
Günlük geçmiş veri: en yüksek sıcaklık, nem, rüzgar, yağış. Kümülatif kuraklık türetildi: "son yağıştan beri geçen gün" (1 milimetreden fazla yağış anlamlı) ve "son 30 günün yağış toplamı". Bu iki değişken, başlangıçtaki biriken kuruluk sezgisinin ölçülebilir halidir.

### 4.3 Arazi örtüsü ve yakıt: ESA WorldCover
10 metre çözünürlük, 2021 sürümü. Cloud-Optimized GeoTIFF sayesinde dev dosya indirilmeden yalnızca gereken pikseller okundu. İki işe yaradı: orman dışı (anız) yangınlarını filtrelemek ve yakıt katmanını sağlamak. WorldCover bu işlevleri eğitim verisinde gördü (her olayın ayak izindeki arazi örtüsü ve yakıt). Operasyonel ulusal ızgarada ise WorldCover rasterı elde olmadığından orman maskesi OpenStreetMap orman poligonlarından alındı ve yakıt orman varsayıldı; yakıtın modeldeki ağırlığı çok düşük olduğundan (katsayı yaklaşık 0.07 büyüklüğünde, negatif) bu basitleştirmenin etkisi ihmal edilebilir.

### 4.4 İnsan baskısı: WorldPop
Türkiye nüfus dağılımı 2020, yaklaşık 100 metre çözünürlük. Her noktanın çevresinde yaklaşık 2 kilometre yarıçaplı dairesel alanın toplam nüfusu hesaplandı; bu, ormana insan erişiminin (orman ile yerleşim sınırı baskısının) vekilidir. Tek bir orman pikselinin nüfusu sıfır olacağından komşuluk toplamı kullanıldı.

Yarıçapın kesinleştirilmesi (kalibrasyon): Ulusal ızgarayı kurarken, ızgara hücrelerinin nüfusunu eğitimdekiyle birebir aynı tanımla hesaplamak kritikti; çünkü model, en güçlü değişkeni olan nüfusu eğitimdeki ölçeğe göre standardize etti ve farklı bir yarıçap skorları sessizce bozardı. Eğitim noktalarının saklı nüfus değerleri, WorldPop'tan farklı yarıçaplarda yeniden üretilerek hangi yarıçapın bu değerleri verdiği arandı. 2 kilometre yarıçap saklı değerleri neredeyse birebir verdi (noktalar arası korelasyon 0.997, ortanca oran 1.11). Böylece eğitimdeki çevre nüfusun fiilen 2 kilometre yarıçaplı bir toplam olduğu ampirik olarak doğrulandı; ulusal ızgarada da aynı yarıçap ve küçük bir kalibrasyon böleni (1.11) kullanılarak nüfus ölçeği eğitimle hizalandı.

### 4.5 Operasyonel hava: Open-Meteo forecast
Canlı 7 günlük tahmin. Eğitim (arşiv) ile operasyon (tahmin) aynı kaynaktan beslendiği için değişken tanımları kaymaz. Biriken kuraklık kesintisiz hesaplanır; mevcut operasyonel sürümde bu süreklilik, geçmişi her koşuda yeniden çekerek değil kuraklık kodlarını bir durum dosyasında taşıyarak sağlanır (bölüm 9). Operasyonel sürümde bu tahmin, ulusal orman ızgarasının her noktası için çekilir ve eğitimdeki kuruluk değişkenlerinin aynısı üretilir. Ham hava değişkenlerinin standart yangın hava indekslerine (FWI sistemi) çevrilmesi ayrıca yürütülmektedir; bkz. bölüm 7.8.

---

## 5. Hedefin Tanımı: Tutuşma Olayları

Önemli bir metodolojik nokta: uydu tespiti ile yangın çıkışı aynı şey değildir. Tek bir yangın günlerce yanıp onlarca piksel tespiti üretir. Bu yüzden tespitler zaman ve mekanda kümelenip her olayın ilk tespiti bir tutuşma sayıldı.

Kümeleme yöntemi: 3 boyutlu ızgara hash ile birleştirme-bulma (union-find). İki tespit, birbirine 2 kilometreden yakın ve 4 günden az aralıkla ise aynı olaya bağlanır. Duyarlılık testi yapıldı: çok daha dar eşiklerde bile sonuç düzen olarak korundu.

Tüm Türkiye yaz tespiti (225.856) kümelendiğinde 53.593 tutuşma olayı çıktı.

İki önemli bulgu:
Yıllara göre olay sayısı oldukça istikrarlı (yılda 2.850 ile 8.061 arası). Felaket yılı 2021'de daha az olay vardı ama olay başına tespit (yanan alan vekili) neredeyse iki kat. Yani her yaz benzer sayıda yangın çıkıyor; felaketi belirleyen, çıkan yangınların kaçının aşırı hava koşullarında dev yangına dönüştüğüdür.

---

## 6. Anız Temizliği

Ürünün hedefi orman olduğundan, tarımsal hasat sonrası tarla yakma (anız) yangınlarının ayıklanması gerekti. ESA WorldCover ile bakıldığında 53.593 olayın büyük çoğunluğunun, yaklaşık yüzde 94'ünün, ağırlıklı olarak tarla, otlak, yerleşim ya da su üzerinde olduğu görüldü; yani büyük çoğunluğu anız yangınıydı. En yoğun anız bölgeleri Çukurova, Şanlıurfa, Adıyaman gibi büyük tarım ovaları.

Orman olaylarını ayırmak için iki yöntem denendi. İlk yöntem olayın yalnızca ilk tespitinin arazi örtüsüne bakıyordu; basitti ama bir kör noktası vardı: tarlada başlayıp ormana sıçrayan yangınları, ilk piksel tarla olduğu için orman dışı sayıp eliyordu. Bu yüzden ikinci ve mevcut yöntem ayak izine geçti: bir olay, tüm tespitlerinin çoğunluğu (yüzde 50 ve üzeri) ağaç ya da maki üzerindeyse orman olayı sayılır. Böylece tarladan ormana sıçrayan gerçek orman yangınları geri kazanılırken, ayak izinin çoğunluğu tarla olan olaylar elenir. Bu geçişin somut bir örneği için bölüm 10'a bakınız.

Sınıflar:
Ağaç örtüsü (kod 10), yakıt ağırlığı 1.0.
Çalılık ve maki (kod 20), yakıt ağırlığı 0.85.
Ekili alan (40), yerleşim (50), çıplak (60), su (80) ve diğerleri yakıt taşımaz, hedeften elendi.

Ayak izi yöntemiyle, ayak izinin çoğunluğu orman ya da maki olan 3.397 tutuşma olayı kaldı (3.160 ağaç, 237 maki). Eşik yüzde 50 seçildi; bu, ayak izinin yarısından fazlasının orman olmasını şart koşar.

---

## 7. Model ve Doğrulama

### 7.1 Çekirdek mantık
Tutuşma riski iki katmanın birleşimidir: İnsan Baskısı ve Doğal Kuruluk. Mantık çarpımsaldır; iki faktör çakışmadan risk yükselmez. Kuru ama ıssız bir yamaç da, kalabalık ama nemli bir koru da düşük risklidir. Tehlike, kuruluğun ve insanın buluştuğu yerdedir.

### 7.2 Varlık ile arka plan tasarımı
Model "tutuşma olan yer" ile "olmayan yer"i ayırt edebilmek için referans noktalarına ihtiyaç duyar. Türkiye genelinde rastgele noktalar üretilip WorldCover ile gerçekten orman ya da maki olanları tutuldu (3.418 referans noktası), her birine olay havuzundan rastgele bir tarih atandı.

### 7.3 İnsan baskısı sinyali
Tutuşma noktaları: ortalama çevre nüfus 4.734, medyan 551.
Referans noktaları: ortalama çevre nüfus 740, medyan 83.
Yangın çıkan orman noktalarında çevre nüfus, çıkmayanlara kıyasla yaklaşık altı buçuk kat yüksek. Orman tutuşması, insanın olduğu yerde oluyor.

### 7.4 Mekansal model
İnsan baskısı (log dönüşümlü çevre nüfus) ve yakıt ile lojistik regresyon eğitildi.
Beş katlı çapraz doğrulama AUC: 0.768.
Sadece insan baskısı tek başına AUC: 0.766 (gücün neredeyse tamamı bu değişkenden).
İnsan baskısı katsayısı (standardize): +1.17, baskın ve pozitif.

### 7.5 Genellenebilirlik (en sağlam sonuç)
Yıllar arası test (her yıl, o yılı görmemiş modelle): her yıl 0.74 ile 0.82 arası, ortalama 0.77. 2021 dahil her yıl tutarlı. Model tek bir felaket yılını ezberlememiş, on yılın her birinde tutarlı çalışıyor. Bu, genellenebilir bir ulusal modeldir.

### 7.6 Tam iki eksenli model
İnsan baskısı ve hava yarışmaz, iki farklı soruyu yanıtlar: insan baskısı "hangi yer yanar" (mekansal), hava "hangi gün yanar" (zamansal). Her iki eksen de ulusal ölçekte modele dahil edildi.

Tam model (insan baskısı, yakıt ve beş hava değişkeni) sonuçları:
Beş katlı çapraz doğrulama AUC: 0.831.
Yıllar arası test (her yıl, o yılı görmemiş modelle): her yıl 0.81 ile 0.87 arası, ortalama 0.83. On yılın her birinde tutarlı; hiçbir yıl çökmüyor.

İki eksenin katkısı (en güçlü kanıt): insan baskısı ile yakıt tek başına 0.77, hava tek başına 0.77, ama ikisi birlikte 0.83. Her iki katman tek başına iyi ama eksik; birleşince belirgin sıçrama yapıyorlar. Bu, iki eksen tezinin doğrudan sayısal ispatıdır.

Katsayılar (standardize, pozitif değer riski artırır): insan baskısı +1.05 (en güçlü), sıcaklık +0.68, 30 günlük yağış -0.27 (çok yağış az risk), rüzgar +0.19, nem -0.17, kuraklık günü +0.00, yakıt -0.07. İşaretler yangın biliminin beklediği yönde; model fiziksel olarak anlamlı bir örüntü öğrendi. İnsan baskısının sıcaklıktan bile güçlü çıkması, ormana erişimin Türkiye'de orman tutuşmasının birincil belirleyicisi olduğunu doğrular.

Dürüstçe bir not: önceki ve daha küçük sette küçük pozitif bir katkısı olan "son yağıştan beri geçen gün" değişkeninin katsayısı, daha geniş ve daha çok gerçek orman yangını içeren bu sette sıfıra indi. En olası neden, aynı kuruluk bilgisinin büyük ölçüde "son 30 günün yağışı" değişkeninde zaten taşınmasıdır (iki değişken arasında eşdoğrusallık). Yani kuraklık sinyali kaybolmadı, ağırlığı tek bir değişkende toplandı. Bu, kuraklığın zemini hazırladığı ama tek başına belirleyici olmadığı tezini zayıflatmaz; aksine, modelin en güçlü ayıracının insan baskısı olmaya devam etmesiyle uyumludur.

Not: Modelleme yapılırken özellikler standardize edilmelidir. Aksi halde farklı ölçekteki değişkenlerin katsayıları yanıltıcı biçimde kıyaslanır (geliştirme sırasında bu hata fark edilip düzeltildi).

### 7.7 Yeni aday özellikler: tarım kenarı ve rekreasyon
Nüfusun yakalayamadığı tutuşma mekanizmalarını arayan iki aday özellik, tamamen elde olan OpenStreetMap verisinden çıkarılıp test edildi.

Tarım kenarı (en yakın tarla, bahçe ya da bağ alanına uzaklık): güçlü ve sağlam bir sinyal çıktı. Tutuşma noktaları tarıma ortanca 2.87 kilometre uzaktayken referans noktaları 7.63 kilometre uzaktaydı. Mevcut modele eklendiğinde beş katlı çapraz doğrulama AUC'si 0.831'den 0.840'a çıktı (artış yaklaşık 0.0085). Bu katkı, özelliğin nüfusla negatif korelasyonuna rağmen geldi (korelasyon eksi 0.55), yani bağımsız bir mekanizma taşıyor: anız ve bahçe ateşinin orman kenarına sıçraması. Sağlamlık iki ek testle doğrulandı. Yıllar arası testte artış sürdü (0.834'ten 0.842'ye). Mekansal blok çapraz doğrulamada (bölgeden bölgeye, daha katı test) artış daha da büyüdü (0.746'dan 0.759'a). Mekansal testte katkının büyümesi kritiktir: eğer bu özellik komşuluk sızıntısından beslenseydi bölge dışı testte katkı sıfıra düşerdi; tersine arttığı için tarım kenarı, bölgeden bölgeye genelleşen gerçek bir tahmin gücüdür. Sonuç: tarım kenarı kalıcı olarak modele eklendi (birleşik model, bölüm 7.9).

Rekreasyon noktaları (en yakın piknik, kamp, manzara ya da cazibe noktasına uzaklık ve 2 kilometre içindeki sayısı): ölü çıktı. Tutuşmalar bu noktalara biraz daha yakın olsa da (ortanca 7.40 kilometreye karşı 10.16) modele eklendiğinde nüfusun ötesinde sıfır katkı verdi; manzara noktaları da eklendi ama tablo değişmedi. Bu, daha önce daha dar bir mesire kümesiyle alınan olumsuz sonucu ikinci kez doğruladı. Nedeni, rekreasyon noktalarının orman hücrelerinin çoğundan uzak olması (ızgara hücrelerinin yalnızca yüzde 7'sinde 2 kilometre içinde böyle bir nokta var) ve var olduğu yerde bilgisinin zaten nüfusta taşınmasıdır. Sonuç: rekreasyon yolu kapatıldı, modele dahil edilmeyecek.

### 7.8 Hava değişkenlerinin yangın hava indekslerine çevrilmesi (FWI)
Mevcut modelde kuruluk, ham değişkenlerle (en yüksek sıcaklık, nem, rüzgar, son yağıştan beri gün, son 30 gün yağış) temsil ediliyor; bunlar biriken kuruluğun kaba vekilleridir. Daha ilkeli yol, dünya standardı olan Kanada Orman Yangını Hava İndeksi (FWI) sistemine geçmektir. Sistem aynı ham girdilerden altı bileşen üretir: ince ölü yakıt nemi (FFMC), orta katman nemi (DMC), derin kuraklık (DC), başlangıç yayılım indeksi (ISI), birikim indeksi (BUI) ve bileşik FWI. Tek günün fotoğrafı yerine yakıt nemini gün gün biriktirip hatırlaması, kaba vekillere temel üstünlüğüdür. Tutuşma için en belirleyici bileşenler hızlı kuruyan FFMC ve onu rüzgarla birleştiren ISI'dir. Akdeniz coğrafyasında yaygın olan Keetch Byram Kuraklık İndeksi (KBDI) de hesaplandı.

FWI motoru kanonik referansa (Van Wagner ve Pickett 1985) karşı birebir doğrulandı (test örneğinde FFMC 87.69, DMC 8.55, DC 19.01, ISI 10.85, BUI 8.49, FWI 10.10). Sistemin özyinelemeli olması, yani her günün değerinin önceki güne bağlı olması, bir zaman serisi gerektirir; bu yüzden her eğitim noktasının olay tarihine kadarki günlük hava dizisi arşivden çekilip FWI hesaplanmaktadır ve sızıntıyı önlemek için yalnızca olay tarihinden önceki hava kullanılmaktadır. FWI hesabı tamamlandı ve sonuçlar dürüstçe ölçüldü. Önemli bir bulgu: FWI bileşenleri kaba hava değişkenlerinin yerine konduğunda baseline'ı geçmedi (yaklaşık 0.828'e karşı 0.831). Yani kaba vekiller tutuşma gününün anlık koşullarını zaten iyi yakalıyor; FWI'nin değeri tek günün fotoğrafında değil, biriken kuraklık hafızasında. Nitekim FWI kaba havanın üstüne eklendiğinde her doğrulama şemasında katkı verdi. Üç şemanın AUC'leri (beş katlı, yıllar arası, mekansal blok) şöyle: yalnızca baseline 0.831, 0.834, 0.746; tarım kenarı eklenince 0.837, 0.840, 0.756; FWI eklenince 0.835, 0.837, 0.757; ikisi birlikte eklenince 0.840, 0.842, 0.763. FWI'nin katkısı en çok mekansal testte belirginleşti (bölgeden bölgeye genelleme), ki ulusal bir araç için en kritik sınav budur. Uyarı: buradaki mekansal blok sayıları (baseline 0.746, tam model 0.763) standart bir mekansal blok CV değil, hava özilinti menzili boyunda büyük ayrımlı bir holdout'tan gelir; test noktasının yaklaşık 150 ile 200 kilometre çevresindeki tüm eğitim verisi atılır. Daha küçük bloklu standart mekansal blok CV tam model için 0.83 ile 0.84 verir; yani 0.763 beklenen değer değil, en kötü durum alt sınırıdır. Bu, sonradan yapılan bir uzlaştırma testiyle doğrulandı (ayrıntı bölüm 12, İtiraz 2). Sonuç: FWI'nin dört kodu (FFMC, DMC, DC, ISI) ile tarım kenarı birlikte modele eklendi (bölüm 7.9). KBDI hesaplandı ama dört kodun yanında ek katkısı olmadığından modele alınmadı.

### 7.9 Birleşik model (mevcut sürüm)
Yukarıdaki testlerin sonucunda modelin mevcut sürümü on iki özellikle donduruldu: insan baskısı (nüfus), yakıt, beş kaba hava değişkeni (en yüksek sıcaklık, nem, rüzgar, son yağıştan beri gün, son 30 gün yağış), FWI'nin dört kodu (FFMC, DMC, DC, ISI) ve en yakın tarım alanına uzaklık. Beş katlı çapraz doğrulama AUC'si 0.840'tır (önceki sürüm 0.831). Model yine yorumlanabilir lojistik regresyondur ve donduruldu; saf aritmetik skorun eğitim kütüphanesiyle birebir aynı olduğu doğrulandı.

Standardize katsayıların büyüklük sırası modelin neye dayandığını şeffaf gösterir: en güçlü ayraç insan baskısıdır (yaklaşık 0.90), onu FFMC ince yakıt kuruluğu (0.48), en yüksek sıcaklık (0.45) ve tarım kenarı (negatif işaretli, yaklaşık 0.39 büyüklüğünde; yani tarıma yakınlık riski artırır) izler, ardından DC ve DMC kuraklık hafızası gelir. Dürüst bir not: FWI kodları modele girince bazı kaba hava değişkenlerinin (son yağıştan beri gün, son 30 gün yağış) tek tek katsayıları işaret değiştirir. Bu, kuraklık bilgisinin artık büyük ölçüde FWI kodlarında taşınmasından doğan eşdoğrusallık etkisidir; modelin bütün olarak tahmin gücünü bozmaz, ama bu iki değişkenin katsayısı artık tek başına yorumlanmamalıdır. Modelin omurgası değişmedi: en güçlü ayraç hâlâ insan baskısıdır, kuruluk ve tarım kenarı zemini hazırlar.

### 7.9b Tarım kenarının ikinci ölçümü (model_v4, on üç özellik)

Tarım kenarı özelliği OpenStreetMap landuse poligonlarından (farmland, orchard, vineyard) hesaplanıyordu. Bu kaynağın Türkiye tarım kapsaması denetlendiğinde eksik olduğu görüldü: hiç orman teması olmayan, yani düpedüz tarlada yanan yangınların en yakın OSM tarım poligonuna ortanca uzaklığı 3.17 kilometre çıkıyor. Tarlada yanan bir yangının tarlaya üç kilometre uzak olması olanaksız olduğuna göre katman, tarım alanının önemli bir kısmını kaçırmaktadır. Buna karşılık ESA WorldCover sınıf 40 (Ekili alan) tam kapsamlıdır ve zaten projenin arazi örtüsü kaynağıdır.

İki ölçüm karşılaştırıldı. WorldCover tabanlı uzaklık, ayırıcılık bakımından belirgin biçimde daha keskindir (pozitiflerde ortanca 0.24 kilometre, referanslarda 1.10; oran 4.5 kat, OSM'de 2.7 kat). Ama OSM'in yerine konduğunda model kazanmaz: 5x10 tekrarlı eşleştirilmiş çapraz doğrulamada fark artı 0.0006, yüzde 95 aralık eksi 0.0060 ile artı 0.0061, p eşittir 0.24. Yani mutlak mesafeler beş kat farklı olsa da sıralama bilgisi aynıdır.

Kazanç ikisinin birlikte kullanılmasındadır. İki ölçümün log korelasyonu yalnızca 0.456'dır, çünkü farklı şeyler ölçerler: OSM haritalanmış ve çoğu yerleşime yakın kalıcı tarımı (bahçe, bağ, tescilli tarla), WorldCover ise fiilî ekili örtüyü yakalar. Birlikte kullanıldığında beş katlı AUC 0.8424'ten 0.8480'e çıkar; eşleştirilmiş fark artı 0.0056, yüzde 95 aralık artı 0.0012 ile artı 0.0089. Ölçek için: tarım kenarının kendisi modele artı 0.0077 katmıştı, yani bu ikinci ölçüm onun yaklaşık yüzde 70'i kadarını daha ekler ve güven aralığı sıfırı içermez.

Model bu on üçüncü özellikle yeniden donduruldu (model_v4.json). İki tarım kenarı katsayısı neredeyse eşittir (eksi 0.378 ve eksi 0.379), yani ikisi de bağımsız ağırlık taşır. Üretim betiği `uretim/farmdist_wc_cek.py`, dondurma betiği `uretim/model_v4_dondur.py`.

Uygulama notu. Uzaklık, WorldCover karolarından okunan pencerelerle hesaplanır. İlk sürüm her noktayı yalnızca kendi üç derecelik karosundan okuyordu; karo kenarına yakın bir nokta için en yakın ekili alan komşu karoda olduğunda bu, sessizce olduğundan büyük bir mesafe üretiyordu. Izgaranın yüzde 2.9'u ve eğitim noktalarının yüzde 1.6'sı bu durumdaydı. Betik, arama penceresine giren bütün karolardan okuyup en küçük mesafeyi alacak biçimde düzeltildi; düzeltme eğitim tarafında 36 noktanın değerini değiştirdi (modele etkisi ihmal edilebilir) ama ulusal ızgarada iki hücrenin değerini boş olmaktan kurtardı, ki bu hücreler aksi halde panelden sessizce düşecekti.

### 7.10 FWI motorunun bağımsız doğrulaması (CEMS)
Motorun Van Wagner denklemlerine karşı birebir doğrulanması hesabın doğruluğunu göstermişti (bölüm 7.8); bu adım ise uçtan uca zincirin, yani Open-Meteo girdisi, ısınma penceresi ve günlük hesabın bütününün, dünya referansıyla aynı tehlike sıralamasını üretip üretmediğini sınadı. Bağımsız referans, Copernicus Acil Durum Yönetim Servisi'nin (CEMS) ERA5 reanalizi ile hesapladığı küresel FWI arşividir; Avrupa'nın resmi yangın bilgi sistemi EFFIS'in altında yatan veridir (yaklaşık 25 kilometre çözünürlük, günlük, 1940'tan bugüne). İki hat tamamen bağımsızdır: farklı hava kaynağı, farklı hesap altyapısı, farklı kurum.

Karşılaştırma 2025 yaz sezonunda yapıldı (Haziran ile Eylül, 122 gün, eksiksiz). Mekansal bağımsızlık için ulusal ızgaranın 5.254 hücresinden, Türkiye'yi kaplayan her karasal CEMS pikseline en yakın tek hücre seçildi (793 nokta); aynı 25 kilometrelik piksele düşen komşu hücrelerin korelasyonu yapay şişirmesi böyle önlendi. Bizim taraf operasyonel motorun kendisiyle, ancak derin kuraklık kodunun oturması için 1 Mart başlangıçlı uzun ısınmayla (92 gün) koşuldu ve 96.746 gün kaydı eşleştirildi.

Sonuç: beş bileşenin tümünde güçlü sıra uyumu. Havuzlanmış Spearman korelasyonları FFMC 0.82, DMC 0.82, DC 0.92, ISI 0.81, bileşik FWI 0.82. Asıl test olan nokta içi sıralamada, yani her noktanın kendi 122 günü içinde hangi günün daha tehlikeli olduğunda, ortanca Spearman FFMC için 0.87, FWI için 0.82 ve DC için 0.99'dur. Motorun biriken kuraklık hafızası, FWI'ye geçmenin asıl gerekçesi olan bileşen, dünya referansının gün gün seyrini neredeyse birebir izlemektedir. Operasyonel açıdan anlamlı bir ek sayı: CEMS'in en riskli yüzde 10'luk gün ve nokta kümesinin yüzde 52'si bizim de en riskli yüzde 10'umuza düşer (şans düzeyi yüzde 10 olurdu).

Mutlak değerlerde sistematik ve tutarlı bir fark vardır: bizim değerler CEMS'ten bir miktar düşüktür (ortalama olarak FFMC 4, bileşik FWI 5, DC 63 puan). İki bilinen kaynağı var. Birincisi girdi geleneği: kanonik sistem ve CEMS öğle saati değerleriyle beslenirken bizim zincir günlük özet değerler kullanır (en yüksek sıcaklık ve rüzgar, ortalama nem); ortalama nemin öğle neminden yüksek olması nem kodlarını aşağı çeker. İkincisi ısınma: CEMS 1940'tan beri kesintisiz koşarken bizim koşu mevsim içinde başlar. DC'deki farkın yaz boyunca sabit kalması (aylık ortalama eksi 62 ile 67 bandında) bunun büyüyen bir hata değil, taşınan bir başlangıç kayması olduğunu gösterir. Bu kayma sıralamayı etkilemez. Nitekim EFFIS tehlike sınıflarında birebir uyum yüzde 44 iken bir sınıf toleransla yüzde 87'dir ve uyuşmazlıkların yaklaşık beşte dördü bizim bir sınıf altta kalmamız yönündedir; fark gürültü değil, tek yönlü ve öngörülebilir bir muhafazakarlıktır. Sabit bir kaydırma düzeltmesi bir sınıf toleranslı uyumu yüzde 92'ye çıkarır.

Sonradan eklenen not: yukarıdaki sayılar, ısınmasını sezon içinde başlatan sürümle üretilmiştir. Zincir bu doğrulamadan sonra durum taşıyan mimariye geçirildi ve DC artık sezon içinde yeniden başlatılmıyor; ikinci kaynağın, yani taşınan başlangıç kaymasının zamanla kapanması beklenmektedir (bölüm 9 ve 10). Birinci kaynak, girdi geleneği farkı, mimariden bağımsızdır ve yerinde durmaktadır.

Dürüst sınırlar: tehlikenin zaten yüksek olduğu alt kümede (CEMS FFMC 87 ve üzeri, kayıtların yaklaşık dörtte üçü) sıra korelasyonu 0.74'e iner; aralık daraldıkça ince sıralama güçleşir. Haftanın tepe günü, iki bağımsız hava kaynağından beslenildiği için yüzde 46 birebir, yüzde 73 bir gün toleransla örtüşür; uzak günlerin eğilim olarak sunulması ilkesi (bölüm 9) burada da geçerlidir. Bu doğrulamanın modele etkisi yoktur ve olmaması da tasarım gereğidir: model FWI kodlarını eğitimde ve operasyonda aynı motordan alır ve standardize ederek kullanır, yani iç tutarlılık korunur. Doğrulamanın gösterdiği şey, panelde gösterilen kodların göreli tehlike sıralaması olarak dünya referansıyla uyumlu olduğudur. Panel bir gün EFFIS ile yan yana mutlak tehlike sınıfı gösterecekse küçük bir kalibrasyon katmanı eklenmelidir.

---

## 8. Yapay Zeka ve Makine Öğrenmesinin Rolü

Bu bölüm, projede yapay zekanın ve makine öğrenmesinin tam olarak nerede ve nasıl kullanıldığını teknik detaylarıyla açıklar. Önce dürüst bir çerçeve: çalışmanın her parçası "yapay zeka" değildir. Bazı adımlar klasik coğrafi veri işleme, bazıları kural tabanlı algoritma, asıl makine öğrenmesi ise tek bir yerde, denetimli sınıflandırıcıdadır. Bu ayrımı net tutmak, hem teknik doğruluk hem de bir muhatap karşısında abartıya düşmemek açısından önemlidir.

### 8.1 Hangi kısım ne
Veri toplama ve coğrafi örnekleme (uydu tespitleri, arazi örtüsü, nüfus verisinin noktalarda okunması) klasik veri mühendisliğidir, makine öğrenmesi değildir. Tutuşma olaylarının kümelenmesi, denetimsiz ve kural tabanlı bir algoritmadır. Asıl makine öğrenmesi, tutuşma noktalarını referans noktalarından ayıran denetimli sınıflandırıcıdır. Bilerek böyle kurduk: gösterişli bir model değil, veriye ve probleme uygun en sade ve şeffaf yöntem.

### 8.2 Tutuşma olayı kümeleme (denetimsiz, algoritmik)
Uydu tespitlerini gerçek yangın olaylarına indirgemek için birleştirme-bulma (union-find, bağlı bileşenler) algoritması kullanıldı. İki tespit birbirine 2 kilometreden yakın ve 4 günden az aralıkla ise aynı bileşene bağlanır; her bağlı bileşen bir yangın olayıdır. 225 binin üzerinde noktayı makul sürede işlemek için 3 boyutlu (enlem, boylam, zaman) ızgara hash kullanıldı; her nokta yalnızca komşu kovalardaki noktalarla karşılaştırıldı, böylece tüm ikili karşılaştırmaların maliyetinden kaçınıldı. Bu adımda etiket yoktur; yöntem tamamen yakınlık kuralına dayanır. Bir tür kümelemedir, ama derin öğrenme ya da denetimli öğrenme değildir.

### 8.3 Özellik mühendisliği (işin asıl zanaatı)
Modelin gücü büyük ölçüde özelliklerin doğru kurulmasından gelir. Türetilen başlıca özellikler:
Biriken kuraklık, kayan pencere ile hesaplandı: günlük yağış serisinde durum taşınarak "son yağıştan beri geçen gün" sayacı ve "son 30 günün yağış toplamı" üretildi.
İnsan baskısı, pencere toplama ile hesaplandı: her noktanın çevresindeki yaklaşık 4 kilometrelik alandaki nüfus toplandı; tek piksel yerine komşuluk kullanmak, ormana erişimi çok daha iyi temsil etti.
Yakıt, arazi örtüsü sınıfından ağırlıklandırıldı; orman dışı sınıflar hedeften elendi.
Nüfus dağılımı çok çarpık (uzun kuyruklu) olduğundan logaritmik dönüşüm uygulandı; birkaç çok kalabalık noktanın modeli ezmesi böyle engellendi.
Özellikler standardize edildi: her özellikten ortalaması çıkarılıp standart sapmasına bölündü. Bu hem modelin daha iyi öğrenmesini sağlar hem de katsayıların birbiriyle kıyaslanabilir olmasını mümkün kılar. Geliştirme sırasında bu adımın atlanması, katsayıların yanıltıcı yorumlanmasına yol açmıştı; standardizasyonla düzeltildi.

### 8.4 Sınıflandırıcı: lojistik regresyon
Asıl makine öğrenmesi modeli budur. Nasıl çalışır: her özellik bir ağırlıkla (katsayı) çarpılır, hepsi bir sabitle (kesişim) toplanır, ve bu doğrusal birleşim bir sigmoid fonksiyondan geçirilerek 0 ile 1 arasında bir olasılığa çevrilir. Bu olasılık, o noktadaki tutuşma riski skorudur.

Tasarım, varlık ile arka plan (presence ile background) yaklaşımıdır; ekolojide tür dağılımı modellemesinde kullanılan mantığın aynısı. Tutuşma noktaları varlık (pozitif), ormanda rastgele seçilmiş yangınsız noktalar arka plandır. Tutuşma ve arka plan sayıları dengesiz olduğunda, model sınıf ağırlıklandırmasıyla (class weight balanced) bu dengesizliği telafi edecek biçimde eğitildi.

Neden lojistik regresyon seçildi, daha karmaşık bir model değil: yorumlanabilirlik (her katsayının işareti ve büyüklüğü doğrudan okunabilir, mesela insan baskısının pozitif ve baskın olması tezi doğruluyor), şeffaflık (yatırımcıya ve OGM'ye kara kutu olmadığını, neyi neden söylediğini açıklayabildiğimizi gösterebilmek), ve aşırı uyum riskinin düşüklüğü. Bu veri ölçeğinde sade model hem yeterli hem güvenilirdir.

### 8.5 Değerlendirme
Modelin başarısı ROC-AUC ile ölçüldü. AUC, rastgele seçilmiş bir tutuşma noktasına, rastgele seçilmiş bir yangınsız noktadan daha yüksek risk verme olasılığıdır; 0.5 saf şans, 1.0 kusursuz ayrımdır.

İki tür doğrulama yapıldı. Beş katlı çapraz doğrulama, modelin genel ayrım gücünü ölçer. Asıl katı test ise yıllar arası doğrulamadır (leave-one-year-out, gruplu çapraz doğrulama): model her seferinde bir yıl hariç tutularak eğitilir ve o görmediği yılda test edilir. Bu, modelin tek bir yılı ezberleyip ezberlemediğini ortaya çıkarır ve zamansal genellenebilirliği dürüstçe ölçer. Geliştirme sürecinin en önemli dersi buradan geldi: tek bölgeli erken model bu testte çöküyordu (tek bir felaket yılına bağımlıydı), ulusal model ise her yıl tutarlı kaldı.

### 8.6 Tarayıcıda çalışan model
Eğitilen modelin parametreleri (özelliklerin ortalama ve standart sapmaları, katsayılar, kesişim) dışa aktarıldı. Panel, bu parametrelerle aynı hesabı tarayıcıda yeniden yapar: özellikleri standardize eder, ağırlıklı doğrusal birleşimi kurar, sigmoidden geçirir. Yani model, sunucuya ihtiyaç duymadan istemcide canlı skor üretebilir. Bu hem hızlı bir demo hem de hafif bir dağıtım sağlar.

### 8.7 Neden derin öğrenme kullanmadık
Dürüst cevap: bu problemde derin öğrenme avantaj sağlamazdı. Veri yapısı tablo biçiminde ve özellik sayısı azdır; bu koşullarda lojistik regresyon ve ağaç tabanlı yöntemler derin ağlarla yarışır, çoğu zaman geçer. Derin öğrenme daha çok veri, daha çok hesap ve yorumlanabilirlikten ödün ister. Bu projede en büyük kazanç model karmaşıklığından değil, veri kalitesinden geldi: anız yangınlarının ayıklanması, hedefin tutuşma olayı olarak doğru tanımlanması, ve dürüst doğrulama. Yani burada yapay zekanın katkısı, gösterişli bir algoritmadan çok, problemi doğru kurmak ve doğru ölçmektir.

### 8.8 İleri makine öğrenmesi yönleri
Zamansal eksen (hava) eklendikten sonra, doğrusal olmayan etkileşimleri yakalamak için ağaç tabanlı yöntemler (gradient boosting, örneğin XGBoost ya da LightGBM) denenebilir. Mekansal blok çapraz doğrulama, komşu noktaların ilişkisinden doğan iyimser yanlılığı önler. Olasılık kalibrasyonu, model skorlarının gerçek olasılıklara karşılık gelmesini sağlar (mesela skoru 0.7 olan yerlerin gerçekten yaklaşık yüzde 70 oranında yanması). Daha zengin özellikler (yola uzaklık, eğim ve bakı, rüzgar yönü, bitki örtüsü zaman serisi) eklenebilir. Tüm bu adımlarda rehber ilke aynı kalır: model karmaşıklığını ancak veri ve doğrulama destekliyorsa artırmak. Bu yönlerden bazıları bu süreçte uygulandı: mekansal blok çapraz doğrulama, tarım kenarı özelliğinin sağlamlığını sınamak için kullanıldı (bölüm 7.7); zengin özellikler tarafında tarım kenarı eklendi ve yangın hava indeksleri yönünde çalışma başladı (bölüm 7.8).

---

## 9. Operasyonel Mimari

Risk skoru her sabah yeniden hesaplanır. Operasyonel katman uçtan uca kuruldu, otomatikleştirildi ve canlıya alındı; aşağıdaki anlatım çalışan bir sistemi tarif eder, bir planı değil.

Dondurulmuş model: Eğitilen modelin parametreleri (özellik sırası, dönüşümler, ortalama ve standart sapmalar, katsayılar, kesişim) tek bir dosyaya donduruldu. Skorlama saf aritmetiktir; herhangi bir nokta listesi, eğitim kütüphanesine ihtiyaç olmadan bu parametrelerle skorlanabilir. Saf aritmetik skorun eğitim kütüphanesiyle birebir aynı sonucu verdiği doğrulandı. Operasyona alınan güncel model, bölüm 7.9'da tanımlanan on iki özellikli birleşik modeldir (AUC 0.840).

Ulusal orman ızgarası: Birkaç örnek bölge yerine tüm Türkiye orman örtüsü yaklaşık 5.5 kilometrelik (0.05 derece) bir ızgaraya bölündü. Orman maskesi ESA WorldCover 10 metre arazi örtüsünden kurulur (ağaç örtüsü sınıf 10 ve maki/çalılık sınıf 20; çayır ve mera bilinçli olarak dışarıda), yani eğitimdeki orman tanımıyla aynı kaynağı kullanır ve eğitim ile operasyon arasındaki eski tanım farkı böylece kapanır. WorldCover, bulut için iyileştirilmiş GeoTIFF olarak dev dosya indirilmeden yalnızca gereken piksellerle okunur. Izgara başlangıçta OpenStreetMap orman poligonlarından kurulmuştu (5.254 hücre); WorldCover'a geçişte kafes birebir korunarak yeni maske eskisiyle birleştirildi. Böylece eski 5.254 hücrenin adları, nüfusu ve kuraklık birikimi değişmeden kaldı, üzerine WorldCover'ın orman görüp ızgarada olmayan 4.218 yeni hücre eklendi (toplam 9.472). Her hücreye, eğitimle aynı 2 kilometre yarıçaplı (kalibre edilmiş) WorldPop nüfusu ve en yakın tarım alanına uzaklık (tarım kenarı) atandı; yakıt yeni hücrelerde arazi örtüsü sınıfından türetilir (ağaç 1,0, maki 0,85), korunan eski hücrelerde 1,0'da bırakıldı. Yeni hücrelerin nüfus dağılımı eğitim orman arka planıyla kıyaslanarak ölçek tutarlılığı doğrulandı (aynı büyüklük mertebesi).

İl ve ilçe etiketleme: Her ızgara hücresine il, il sınır poligonlarıyla nokta içinde testiyle kesin atandı; ilçe ise resmi mülki idare sınırlarından atandı: resmi sınır çizgileri poligonlaştırılıp her poligon içine düşen resmi idari merkez noktasıyla isimlendirildi, sonra hücreler nokta içinde testiyle eşlendi (5.254 hücrenin tamamı; yüzde 99'u resmi poligondan, kalanı en yakın merkezden).

Günlük zincir: İki betik. Birincisi ızgaranın her noktası için Open-Meteo'dan canlı 7 günlük tahmini çeker (hız limitine takılmamak için küçük öbekler, bekleme ve kaldığı yerden devam edebilme ile), biriken kuraklığı bir gün ilerletir ve her tahmin gününe FWI kodları (FFMC, DMC, DC, ISI) eklenir. İkincisi dondurulmuş modeli, ızgaranın statik özelliklerini ve o sabahki tahmini birleştirip her hücre için 7 günlük riski hesaplar ve haftanın en riskli gününe göre sıralar. Çıktı, panelin Bu Hafta sekmesinde ulusal bir risk haritası (her hücre renk kodlu nokta, sokak ve uydu zemin seçeneğiyle, tutuşma haritasıyla aynı dilde popup) ve en riskli ilk 30 hücrenin il ile ilçe etiketli listesi olarak gösterilir. Her hücrenin popup'ında bu haftaki risk, en riskli gün ve haftalık ortalamanın yanı sıra tepe günün FWI kodları (FFMC, DMC, DC, ISI) ve o günün ham hava değişkenleri (en yüksek sıcaklık, nem, rüzgar, son yağıştan beri geçen gün, son 30 günün yağışı) yer alır; hava tahmini olduğu, uzak günlerde kesinlik değil eğilim taşıdığı popup'ta ayrıca belirtilir.

Durum taşıyan kuraklık zinciri: İlk sürümde DC'nin oturması için her koşuda 60 günlük geçmiş yeniden çekiliyordu. FWI özyinelemeli olduğu için bu, her sabah aynı hesabı baştan yapmak demekti ve nokta başına istek penceresini 67 güne çıkarıyordu. Mevcut sürüm bunun yerine durum taşır: her hücrenin FFMC, DMC ve DC değerleri, yağışsız gün sayacı ve son 30 günün yağışı bir durum dosyasında saklanır, ertesi sabahki koşu oradan devam eder. Günlük istek penceresi 7 geçmiş artı 7 tahmin gününe iner ve günlük ağırlıklı çağrı maliyeti yaklaşık 25.100'den 5.254'e düşer. Geçmiş yedi günün yine de istenmesinin nedeni maliyet değil dayanıklılıktır: sağlayıcının ağırlık formülünde gün sayısının asgarisi 14 olduğundan bu yedi gün ek yük getirmez, karşılığında koşu birkaç gün aksarsa eksik günler ertesi koşuda kendiliğinden tamamlanır. Boşluk yedi günü aşarsa, durum dosyası bozulursa ya da ızgaraya yeni nokta eklenirse betik kendiliğinden soğuk başlangıca düşer ve 60 günlük ısınmayla durumu sıfırdan kurar.

Bu değişikliğin asıl önemi maliyette değil süreklilikte: kuraklık kodları artık sezon içinde yeniden başlatılmıyor, kesintisiz birikiyor. Doğrudan metodolojik sonucu bölüm 10'da anlatılmıştır.

Otomasyon ve yayın: Zincir her sabah 07:00 Türkiye saatinde bulut tabanlı bir iş akışı üzerinde kendiliğinden dönmektedir. Koşu skorları üretir, çıktı dosyalarını depoya bir bot kullanıcısıyla işler; panel aynı depodan yayımlanır ve bu dosyayı okur. Ayrı bir sunucu ya da veritabanı yoktur, sabit gider yalnızca hava sağlayıcısının ticari aboneliğidir. Zamanlayıcı dakika hassasiyeti garanti etmez, başlama saati bir çeyrek saat sarkabilir; günlük çalışan bir sistemde bu önemsizdir.

Hata dayanıklılığı üç kademelidir. Zaman aşımı, bağlantı hatası, hız sınırı ve sunucu hataları kademeli beklemeyle tekrar denenir. Bir öbek yine de alınamazsa o noktalar atlanır ve durumları dokunulmadan kalır; ertesi günün geçmiş penceresi boşluğu kendiliğinden kapatır. Kayıp yüzde 10'u aşarsa betik hata koduyla durur, durum dosyası yazılmaz ve skorlama adımına hiç geçilmez. Böyle bir günde panel son başarılı günün dosyasını göstermeye devam eder, ancak haritadaki güncelleme damgası 36 saati aştığında renk değiştirip son başarılı koşuya işaret eder. İlke şudur: sistem aksadığında sessizce eski veri göstermez, gösterdiği verinin ne kadar taze olduğunu kullanıcıya söyler.

Kendiliğinden biriken arşiv: Bot her gün skor dosyasını depoya işlediği için her günün ulusal risk haritası sürüm geçmişinde saklanır. Bu, tahminlerin sonradan gerçekleşen uydu tespitleriyle karşılaştırılacağı hindcast analizi için bedava ve kendiliğinden büyüyen bir veri tabanıdır; belediye pilotunda isabet doğrulaması ayrıca veri toplamayı gerektirmeyecektir.

Dürüst not: hava tahmini ile gözlem aynı güvenilirlikte değildir. İlk 2 ile 3 gün isabetli, 5 ile 7 güne uzadıkça belirsizlik artar; uzak günler kesin değil eğilim olarak sunulmalıdır.

---

## 10. Sınırlar (dürüstçe)

Model artık iki eksenlidir (mekansal artı zamansal/hava). Kalan bir teknik nokta, arka plan noktalarının yaklaşık yüzde 6'sının hava çekme aşamasında tamamlanamamasıdır; bu, dengeyi bozmayacak kadar küçüktür ve sonradan tamamlanabilir.
Model tutuşma noktasını tahmin eder (önleme), başlamış yangının yayılımını değil; yayılım ayrı bir problemdir ve OGM'nin sahasıdır.
İnsan baskısı vekili nüfustur (WorldPop çevre nüfus toplamı). Ormana erişimin daha keskin bir vekil olup olmayacağı ayrıca sınandı: her nokta için en yakın yola, en yakın küçük yola ya da orman yoluna (track) ve en yakın yerleşime uzaklık OpenStreetMap'ten hesaplandı. Sonuç tezi yön olarak doğruladı (uzaklık katsayıları negatif, tutuşmalar yola ve yerleşime referans noktalarından belirgin biçimde daha yakın; örneğin yola ortanca 154 metreye karşı 421 metre), ama tahmin gücünü artırmadı: erişim uzaklıkları nüfusla örtüştüğü için tek başına nüfustan zayıf kaldı (mekansal AUC 0.69 ile 0.77 aralığında, nüfusunki 0.77) ve modele eklendiğinde kazanç ihmal edilebilir düzeydeydi (AUC 0.831'den 0.834'e). Nedeni, Türkiye'de yolların her yerde olması (en yakın yol zayıf bir ayraç) ve orman yolu haritasının OSM'de seyrek ve eksik olmasıdır. Dolayısıyla erişim, modelin girdisi değil, mekanizmanın doğrudan delilidir; insan ekseni olarak nüfus korunur. Erişimin asıl operasyonel değeri bir girdi olmakta değil, eğitilmiş modelin mesire ve orman parkı koordinatlarında çalıştırılıp "bu hafta sonu en riskli mesireler" sıralamasının üretilmesindedir.

Hedef tanımının bir kör noktası ve düzeltilişi: olayların orman olup olmadığına yalnızca ilk tespitin arazi örtüsüne bakarak karar veren erken yöntem, tarlada başlayıp ormana sıçrayan yangınları kaçırıyordu. Somut örnek, 8 Ağustos 2025 Çanakkale Sarıcaeli yangınıdır: olay tarla kenarında başlamış, ilk piksel ekili alan olduğu için erken yöntem bu gerçek orman yangınını orman dışı sayıp eliyordu. Oysa olayın 26 tespitinin 22'si (yaklaşık yüzde 85'i) orman üzerindeydi. Ayak izi yöntemine (tespitlerin çoğunluğunun orman olması) geçilince Sarıcaeli ve benzeri toplam 1.147 olay sete dahil oldu, ayak izi gerçekte tarla olan 452 olay ise düştü. Yine de yeni yöntemin kendi sınırı var: yüzde 50 eşiği bir yargı kararıdır ve eşiği oynatmak, sınırdaki olayların içeride mi dışarıda mı kalacağını değiştirir. Eşik dürüstçe seçilmiş bir denge noktasıdır, mutlak bir doğru değil.

Operasyonel ızgaranın orman maskesi başlangıçta OpenStreetMap orman poligonlarındandı; OSM kapsaması bazı bölgelerde eksik olduğu için görünür orman alanları noktasız kalıyor ve maske, eğitimdeki WorldCover tanımından ayrışıyordu. Bu maske ESA WorldCover'a taşındı (ağaç ve maki sınıfları), böylece eğitim ile operasyon aynı orman tanımını kullanır hale geldi ve kapsama boşlukları kapandı (ızgara 5.254'ten 9.472 hücreye çıktı). Kalan bir bilinçli tutarsızlık var: kuraklık birikimini ve canlı sıralamayı bozmamak için eski 5.254 hücre, WorldCover onları orman saymasa da (yaklaşık yüzde 21) ızgarada tutuldu ve yakıtları 1,0'da bırakıldı. Yani ızgarada küçük bir OSM kalıntısı tasarım gereği duruyor; ileride bu hücreler tek tek gözden geçirilebilir.

İlçe etiketi resmi mülki idare sınırlarından atanmaktadır (sınır çizgileri poligonlaştırılıp resmi merkez noktalarıyla isimlendirilerek). Daha önce kısa süre OpenStreetMap, en başta da en yakın kayıtlı yangının ilçesini ödünç alan yaklaşık yöntem kullanılmıştı; ikisi de terk edildi. İl etiketi de il sınırlarından kesindir.

FWI tarafında derin kuraklık bileşeni DC yavaş kuruduğundan tam oturması için uzun bir ısınma ister. İlk operasyonel sürümde her koşu 60 günlük bir pencereyle yeniden başladığından bu ısınma FFMC ve DMC'ye yetiyor, DC'ye kısmi kalıyordu. CEMS doğrulaması bu yaklaşıklığı sayıya döktü: mevsim içi başlangıcın DC'de yarattığı kayma yaz boyunca sabit kalıyor (yaklaşık 60 ile 65 puan) ve gün sıralamasını etkilemiyordu (nokta içi ortanca Spearman 0.99, bölüm 7.10).

Durum taşıyan mimariye geçişle (bölüm 9) bu kısıt yapısal olarak kalktı. DC artık her koşuda yeniden başlatılmıyor, kesintisiz birikiyor; beklenen sonuç, sabit başlangıç kaymasının kendiliğinden erimesi ve iki üç ay içinde ihmal edilebilir düzeye inmesidir. DC'nin zaman sabiti bu mertebededir. Bunun panelde görünür etkisi, mutlak sayıların bu süreçte bir miktar yükselmesidir; hücreler arası sıralama, yani ürünün fiilen sattığı bilgi, etkilenmez. Beklentinin tutup tutmadığı sezon sonunda aynı karşılaştırma tekrarlanarak ölçülecektir (bölüm 11).

Kısıtın kalan kısmı şudur: durum dosyası bozulur, ızgaraya yeni nokta eklenir ya da koşu bir haftadan uzun aksarsa betik soğuk başlangıca düşer ve ilgili hücrelerde DC birikimi sıfırlanır; aynı aşağı kayma o hücreler için yeniden başlar. Doğrulama yapan bir muhatabın bilmesi gereken nokta budur. Ayrıca CEMS farkının ikinci kaynağı olan girdi geleneği (öğle değerleri yerine günlük özet değerler, bölüm 7.10) mimariden bağımsızdır ve yerinde durmaktadır.

---

## 11. Mevcut Durum ve Sıradaki Adımlar

Tamamlananlar: tez ulusal ölçekte doğrulandı; hedef tanımı ayak izi yöntemiyle iyileştirildi (3.397 orman olayı); nüfus tanımı kalibrasyonla kesinleştirildi (2 kilometre yarıçap); model aday özelliklerle güçlendirilip yeniden dondurularak on iki özelliğe çıkarıldı (insan, yakıt, beş kaba hava, FWI'nin dört kodu, tarım kenarı; beş katlı AUC 0.831'den 0.840'a, üç doğrulama şemasında da tutarlı), rekreasyon elendi; il ve ilçe etiketleri resmi mülki idare sınırlarından kesinleştirildi; ulusal panel kuruldu (Tutuşma haritası, Bu Hafta ulusal risk haritası, en riskli ilçe listesi, sokak ve uydu zemin); operasyonel katman uçtan uca kuruldu ve birleşik modele uyarlandı (o aşamada 60 günlük geçmişten FWI üreten haftalık hava çekimi, dondurulmuş model, 5.254 hücrelik ulusal orman ızgarası). Panel birleşik modelin operasyonel çıktısıyla tazelendi: Bu Hafta sekmesi örnek veriden gerçek haftalık skorlara geçirildi (5.254 hücre) ve tepe günün FWI kodları popup'a eklendi. Tutuşma haritasının tekil olaylar katmanına yanan alan ayak izi poligonları eklendi (VIIRS S-NPP tespitlerinden, 190 metre tampon ile). FWI motoru bağımsız referansa karşı doğrulandı: CEMS'in ERA5 tabanlı arşiviyle 2025 yaz sezonu, 793 mekansal bağımsız nokta ve 96.746 gün kaydı üzerinden; beş bileşende havuzlanmış Spearman 0.81 ile 0.92, DC'de nokta içi ortanca 0.99, EFFIS sınıf uyumu bir sınıf toleransla yüzde 87 (ayrıntı bölüm 7.10). Son olarak operasyonel zincir otomatikleştirilip yayına alındı: kuraklık kodları durum taşıyan mimariye geçirildi (nokta başına günlük istek penceresi 67 günden 14 güne, günlük ağırlıklı çağrı maliyeti yaklaşık 25.100'den 5.254'e indi), zincir her sabah 07:00'de kendiliğinden koşuyor, çıktıyı bot depoya işliyor ve panel bu dosyayı okuyarak yayımlanıyor (ayrıntı bölüm 9). Böylece sistem elle çalıştırılan bir zincir olmaktan çıkıp her gün kendini tazeleyen canlı bir ürüne dönüştü.

Not: bir önceki sürümün birinci sıradaki adımı, tam otomasyon, tamamlandı; zincir artık her sabah kendiliğinden koşup paneli tazeliyor (yukarıda Tamamlananlar, ayrıntı bölüm 9). Ondan önceki sürümün birinci adımı olan "paneli yeni modelin skorlarıyla tazelemek" de tamamlanmıştı.

Sıradaki adımlar:
1. Belediye pilotu: sahada isabet doğrulaması ve ilk gelir. Günlük skor arşivi kendiliğinden biriktiği için isabet ölçümü geriye dönük olarak da yapılabilir.
2. Kuraklık kodlarının yakınsamasının ölçülmesi: DC kesintisiz biriktiğine göre CEMS'e karşı ölçülen sistematik kaymanın iki üç ay içinde kapanması beklenir. Aynı karşılaştırma sezon sonunda tekrarlanıp sonuç bölüm 7.10'a işlenmelidir; beklentinin tutması, mimarinin bağımsız bir sınavı olur.
3. Yangın yayılım modülü: ayrı ürün, OGM iş birliği.

İkincil işler: alan adının yayına bağlanması; panelde mutlak tehlike sınıfı gösterilecekse EFFIS ile hizalayan küçük bir kalibrasyon katmanı (bölüm 7.10); ilk haftalarda koşu süresinin, kayıp oranının ve durum dosyası boyutunun izlenmesi.

Not: erişim katmanı (yola ve yerleşime uzaklık) sınandı ve nüfusu geçemediği için kapatıldı; ayrıntı bölüm 10'dadır.

---

## 12. Bilinen İtirazlar ve Yanıtlar

Bu bölüm, tezin ve yöntemin kamusal bir tartışmada karşılaşacağı en güçlü itirazları önden yazar ve elde olan veriyle sınar. Amaç, bir bilirkişinin (OGM, yatırımcı, akademik hakem) soracağı zor soruyu o sormadan sormak ve dürüstçe yanıtlamaktır. Her itiraz mümkün olduğunca sayıyla test edilir; sonuçlar tezi zayıflatsa da olduğu gibi yazılır.

### İtiraz 1: Model tezi sınamak yerine örnekleme çerçevesiyle en baştan varsayıyor olabilir (maruziyet sorunu)

**İtiraz.** Model, varlık arka plan (presence background) tasarımıyla kurulur: tutuşma noktaları (varlık) ile Türkiye ormanlarından rastgele seçilmiş noktalar (arka plan) ayırt edilir. Ama Türkiye'de rastgele bir orman pikseli ezici çoğunlukla ıssız dağ yamacıdır; tutuşma noktaları ise tanımı gereği insan etkinliğinin olduğu yerdir. Dolayısıyla iki grubu en iyi ayıran değişkenin çevre nüfus çıkması neredeyse tasarımın bir zorunluluğudur, bağımsız bir bulgu değil. Bir eleştirmen şöyle diyebilir: "Bu bir tutuşma modeli değil, ormana yakın nüfus haritası; yüksek AUC de buradan geliyor." Buna bir de hava asimetrisi eklenir: arka plan noktalarına olay havuzundan rastgele bir tarih atanır (bölüm 7.2), yani nüfus kontrastı yapısalken hava kontrastı yapaydır ve bu, nüfusu haksız yere baskın gösterebilir.

**Sınama.** Kaygıyı doğrudan test etmek için maruziyet sabitlendi. Her tutuşma noktası, neredeyse aynı log çevre nüfusa sahip bir arka plan noktasıyla birebir eşleştirildi (log nüfus üzerinde caliper eşleştirme). Eşleştirilmiş sette nüfus artık iki grubu ayıramaz; geriye "eşit nüfuslu orman noktaları arasında model hâlâ tutuşmayı ayırıyor mu" sorusu kalır. Üç kesit alındı: dondurulmuş modelin eşleştirilmiş AUC'si, çevre nüfus çıkarılmış modelin (hava, yakıt, tarım kenarı) çapraz doğrulama AUC'si, ve nüfusun doz yanıtı.

**Bulgular.** Eşleştirmeden önce log nüfusun standardize ortalama farkı 1.01, yani çok büyük (ham çevre nüfus ortancası tutuşmada 551, arka planda 83). Eşleştirme bu farkı 0.02'ye indirdi (2109 çift).

| Ölçüm | Tam set | Nüfus eşleştirilmiş |
|---|---|---|
| Dondurulmuş model (yeniden fit yok) | 0.844 | 0.706 |
| Yalnız çevre nüfus | 0.766 | 0.491 |
| Nüfussuz (hava, yakıt, tarım kenarı) | 0.811 | 0.749 |
| Tam on iki özellik (yeniden fit) | 0.843 | 0.752 |

Nüfusun doz yanıtı basamak değil düzgün gradyandır: çevre nüfus desilleri boyunca varlık oranı 0.15, 0.18, 0.32, 0.44, 0.44, 0.50, 0.61, 0.70, 0.78, 0.86 diye monoton yükselir. "İnsan var ya da yok" ikili eşiği olsaydı ilk desillerde bir basamak beklenirdi; onun yerine üç büyüklük mertebesi boyunca süren bir gradyan görülür. Ek olarak erişilebilir alt kümede (çevre nüfus, tutuşma ortancası olan 551 ve üzeri) yalnız nüfusun AUC'si hâlâ 0.628'dir; etki, kalabalıklaştıkça artmaya devam eder.

**Yanıt.** İtirazın bir yarısı haklıdır ve artık sayısı vardır. Dondurulmuş modelin şans üstü ayrım payının (0.344) yaklaşık yüzde 40'ı, kalabalık orman ile ıssız orman arasındaki maruziyet kontrastından gelir; maruziyet dengelendiğinde beceri 0.706'ya iner. Bu yüzden 0.840 rakamı, temiz ayrım becerisi olarak değil, örneklem çerçevesinin bir kısmını içeren bir değer olarak okunmalıdır; maruziyet kontrollü gerçek beceri 0.71 ile 0.75 bandındadır. Dışarıya sunumda bu ayrım açıkça yapılmalıdır.

İtirazın diğer yarısı, yani "model yalnızca bir nüfus haritasıdır, hava kozmetiktir" iddiası ise yanlışlanır. En sert senaryoda eşleştirilmiş AUC'nin 0.5'e düşmesi beklenirdi; düşmedi, 0.749'da kaldı (yalnız hava 0.736). Eşit nüfuslu orman noktaları arasında bile gerçek tutuşma günü koşulları rastgele orman gününden güçlü biçimde ayrılır; yani nüfustan bağımsız, gerçek bir ikinci eksen vardır. Buna doz yanıtının monotonluğu ve gradyanın erişilebilir alt kümede sürmesi eklenince tezin çekirdeği (insan baskısı birincil eksen, hava ikinci eksen) ayakta kalır. Değişen tek şey, tek bir rakamın nasıl sunulduğudur.

**Nihai test: zamansal case-crossover.** Eşleştirme yalnızca nüfus eksenini sabitler; arka plan noktaları hâlâ rastgele tarih taşıdığından "hava ayırıyor" bulgusu kısmen "gerçek tutuşma günü rastgele yaz gününden sıcaktır" tautolojisinden beslenir ve 0.749 bir tavan değeridir. Bunu temizlemek için zamansal case-crossover kuruldu: her tutuşma olayı, aynı konumun yanmayan günleriyle karşılaştırıldı (aynı yıl, olay gününün ±21 günü içinde, Haziran ile Eylül bandında, ±3 günlük tampon hariç; olay başına ortalama 32 referans gün). Bu tasarım nüfusu, yakıtı, tarım kenarını ve araziyi birebir sabitler (aynı konum) ve kontrol günleri gerçektir; hem "uzak ıssız konum" hem "rastgele tarih" artefaktı ortadan kalkar. Aynı konumda statik özellikler sabit olduğundan tabaka içi sıralamayı etkilemez; yani ölçülen şey doğrudan dağıtılmış modelin hangi günü seçtiği, yani hava alt skorudur. 900 olay üzerinde koşuldu (yıla göre tabakalı örnek; olay günü havasının eğitim değerleriyle birebir aynı olduğu doğrulandı).

Sonuç: tabaka içi case-crossover AUC'si (0.5, havanın gün zamanlamada etkisiz olması demektir) modelin hava alt skoru için 0.587'dir (yüzde 95 güven aralığı 0.569 ile 0.605), yani 0.5'in belirgin üstünde ama mütevazı. Sinyali hızlı tepki veren bileşenler taşır: nem 0.610, ISI 0.606, FFMC 0.603, bileşik FWI 0.600; yavaş kuraklık kodları ise sıfıra yakındır (DC 0.523, DMC 0.531, son 30 gün yağış 0.510). Olay günü, kendi üç haftalık penceresinin en tehlikeli günü olma oranı yüzde 7.7'dir (şans yaklaşık yüzde 3).

Yorum. Bu bulgu üç şeyi netleştirir. Birincisi, "yalnız hava" için raporlanan yaklaşık 0.77'lik gücün büyük kısmı mevsimsel ve bölgesel hava farkından gelir (sıcak kurak bölge ya da ay ile rastgele nokta arasındaki fark), günden güne zamanlamadan değil; sabit bir yerde havanın gün seçme becerisi yalnızca 0.587'dir. Model havayı meşru biçimde kullanır, ama gücü "hangi mevsim ve hangi bölge" ekseninde yoğunlaşır. İkincisi, bu tezi güçlendirir: bir orman haftalar boyunca kuruyup pencere yanmaya hazır hale geldiğinde, o pencere içinde tam hangi günün tutuşacağını hava ancak zayıf ayırır; geri kalanı, tanımı gereği havayla öngörülemeyen insan kıvılcımıdır. "Kuraklık zemini hazırlar, kıvılcımı insan çakar" cümlesinin doğrudan sayısal izi budur. Üçüncüsü, sinyalin hızlı yakıt nemi ve yayılım bileşenlerinde toplanması, bölüm 7.8'deki FFMC ve ISI vurgusunu bağımsız biçimde doğrular.

Ürün açısından dürüst sonuç: aracın gerçek çözünürlüğü "hangi hafta ve hangi yer" düzeyindedir; "hangi tam gün" düzeyinde havanın katkısı sınırlıdır (case-crossover AUC 0.587, en riskli gün yüzde 7.7). Panelin uzak günleri kesinlik değil eğilim olarak sunma ilkesi (bölüm 9) bu bulguyla uyumludur ve korunmalıdır.

Tasarım sınırı: case-crossover mevsimsel ve mekansal sinyali bilinçli olarak siler, yalnız kısa vadeli günlük anomaliyi bırakır; dolayısıyla 0.587 modelin genel becerisi değil, "aynı yer, aynı mevsim, hangi gün" becerisidir. Modelin mekansal ve mevsimsel gücü ayrıdır ve bu testin kapsamı dışındadır.

### İtiraz 2: Manşetteki 0.840 mekansal sızıntıyla şişmiş olabilir

**İtiraz.** Manşetteki 0.840 rastgele beş katlı çapraz doğrulamadan gelir. Mekansal veride rastgele katlama, bir test noktasının birkaç kilometre ötesinde bir eğitim noktası bırakabilir; nüfus ve tarım kenarı gibi statik mekansal özellikler komşu noktalarda neredeyse aynı olduğundan model bu yakınlıktan iyimser bir avantaj devşirir. Bir eleştirmen şöyle diyebilir: "Gerçek mekansal genelleme çok daha düşüktür; 0.840 komşuluk sızıntısıyla şişmiştir."

**Sınama.** Önce boru hattının sadık olduğu doğrulandı: beş katlı 0.843, yıllar arası 0.845, baseline beş katlı 0.831; üçü de dokümanın kayıtlı sayılarıyla örtüşür. Sonra mekansal şemalar süpürüldü: blok boyutu 0.25 ile 5 derece, tampon 0 ile 200 kilometre, bırak-bir-bölge (KMeans) K 2 ile 12; her biri hem kat ortalaması hem havuzlanmış AUC ile.

**Bulgular.**

| Şema (tam model) | AUC |
|---|---|
| Rastgele beş katlı (manşet) | 0.843 |
| Standart mekansal blok (0.25 ile 5 derece, tampon 50 km ve altı) | 0.83 ile 0.84 |
| Orta tampon (100 ile 150 km) | 0.80 ile 0.82 |
| Bırak-bir-bölge (K 2 ile 12) | 0.80 ile 0.83 |
| Agresif ayrım (yaklaşık 200 km tampon) | 0.74 ile 0.77 |

**Yanıt.** Komşuluk sızıntısı küçüktür. Standart mekansal blok CV'de düşüş yalnızca 0.01 ile 0.03 mertebesindedir; manşetteki 0.840 mekansal olarak dürüsttür ve ürün yeni bir bölgeye taşındığında beklenen beceri yaklaşık 0.80 ile 0.84'tür. Nedeni fizikseldir: baskın değişken olan nüfus 0.05 derecede gerçekten yerel olarak değişir (kalabalık bir vadi, hemen yanında ıssız bir sırt), hava ise bölgeseldir ve zaten düzgün genelleşir; bu yüzden komşuluğun katacağı iyimserlik sınırlıdır. Bu bulgu, tarım kenarının katkısının mekansal testte büyümesiyle (bölüm 7.7) de tutarlıdır.

Bu sınama aynı zamanda bölüm 7.8'deki mekansal blok sayısını (tam model 0.763, baseline 0.746) uzlaştırdı. O sayı ancak yaklaşık 150 ile 200 kilometrelik agresif bir mekansal ayrımla, yani test noktasının çevresindeki geniş bir bantta tüm eğitim verisi atıldığında çıkar. Bu, hava özilinti menzili boyunda ilkeli ama muhafazakâr bir holdout'tur; bir hata değil, bir en kötü durum alt sınırıdır. Dolayısıyla iki uç okuma da yanlıştır: "0.840 sahtedir" de, "modelin gerçek mekansal becerisi 0.76'dır" da. Dürüst operasyonel sayı standart mekansal blokla 0.83 ile 0.84, en katı büyük ayrımlı holdout'ta ise 0.76'ya inen bir alt sınırdır.

### İtiraz 3: Orman yangını tanımındaki yüzde 50 eşiği keyfidir

**İtiraz.** Hedef kümesi, tespit ayak izinin yarısından fazlasının ESA WorldCover ağaç ya da maki sınıfında olması şartıyla kuruldu (bölüm 6). Bir eleştirmen haklı olarak sorar: neden yüzde 50? Neden 40 ya da 70 değil? Eşik bir kaç puan oynatıldığında hedef kümesi ve dolayısıyla bütün sonuçlar değişiyorsa, manşetteki rakamlar bir ölçümden çok bir tercihin sonucudur.

Bu itiraz somut bir vakayla tetiklendi. Edirne'nin Enez ilçesine bağlı Büyükevren ve Gülçavuş köyleri sahilinde 11 Ağustos 2025 gecesi çıkan ve rüzgarla büyüyen yangın (64 VIIRS tespiti, yaklaşık 700 hektarlık ayak izi) veri kümesinde orman yangını olarak görünmez. Ayak izinin ağaç ve maki payı, makul dört farklı uygulama altında yüzde 46.9 ile yüzde 50.5 arasında ölçülür; yani ölçüm belirsizliği eşiğin kendisinden büyüktür ve olay eşiğin yanlış tarafına yarım puanla düşmüştür. Alanın yüzde 39.5'i Çayır ve Mera sınıfındadır, bu sınıf orman tanımına bilinçli olarak dahil edilmemiştir.

**Sınama.** Üç ayrı test yapıldı. Birincisi, eşiğin doğal bir ayrım noktasına düşüp düşmediği: 6.000 kümelik rastgele örneklemde ayak izi orman payının dağılımı çıkarıldı. İkincisi, eşik duyarlılığı: hedef kümesi giderek daha saf orman şartıyla budanıp model her seferinde yeniden kuruldu. Üçüncüsü, eşiğin hemen altındaki yangınların sistematik olarak farklı olup olmadığı: yüzde 40 ile 50 bandındaki kümelerin tarıma uzaklığı ve çevre nüfusu, eşiği geçenlerle karşılaştırıldı.

**Bulgular.** Dağılım tek tepelidir ve yüzde 50 civarında ne tepe ne vadi vardır.

| Orman payı | Küme | Pay |
|---|---|---|
| Yüzde 0 ile 5 | 4.614 | yüzde 76.9 |
| Yüzde 5 ile 30 | 943 | yüzde 15.7 |
| Yüzde 30 ile 40 | 128 | yüzde 2.1 |
| Yüzde 40 ile 50 | 65 | yüzde 1.1 |
| Yüzde 50 ile 60 | 72 | yüzde 1.2 |
| Yüzde 60 ile 80 | 88 | yüzde 1.5 |
| Yüzde 80 ile 100 | 90 | yüzde 1.5 |

Eşik duyarlılığı ise belirgindir.

| Orman saflığı şartı | Pozitif | Beş katlı AUC | Tarım kenarı katsayısı | Nüfus katsayısı |
|---|---|---|---|---|
| Yüzde 50 (mevcut) | 3.397 | 0.843 | eksi 0.448 | artı 0.880 |
| Yüzde 55 | 1.549 | 0.811 | eksi 0.315 | artı 0.631 |
| Yüzde 60 | 1.374 | 0.806 | eksi 0.267 | artı 0.630 |
| Yüzde 70 | 1.048 | 0.794 | eksi 0.237 | artı 0.559 |
| Yüzde 80 | 715 | 0.774 | eksi 0.188 | artı 0.484 |
| Eşik yerine sürekli ağırlık | 3.397 | 0.841 | eksi 0.376 | artı 0.741 |

Üçüncü test ise beklenenin tersini verdi: yüzde 40 ile 50 bandındaki yangınlar, eşiği geçenlerden tarıma uzaklık bakımından (ortanca 3.54 ile 3.15 kilometre, Mann-Whitney p eşittir 0.55) ve çevre nüfus bakımından (590 ile 613, p eşittir 0.96) ayırt edilemez.

**Yanıt.** İtiraz kısmen haklıdır ve sınırı artık bilinmektedir. Filtrenin asıl işi tartışmasız doğrudur: kümelerin yüzde 77'si neredeyse sıfır ormanlıdır, yani saf anız yangınıdır ve bunların ayıklanması hiçbir eşik tartışmasına gerek bırakmaz. Eşiğin tam yeri de marjinal olarak önemsizdir; yüzde 40 ile 50 bandındaki yangınlar eşiği geçenlerden ayırt edilemediğine göre eşiği yüzde 40'a çekmek katsayıları kayda değer biçimde değiştirmezdi.

Buna karşılık eşiğin varlığı önemsiz değildir. Saflık şartı yükseldikçe tarım kenarı katsayısı yüzde 58, nüfus katsayısı yüzde 45 küçülür. Bunun okuması şudur: insan erişimi mekanizması ağırlıklı olarak orman ile tarımın kesiştiği arayüzde çalışır, saf orman içinde zayıflar. Bu, tezi çürütmez ama kapsamını daraltır ve dışarıya sunumda bu ayrım yapılmalıdır.

Metodolojik olarak asıl kusur eşiğin değeri değil, cinsidir. Yüzde 50, uzaktan algılamada alansal birimlere tek sınıf atarken kullanılan baskın sınıf kuralıdır; bir orman tanımı değildir. Uluslararası ölçüt (FAO) ormanı yüzde 10 tepe kapalılığıyla tanımlar, 6831 sayılı Orman Kanunu ise ormanı hukuki bir statü olarak tanımlar ve o an ağaç örtüsü olmayan alanları da kapsar. Her iki tanıma göre de Enez yangını bir orman yangınıdır. Dahası mevcut ölçüt, yanmış alan bileşimine yani bir sonuca bakar; sonuç ise söndürme başarısına, rüzgara ve yakıt sürekliliğine bağlıdır ve bunların hiçbiri tutuşma anına ait değildir. Tarlada başlayıp ormanın kenarını yalayan ve hızla söndürülen bir yangın elenirken, aynı yangın ekip geç kalsaydı veri kümesine girecekti; yani mevcut hedef kısmen söndürmeden kaçabilmiş yangınlara doğru yanlıdır. Doğru yön, ölçütü sonuçtan maruziyete taşımaktır: tutuşma noktasının ormana uzaklığı, tutuşmadan önce var olan ve sağlam ölçülebilen bir büyüklüktür. Bu değişiklik sıradaki adımlar arasına alınmıştır.

### İtiraz 4: Hedef kümesi bu dokümandaki tarifle yeniden üretilemiyor

**İtiraz.** Bir hakem, yöntemi okuyup 3.397 olaylık hedef kümesini ham veriden yeniden üretmek isteyebilir. Yeniden üretilemiyorsa, sonraki bütün sayılar doğrulanamaz.

**Sınama.** Boru hattı ham veriden adım adım yeniden kuruldu ve her adım kayıtlı sayılarla karşılaştırıldı. Ardından bölüm 6'daki kural (ayak izinin yüzde 50'den fazlası ağaç ya da maki) dört farklı ayak izi tanımıyla uygulandı ve boru hattının kararıyla karşılaştırıldı.

**Bulgular.** İlk iki adım sadıktır. Yaz tespiti sayısı birebir tutar (225.856). Kümeleme 53.438 olay verir, kayıtlı 53.593 sayısından yüzde 0.29 sapar; bu fark, dokümanda tarif edilen üç boyutlu ızgara hash yaklaşımının komşu kova karşılaştırmasında birkaç bağı kaçırmasıyla tutarlıdır. Kümelerin boyutları yayımlanmış olay indeksiyle yüzde 99.6 oranında birebir aynıdır ve bölüm 6'daki 3.160 ağaç ile 237 maki ayrımı da yeniden üretilir.

Filtre adımı ise yeniden üretilemez.

| Ayak izi tanımı | Cohen kappa | Kesinlik | Duyarlılık |
|---|---|---|---|
| 190 metre tampon, sadeleştirilmiş | 0.656 | yüzde 85.2 | yüzde 55.6 |
| 190 metre tampon, sadeleştirilmemiş | 0.646 | yüzde 85.2 | yüzde 54.3 |
| 375 metre tampon | 0.581 | yüzde 76.6 | yüzde 49.6 |
| 90 metre tampon | 0.721 | yüzde 92.8 | yüzde 60.8 |

Korunan 3.397 olayın yaklaşık yarısı (yüzde 49) dokümandaki eşiği sağlamaz; yüzde 28'i yüzde 30'un bile altındadır. Hata iki yönlüdür: kuralı sağladığı halde elenmiş kümeler de vardır.

**Yanıt.** İtiraz haklıdır. Kümeleme adımı yeniden üretilebilir ve sadıktır; sapma filtre adımındadır ve o adımı üreten betik arşivde bulunmamaktadır, dolayısıyla farkın nereden geldiği kesin olarak saptanamamıştır. Bu, sonuçların yanlış olduğu anlamına gelmez ama hedef kümesinin kaynağının belgesiz olduğu anlamına gelir ve bu haliyle bir tez için kabul edilebilir değildir.

Açık kapatılmıştır: hedefi ham veriden tek komutla, sabit tohumla ve her adımın sayısını bir manifest dosyasına yazarak kuran `hedef_kur.py` yazılmıştır. Betik iki tasarım kararı taşır. Birincisi, eşik dondurulmuş değildir; her kayıt için tam arazi örtüsü sınıf dağılımı diske yazılır, böylece farklı bir eşikle çalışmak yeniden koşu gerektirmez ve İtiraz 3'teki duyarlılık analizi ucuzlar. İkincisi, ölçüm operatörü iki sınıfta aynıdır (aşağıya bakınız).

Bu itiraz, İtiraz 3'teki sayıları da nitelendirir: oradaki duyarlılık analizi kaynağı belgesiz bir hedef kümesi üzerinde yürütülmüştür, dolayısıyla eğilimi gösterir ama kesin değerleri taşımaz. Yeni betikle üretilen hedef kümesi üzerinde tekrarlanacaktır.

### İtiraz 5: Pozitif sınıf ile referans sınıfı farklı kurallarla tanımlanmıştır

**İtiraz.** Pozitif olaylar ayak izinin alan çoğunluğu testiyle orman sayılır (bölüm 6), referans noktaları ise tek nokta testiyle (bölüm 7.2: rastgele noktalardan WorldCover'a göre gerçekten orman ya da maki olanlar tutuldu). Bunlar farklı katılıkta işlemlerdir. Tek nokta testi bir maki mozaiğindeki noktayı rahatça geçirir, alan çoğunluğu testi aynı mozaikteki yangını eler. Model böylece iki sınıfı, sistematik olarak farklı tanımlanmış bir uzayda ayırt etmeye çalışır.

**Sınama.** Eğitim tablosundaki arazi örtüsü etiketleri iki sınıf için ayrı ayrı sayıldı.

**Bulgular.** Pozitiflerde dağılım 3.160 ağaç ve 237 maki, referanslarda 3.303 ağaç ve 115 makidir. Referans tarafındaki maki payı (yüzde 3.4) pozitif taraftakinin (yüzde 7.0) yarısı kadardır; iki sınıf aynı orman tanımından gelmemektedir.

**Yanıt.** İtiraz haklıdır ve düzeltilmiştir. `hedef_kur.py` içinde her referans noktasına, rastgele seçilmiş bir pozitif olayın tespit deseni giydirilir; yani referans noktası da aynı şekil ve aynı alan üzerinden, aynı eşikle ölçülür. Referans noktaları ayrıca ilçe poligonlarıyla Türkiye kara sınırlarına kırpılır ve iki sınıf, eşiği geçen sayıya göre birebir dengelenir. Bu düzeltmenin model sonuçlarına etkisi, yeni hedef kümesi üretildiğinde ölçülüp buraya işlenecektir.

---

## 13. Kaynaklar

NASA FIRMS. Uydu yangın tespitleri, VIIRS S-NPP 375 metre. firms.modaps.eosdis.nasa.gov
OpenStreetMap. Yol ve yerleşim verisi, Overpass API. openstreetmap.org
Open-Meteo. Günlük geçmiş hava arşivi ve canlı tahmin. open-meteo.com
ESA WorldCover. 10 metre arazi örtüsü 2021. esa-worldcover.org
WorldPop. Türkiye nüfus dağılımı 2020. worldpop.org
OpenStreetMap. İdari sınırlar (il, ilçe), orman ve tarım arazi kullanımı, rekreasyon noktaları. openstreetmap.org
Van Wagner, C.E. ve Pickett, T.L. (1985). Kanada Orman Yangını Hava İndeksi Sistemi denklemleri. Yangın hava indeksi hesabının kaynağı.
Resmi mülki idare sınırları (Türkiye). İl ve ilçe sınır çizgileri ile idari merkez noktaları; ilçe etiketlemesinde kullanıldı.
Copernicus Emergency Management Service (CEMS). ERA5 tabanlı yangın tehlike indeksleri tarihsel arşivi (cems-fire-historical-v1), FWI motorunun bağımsız doğrulamasında referans olarak kullanıldı. ewds.climate.copernicus.eu

Tüm kaynaklar kamuya açık ve ücretsizdir. Risk modeli geliştirme aşamasındadır; saha doğrulaması sürmektedir.

---

Bu doküman, projenin canlı bir kaydıdır ve yeni adımlar tamamlandıkça güncellenmelidir.

Son güncelleme: 29 Temmuz 2026 (CEMS FWI doğrulaması eklendi, bölüm 7.10)

Son güncelleme: 30 Temmuz 2026 (durum taşıyan mimari ve tam otomasyon işlendi; bölüm 9 yeniden yazıldı, bölüm 4.5, 7.10, 10 ve 11 güncellendi)

Son güncelleme: 31 Temmuz 2026 (operasyonel orman maskesi OpenStreetMap'ten ESA WorldCover'a taşındı, ızgara 5.254'ten 9.472 hücreye çıktı; bölüm 9 ve 10 güncellendi)

Son güncelleme: 6 Ağustos 2026 (Bilinen İtirazlar ve Yanıtlar bölümü eklendi; İtiraz 1, maruziyet çerçevesi eşleştirme testiyle sayısal olarak sınandı; Kaynaklar bölüm 13'e kaydı)

Son güncelleme: 6 Ağustos 2026 (İtiraz 1 nihai testi, zamansal case-crossover, 900 olayla tamamlandı ve bölüme işlendi; modelin hava alt skorunun gün zamanlama becerisi case-crossover AUC 0.587)

Son güncelleme: 6 Ağustos 2026 (İtiraz 2 eklendi, mekansal sızıntı sınandı; bölüm 7.8'deki mekansal blok 0.763 uzlaştırıldı, standart mekansal blok CV 0.83 ile 0.84, 0.763 büyük ayrımlı en kötü durum alt sınırı olarak netleştirildi)

Son güncelleme: 15 Ağustos 2026 (İtiraz 3, 4 ve 5 eklendi. Enez Büyükevren yangınının veri kümesinde bulunmaması üzerine hedef tanımı denetlendi: yüzde 50 eşiğinin doğal bir ayrım noktası olmadığı ve saflık şartı yükseldikçe tarım kenarı katsayısının yüzde 58, nüfus katsayısının yüzde 45 küçüldüğü ölçüldü; hedef kümesinin bu dokümandaki tarifle yeniden üretilemediği saptandı, kümeleme adımı yüzde 99.6 sadık, filtre adımı Cohen kappa 0.72 tavanında; pozitif ve referans sınıflarının farklı kurallarla tanımlandığı doğrulandı. Üç açığı da kapatan `hedef_kur.py` yazıldı)
