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
Canlı 7 günlük tahmin. Eğitim (arşiv) ile operasyon (tahmin) aynı kaynaktan beslendiği için değişken tanımları kaymaz. Geçmiş 35 gün ile gelecek 7 gün birleştirilerek biriken kuraklık kesintisiz hesaplanır. Operasyonel sürümde bu tahmin, ulusal orman ızgarasının her noktası için çekilir ve eğitimdeki kuruluk değişkenlerinin aynısı üretilir. Ham hava değişkenlerinin standart yangın hava indekslerine (FWI sistemi) çevrilmesi ayrıca yürütülmektedir; bkz. bölüm 7.8.

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

FWI motoru kanonik referansa (Van Wagner ve Pickett 1985) karşı birebir doğrulandı (test örneğinde FFMC 87.69, DMC 8.55, DC 19.01, ISI 10.85, BUI 8.49, FWI 10.10). Sistemin özyinelemeli olması, yani her günün değerinin önceki güne bağlı olması, bir zaman serisi gerektirir; bu yüzden her eğitim noktasının olay tarihine kadarki günlük hava dizisi arşivden çekilip FWI hesaplanmaktadır ve sızıntıyı önlemek için yalnızca olay tarihinden önceki hava kullanılmaktadır. FWI hesabı tamamlandı ve sonuçlar dürüstçe ölçüldü. Önemli bir bulgu: FWI bileşenleri kaba hava değişkenlerinin yerine konduğunda baseline'ı geçmedi (yaklaşık 0.828'e karşı 0.831). Yani kaba vekiller tutuşma gününün anlık koşullarını zaten iyi yakalıyor; FWI'nin değeri tek günün fotoğrafında değil, biriken kuraklık hafızasında. Nitekim FWI kaba havanın üstüne eklendiğinde her doğrulama şemasında katkı verdi. Üç şemanın AUC'leri (beş katlı, yıllar arası, mekansal blok) şöyle: yalnızca baseline 0.831, 0.834, 0.746; tarım kenarı eklenince 0.837, 0.840, 0.756; FWI eklenince 0.835, 0.837, 0.757; ikisi birlikte eklenince 0.840, 0.842, 0.763. FWI'nin katkısı en çok mekansal testte belirginleşti (bölgeden bölgeye genelleme), ki ulusal bir araç için en kritik sınav budur. Sonuç: FWI'nin dört kodu (FFMC, DMC, DC, ISI) ile tarım kenarı birlikte modele eklendi (bölüm 7.9). KBDI hesaplandı ama dört kodun yanında ek katkısı olmadığından modele alınmadı.

### 7.9 Birleşik model (mevcut sürüm)
Yukarıdaki testlerin sonucunda modelin mevcut sürümü on iki özellikle donduruldu: insan baskısı (nüfus), yakıt, beş kaba hava değişkeni (en yüksek sıcaklık, nem, rüzgar, son yağıştan beri gün, son 30 gün yağış), FWI'nin dört kodu (FFMC, DMC, DC, ISI) ve en yakın tarım alanına uzaklık. Beş katlı çapraz doğrulama AUC'si 0.840'tır (önceki sürüm 0.831). Model yine yorumlanabilir lojistik regresyondur ve donduruldu; saf aritmetik skorun eğitim kütüphanesiyle birebir aynı olduğu doğrulandı.

Standardize katsayıların büyüklük sırası modelin neye dayandığını şeffaf gösterir: en güçlü ayraç insan baskısıdır (yaklaşık 0.90), onu FFMC ince yakıt kuruluğu (0.48), en yüksek sıcaklık (0.45) ve tarım kenarı (negatif işaretli, yaklaşık 0.39 büyüklüğünde; yani tarıma yakınlık riski artırır) izler, ardından DC ve DMC kuraklık hafızası gelir. Dürüst bir not: FWI kodları modele girince bazı kaba hava değişkenlerinin (son yağıştan beri gün, son 30 gün yağış) tek tek katsayıları işaret değiştirir. Bu, kuraklık bilgisinin artık büyük ölçüde FWI kodlarında taşınmasından doğan eşdoğrusallık etkisidir; modelin bütün olarak tahmin gücünü bozmaz, ama bu iki değişkenin katsayısı artık tek başına yorumlanmamalıdır. Modelin omurgası değişmedi: en güçlü ayraç hâlâ insan baskısıdır, kuruluk ve tarım kenarı zemini hazırlar.

