import tkinter as tk
from tkinter import messagebox, filedialog
from gtts import gTTS, lang
import os
import shutil

class Uygulama(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("NMSpeech")
        self.geometry("900x800")
        self.resizable(False, False)

        # Dil seçimi butonu
        self.dil_sec_butonu = tk.Button(self, text="Dil seçin", command=self.dil_secim_penceresi)
        self.dil_sec_butonu.pack()

        # Metin girişi
        self.metin_etiketi = tk.Label(self, text="Metin girin:")
        self.metin_etiketi.pack()
        self.metin_girisi = tk.Text(self, height=10, width=40)
        self.metin_girisi.pack()

        # Sentezle butonu
        self.sentezle_butonu = tk.Button(self, text="Sentezle", command=self.metin_sentezle)
        self.sentezle_butonu.pack()

        # Varsayılan dil
        self.dil = "en"

    def dil_secim_penceresi(self):
        # Dil seçimi için yeni bir pencere aç
        self.dil_penceresi = tk.Toplevel(self)
        self.dil_penceresi.title("Dil Seçimi")
        self.dil_penceresi.geometry("600x500")

        # gTTS'in desteklediği dilleri al
        self.dil_secenekleri = lang.tts_langs()

        # Görüntüleme adları ve dil kodları için sözlük oluştur
        self.goruntuleme_dilleri = {name: code for code, name in self.dil_secenekleri.items()}

        # Listbox oluştur ve dil adlarını ekle
        self.dil_listbox = tk.Listbox(self.dil_penceresi)
        for dil_adi in self.goruntuleme_dilleri.keys():
            self.dil_listbox.insert(tk.END, dil_adi)
        self.dil_listbox.pack()

        # Seçim butonu
        self.secim_butonu = tk.Button(self.dil_penceresi, text="Seç", command=self.dil_secimi)
        self.secim_butonu.pack()

    def dil_secimi(self):
        # Seçilen dil adını al ve dil kodunu ayarla
        secilen_dil_adi = self.dil_listbox.get(tk.ACTIVE)
        self.dil = self.goruntuleme_dilleri.get(secilen_dil_adi, "en")
        self.dil_penceresi.destroy()
        # Dil seçimini ekranda göster
        self.dil_sec_butonu.config(text=f"Dil seçildi: {secilen_dil_adi}")

    def metin_sentezle(self):
        metin = self.metin_girisi.get("1.0", "end-1c")
        tts = gTTS(text=metin, lang=self.dil)
        tts.save("gecici.mp3")
        self.ses_oynatici = messagebox.askyesno("Ses kaydet", "Ses dosyasını kaydetmek istiyor musunuz?")
        if self.ses_oynatici:
            dosya_yolu = filedialog.asksaveasfilename(defaultextension=".mp3")
            if dosya_yolu:
                shutil.move("gecici.mp3", dosya_yolu)
        else:
            if os.name == 'nt':  # Windows
                os.system("start gecici.mp3")
            elif os.name == 'darwin':  # macOS
                os.system("afplay gecici.mp3")
            else:  # Linux
                os.system("aplay gecici.mp3")

if __name__ == "__main__":
    uygulama = Uygulama()
    uygulama.mainloop()

