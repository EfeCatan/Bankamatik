
import tkinter as tk
from tkinter import messagebox
import csv
import random
from LoginScreen import LoginScreen, Kullanici  

class Bankamatik:
    def __init__(self):
        self.kullanicilar = []
        self.krediler = [
            Kredi("İhtiyaç Kredisi", 0.10, 48, 12, 100000, 1000),
            Kredi("Konut Kredisi", 0.08, 240, 36, 1000000, 50000),
            Kredi("Taşıt Kredisi", 0.12, 60, 12, 500000, 10000),
            Kredi("Bayram Kredisi", 0.15, 24, 6, 20000, 500),
            Kredi("Evlilik Kredisi", 0.11, 60, 12, 200000, 5000),
            Kredi("İpotekli İhtiyaç Kredisi", 0.09, 120, 24, 500000, 10000),
            Kredi("Esnaf Kredisi", 0.13, 36, 6, 300000, 10000),
            Kredi("Öğrenci Kredisi", 0.07, 120, 12, 50000, 1000)
        ]
        self.root = tk.Tk()
        self.login_screen = LoginScreen(self.root, self)
        self.kullanicilari_yukle()  # Program başladığında kayıtlı kullanıcı bilgilerini yükle
        self.root.mainloop()
        self.btn_kaydet = None

    def giris_ekrani_ac(self):
        self.root.deiconify()  # Ana pencereyi görünür yap

    def yeni_kullanici_olustur(self, kullanici_adi, sifre, kullanici_tipi):
        kullanici = Kullanici(kullanici_adi, sifre, kullanici_tipi)
        self.kullanicilar.append(kullanici)
        self.kullanicilari_kaydet()

    def kullanici_sil(self, kullanici_adi):
        for kullanici in self.kullanicilar:
            if kullanici.kullanici_adi == kullanici_adi:
                self.kullanicilar.remove(kullanici)
                self.kullanicilari_kaydet()
                messagebox.showinfo("Başarılı", f"{kullanici_adi} kullanıcısı başarıyla silindi.")
                return
        messagebox.showerror("Hata", f"{kullanici_adi} kullanıcısı bulunamadı!")

    def kayitli_kullanicilar_getir(self):
        return self.kullanicilar
    

    def panel_ac(self, kullanici):
        panel_penceresi = tk.Toplevel()
        panel_penceresi.title("Kullanıcı Paneli")
        panel_penceresi.geometry("300x200")

        label_hosgeldiniz = tk.Label(panel_penceresi, text=f"Hoşgeldiniz, {kullanici.kullanici_adi}!")
        label_hosgeldiniz.pack()

        btn_para_cekme = tk.Button(panel_penceresi, text="Para Çekme", command=lambda: self.para_cekme_menu(kullanici))
        btn_para_cekme.pack()

        btn_para_yatirma = tk.Button(panel_penceresi, text="Para Yatırma", command=lambda: self.para_yatirma_menu(kullanici))
        btn_para_yatirma.pack()

        btn_para_transferi = tk.Button(panel_penceresi, text="Para Transferi", command=lambda: self.para_transferi_menu(kullanici))
        btn_para_transferi.pack()

    def kullanicilari_yukle(self):
        try:
            with open("kullanicilar.csv", newline='') as file:
                reader = csv.reader(file)
                for row in reader:
                    if len(row) == 5:  # Satır beş sütundan oluşmalı (bakiye ve IBAN eklenmiş)
                        kullanici_adi, sifre, kullanici_tipi, bakiye, iban = row
                        kullanici = Kullanici(kullanici_adi, sifre, kullanici_tipi, iban, bakiye)
                        kullanici.bakiye = float(bakiye)
                        # Eğer kullanıcı zaten varsa güncelle, yoksa ekle
                        self.kullanici_guncelle_veya_ekle(kullanici)
        except FileNotFoundError:
            print("Dosya bulunamadı: kullanicilar.csv")


    def kullanici_guncelle_veya_ekle(self, yeni_kullanici):
        """
        Yeni bir kullanıcı ekler veya mevcut kullanıcının bilgilerini günceller.
        """
        for i, kullanici in enumerate(self.kullanicilar):
            if kullanici.kullanici_adi == yeni_kullanici.kullanici_adi:
                self.kullanicilar[i] = yeni_kullanici
                return
        self.kullanicilar.append(yeni_kullanici)        


    def kullanicilari_kaydet(self):
        with open("kullanicilar.csv", "w", newline='') as file:
            writer = csv.writer(file)
            for kullanici in self.kullanicilar:
                writer.writerow([kullanici.kullanici_adi, kullanici.sifre, kullanici.kullanici_tipi, kullanici.bakiye, kullanici.iban])

class Kredi:
    def __init__(self, ad, faiz_orani, max_taksit, min_taksit, max_kredi_miktari, min_kredi_miktari):
        self.ad = ad
        self.faiz_orani = faiz_orani
        self.max_taksit = max_taksit
        self.min_taksit = min_taksit
        self.max_kredi_miktari = max_kredi_miktari
        self.min_kredi_miktari = min_kredi_miktari

    def __str__(self):
        return f"{self.ad} Kredisi:\n"\
               f"Faiz Oranı: %{self.faiz_orani*100}\n"\
               f"Maksimum Taksit: {self.max_taksit} ay\n"\
               f"Minimum Taksit: {self.min_taksit} ay\n"\
               f"Maksimum Kredi Miktarı: {self.max_kredi_miktari} TL\n"\
               f"Minimum Kredi Miktarı: {self.min_kredi_miktari} TL"

bankamatik = Bankamatik()   
