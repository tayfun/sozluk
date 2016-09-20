Sözlük
======

Turk Dil Kurumu sayfalarini gezinerek once kelime listesini, sonra anlamlarini cikarir ve veritabanina aktarir. Bunun yaninda bir API yardimiyla anlam bilgisini kullanima sunar.

Arka planda Python (2.7, cunku AWS Lambda icin Python 3'u desteklemiyor) kullanilmistir. Teknoloji kumesi tamamen AWS tabanlidir ve ucretsiz limitleri asmamaktadir. Dolayisiyla siz de kendi sozlugunuze sahip olabilirsiniz. Amazon AWS uzerinde sunucusuz bir yigin (stack) kullanilmaktadir. AWS Lambda, DynamoDB ve API Gateway icin basit bir referans uygulama da diyebiliriz.

Amac
----

TDK ag sayfasi asiri derece kullanissiz tasarlanmis bir sayfa. Arama yaptiginiz sayfayi baskalariyla paylasamiyorsunuz (cunku varsayilan olarak POST yontemi kullaniliyor ve aranan kelime kayboluyor), sayfa asiri yavas ve gereksiz cok fazla bolum var. Kaynak koduna baktiginizda bunun nedenlerini anliyorsunuz; sayfa Frontpage ile yazilmis ve `body` kisminda garip HTML bolumleri var. Turkce'ye onem veren birisi olarak sozlugu daha kullanilabilir yapmak istedim.

Genel Isleyis
-------------

Lambda fonksiyonlarinin tamami main.py dosyasinda bulunmaktalar. Burada bulunan `add_entries` fonksiyonu kelime listesi sayfasini tarayarak kelimeleri `entries` DynamoDB tablosuna ekler ve bulabildigi yeni kelime listesi bulunan URL'leri de `urls` tablosuna ekler. Yine ayni dosyadaki `add_meaning` fonksiyonu ise bu kelimelerin anlamlarini bularak `dictionary` isimli tabloya eklemektedir.

Lambda fonksiyonlarinin calismalarini DynamoDB olaylari (events) tetiklemektedir. Yani `urls` tablosuna bir giris yapildiginda `add_entries` eklenen sayfaya giderek kelime listesini cikarmakta ve bunlari `entries` tablosuna eklemektedir. Yine ayni sekilde `entries` tablosu da `add_meaning` fonksiyonunu tetiklemekte ve kelimelerin anlamlarinin `dictionary` tablosuna yazilmasini saglamakta.

Gereklilikler
-------------

En iyi programcilar baska kutuphaneleri kullananlardir onermesine katiliyorum, dolayisiyla bu projede varolan kutuphaneleri yeniden yazmak hic amacim olmadi. Gereklilikleri `requirements.txt` dosyasina koydum. Bunlari kurarken onemli bir nokta var, o da su: kurulan kutuphaneleri lambda'ya yukleyebilmek icin olagan yerlerine degil kok dizine kurmak gerekiyor. Bunun icin, `pip` ile `-t` secenegini kullanmaliyiz::

    pip install -r requirements.txt -t .

AWS tarafindan Lambda ortaminda varsayilan olarak gelmeyen kutuphaneleri kurmak saf Python olan kutuphaneler icin bu kadar basit. Yani sadece kutuphaneyi paketlemeniz gerekiyor. `lxml` gibi C dilinde gereklilikleri olan kutuphaneler ise biraz mesakkatli, bunlari kendimiz `AMI uzerinde derleyip paketlememiz gerekiyor`_. Kod icindeki `lxml-ami-build` dizini bunun icin var. Yerel makinemizle buyuk olasilikla uyumlu olmayan bu kutuphanenin cakisma yapmamasi icin ismini `lxml` yerine `lxml-ami-build` koydum. `Makefile` paketlerken ismini `lxml` yapacaktir.

.. _AMI uzerinde derleyip paketlememiz gerekiyor: https://www.azavea.com/blog/2016/06/27/using-python-lxml-amazon-lambda/

AWS uzerinde 3 tane DynamoDB tablosunu hazir etmeniz gerekiyor. Bunlari su sekilde hazirlayabilirsiniz::

    aws dynamodb  --profile my-aws-profile create-table --table-name dictionary --attribute-definitions AttributeName=entry,AttributeType=S AttributeName=norm,AttributeType=S --key-schema AttributeName=norm,KeyType=HASH AttributeName=entry,KeyType=RANGE --provisioned-throughput ReadCapacityUnits=10,WriteCapacityUnits=10 --region eu-west-1

    aws dynamodb  --profile my-aws-profile --region eu-west-1 create-table --table-name entries --attribute-definitions AttributeName=entry,AttributeType=S --key-schema AttributeName=entry,KeyType=HASH  --provisioned-throughput ReadCapacityUnits=14,WriteCapacityUnits=14 --stream-specification StreamEnabled=true,StreamViewType=KEYS_ONLY

    aws dynamodb  --profile my-aws-profile --region eu-west-1 create-table --table-name urls --attribute-definitions AttributeName=url,AttributeType=S --key-schema AttributeName=url,KeyType=HASH  --provisioned-throughput ReadCapacityUnits=1,WriteCapacityUnits=1 --stream-specification StreamEnabled=true,StreamViewType=KEYS_ONLY

Ucretsiz sinirlar dahilinde olmasi icin tablolarin ayrilmis kapasite toplaminin 25'i gecmemesine dikkat ettim. Yukaridaki komutlarda profil ismini `.aws/credentials` dosyasinda belirlediginiz isim ve `region` kismini da calismak istediginiz bolge ile degistirmeyi unutmayin.

Bundan sonra `make` komutunu calistirin ve olusturulan zip dosyasini `upload` ederek AWS Lambda uzerinde iki tane lambda fonksiyonu hazirlayin. Ilk fonksiyon `urls` uzerinden tetiklenen `add_entries` ve ikincisi `entries` uzerinden tetiklenen `add_meaning` fonksiyonlari. Lambda fonksiyonlarini olustururken `policy` icin `lambda_policy.json` dosyasini sablon olarak kullanabilirsiniz. Tebrikler, artik TDK uzerinde gezinmeye baslayabiliriz.

Ilk tetigi baslatmak icin kelime listelerinin ilk sayfalarini `urls` tablosuna yazmak gerekiyor. Kelime listesi TDK web sitesinde kolay bulunamiyor. Ben kelime listesini yazim kilavuzunu gezerek toplama yolunu sectim. Bunun icin her harf icin yazim kilavuzunun ilk sayfasini `urls` tablosuna ekliyorum. Yani tetigi baslatmak icin su komutu calistirmak yeterli::

    for letter in {a,b,c,ç,d,e,f,g,ğ,h,ı,i,j,k,l,m,n,o,ö,p,r,s,ş,t,u,ü,v,y,z}; do aws dynamodb  --profile my-aws-profile --region eu-west-1 put-item --table-name urls --item "{\"url\": {\"S\": \"http://tdk.org.tr/index.php?option=com_yazimkilavuzu&arama=kelime&kelime=$letter&kategori=yazim_listeli&ayn=bas\"}}" --return-consumed-capacity TOTAL ; done


