
import tkinter as tk
import random
from tkinter import messagebox
from Admin import AdminPaneli


class LoginScreen:
    def __init__(self, root, bankamatik):
        self.root = root
        self.bankamatik = bankamatik  # Doğru şekilde Bankamatik sınıfını oluşturun
        self.oturum_acan_kullanici = None
        self.bankamatik.kullanicilari_yukle()  # bankamatik nesnesini kullanırken self argümanına gerek yok
        self.root.title("Kullanıcı Girişi")
        self.root.geometry("300x300")
        
        self.frame = tk.Frame(root)
        self.frame.pack()
        
        self.label_kullanici_adi = tk.Label(root, text="Kullanıcı Adı:")
        self.label_kullanici_adi.pack()

        self.entry_kullanici_adi = tk.Entry(root)
        self.entry_kullanici_adi.pack()

        self.label_sifre = tk.Label(root, text="Şifre:")
        self.label_sifre.pack()

        self.entry_sifre = tk.Entry(root, show="*")
        self.entry_sifre.pack()

        self.btn_giris_yap = tk.Button(root, text="Giriş Yap", command=self.giris_yap)
        self.btn_giris_yap.pack()

        self.btn_kayit_ol = tk.Button(root, text="Kayıt Ol", command=self.kayit_ol_ekrani_ac)
        self.btn_kayit_ol.pack()

    def kayit_ol_ekrani_ac(self):
        self.kayit_ol_penceresi = tk.Toplevel()
        self.kayit_ol_penceresi.title("Yeni Kullanıcı Kaydı")
        self.kayit_ol_penceresi.geometry("300x200")

        label_kullanici_adi = tk.Label(self.kayit_ol_penceresi, text="Kullanıcı Adı:")
        label_kullanici_adi.pack()

        self.entry_kullanici_adi_kayit = tk.Entry(self.kayit_ol_penceresi)
        self.entry_kullanici_adi_kayit.pack()

        label_sifre = tk.Label(self.kayit_ol_penceresi, text="Şifre:")
        label_sifre.pack()

        self.entry_sifre_kayit = tk.Entry(self.kayit_ol_penceresi, show="*")
        self.entry_sifre_kayit.pack()

        label_kullanici_tipi = tk.Label(self.kayit_ol_penceresi, text="Kullanıcı Tipi:")
        label_kullanici_tipi.pack()

        self.secilen_kullanici_turu_kayit = tk.StringVar(value="Müşteri")
        tur_secim_menusu = tk.OptionMenu(self.kayit_ol_penceresi, self.secilen_kullanici_turu_kayit, "Müşteri", "Admin")
        tur_secim_menusu.pack()

        btn_kaydet = tk.Button(self.kayit_ol_penceresi, text="Kaydet", command=self.yeni_kullanici_olustur)
        btn_kaydet.pack()


    def yeni_kullanici_olustur(self):
        kullanici_adi = self.entry_kullanici_adi_kayit.get()
        sifre = self.entry_sifre_kayit.get()
        kullanici_tipi = self.secilen_kullanici_turu_kayit.get()
        
        kullanici = Kullanici(kullanici_adi, sifre, kullanici_tipi)
        self.bankamatik.kullanicilar.append(kullanici)
        self.bankamatik.kullanicilari_kaydet()
        
        messagebox.showinfo("Başarılı", f"{kullanici_adi} kullanıcısı başarıyla oluşturuldu.")
        self.kayit_ol_penceresi.destroy()
    
    def kullanici_bul_by_iban(self, iban):
        """
        Verilen IBAN numarasına göre kullanıcıyı bulur.
        """
        print(f"Aranan IBAN: {iban}")
        for kullanici in self.bankamatik.kullanicilar:
            print(f"Kullanıcı adı: {kullanici.kullanici_adi}, IBAN: {kullanici.iban}")
            if kullanici.iban == iban:
                print("Kullanıcı bulundu!")
                return kullanici
        print("Kullanıcı bulunamadı.")
        return None




    def giris_yap(self):
        # Kullanıcıları yükle
        self.bankamatik.kullanicilari_yukle()

        kullanici_adi = self.entry_kullanici_adi.get()
        sifre = self.entry_sifre.get()

        for kullanici in self.bankamatik.kullanicilar:
            if kullanici.kullanici_adi == kullanici_adi and kullanici.sifre == sifre:
                self.oturum_acan_kullanici = kullanici
                if self.oturum_acan_kullanici.kullanici_tipi == "Admin":
                    self.admin_paneli_ac()
                else:
                    self.menu_ekrani()
                return

        messagebox.showerror("Hata", "Geçersiz kullanıcı adı veya şifre!")


    def admin_paneli_ac(self):
        self.root.withdraw()
        admin_panel = tk.Toplevel()
        admin_panel.title("Admin Paneli")
        admin_panel.geometry("200x150")
        AdminPaneli(admin_panel, self.bankamatik)

    def menu_ekrani(self):
        self.root.withdraw()
        menu = tk.Toplevel()
        menu.title("Ana Menü")
        menu.geometry("300x300")

        label_welcome = tk.Label(menu, text=f"Hoş geldiniz, {self.oturum_acan_kullanici.kullanici_adi}!")
        label_welcome.pack()

        if self.oturum_acan_kullanici.kullanici_tipi == "Müşteri":
            btn_para_cek = tk.Button(menu, text="Para Çek", command=self.para_cek_ekrani)
            btn_para_cek.pack()

            btn_para_yatir = tk.Button(menu, text="Para Yatır", command=self.para_yatir_ekrani)
            btn_para_yatir.pack()

            btn_kredi_basvuru = tk.Button(menu, text="Kredi Başvuru", command=self.kredi_basvuru_ekrani)
            btn_kredi_basvuru.pack()

            # "Hesap Bilgileri" butonunu ekle
            btn_hesap_bilgileri = tk.Button(menu, text="Hesap Bilgileri", command=self.hesap_bilgileri_ekrani)
            btn_hesap_bilgileri.pack()

            # "Para Transferi" butonunu ekle
            btn_para_transferi = tk.Button(menu, text="Para Transferi", command=self.para_transferi_menu)
            btn_para_transferi.pack()

            btn_cikis = tk.Button(menu, text="Çıkış", command=self.root.destroy)
            btn_cikis.pack()

            menu.mainloop()
    

    def hesap_bilgileri_ekrani(self):
        # Yeni pencere oluştur
        hesap_bilgileri_penceresi = tk.Toplevel()
        hesap_bilgileri_penceresi.title("Hesap Bilgileri")
        hesap_bilgileri_penceresi.geometry("300x200")

        # Kullanıcı bilgilerini gösteren etiketler
        label_kullanici_adi = tk.Label(hesap_bilgileri_penceresi, text=f"Kullanıcı Adı: {self.oturum_acan_kullanici.kullanici_adi}")
        label_kullanici_adi.pack()

        label_kullanici_tipi = tk.Label(hesap_bilgileri_penceresi, text=f"Kullanıcı Tipi: {self.oturum_acan_kullanici.kullanici_tipi}")
        label_kullanici_tipi.pack()

        label_bakiye = tk.Label(hesap_bilgileri_penceresi, text=f"Bakiye: {self.oturum_acan_kullanici.bakiye} TL")
        label_bakiye.pack()

        label_iban = tk.Label(hesap_bilgileri_penceresi, text=f"IBAN: {self.oturum_acan_kullanici.iban}")
        label_iban.pack()

        # Yeni pencereyi göster
        hesap_bilgileri_penceresi.mainloop()

        # Ana menü ekranına "Hesap Bilgileri" butonunu ekleme
        btn_hesap_bilgileri = tk.Button(menu, text="Hesap Bilgileri", command=self.hesap_bilgileri_ekrani)
        btn_hesap_bilgileri.pack()



    def para_cek_ekrani(self):
        para_cek_penceresi = tk.Toplevel()
        para_cek_penceresi.title("Para Çek")
        para_cek_penceresi.geometry("300x150")

        label_miktar = tk.Label(para_cek_penceresi, text="Çekmek istediğiniz miktarı giriniz:")
        label_miktar.pack()

        entry_miktar = tk.Entry(para_cek_penceresi)
        entry_miktar.pack()

        def para_cek():
            miktar = float(entry_miktar.get())
            
            if miktar <= 0:
                messagebox.showerror("Hata", "Geçersiz miktar. Lütfen pozitif bir miktar girin.")
                return
            
            if miktar > self.oturum_acan_kullanici.bakiye:
                messagebox.showerror("Hata", "Yetersiz bakiye. İstenilen miktarı çekecek kadar bakiyeniz yok.")
                return
            
            self.oturum_acan_kullanici.bakiye -= miktar
            self.bankamatik.kullanicilari_kaydet()
            messagebox.showinfo("Başarılı", f"{miktar} TL çekildi.")
            para_cek_penceresi.destroy()

        btn_onayla = tk.Button(para_cek_penceresi, text="Onayla", command=para_cek)
        btn_onayla.pack()


    def para_yatir_ekrani(self):
        para_yatir_penceresi = tk.Toplevel()
        para_yatir_penceresi.title("Para Yatır")
        para_yatir_penceresi.geometry("300x150")

        label_miktar = tk.Label(para_yatir_penceresi, text="Yatırmak istediğiniz miktarı giriniz:")
        label_miktar.pack()

        entry_miktar = tk.Entry(para_yatir_penceresi)
        entry_miktar.pack()

        def para_yatir():
            miktar_str = entry_miktar.get()

            # Miktarın pozitif bir float değer olup olmadığını kontrol et
            try:
                miktar = float(miktar_str)
                if miktar <= 0:
                    raise ValueError("Geçersiz miktar. Lütfen pozitif bir miktar girin.")
            except ValueError as e:
                messagebox.showerror("Hata", str(e))
                return

            # Miktarı kullanıcının bakiyesine ekle
            self.oturum_acan_kullanici.bakiye += miktar
            self.bankamatik.kullanicilari_kaydet()
            messagebox.showinfo("Başarılı", f"{miktar} TL yatırıldı.")

            para_yatir_penceresi.destroy()

        btn_onayla = tk.Button(para_yatir_penceresi, text="Onayla", command=para_yatir)
        btn_onayla.pack()

    
    def para_transferi_menu(self):
        para_transferi_penceresi = tk.Toplevel()
        para_transferi_penceresi.title("Para Transferi")
        para_transferi_penceresi.geometry("300x200")

        label_alici_iban = tk.Label(para_transferi_penceresi, text="Alıcı IBAN:")
        label_alici_iban.pack()

        entry_alici_iban = tk.Entry(para_transferi_penceresi)
        entry_alici_iban.pack()

        label_miktar = tk.Label(para_transferi_penceresi, text="Transfer Miktarı:")
        label_miktar.pack()

        entry_miktar = tk.Entry(para_transferi_penceresi)
        entry_miktar.pack()

        def transfer_et():
            alici_iban = entry_alici_iban.get()
            miktar_str = entry_miktar.get()

            # Miktarın pozitif bir float değer olup olmadığını kontrol et
            try:
                miktar = float(miktar_str)
                if miktar <= 0:
                    raise ValueError("Geçersiz miktar. Lütfen pozitif bir miktar girin.")
            except ValueError as e:
                messagebox.showerror("Hata", str(e))
                return

            alici_kullanici = self.kullanici_bul_by_iban(alici_iban)

            if alici_kullanici:
                if self.oturum_acan_kullanici.bakiye >= miktar:
                    self.oturum_acan_kullanici.bakiye -= miktar
                    alici_kullanici.bakiye += miktar
                    self.bankamatik.kullanicilari_kaydet()  # Kullanıcıları kaydetme işlevi
                    messagebox.showinfo("Başarılı", f"{miktar} TL başarıyla transfer edildi.")
                    para_transferi_penceresi.destroy()
                else:
                    messagebox.showerror("Hata", "Yetersiz bakiye.")
            else:
                messagebox.showerror("Hata", "Alıcı kullanıcı bulunamadı.")

        btn_onayla = tk.Button(para_transferi_penceresi, text="Onayla", command=transfer_et)
        btn_onayla.pack()


    def kredi_basvuru_ekrani(self):
        def kredi_secimi_degisti(selected_kredi):
            if isinstance(selected_kredi, str):  # Eğer selected_kredi bir dize ise
                kredi_secildi(selected_kredi)    # Fonksiyonu çağırarak devam et
            else:
                kredi_secildi(selected_kredi.get())  # Değilse, .get() metodunu kullanarak gerçek değeri al


        def kredi_secildi(kredi_ad):
            kredi = next((x for x in self.bankamatik.krediler if x.ad == kredi_ad), None)
            if kredi:
                kredi_bilgileri_penceresi = tk.Toplevel()
                kredi_bilgileri_penceresi.title("Kredi Bilgileri")
                kredi_bilgileri_penceresi.geometry("250x200")

                label_kredi_bilgileri = tk.Label(kredi_bilgileri_penceresi, text=f"Seçilen Kredi: {kredi.ad}\n"
                                                                                f"Maksimum Kredi Miktarı: {kredi.max_kredi_miktari} TL\n"
                                                                                f"Minimum Kredi Miktarı: {kredi.min_kredi_miktari} TL\n"
                                                                                f"Faiz Oranı: %{kredi.faiz_orani*100}\n"
                                                                                f"Maksimum Taksit Sayısı: {kredi.max_taksit}\n"
                                                                                f"Minimum Taksit Sayısı: {kredi.min_taksit}")
                label_kredi_bilgileri.pack()


        def toplam_odenecek_miktar_hesapla():
            miktar_str = entry_miktar.get()
            if miktar_str:
                miktar = float(miktar_str)
                kredi_ad = selected_kredi.get()
                kredi = next((x for x in self.bankamatik.krediler if x.ad == kredi_ad), None)
                if kredi:
                    vade = float(entry_vade.get())
                    faiz_miktari = miktar * kredi.faiz_orani * vade / 12
                    toplam_miktar = miktar + faiz_miktari
                    return toplam_miktar
            return None

        def guncelle_toplam_miktar(event=None):
            miktar_str = entry_miktar.get()
            if miktar_str:
                miktar = float(miktar_str)
                kredi_ad = selected_kredi.get()
                kredi = next((x for x in self.bankamatik.krediler if x.ad == kredi_ad), None)
                if kredi:
                    faiz_miktari = miktar * kredi.faiz_orani
                    toplam_miktar = miktar + faiz_miktari
                    label_toplam_miktar.config(text=f"Toplam Ödeme: {toplam_miktar:.2f} TL")
            else:
                label_toplam_miktar.config(text="")

        kredi_basvuru_penceresi = tk.Toplevel()
        kredi_basvuru_penceresi.title("Kredi Başvuru")
        kredi_basvuru_penceresi.geometry("350x350")

        label_kredi_secimi = tk.Label(kredi_basvuru_penceresi, text="Başvurmak istediğiniz krediyi seçiniz:")
        label_kredi_secimi.pack()

        # Kredileri listeleme
        kredi_secenekleri = [kredi.ad for kredi in self.bankamatik.krediler]
        selected_kredi = tk.StringVar(value=kredi_secenekleri[0])
        kredi_secim_menusu = tk.OptionMenu(kredi_basvuru_penceresi, selected_kredi, *kredi_secenekleri, command=kredi_secimi_degisti)
        kredi_secim_menusu.pack()

        # Minimum ve maksimum miktarı ile faizi gösterme
        label_miktar_faiz = tk.Label(kredi_basvuru_penceresi, text="")
        label_miktar_faiz.pack()

        label_miktar = tk.Label(kredi_basvuru_penceresi, text="Başvurmak istediğiniz miktarı giriniz:")
        label_miktar.pack()

        entry_miktar = tk.Entry(kredi_basvuru_penceresi)
        entry_miktar.pack()

        label_vade = tk.Label(kredi_basvuru_penceresi, text="Vade (ay cinsinden) giriniz:")
        label_vade.pack()

        entry_vade = tk.Entry(kredi_basvuru_penceresi)
        entry_vade.pack()

        label_toplam_miktar = tk.Label(kredi_basvuru_penceresi, text="")
        label_toplam_miktar.pack()

        # Kredi seçimi değiştiğinde bu fonksiyon çağrılacak
        kredi_secim_menusu.bind("<<MenuSelect>>", lambda event: kredi_secildi(selected_kredi.get()))

        # Entry'lerden biri odak dışında olduğunda toplam miktarı güncelle
        entry_miktar.bind("<FocusOut>", guncelle_toplam_miktar)
        entry_vade.bind("<FocusOut>", guncelle_toplam_miktar)

        # Başlangıçta toplam miktarı hesapla ve göster
        toplam_miktar = toplam_odenecek_miktar_hesapla()
        if toplam_miktar:
            label_toplam_miktar.config(text=f"Toplam Ödeme: {toplam_miktar:.2f} TL")


        # Entry'lerin olay dinleyicilerini tanımlamak için kredi seçimini beklemeye gerek yoktur.
        kredi_secildi(None)

class Kullanici:
    def __init__(self, kullanici_adi, sifre, kullanici_tipi, iban=None, bakiye=0.0):
        self.kullanici_adi = kullanici_adi
        self.sifre = sifre
        self.kullanici_tipi = kullanici_tipi
        self.bakiye = bakiye

        if iban:
            self.iban = iban
        elif kullanici_tipi == "Müşteri":
            self.iban = self.generate_random_iban()
        else:
            self.iban = None

    @staticmethod 
    def generate_random_iban():
        iban = "TR"
        for _ in range(22):
            iban += str(random.randint(0, 9))
        return iban