### 7.10 FWI motorunun bağımsız doğrulaması (CEMS)
Motorun Van Wagner denklemlerine karşı birebir doğrulanması hesabın doğruluğunu göstermişti (bölüm 7.8); bu adım ise uçtan uca zincirin, yani Open-Meteo girdisi, ısınma penceresi ve günlük hesabın bütününün, dünya referansıyla aynı tehlike sıralamasını üretip üretmediğini sınadı. Bağımsız referans, Copernicus Acil Durum Yönetim Servisi'nin (CEMS) ERA5 reanalizi ile hesapladığı küresel FWI arşividir; Avrupa'nın resmi yangın bilgi sistemi EFFIS'in altında yatan veridir (yaklaşık 25 kilometre çözünürlük, günlük, 1940'tan bugüne). İki hat tamamen bağımsızdır: farklı hava kaynağı, farklı hesap altyapısı, farklı kurum.

Karşılaştırma 2025 yaz sezonunda yapıldı (Haziran ile Eylül, 122 gün, eksiksiz). Mekansal bağımsızlık için ulusal ızgaranın 5.254 hücresinden, Türkiye'yi kaplayan her karasal CEMS pikseline en yakın tek hücre seçildi (793 nokta); aynı 25 kilometrelik piksele düşen komşu hücrelerin korelasyonu yapay şişirmesi böyle önlendi. Bizim taraf operasyonel motorun kendisiyle, ancak derin kuraklık kodunun oturması için 1 Mart başlangıçlı uzun ısınmayla (92 gün) koşuldu ve 96.746 gün kaydı eşleştirildi.

Sonuç: beş bileşenin tümünde güçlü sıra uyumu. Havuzlanmış Spearman korelasyonları FFMC 0.82, DMC 0.82, DC 0.92, ISI 0.81, bileşik FWI 0.82. Asıl test olan nokta içi sıralamada, yani her noktanın kendi 122 günü içinde hangi günün daha tehlikeli olduğunda, ortanca Spearman FFMC için 0.87, FWI için 0.82 ve DC için 0.99'dur. Motorun biriken kuraklık hafızası, FWI'ye geçmenin asıl gerekçesi olan bileşen, dünya referansının gün gün seyrini neredeyse birebir izlemektedir. Operasyonel açıdan anlamlı bir ek sayı: CEMS'in en riskli yüzde 10'luk gün ve nokta kümesinin yüzde 52'si bizim de en riskli yüzde 10'umuza düşer (şans düzeyi yüzde 10 olurdu).

Mutlak değerlerde sistematik ve tutarlı bir fark vardır: bizim değerler CEMS'ten bir miktar düşüktür (ortalama olarak FFMC 4, bileşik FWI 5, DC 63 puan). İki bilinen kaynağı var. Birincisi girdi geleneği: kanonik sistem ve CEMS öğle saati değerleriyle beslenirken bizim zincir günlük özet değerler kullanır (en yüksek sıcaklık ve rüzgar, ortalama nem); ortalama nemin öğle neminden yüksek olması nem kodlarını aşağı çeker. İkincisi ısınma: CEMS 1940'tan beri kesintisiz koşarken bizim koşu mevsim içinde başlar. DC'deki farkın yaz boyunca sabit kalması (aylık ortalama eksi 62 ile 67 bandında) bunun büyüyen bir hata değil, taşınan bir başlangıç kayması olduğunu gösterir. Bu kayma sıralamayı etkilemez. Nitekim EFFIS tehlike sınıflarında birebir uyum yüzde 44 iken bir sınıf toleransla yüzde 87'dir ve uyuşmazlıkların yaklaşık beşte dördü bizim bir sınıf altta kalmamız yönündedir; fark gürültü değil, tek yönlü ve öngörülebilir bir muhafazakarlıktır. Sabit bir kaydırma düzeltmesi bir sınıf toleranslı uyumu yüzde 92'ye çıkarır.

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

