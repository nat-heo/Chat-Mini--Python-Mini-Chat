import socket
import threading
import os
from datetime import datetime

istemciler = []
kullanici_adlari = []
istemci_adresleri = {}
yasakli_ipler = set()

def yayinla(mesaj, gonderen=None):
    zaman = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if gonderen:
        log_mesaj = f"{gonderen} | {mesaj.decode('utf-8')} | {zaman}"
        with open("log.txt", "a", encoding="utf-8") as f:
            f.write(log_mesaj + "\n")

    for istemci in istemciler:
        try:
            istemci.send(mesaj)
        except:
            pass

def istemciyi_yonet(istemci):
    indeks = istemciler.index(istemci)
    kullanici_adi = kullanici_adlari[indeks]
    ip = istemci_adresleri[istemci]

    while True:
        try:
            mesaj = istemci.recv(1024)
            if not mesaj:
                break
            yayinla(mesaj, gonderen=kullanici_adi)
        except:
            break

    istemciler.remove(istemci)
    kullanici_adlari.remove(kullanici_adi)
    del istemci_adresleri[istemci]
    istemci.close()
    yayinla(f"{kullanici_adi} sohbetten ayrıldı.".encode('utf-8'))

def komutlari_dinle():
    while True:
        komut = input()
        if komut.startswith("/block "):
            ip = komut.split("/block ")[1].strip()
            yasakli_ipler.add(ip)
            print(f"IP adresi engellendi: {ip}")
        elif komut.startswith("/unblock "):
            ip = komut.split("/unblock ")[1].strip()
            if ip in yasakli_ipler:
                yasakli_ipler.remove(ip)
                print(f"IP adresi engeli kaldırıldı: {ip}")
            else:
                print(f"Bu IP engellenmemiş: {ip}")
        elif komut.strip() == "/help":
            print("/block USER_IP")
            print("/unblock USER_IP")
        else:
            print("Bilinmeyen komut. Yardım için /help yaz.")

def dinle():
    os.system("cls" if os.name == "nt" else "clear")

    sunucu = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sunucu.bind(("0.0.0.0", 55555))
    sunucu.listen()
    print("Sunucu çalışıyor...")

    threading.Thread(target=komutlari_dinle, daemon=True).start()

    while True:
        istemci, adres = sunucu.accept()
        ip = adres[0]

        if ip in yasakli_ipler:
            print(f"Engellenmiş IP'den bağlantı engellendi: {ip}")
            istemci.close()
            continue

        istemci.send("KULLANICI_ADI".encode('utf-8'))
        try:
            kullanici_adi = istemci.recv(1024).decode('utf-8')
        except:
            istemci.close()
            continue

        zaman = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{kullanici_adi} | IP: {ip} | {zaman}")

        # Bağlantı logunu dosyaya yaz
        with open("connect_log.txt", "a", encoding="utf-8") as f:
            f.write(f"{kullanici_adi} | {ip} | {zaman}\n")

        kullanici_adlari.append(kullanici_adi)
        istemciler.append(istemci)
        istemci_adresleri[istemci] = ip

        yayinla(f"{kullanici_adi} sohbete katıldı!".encode('utf-8'))

        is_parcasi = threading.Thread(target=istemciyi_yonet, args=(istemci,))
        is_parcasi.start()

dinle()
