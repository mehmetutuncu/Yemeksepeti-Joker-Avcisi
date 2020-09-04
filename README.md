# Yemeksepeti Joker Avcısı
Bu program yemeksepeti üzerinde joker yakalamanızı sağlar.
### 1- Bağımlılıkların Yüklenmesi 
```pip install -r requirements.pip```
### 2- SQLite Database
Program kendisi yemeksepeti.db dosyasını oluşturacaktır.<br>
İlk adımda databasedeki User ve Region tablosuna kayıt eklenmesi gerekmektedir.
<br> Eklenmemesi durumunda sistem hata log'u olarak basacaktır.

### 3- Programı Çalıştırma
Konsola ```python main.py``` yazarak çalıştırıyoruz. 
Programın joker bulması durumunda konsol üzerinde yönergeler geliyor.<br> 
restaurant_info.json dosyasının içerisinde paymentAccepted anahtarında ödeme seçenekleri gelmekte. 
İsteğinize göre kod içerisinden revize edebilirsiniz.

### 4- Output
````commandline
INFO:root:Yıldız Hilal Mah. joker aranıyor...
INFO:root:Yıldız Hilal Mah. joker bulundu!

INFO:root:
Restorant Adı: Madame Waffle
Ödeme Şekli: Ticket Restaurant Yemek Kartı geçerli değildir.
Adres:Çankaya (Birlik Mah.), Ankara
Hız: 9,4 / Servis: 9,4 / Lezzet: 9,3

INFO:root:
Restorant Adı: Tencere Ev Yemekleri
Ödeme Şekli: Ticket Restaurant Yemek Kartı geçerlidir.
Adres:G.O.P (Nenehatun), Ankara
Hız: 8,7 / Servis: 8,9 / Lezzet: 8,8

INFO:root:
Restorant Adı: Dicle Pide & Kebap
Ödeme Şekli: Ticket Restaurant Yemek Kartı geçerli değildir.
Adres:Çankaya (Güzeltepe Mah.), Ankara
Hız: 8,5 / Servis: 8,6 / Lezzet: 8,3

INFO:root:
Restorant Adı: Light Fit Sports Cafe
Ödeme Şekli: Ticket Restaurant Yemek Kartı geçerlidir.
Adres:Yukarı Ayrancı, Ankara
Hız: 9,2 / Servis: 9,3 / Lezzet: 9,2

Geçmek istiyor musunuz? e/h: 
````