Ürün canlıya geçtiğinde risk skoru periyodik (haftalık ya da günlük) yeniden hesaplanır. Operasyonel katman uçtan uca kuruldu ve gerçek tahminle çalıştırıldı.

Dondurulmuş model: Eğitilen modelin parametreleri (özellik sırası, dönüşümler, ortalama ve standart sapmalar, katsayılar, kesişim) tek bir dosyaya donduruldu. Skorlama saf aritmetiktir; herhangi bir nokta listesi, eğitim kütüphanesine ihtiyaç olmadan bu parametrelerle skorlanabilir. Saf aritmetik skorun eğitim kütüphanesiyle birebir aynı sonucu verdiği doğrulandı. Operasyona alınan güncel model, bölüm 7.9'da tanımlanan on iki özellikli birleşik modeldir (AUC 0.840).

Ulusal orman ızgarası: Birkaç örnek bölge yerine tüm Türkiye orman örtüsü yaklaşık 5.5 kilometrelik (0.05 derece) bir ızgaraya bölündü. Orman maskesi OpenStreetMap orman poligonlarından alındı ve ızgaranın orman içine düşen hücreleri tutuldu (5.254 hücre). Her hücreye, eğitimle aynı 2 kilometre yarıçaplı (kalibre edilmiş) WorldPop nüfusu, yakıt ve en yakın tarım alanına uzaklık (tarım kenarı) atandı. Izgaranın nüfus dağılımı eğitim orman arka planıyla kıyaslanarak ölçek tutarlılığı doğrulandı (ızgara ortancası 63, eğitim referansı 83, aynı büyüklük mertebesi).

