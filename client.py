import socket
import threading
import customtkinter as ctk
from tkinter import*
from PIL import Image, ImageTk
from tkinter import messagebox
import time

def kullanici_adi_al():
    nickname = None

    def on_submit():
        nonlocal nickname
        nickname = entry.get().strip()
        if not nickname:
            messagebox.showwarning("Hata!","Kullanıcı adınızı girmeden sohbet edemezsiniz!")
        else:
            login.destroy()

    login = ctk.CTk()
    login.geometry("565x600")
    login.title("Kullanıcı Girişi")
    login.iconbitmap("chat_1089877.ico")

    font_normal2=ctk.CTkFont(family="Arial", size=18)
    font_normal3=ctk.CTkFont(family="Arial", size=30)

    image1=Image.open("chat_1089877.png")
    resized_image1 = image1.resize((180, 180))
    image1_=ImageTk.PhotoImage(resized_image1)

    logo1 = ctk.CTkLabel(login,text="",image=image1_)
    logo1.place(x=200,y=80)
    logo_name_label = ctk.CTkLabel(login,text="Chat Mini!",font=font_normal3)
    logo_name_label.place(x=220,y=265)

    label = ctk.CTkLabel(login,text="Kullanıcı adınızı giriniz!",font=font_normal2)
    label.place(x=203,y=320)

    entry = ctk.CTkEntry(login,font=font_normal2)
    entry.place(x=225,y=355)
    entry.bind("<Return>", lambda e: on_submit())

    submit_btn = ctk.CTkButton(login, text="Gönder", command=on_submit,font=font_normal2)
    submit_btn.place(x=225,y=390)

    login.mainloop()
    return nickname

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("green")

kullanici_adi = kullanici_adi_al()

istemci_soketi = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
istemci_soketi.connect(("YOU İP", 55555))

ana_pencere = ctk.CTk()
ana_pencere.title(f"Chat Mini! - {kullanici_adi}")
ana_pencere.geometry("565x600")
ana_pencere.resizable(False, False)
ana_pencere.iconbitmap("chat_1089877.ico")

font_normal = ctk.CTkFont(family="Arial", size=16)

chat_frame = ctk.CTkScrollableFrame(ana_pencere, width=500, height=450, fg_color="white", corner_radius=20)
chat_frame.place(x=15, y=10)

mesaj_kutusu = ctk.CTkEntry(ana_pencere, width=350, height=40, font=font_normal, placeholder_text="Senin mesajın...")
mesaj_kutusu.place(x=40, y=510)


def saati_guncelle():
    saat = time.strftime("%H.%M")
    saat_label.configure(text=f"Saat | {saat}")
    ana_pencere.after(1000, saati_guncelle)

saat_label = ctk.CTkLabel(ana_pencere, text="",bg_color="white",font=font_normal)
saat_label.place(x=445, y=33)

saati_guncelle()

def mesaj_gonder():
    mesaj = mesaj_kutusu.get()
    if mesaj.strip() == "":
        return
    tam_mesaj = f"{kullanici_adi}: {kullanici_adi} | {mesaj}"
    istemci_soketi.send(tam_mesaj.encode('utf-8'))
    mesaj_kutusu.delete(0, ctk.END)

mesaj_kutusu.bind("<Return>", lambda e: mesaj_gonder())

gonder = ctk.CTkButton(ana_pencere, text="Gönder", command=mesaj_gonder,font=font_normal, width=100, height=40)
gonder.place(x=410, y=510)

def mesaj_goster(mesaj):
    if ":" in mesaj:
        isim, icerik = mesaj.split(":", 1)
        isim = isim.strip()
        icerik = icerik.strip()

        balon_renk = "#2ECC71" if isim == kullanici_adi else "#E5E5EA"
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
