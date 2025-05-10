import socket
import threading

istemciler = []
kullanici_adlari = []

def yayinla(mesaj):
    for istemci in istemciler:
        istemci.send(mesaj)

def istemciyi_yonet(istemci):
    while True:
        try:
            mesaj = istemci.recv(1024)
            yayinla(mesaj)
        except:
            indeks = istemciler.index(istemci)
            istemciler.remove(istemci)
            istemci.close()
            kullanici_adi = kullanici_adlari[indeks]
            kullanici_adlari.remove(kullanici_adi)
            break

def dinle():
    sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sunucu.bind(("0.0.0.0", 55555))
    sunucu.listen()

    print("Sunucu çalışıyor...")

    while True:
        istemci, adres = sunucu.accept()
        print(f"Bağlanan: {str(adres)}")

        istemci.send("KULLANICI_ADI".encode('utf-8'))
        kullanici_adi = istemci.recv(1024).decode('utf-8')
        kullanici_adlari.append(kullanici_adi)
        istemciler.append(istemci)

        print(f"Kullanıcı adı: {kullanici_adi}")
        yayinla(f"{kullanici_adi} sohbete katıldı!".encode('utf-8'))
        istemci.send("Bağlantı başarılı.".encode('utf-8'))

        is_parcasi = threading.Thread(target=istemciyi_yonet, args=(istemci,))
        is_parcasi.start()

dinle()