İl ve ilçe etiketleme: Her ızgara hücresine il, il sınır poligonlarıyla nokta içinde testiyle kesin atandı; ilçe ise resmi mülki idare sınırlarından atandı: resmi sınır çizgileri poligonlaştırılıp her poligon içine düşen resmi idari merkez noktasıyla isimlendirildi, sonra hücreler nokta içinde testiyle eşlendi (5.254 hücrenin tamamı; yüzde 99'u resmi poligondan, kalanı en yakın merkezden).

Haftalık zincir: İki betik. Birincisi ızgaranın her noktası için Open-Meteo'dan canlı 7 günlük tahmini ve biriken kuraklığı çeker (hız limitine takılmamak için küçük batch, bekleme ve kaldığı yerden devam edebilme ile). Derin kuraklık kodunun (DC) oturması için 60 günlük geçmiş de çekilir ve her tahmin gününe FWI kodları (FFMC, DMC, DC, ISI) eklenir. İkincisi dondurulmuş modeli, ızgaranın statik özelliklerini ve bu haftanın tahminini birleştirip her hücre için 7 günlük riski hesaplar ve haftanın en riskli gününe göre sıralar. Çıktı, panelin Bu Hafta sekmesinde ulusal bir risk haritası (her hücre renk kodlu nokta, sokak ve uydu zemin seçeneğiyle, tutuşma haritasıyla aynı dilde popup) ve en riskli ilk 30 hücrenin il ile ilçe etiketli listesi olarak gösterilir. Her hücrenin popup'ında bu haftaki risk, en riskli gün ve haftalık ortalamanın yanı sıra tepe günün FWI kodları (FFMC, DMC, DC, ISI) da yer alır.

Tam otomasyon (her sabah dönen zamanlanmış görev ve sonucu saklayan arka uç) henüz kurulmadı; mevcut zincir komutla çalıştırılıp panele gömülmektedir.

Dürüst not: hava tahmini ile gözlem aynı güvenilirlikte değildir. İlk 2 ile 3 gün isabetli, 5 ile 7 güne uzadıkça belirsizlik artar; uzak günler kesin değil eğilim olarak sunulmalıdır.

---

## 10. Sınırlar (dürüstçe)

Model artık iki eksenlidir (mekansal artı zamansal/hava). Kalan bir teknik nokta, arka plan noktalarının yaklaşık yüzde 6'sının hava çekme aşamasında tamamlanamamasıdır; bu, dengeyi bozmayacak kadar küçüktür ve sonradan tamamlanabilir.
Model tutuşma noktasını tahmin eder (önleme), başlamış yangının yayılımını değil; yayılım ayrı bir problemdir ve OGM'nin sahasıdır.
İnsan baskısı vekili nüfustur (WorldPop çevre nüfus toplamı). Ormana erişimin daha keskin bir vekil olup olmayacağı ayrıca sınandı: her nokta için en yakın yola, en yakın küçük yola ya da orman yoluna (track) ve en yakın yerleşime uzaklık OpenStreetMap'ten hesaplandı. Sonuç tezi yön olarak doğruladı (uzaklık katsayıları negatif, tutuşmalar yola ve yerleşime referans noktalarından belirgin biçimde daha yakın; örneğin yola ortanca 154 metreye karşı 421 metre), ama tahmin gücünü artırmadı: erişim uzaklıkları nüfusla örtüştüğü için tek başına nüfustan zayıf kaldı (mekansal AUC 0.69 ile 0.77 aralığında, nüfusunki 0.77) ve modele eklendiğinde kazanç ihmal edilebilir düzeydeydi (AUC 0.831'den 0.834'e). Nedeni, Türkiye'de yolların her yerde olması (en yakın yol zayıf bir ayraç) ve orman yolu haritasının OSM'de seyrek ve eksik olmasıdır. Dolayısıyla erişim, modelin girdisi değil, mekanizmanın doğrudan delilidir; insan ekseni olarak nüfus korunur. Erişimin asıl operasyonel değeri bir girdi olmakta değil, eğitilmiş modelin mesire ve orman parkı koordinatlarında çalıştırılıp "bu hafta sonu en riskli mesireler" sıralamasının üretilmesindedir.

Hedef tanımının bir kör noktası ve düzeltilişi: olayların orman olup olmadığına yalnızca ilk tespitin arazi örtüsüne bakarak karar veren erken yöntem, tarlada başlayıp ormana sıçrayan yangınları kaçırıyordu. Somut örnek, 8 Ağustos 2025 Çanakkale Sarıcaeli yangınıdır: olay tarla kenarında başlamış, ilk piksel ekili alan olduğu için erken yöntem bu gerçek orman yangınını orman dışı sayıp eliyordu. Oysa olayın 26 tespitinin 22'si (yaklaşık yüzde 85'i) orman üzerindeydi. Ayak izi yöntemine (tespitlerin çoğunluğunun orman olması) geçilince Sarıcaeli ve benzeri toplam 1.147 olay sete dahil oldu, ayak izi gerçekte tarla olan 452 olay ise düştü. Yine de yeni yöntemin kendi sınırı var: yüzde 50 eşiği bir yargı kararıdır ve eşiği oynatmak, sınırdaki olayların içeride mi dışarıda mı kalacağını değiştirir. Eşik dürüstçe seçilmiş bir denge noktasıdır, mutlak bir doğru değil.

Operasyonel ızgaranın orman maskesi WorldCover değil OpenStreetMap orman poligonlarıdır; OSM orman kapsamı bazı bölgelerde eksik olabileceğinden çok az sayıda gerçek orman hücresi ızgaraya girmemiş olabilir. Bu, eğitimi değil yalnızca skorlanan nokta kümesini etkiler ve ileride resmi orman katmanıyla zenginleştirilebilir.

