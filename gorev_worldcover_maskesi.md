# Görev: operasyonel orman maskesini WorldCover'a taşımak

Hazırlanma tarihi: 31 Temmuz 2026. Bu, sıradaki tek iştir; bittiğinde bu dosya
silinebilir, kalıcı bilgi `devir_notu.md` ve yöntem dokümanına işlenir.

## Neden

İki ayrı sorun var, ikisi de aynı kökten geliyor.

**Kapsama boşluğu.** Panelin Bu Hafta haritasında gözle görülür orman alanları
noktasız duruyor. Sebebi iki katmanlı. Birincisi, hücreler ormanı kaplamıyor;
ızgara düğümleri ormanın içine düşüp düşmediğine göre eleniyor, dolayısıyla
4 ile 5 km'den dar bir orman içinden hiç düğüm geçmeyebiliyor (vadi boyunca
uzanan şerit ormanlar, dar kıyı bantları). İkincisi ve daha büyüğü, orman
maskesinin OpenStreetMap orman poligonlarından gelmesi; OSM'nin Türkiye
kapsaması düzensiz, bazı bölgelerde neredeyse boş.

**Tanım tutarsızlığı.** Eğitimde orman tanımı ESA WorldCover'dan geliyor
(ağaç örtüsü kod 10, maki ve çalılık kod 20), operasyonda ise OSM'den. Yani
model bir orman tanımıyla eğitilip başka bir orman tanımıyla çalıştırılıyor.
Yöntem dokümanının 10. bölümünde bu zaten dürüstçe kayıtlı bir sınır. Kapatmak
metodolojik bir kazanç ve dokümana yazılacak cinsten.

## Yapılacak

Ulusal ızgaranın orman maskesi ESA WorldCover'dan yeniden kurulacak ve
`noktalar_baz_grid.json` yeniden üretilecek.

Eğitimde WorldCover, Cloud-Optimized GeoTIFF olarak, dev dosya indirilmeden
yalnızca gereken pikseller okunarak kullanılmıştı. Aynı teknik burada da
geçerli; ızgara düğümü sayısı sınırlı olduğu için maliyet düşük.

## Zorunlu kısıtlar

Bunlar pazarlık konusu değil, ihlali sessiz bozulma üretir.

**Kafes aynı kalacak.** 0,05 derecelik adım ve mevcut başlangıç noktası
korunacak. Hücre adı `"enlem,boylam"` biçiminde, üç ondalık. Böylece bugünkü
5.254 hücrenin adları birebir aynı kalır, `data/fwi_durum.json` ile eşleşir ve
kuraklık birikimleri korunur. Kafes kayarsa hepsi yeni sayılır.

**Nüfus tanımı değişmeyecek.** 2 km yarıçaplı WorldPop toplamı, 1,11 kalibrasyon
böleni. Yeni hücrelerin nüfusu mevcut hücrelerle **aynı kodla** hesaplanmalı.
Bu yüzden ızgarayı üreten mevcut betik esas alınacak, sıfırdan yazılmayacak.

**Çıktı şeması değişmeyecek.** `noktalar_baz_grid.json` içindeki kayıtlar
bugünkü alanları taşımalı: `ad`, `lat`, `lon`, `human`, `fuel`, `farm_dist`.

## Değişecek bir şey: yakıt artık gerçek

Bugün operasyonel ızgarada yakıt orman varsayılıyor, yani her hücrede 1,0.
WorldCover'a geçince yakıt eğitimdeki gibi sınıftan türetilebilir: ağaç örtüsü
1,0, maki ve çalılık 0,85. Model katsayısı küçük (yaklaşık eksi 0,07) olduğu
için etkisi sınırlı, ama eğitim ile operasyon arasındaki bir tutarsızlık daha
kapanır.

## Beklenen sonuçlar

**Hücre sayısı artacak.** Türkiye orman varlığı kabaca 230 bin kilometrekare,
hücre başına yaklaşık 24 kilometrekare. Tam kapsama yaklaşık 9.000 hücre eder;
bugün 5.254'teyiz. Yani ızgara ikiye katlanabilir.

**Maliyet ve boyut aynı oranda artar.** Günlük ağırlıklı çağrı 5.254'ten
9.000 civarına (ayda 158 binden 270 bine, bütçe 1 milyon). Koşu süresi ve
`data/skorlar.json` boyutu da benzer oranda. Dosya boyutunu izlemek gerekir,
panel onu her açılışta indiriyor.

**İdari etiketler yeniden üretilmeli.** `noktalar_idari.json` hücre başına il ve
ilçe tutuyor. Yeni hücrelerin etiketi olmayacağı için panelde koordinat olarak
görünürler. O eşleştirme de yeniden koşturulmalı.

**Isınma maliyeti sınırlı.** `operasyonel_hava.py` 31 Temmuz 2026'da kısmi
ısınmaya geçirildi: ızgaraya yeni nokta eklendiğinde eski hücreler ILIK kalır,
yalnızca yeni hücreler 60 günlük pencereyle ısınır. Yani bu değişiklik mevcut
hücrelerin DC birikimini sıfırlamaz. Eksik oran yüzde 50'yi aşarsa tam soğuk
başlangıca düşülür; maske ikiye katlarsa bu eşiğe yaklaşılır, koşudan önce
kontrol edilmeli.

## Gerekli girdiler

Izgarayı üreten mevcut betik (nüfus, yakıt ve tarım kenarı hesabını içeren).
WorldPop Türkiye nüfus rasterı. WorldCover COG adresleri. İdari etiketleri
üreten betik.

## Kabul kriterleri

Yeni `noktalar_baz_grid.json` üretildikten sonra, panele geçirmeden önce:

Bugünkü 5.254 hücrenin tamamı yeni dosyada aynı `ad` ile bulunuyor mu.

Ortak hücrelerin `human` değerleri eskisiyle birebir aynı mı (kalibrasyon
bölenine kadar). Fark varsa nüfus hesabı kaymış demektir, durulmalı.

Yeni hücre sayısı ve toplam sayı beklenen aralıkta mı.

Panelin Bu Hafta haritasında daha önce boş olan bilinen orman alanları artık
nokta gösteriyor mu (görsel kontrol yeterli).

Yeni ızgarayla bir koşu yapıldığında kayıp oranı yüzde 10 eşiğinin altında mı,
süre kabul edilebilir mi.

Bunlar geçtikten sonra yöntem dokümanının 9. bölümündeki ızgara tarifi ve
10. bölümündeki OSM maskesi sınırı güncellenir, sonuna yeni bir
"Son güncelleme" satırı eklenir.
