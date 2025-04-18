import socket
import threading
import customtkinter as ctk
from tkinter import simpledialog
import random

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")


istemci_soketi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
istemci_soketi.connect(("127.0.0.1", 55555))

kullanici_adi = simpledialog.askstring ("CM!","Kullanıcı adınızı giriniz!")

ana_pencere = ctk.CTk()
ana_pencere.title(f"Chat Mini!-{kullanici_adi}")
ana_pencere.geometry("435x600")
ana_pencere.resizable(False, False)
ana_pencere.iconbitmap("chat_1089877.ico")

font_normal = ctk.CTkFont(family="Arial", size=16)

chat_frame = ctk.CTkScrollableFrame(ana_pencere, width=370, height=480, fg_color="white", corner_radius=20) #mesagebox
chat_frame.place(x=15, y=10)

mesaj_kutusu = ctk.CTkEntry(ana_pencere, width=260, height=40, font=font_normal, placeholder_text="Senin mesajın...")
mesaj_kutusu.place(x=30, y=510)

def mesaj_gonder():
    mesaj = mesaj_kutusu.get()
    if mesaj.strip() == "":
        return
    tam_mesaj = f"{kullanici_adi}: {kullanici_adi} > {mesaj}"
    istemci_soketi.send(tam_mesaj.encode('utf-8'))
    mesaj_kutusu.delete(0, ctk.END)

mesaj_kutusu.bind("<Return>", lambda e: mesaj_gonder())

gonder = ctk.CTkButton(ana_pencere, text="Gönder", command=mesaj_gonder, width=100,height=40)
gonder.place(x=285, y=510)

def mesaj_goster(mesaj):
    if ":" in mesaj:
        isim, icerik = mesaj.split(":", 1)
        isim = isim.strip()
        icerik = icerik.strip()

        balon_renk = "#34C759" if isim == kullanici_adi else "#E5E5EA"
        yazı_rengi = "white" if isim == kullanici_adi else "black"
        hizalama = "e" if isim == kullanici_adi else "w"

        mesaj_label = ctk.CTkLabel(
            master=chat_frame,
            text=icerik,
            font=font_normal,
            text_color=yazı_rengi,
            fg_color=balon_renk,
            corner_radius=20,
            justify="left",
            wraplength=220,
            width=10,
            anchor="w",
            padx=10,
            pady=8
        )
        mesaj_label.pack(anchor=hizalama, padx=10, pady=5, fill="none")

    else:
        mesaj_label = ctk.CTkLabel(master=chat_frame, text=mesaj, font=font_normal)
        mesaj_label.pack(anchor="center", pady=5)


def mesaj_al():
    while True:
        try:
            gelen_mesaj = istemci_soketi.recv(1024).decode('utf-8')
            if gelen_mesaj == "KULLANICI_ADI":
                istemci_soketi.send(kullanici_adi.encode('utf-8'))
            else:
                mesaj_goster(gelen_mesaj)
        except:
            print("Bağlantı kesildi.")
            istemci_soketi.close()
            break

threading.Thread(target=mesaj_al, daemon=True).start()

ana_pencere.mainloop()