İlçe etiketi resmi mülki idare sınırlarından atanmaktadır (sınır çizgileri poligonlaştırılıp resmi merkez noktalarıyla isimlendirilerek). Daha önce kısa süre OpenStreetMap, en başta da en yakın kayıtlı yangının ilçesini ödünç alan yaklaşık yöntem kullanılmıştı; ikisi de terk edildi. İl etiketi de il sınırlarından kesindir.

FWI tarafında derin kuraklık bileşeni DC yavaş kuruduğundan, operasyonel tahmin penceresinde tam oturması için uzun bir ısınma süresi ister; mevcut pencere FFMC ve DMC için yeterli, DC için kısmidir. DC tutuşmada ikincil olduğundan etkisi sınırlıdır, ama bu bir yaklaşıklıktır. CEMS doğrulaması bu yaklaşıklığı sayıya döktü: mevsim içi başlangıcın DC'de yarattığı kayma yaz boyunca sabit kalır (yaklaşık 60 ile 65 puan) ve gün sıralamasını etkilemez (nokta içi ortanca Spearman 0.99, bölüm 7.10).

---

## 11. Mevcut Durum ve Sıradaki Adımlar

Tamamlananlar: tez ulusal ölçekte doğrulandı; hedef tanımı ayak izi yöntemiyle iyileştirildi (3.397 orman olayı); nüfus tanımı kalibrasyonla kesinleştirildi (2 kilometre yarıçap); model aday özelliklerle güçlendirilip yeniden dondurularak on iki özelliğe çıkarıldı (insan, yakıt, beş kaba hava, FWI'nin dört kodu, tarım kenarı; beş katlı AUC 0.831'den 0.840'a, üç doğrulama şemasında da tutarlı), rekreasyon elendi; il ve ilçe etiketleri resmi mülki idare sınırlarından kesinleştirildi; ulusal panel kuruldu (Tutuşma haritası, Bu Hafta ulusal risk haritası, en riskli ilçe listesi, sokak ve uydu zemin); operasyonel katman uçtan uca kuruldu ve birleşik modele uyarlandı (60 günlük geçmişten FWI üreten haftalık hava çekimi, dondurulmuş model, 5.254 hücrelik ulusal orman ızgarası). Panel birleşik modelin operasyonel çıktısıyla tazelendi: Bu Hafta sekmesi örnek veriden gerçek haftalık skorlara geçirildi (5.254 hücre) ve tepe günün FWI kodları popup'a eklendi. Tutuşma haritasının tekil olaylar katmanına yanan alan ayak izi poligonları eklendi (VIIRS S-NPP tespitlerinden, 190 metre tampon ile). FWI motoru bağımsız referansa karşı doğrulandı: CEMS'in ERA5 tabanlı arşiviyle 2025 yaz sezonu, 793 mekansal bağımsız nokta ve 96.746 gün kaydı üzerinden; beş bileşende havuzlanmış Spearman 0.81 ile 0.92, DC'de nokta içi ortanca 0.99, EFFIS sınıf uyumu bir sınıf toleransla yüzde 87 (ayrıntı bölüm 7.10).

Not: bir önceki sürümün birinci sıradaki adımı, "paneli yeni modelin skorlarıyla tazelemek", tamamlandı; birleşik modelin operasyonel haftalık skorları Bu Hafta sekmesine gömüldü (yukarıda Tamamlananlar).

Sıradaki adımlar:
1. Tam otomasyon: her sabah dönen, canlı veriyle skor üretip paneli güncelleyen zamanlanmış sistem ve sonucu saklayan arka uç.
2. Belediye pilotu: sahada isabet doğrulaması ve ilk gelir.
3. Yangın yayılım modülü: ayrı ürün, OGM iş birliği.

Not: erişim katmanı (yola ve yerleşime uzaklık) sınandı ve nüfusu geçemediği için kapatıldı; ayrıntı bölüm 10'dadır.

---

## 12. Kaynaklar

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
