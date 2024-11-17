import csv
import tkinter as tk
from tkinter import messagebox


class AdminPaneli:
    def __init__(self, root, bankamatik):
        self.root = root
        self.bankamatik = bankamatik
        self.entry_kullanici_adi = None
        self.root.protocol("WM_DELETE_WINDOW", self.cikis)
        self.root.geometry("300x150")

        label_islem_secin = tk.Label(root, text="Kullanıcı işlemi seçin:")
        label_islem_secin.grid(row=0, column=0, columnspan=2, pady=5)

        btn_kullanici_ekle = tk.Button(root, text="Kullanıcı Ekle", command=self.kullanici_ekle_ekrani_ac)
        btn_kullanici_ekle.grid(row=1, column=0, padx=5, pady=5)

        btn_kullanici_sil = tk.Button(root, text="Kullanıcı Sil", command=self.kullanici_sil_ekrani)
        btn_kullanici_sil.grid(row=1, column=1, padx=5, pady=5)

        btn_kullanici_listesi = tk.Button(root, text="Kayıtlı Kullanıcıları Göster", command=self.kullanici_listesi_goster)
        btn_kullanici_listesi.grid(row=2, column=0, columnspan=2, pady=5)

        btn_cikis = tk.Button(root, text="Çıkış", command=self.cikis)
        btn_cikis.grid(row=4, column=0, columnspan=2, pady=5)

    def kullanici_ekle_ekrani_ac(self):
        self.kullanici_ekle_penceresi = tk.Toplevel()
        self.kullanici_ekle_penceresi.title("Yeni Kullanıcı Ekle")
        self.kullanici_ekle_penceresi.geometry("300x200")

        label_kullanici_adi = tk.Label(self.kullanici_ekle_penceresi, text="Kullanıcı Adı:")
        label_kullanici_adi.grid(row=0, column=0, padx=5, pady=5)

        self.entry_kullanici_adi = tk.Entry(self.kullanici_ekle_penceresi)
        self.entry_kullanici_adi.grid(row=0, column=1, padx=5, pady=5)

        label_sifre = tk.Label(self.kullanici_ekle_penceresi, text="Şifre:")
        label_sifre.grid(row=1, column=0, padx=5, pady=5)

        self.entry_sifre = tk.Entry(self.kullanici_ekle_penceresi, show="*")
        self.entry_sifre.grid(row=1, column=1, padx=5, pady=5)

        label_kullanici_tipi = tk.Label(self.kullanici_ekle_penceresi, text="Kullanıcı Tipi:")
        label_kullanici_tipi.grid(row=2, column=0, padx=5, pady=5)

        self.secilen_kullanici_turu = tk.StringVar(value="Müşteri")
        tur_secim_menusu = tk.OptionMenu(self.kullanici_ekle_penceresi, self.secilen_kullanici_turu, "Müşteri", "Admin")
        tur_secim_menusu.grid(row=2, column=1, padx=5, pady=5)
        btn_kaydet = tk.Button(self.kullanici_ekle_penceresi, text="Kaydet", command=self.kullanici_ekle)
        btn_kaydet.grid(row=3, column=0, columnspan=2, pady=5)

    def kullanici_ekle(self):
        kullanici_adi = self.entry_kullanici_adi.get()
        sifre = self.entry_sifre.get()
        kullanici_tipi = self.secilen_kullanici_turu.get()
        if kullanici_adi and sifre and kullanici_tipi:
            self.bankamatik.yeni_kullanici_olustur(kullanici_adi, sifre, kullanici_tipi)
            messagebox.showinfo("Başarılı", "Yeni kullanıcı oluşturuldu.")
            self.kullanici_ekle_penceresi.destroy()
        else:
            messagebox.showerror("Hata", "Tüm alanları doldurunuz.")


    def kullanici_sil_ekrani(self):
        kullanici_sil_penceresi = tk.Toplevel()
        kullanici_sil_penceresi.title("Kullanıcı Sil")
        kullanici_sil_penceresi.geometry("300x150")

        label_kullanici_adi = tk.Label(kullanici_sil_penceresi, text="Silmek istediğiniz kullanıcı adını giriniz:")
        label_kullanici_adi.grid(row=0, column=0, padx=5, pady=5)

        entry_kullanici_adi = tk.Entry(kullanici_sil_penceresi)
        entry_kullanici_adi.grid(row=0, column=1, padx=5, pady=5)

        def kullanici_sil():
            kullanici_adi = entry_kullanici_adi.get()
            self.bankamatik.kullanici_sil(kullanici_adi)
            kullanici_sil_penceresi.destroy()

        btn_sil = tk.Button(kullanici_sil_penceresi, text="Sil", command=kullanici_sil)
        btn_sil.grid(row=1, column=0, columnspan=2, pady=5)
    
    def kullanici_listesi_goster(self):
        kullanici_listesi_penceresi = tk.Toplevel(self.root)
        kullanici_listesi_penceresi.title("Kayıtlı Kullanıcılar")
        kullanici_listesi_penceresi.geometry("400x300")

        label_baslik = tk.Label(kullanici_listesi_penceresi, text="Kayıtlı Kullanıcılar", font=("Helvetica", 14))
        label_baslik.pack(pady=10)

        listbox_kullanicilar = tk.Listbox(kullanici_listesi_penceresi, width=50, height=10)
        listbox_kullanicilar.pack(padx=20, pady=10)

        # CSV dosyasını okuma ve Listbox'a ekleme
        try:
            with open('kullanicilar.csv', newline='') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    listbox_kullanicilar.insert(tk.END, row[0])  # Sadece kullanıcı adını ekliyoruz
        except FileNotFoundError:
            messagebox.showerror("Hata", "CSV dosyası bulunamadı.")

            
    def cikis(self):
        self.bankamatik.giris_ekrani_ac()  # Yeni ekranı açar
        self.root.destroy()  # Admin panel penceresini kapatır