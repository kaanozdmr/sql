import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

class Gemi:
    def __init__(self, seri_no, ad, agirlik, yapim_yili):
        self.seri_no = seri_no
        self.ad = ad
        self.agirlik = agirlik
        self.yapim_yili = yapim_yili

class Sefer:
    def __init__(self, sefer_id, yolcu_gemi, kaptanlar, murettebat, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani):
        self.sefer_id = sefer_id
        self.yolcu_gemi = yolcu_gemi
        self.kaptanlar = kaptanlar
        self.murettebat = murettebat
        self.yola_cikis_tarihi = yola_cikis_tarihi
        self.donus_tarihi = donus_tarihi
        self.yola_cikis_limani = yola_cikis_limani

class Liman:
    def __init__(self, liman_adi, ulke, nufus, pasaport_gerekli, demirleme_ucreti):
        self.liman_adi = liman_adi
        self.ulke = ulke
        self.nufus = nufus
        self.pasaport_gerekli = pasaport_gerekli
        self.demirleme_ucreti = demirleme_ucreti

class Kaptan:
    def __init__(self, kaptan_id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans):
        self.kaptan_id = kaptan_id
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.vatandaslik = vatandaslik
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi
        self.lisans = lisans

class Murettebat:
    def __init__(self, murettebat_id, ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev):
        self.murettebat_id = murettebat_id
        self.ad = ad
        self.soyad = soyad
        self.adres = adres
        self.vatandaslik = vatandaslik
        self.dogum_tarihi = dogum_tarihi
        self.ise_giris_tarihi = ise_giris_tarihi
        self.gorev = gorev
        
# Veritabanı bağlantısını oluştur
def Baglanti_olustur():
    Baglanti = sqlite3.connect("gezgin_gemi5.db")
    return Baglanti


# Gerekli tabloları oluştur
def tablo_olustur(Baglanti):
    with Baglanti:
        # Gemiler tablosunu oluştur
        Baglanti.execute("""
            CREATE TABLE IF NOT EXISTS Gemiler (
                seri_no TEXT PRIMARY KEY,
                ad TEXT,
                agirlik REAL,
                yapim_yili INTEGER,
                gemi_turu TEXT
            )
        """)

        # Kaptanlar tablosunu oluştur
        Baglanti.execute("""
            CREATE TABLE IF NOT EXISTS Kaptanlar (
                kaptan_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT,
                soyad TEXT,
                adres TEXT,
                vatandaslik TEXT,
                dogum_tarihi DATE,
                ise_giris_tarihi DATE,
                lisans TEXT
            )
        """)

        # Mürettebat tablosunu oluştur
        Baglanti.execute("""
            CREATE TABLE IF NOT EXISTS Murettebat (
                murettebat_id INTEGER PRIMARY KEY AUTOINCREMENT,
                ad TEXT,
                soyad TEXT,
                adres TEXT,
                vatandaslik TEXT,
                dogum_tarihi DATE,
                ise_giris_tarihi DATE,
                gorev TEXT
            )
        """)
        # limalar tablosu
        Baglanti.execute("""
            CREATE TABLE IF NOT EXISTS Limanlar (
                liman_adi TEXT,
                ulke TEXT,
                nufus INTEGER,
                pasaport_gerekli BOOLEAN,
                demirleme_ucreti REAL,
                PRIMARY KEY(liman_adi, ulke)
            )
        """)
        # Seferler tablosu
        Baglanti.execute("""
            CREATE TABLE IF NOT EXISTS Seferler (
                sefer_id INTEGER PRIMARY KEY,
                yolcu_gemi TEXT,
                yola_cikis_tarihi DATE,
                donus_tarihi DATE,
                yola_cikis_limani TEXT,
                FOREIGN KEY(yolcu_gemi) REFERENCES Gemiler(seri_no)
            )
        """)


# Ana uygulama ve menü
class AnaUygulama(tk.Frame):
    def __init__(self, master, Baglanti):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.menu_olustur()  # Menü çubuğunu oluştur
        self.sekme_olustur()

    def menu_olustur(self):
        menu_bar = tk.Menu(self.master)

        # Gemi menüsü
        gemi_menu = tk.Menu(menu_bar, tearoff=0)
        gemi_menu.add_command(label="Yeni Gemi", command=self.goster_gemi_form)  # Yeni gemi eklemek için
        gemi_menu.add_command(label="Sil", command=self.sil_gemi)  # Seçilen gemiyi silmek için
        gemi_menu.add_command(label="Düzenle", command=self.duzenle_gemi)  # Seçilen gemiyi düzenlemek için
        gemi_menu.add_command(label="Görüntüle", command=self.goster_gemiler)  # Tüm gemileri görüntülemek için
        menu_bar.add_cascade(label="Gemiler", menu=gemi_menu)  # Menü çubuğuna gemi menüsünü ekler

        # Kaptan menüsü
        kaptan_menu = tk.Menu(menu_bar, tearoff=0)
        kaptan_menu.add_command(label="Yeni Kaptan", command=self.goster_kaptan_form)
        kaptan_menu.add_command(label="Sil", command=self.sil_kaptan)
        kaptan_menu.add_command(label="Düzenle", command=self.duzenle_kaptan)
        kaptan_menu.add_command(label="Görüntüle", command=self.goster_kaptanlar)
        menu_bar.add_cascade(label="Kaptanlar", menu=kaptan_menu)

        # Mürettebat menüsü
        murettebat_menu = tk.Menu(menu_bar, tearoff=0)
        murettebat_menu.add_command(label="Yeni Mürettebat", command=self.goster_murettebat_form)
        murettebat_menu.add_command(label="Sil", command=self.sil_murettebat)
        murettebat_menu.add_command(label="Görüntüle", command=self.goster_murettebatlar)
        murettebat_menu.add_command(label="Düzenle", command=self.duzenle_murettebat)
        menu_bar.add_cascade(label="Mürettebat", menu=murettebat_menu)
        # Limanlar menüsü
        liman_menu = tk.Menu(menu_bar, tearoff=0)
        liman_menu.add_command(label="Yeni Liman", command=self.goster_liman_form)
        liman_menu.add_command(label="Sil", command=self.sil_liman)
        liman_menu.add_command(label="Görüntüle", command=self.goster_limanlar)
        liman_menu.add_command(label="Düzenle", command=self.duzenle_liman)
        menu_bar.add_cascade(label="Limanlar", menu=liman_menu)
        # Seferler menüsü
        sefer_menu = tk.Menu(menu_bar, tearoff=0)
        sefer_menu.add_command(label="Yeni Sefer", command=self.goster_sefer_form)
        sefer_menu.add_command(label="Sil", command=self.sil_sefer)
        sefer_menu.add_command(label="Düzenle", command=self.duzenle_sefer)
        sefer_menu.add_command(label="Görüntüle", command=self.goster_seferler)
        menu_bar.add_cascade(label="Seferler", menu=sefer_menu)
        self.master.config(menu=menu_bar)

    def sekme_olustur(self):
        self.Tablo_goruntusu = ttk.Treeview(self)
        self.Tablo_goruntusu.pack(padx=10, pady=10)

    def goster_gemiler(self):
        self.Tablo_goruntusu.configure(columns=("seri_no", "ad", "agirlik", "yapim_yili", "gemi_turu"), show="headings")
        self.Tablo_goruntusu.heading("seri_no", text="Seri No")
        self.Tablo_goruntusu.heading("ad", text="Ad")
        self.Tablo_goruntusu.heading("agirlik", text="Ağırlık")
        self.Tablo_goruntusu.heading("yapim_yili", text="Yapım Yılı")
        self.Tablo_goruntusu.heading("gemi_turu", text="Gemi Türü")

        self.yukle_gemiler()

    def goster_kaptanlar(self):
        self.Tablo_goruntusu.configure(
            columns=("kaptan_id", "ad", "soyad", "adres", "vatandaslik", "dogum_tarihi", "ise_giris_tarihi", "lisans"),
            show="headings")
        self.Tablo_goruntusu.heading("kaptan_id", text="Kaptan ıd")
        self.Tablo_goruntusu.heading("ad", text="Ad")
        self.Tablo_goruntusu.heading("soyad", text="Soyad")
        self.Tablo_goruntusu.heading("adres", text="Adres")
        self.Tablo_goruntusu.heading("vatandaslik", text="Vatandaşlık")
        self.Tablo_goruntusu.heading("dogum_tarihi", text="Doğum Tarihi")
        self.Tablo_goruntusu.heading("ise_giris_tarihi", text="İşe Giriş Tarihi")
        self.Tablo_goruntusu.heading("lisans", text="Lisans")

        self.yukle_kaptanlar()

    def goster_murettebatlar(self):
        self.Tablo_goruntusu.configure(columns=(
        "murettebat_id", "ad", "soyad", "adres", "vatandaslik", "dogum_tarihi", "ise_giris_tarihi", "gorev"),
                                       show="headings")
        self.Tablo_goruntusu.heading("murettebat_id", text="Mürettebat ıd")
        self.Tablo_goruntusu.heading("ad", text="Ad")
        self.Tablo_goruntusu.heading("soyad", text="Soyad")
        self.Tablo_goruntusu.heading("adres", text="Adres")
        self.Tablo_goruntusu.heading("vatandaslik", text="Vatandaşlık")
        self.Tablo_goruntusu.heading("dogum_tarihi", text="Doğum Tarihi")
        self.Tablo_goruntusu.heading("ise_giris_tarihi", text="İşe Giriş Tarihi")
        self.Tablo_goruntusu.heading("gorev", text="Görev")

        self.yukle_murettebatlar()

    def goster_limanlar(self):
        self.Tablo_goruntusu.configure(columns=("liman_adi", "ulke", "nufus", "pasaport_gerekli", "demirleme_ucreti"),
                                       show="headings")
        self.Tablo_goruntusu.heading("liman_adi", text="Liman Adı")
        self.Tablo_goruntusu.heading("ulke", text="Ülke")
        self.Tablo_goruntusu.heading("nufus", text="Nüfus")
        self.Tablo_goruntusu.heading("pasaport_gerekli", text="Pasaport Gerekli")
        self.Tablo_goruntusu.heading("demirleme_ucreti", text="Demirleme Ücreti")

        self.yukle_limanlar()

    def goster_seferler(self):
        self.Tablo_goruntusu.configure(
            columns=("sefer_id", "yolcu_gemi", "yola_cikis_tarihi", "donus_tarihi", "yola_cikis_limani"),
            show="headings")
        self.Tablo_goruntusu.heading("sefer_id", text="Sefer ıd")
        self.Tablo_goruntusu.heading("yolcu_gemi", text="Yolcu Gemisi")
        self.Tablo_goruntusu.heading("yola_cikis_tarihi", text="Yola Çıkış Tarihi")
        self.Tablo_goruntusu.heading("donus_tarihi", text="Dönüş Tarihi")
        self.Tablo_goruntusu.heading("yola_cikis_limani", text="Yola Çıkış Limanı")

        self.yukle_seferler()

    def goster_gemi_form(self):
        gemi_form = GemiForm(self.master, self.Baglanti, self)
        gemi_form.pack(padx=20, pady=20)

    def goster_kaptan_form(self):
        kaptan_form = KaptanForm(self.master, self.Baglanti, self)
        kaptan_form.pack(padx=20, pady=20)

    def goster_murettebat_form(self):
        murettebat_form = MurettebatForm(self.master, self.Baglanti, self)
        murettebat_form.pack(padx=20, pady=20)

    def goster_liman_form(self):
        liman_form = LimanForm(self.master, self.Baglanti, self)
        liman_form.pack(padx=20, pady=20)

    def goster_sefer_form(self):
        sefer_form = SeferForm(self.master, self.Baglanti, self)
        sefer_form.pack(padx=20, pady=20)

    def yukle_gemiler(self):
        self.Tablo_goruntusu.delete(*self.Tablo_goruntusu.get_children())
        cursor = self.Baglanti.execute("SELECT * FROM Gemiler")
        for row in cursor:
            self.Tablo_goruntusu.insert("", "end", values=row)

    def yukle_kaptanlar(self):
        self.Tablo_goruntusu.delete(*self.Tablo_goruntusu.get_children())
        cursor = self.Baglanti.execute("SELECT * FROM Kaptanlar")
        for row in cursor:
            self.Tablo_goruntusu.insert("", "end", values=row)

    def yukle_murettebatlar(self):
        self.Tablo_goruntusu.delete(*self.Tablo_goruntusu.get_children())
        cursor = self.Baglanti.execute("SELECT * FROM Murettebat")
        for row in cursor:
            self.Tablo_goruntusu.insert("", "end", values=row)

    def yukle_limanlar(self):
        self.Tablo_goruntusu.delete(*self.Tablo_goruntusu.get_children())
        cursor = self.Baglanti.execute("SELECT * FROM Limanlar")
        for row in cursor:
            self.Tablo_goruntusu.insert("", "end", values=row)

    def yukle_seferler(self):
        self.Tablo_goruntusu.delete(*self.Tablo_goruntusu.get_children())
        cursor = self.Baglanti.execute("SELECT * FROM Seferler")
        for row in cursor:
            self.Tablo_goruntusu.insert("", "end", values=row)

    def duzenle_gemi(self):
        try:
            item = self.Tablo_goruntusu.selection()[0]  # Seçilen gemiyi al
            gemi_values = self.Tablo_goruntusu.item(item, "values")
            gemi_duzenle = GemiDuzenleForm(self.master, self.Baglanti, gemi_values, self)  # Gemi düzenleme formunu aç
            gemi_duzenle.pack(padx=20, pady=20)
        except IndexError:
            messagebox.showerror("Hata", "Düzenlemek için bir gemi seçin.")

    def duzenle_kaptan(self):
        try:
            item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            kaptan_values = self.Tablo_goruntusu.item(item, "values")
            kaptan_duzenle = KaptanDuzenleForm(self.master, self.Baglanti, kaptan_values,
                                               self)  # Kaptan düzenleme formunu aç
            kaptan_duzenle.pack(padx=20, pady=20)
        except IndexError:
            messagebox.showerror("Hata", "Düzenlemek için bir kaptan seçin.")

    def duzenle_murettebat(self):
        try:
            item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            murettebat_values = self.Tablo_goruntusu.item(item, "values")
            murettebat_duzenle = MurettebatDuzenleForm(self.master, self.Baglanti, murettebat_values,
                                                       self)  # Mürettebat düzenleme formunu aç
            murettebat_duzenle.pack(padx=20, pady=20)
        except IndexError:
            messagebox.showerror("Hata", "Düzenlemek için bir mürettebat seçin.")

    def duzenle_liman(self):
        try:
            item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            liman_values = self.Tablo_goruntusu.item(item, "values")
            liman_duzenle = LimanDuzenleForm(self.master, self.Baglanti, liman_values,
                                             self)  # Liman düzenleme formunu aç
            liman_duzenle.pack(padx=20, pady=20)
        except IndexError:
            messagebox.showerror("Hata", "Düzenlemek için bir liman seçin.")

    def duzenle_sefer(self):
        try:
            item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            sefer_values = self.Tablo_goruntusu.item(item, "values")
            sefer_duzenle = SeferDuzenleForm(self.master, self.Baglanti, sefer_values,
                                             self)  # Sefer düzenleme formunu aç
            sefer_duzenle.pack(padx=20, pady=20)
        except IndexError:
            messagebox.showerror("Hata", "Düzenlemek için bir sefer seçin.")

    def goster_gemi_form(self):
        gemi_form = GemiForm(self.master, self.Baglanti, self)  # Yeni gemi ekleme formu
        gemi_form.pack(padx=20, pady=20)

    def goster_kaptan_form(self):
        kaptan_form = KaptanForm(self.master, self.Baglanti, self)  # Yeni kaptan ekleme formu
        kaptan_form.pack(padx=20, pady=20)

    def goster_murettebat_form(self):
        murettebat_form = MurettebatForm(self.master, self.Baglanti, self)  # Yeni mürettebat ekleme formu
        murettebat_form.pack(padx=20, pady=20)

    def goster_liman_form(self):
        liman_form = LimanForm(self.master, self.Baglanti, self)  # Yeni liman ekleme formu
        liman_form.pack(padx=20, pady=20)  # Formu yerleştir

    def goster_sefer_form(self):
        sefer_form = SeferForm(self.master, self.Baglanti, self)  # Yeni sefer ekleme formu
        sefer_form.pack(padx=20, pady=20)

    def sil_gemi(self):
        try:
            selected_item = self.Tablo_goruntusu.selection()[0]  # Seçilen gemiyi al
            gemi_values = self.Tablo_goruntusu.item(selected_item, "values")
            seri_no = gemi_values[0]

            with self.Baglanti:
                self.Baglanti.execute("DELETE FROM Gemiler WHERE seri_no = ?", (seri_no,))  # Gemi kaydını sil
                self.yukle_gemiler()  # Güncellenmiş gemi listesini yükle

            messagebox.showinfo("Başarılı", "Gemi başarıyla silindi.")  # Başarı mesajı
        except IndexError:
            messagebox.showerror("Hata", "Silmek için bir gemi seçin.")

    def sil_kaptan(self):
        try:
            selected_item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            kaptan_values = self.Tablo_goruntusu.item(selected_item, "values")
            kaptan_id = kaptan_values[0]

            with self.Baglanti:
                self.Baglanti.execute("DELETE FROM Kaptanlar WHERE kaptan_id = ?", (kaptan_id,))  # Kaptanı sil
                self.yukle_kaptanlar()  # Kaptanları yeniden yükle

            messagebox.showinfo("Başarılı", "Kaptan başarıyla silindi.")  # Başarı mesajı
        except IndexError:
            messagebox.showerror("Hata", "Silmek için bir kaptan seçin.")

    def sil_murettebat(self):
        try:
            selected_item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            murettebat_values = self.Tablo_goruntusu.item(selected_item, "values")
            murettebat_id = murettebat_values[0]

            with self.Baglanti:
                self.Baglanti.execute("DELETE FROM Murettebat WHERE murettebat_id = ?", (murettebat_id,))
                self.yukle_murettebatlar()  # Güncellenmiş mürettebat listesini yükle

            messagebox.showinfo("Başarılı", "Mürettebat başarıyla silindi.")  # Başarı mesajı
        except IndexError:
            messagebox.showerror("Hata", "Silmek için bir mürettebat seçin.")

    def sil_liman(self):
        try:
            selected_item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            liman_values = self.Tablo_goruntusu.item(selected_item, "values")
            liman_adi = liman_values[0]
            ulke = liman_values[1]

            with self.Baglanti:
                self.Baglanti.execute("DELETE FROM Limanlar WHERE liman_adi = ? AND ulke = ?", (liman_adi, ulke))
                self.yukle_limanlar()  # Limanları yeniden yükle

            messagebox.showinfo("Başarılı", "Liman başarıyla silindi.")  # Başarı mesajı
        except IndexError:
            messagebox.showerror("Hata", "Silmek için bir liman seçin.")

    def sil_sefer(self):
        try:
            selected_item = self.Tablo_goruntusu.selection()[0]  # Seçilen öğeyi al
            sefer_values = self.Tablo_goruntusu.item(selected_item, "values")
            sefer_id = sefer_values[0]  # Sefer ıd sini al

            with self.Baglanti:
                self.Baglanti.execute("DELETE FROM Seferler WHERE sefer_id = ?", (sefer_id,))
                self.yukle_seferler()  # Seferleri yeniden yükle

            messagebox.showinfo("Başarılı", "Sefer başarıyla silindi.")  # Başarı mesajı
        except IndexError:
            messagebox.showerror("Hata", "Silmek için bir sefer seçin.")


class GemiForm(tk.Frame):
    def __init__(self, master, Baglanti, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_seri_no = tk.Label(self, text="Seri No:")
        self.entry_seri_no = tk.Entry(self)
        self.lbl_seri_no.grid(row=0, column=0)
        self.entry_seri_no.grid(row=0, column=1)

        self.lbl_ad = tk.Label(self, text="Ad:")
        self.entry_ad = tk.Entry(self)
        self.lbl_ad.grid(row=1, column=0)
        self.entry_ad.grid(row=1, column=1)

        self.lbl_agirlik = tk.Label(self, text="Ağırlık:")
        self.entry_agirlik = tk.Entry(self)
        self.lbl_agirlik.grid(row=2, column=0)
        self.entry_agirlik.grid(row=2, column=1)

        self.lbl_yapim_yili = tk.Label(self, text="Yapım Yılı:")
        self.entry_yapim_yili = ttk.Entry(self)
        self.lbl_yapim_yili.grid(row=3, column=0)
        self.entry_yapim_yili.grid(row=3, column=1)

        self.lbl_gemi_turu = tk.Label(self, text="Gemi Türü:")
        self.gemi_turu_var = ttk.Combobox(self, values=["Yolcu Gemisi", "Petrol Tankeri", "Konteyner Gemisi"])
        self.gemi_turu_var.grid(row=4, column=0)
        self.lbl_gemi_turu.grid(row=4, column=1)

        self.btn_ekle = ttk.Button(self, text="Ekle", command=self.ekle_gemi)
        self.btn_ekle.grid(row=5, column=1)

    def ekle_gemi(self):
        seri_no = self.entry_seri_no.get().strip()
        ad = self.entry_ad.get().strip()
        agirlik = float(self.entry_agirlik.get().strip())
        yapim_yili = int(self.entry_yapim_yili.get().strip())
        gemi_turu = self.gemi_turu_var.get().strip()

        if not (seri_no and ad and gemi_turu):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    INSERT INTO Gemiler (seri_no, ad, agirlik, yapim_yili, gemi_turu)
                    VALUES (?, ?, ?, ?, ?)
                """, (seri_no, ad, agirlik, yapim_yili, gemi_turu))

            messagebox.showinfo("Başarılı", "Gemi başarıyla eklendi.")

            self.ana_uygulama.yukle_gemiler()
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


class GemiDuzenleForm(tk.Frame):
    def __init__(self, master, Baglanti, gemi_values, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.gemi_values = gemi_values
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_seri_no = tk.Label(self, text="Seri No:")
        self.entry_seri_no = tk.Entry(self)
        self.entry_seri_no.insert(0, self.gemi_values[0])
        self.entry_seri_no.config(state='readonly')  # Seri no değiştirilemez
        self.lbl_seri_no.grid(row=0, column=0)
        self.entry_seri_no.grid(row=0, column=1)

        self.lbl_ad = tk.Label(self, text="Gemi Adı:")
        self.entry_ad = tk.Entry(self)
        self.entry_ad.insert(0, self.gemi_values[1])
        self.lbl_ad.grid(row=1, column=0)
        self.entry_ad.grid(row=1, column=1)

        self.lbl_agirlik = tk.Label(self, text="Ağırlık:")
        self.entry_agirlik = tk.Entry(self)
        self.entry_agirlik.insert(0, self.gemi_values[2])
        self.lbl_agirlik.grid(row=2, column=0)
        self.entry_agirlik.grid(row=2, column=1)

        self.lbl_yapim_yili = tk.Label(self, text="Yapım Yılı:")
        self.entry_yapim_yili = tk.Entry(self)
        self.entry_yapim_yili.insert(0, self.gemi_values[3])
        self.lbl_yapim_yili.grid(row=3, column=0)
        self.entry_yapim_yili.grid(row=3, column=1)

        self.lbl_gemi_turu = tk.Label(self, text="Gemi Türü:")
        self.gemi_turu_var = tk.StringVar()
        self.combobox_gemi_turu = ttk.Combobox(self, textvariable=self.gemi_turu_var,
                                               values=["Yolcu Gemisi", "Petrol Tankeri", "Konteyner Gemisi"])
        self.combobox_gemi_turu.set(self.gemi_values[4])
        self.lbl_gemi_turu.grid(row=4, column=0)
        self.combobox_gemi_turu.grid(row=4, column=1)

        self.btn_guncelle = tk.Button(self, text="Güncelle", command=self.guncelle_gemi)
        self.btn_guncelle.grid(row=5, column=1)

    def guncelle_gemi(self):
        seri_no = self.entry_seri_no.get().strip()
        ad = self.entry_ad.get().strip()
        agirlik = self.entry_agirlik.get().strip()
        yapim_yili = self.entry_yapim_yili.get().strip()
        gemi_turu = self.gemi_turu_var.get().strip()

        # Girdi doğrulama
        try:
            agirlik = float(agirlik)
            yapim_yili = int(yapim_yili)
        except ValueError:
            messagebox.showerror("Hata", "Ağırlık ve yapım yılı sayısal olmalıdır.")
            return

        if not (ad and gemi_turu):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")  # Alanların dolu olmasına dikkat
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    UPDATE Gemiler
                    SET ad = ?, agirlik = ?, yapim_yili = ?, gemi_turu = ?
                    WHERE seri_no = ?
                """, (ad, agirlik, yapim_yili, gemi_turu, seri_no))  # Gemi bilgilerini güncelle

            messagebox.showinfo("Başarılı", "Gemi başarıyla güncellendi.")  # Başarı mesajı

            # AnaUygulama daki gemileri yeniden yükle
            self.ana_uygulama.yukle_gemiler()  # Gemileri yeniden yükle
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


class KaptanForm(tk.Frame):
    def __init__(self, master, Baglanti, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        # Ad ve Soyad
        self.lbl_ad = ttk.Label(self, text="Ad:")
        self.entry_ad = ttk.Entry(self)
        self.lbl_ad.grid(row=0, column=0)
        self.entry_ad.grid(row=0, column=1)

        self.lbl_soyad = ttk.Label(self, text="Soyad:")
        self.entry_soyad = ttk.Entry(self)
        self.lbl_soyad.grid(row=1, column=0)
        self.entry_soyad.grid(row=1, column=1)

        # Adres ve Vatandaşlık
        self.lbl_adres = ttk.Label(self, text="Adres:")
        self.entry_adres = ttk.Entry(self)
        self.lbl_adres.grid(row=2, column=0)
        self.entry_adres.grid(row=2, column=1)

        self.lbl_vatandaslik = ttk.Label(self, text="Vatandaşlık:")
        self.entry_vatandaslik = ttk.Entry(self)
        self.lbl_vatandaslik.grid(row=3, column=0)
        self.entry_vatandaslik.grid(row=3, column=1)

        # Doğum ve İşe Giriş Tarihi
        self.lbl_dogum_tarihi = ttk.Label(self, text="Doğum Tarihi (YYYY-MM-DD):")
        self.entry_dogum_tarihi = ttk.Entry(self)
        self.lbl_dogum_tarihi.grid(row=4, column=0)
        self.entry_dogum_tarihi.grid(row=4, column=1)

        self.lbl_ise_giris_tarihi = ttk.Label(self, text="İşe Giriş Tarihi (YYYY-MM-DD):")
        self.entry_ise_giris_tarihi = ttk.Entry(self)
        self.lbl_ise_giris_tarihi.grid(row=5, column=0)
        self.entry_ise_giris_tarihi.grid(row=5, column=1)

        # Lisans
        self.lbl_lisans = ttk.Label(self, text="Lisans:")
        self.entry_lisans = ttk.Entry(self)
        self.lbl_lisans.grid(row=6, column=0)
        self.entry_lisans.grid(row=6, column=1)

        # Ekle Butonu
        self.btn_ekle = ttk.Button(self, text="Ekle", command=self.ekle_kaptan)
        self.btn_ekle.grid(row=7, column=1)

    def ekle_kaptan(self):
        ad = self.entry_ad.get().strip()
        soyad = self.entry_soyad.get().strip()
        adres = self.entry_adres.get().strip()
        vatandaslik = self.entry_vatandaslik.get().strip()
        dogum_tarihi = self.entry_dogum_tarihi.get().strip()
        ise_giris_tarihi = self.entry_ise_giris_tarihi.get().strip()
        lisans = self.entry_lisans.get().strip()

        # Girdi doğrulama
        if not (ad and soyad and adres and vatandaslik and dogum_tarihi and ise_giris_tarihi and lisans):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    INSERT INTO Kaptanlar (ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, lisans))

            messagebox.showinfo("Başarılı", "Kaptan başarıyla eklendi.")

            self.ana_uygulama.yukle_kaptanlar()  # Kaptanları yeniden yükle
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


class KaptanDuzenleForm(tk.Frame):
    def __init__(self, master, Baglanti, kaptan_values, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.kaptan_values = kaptan_values
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_kaptan_id = tk.Label(self, text="Kaptan ıd:")
        self.entry_kaptan_id = tk.Entry(self)
        self.entry_kaptan_id.insert(0, self.kaptan_values[0])
        self.entry_kaptan_id.config(state='readonly')  # Kaptan ıd değiştirilemez
        self.lbl_kaptan_id.grid(row=0, column=0)
        self.entry_kaptan_id.grid(row=0, column=1)

        self.lbl_ad = tk.Label(self, text="Ad:")
        self.entry_ad = tk.Entry(self)
        self.entry_ad.insert(0, self.kaptan_values[1])
        self.lbl_ad.grid(row=1, column=0)
        self.entry_ad.grid(row=1, column=1)

        self.lbl_soyad = tk.Label(self, text="Soyad:")
        self.entry_soyad = tk.Entry(self)
        self.entry_soyad.insert(0, self.kaptan_values[2])
        self.lbl_soyad.grid(row=2, column=0)
        self.entry_soyad.grid(row=2, column=1)

        self.lbl_lisans = tk.Label(self, text="Lisans:")
        self.entry_lisans = tk.Entry(self)
        self.entry_lisans.insert(0, self.kaptan_values[3])
        self.lbl_lisans.grid(row=3, column=0)
        self.entry_lisans.grid(row=3, column=1)

        self.lbl_ise_giris_tarihi = tk.Label(self, text="İşe Giriş Tarihi:")
        self.entry_ise_giris_tarihi = tk.Entry(self)
        self.entry_ise_giris_tarihi.insert(0, self.kaptan_values[4])
        self.lbl_ise_giris_tarihi.grid(row=4, column=0)
        self.entry_ise_giris_tarihi.grid(row=4, column=1)

        self.btn_guncelle = tk.Button(self, text="Güncelle", command=self.guncelle_kaptan)
        self.btn_guncelle.grid(row=5, column=1)

    def guncelle_kaptan(self):
        kaptan_id = self.entry_kaptan_id.get().strip()
        ad = self.entry_ad.get().strip()
        soyad = self.entry_soyad.get().strip()
        lisans = self.entry_lisans.get().strip()
        ise_giris_tarihi = self.entry_ise_giris_tarihi.get().strip()

        if not (ad and soyad and lisans and ise_giris_tarihi):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")  # Tüm alanların dolu olmasına dikkat et
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    UPDATE Kaptanlar
                    SET ad = ?, soyad = ?, lisans = ?, ise_giris_tarihi = ?
                    WHERE kaptan_id = ?
                """, (ad, soyad, lisans, ise_giris_tarihi, kaptan_id))  # Kaptan bilgilerini güncelle

            messagebox.showinfo("Başarılı", "Kaptan başarıyla güncellendi.")

            self.ana_uygulama.yukle_kaptanlar()  # Kaptanları yeniden yükle
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")

        # Mürettebat Ekleme Formu


class MurettebatForm(tk.Frame):
    def __init__(self, master, Baglanti, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_ad = ttk.Label(self, text="Ad:")
        self.entry_ad = ttk.Entry(self)
        self.lbl_ad.grid(row=0, column=0)
        self.entry_ad.grid(row=0, column=1)

        self.lbl_soyad = ttk.Label(self, text="Soyad:")
        self.entry_soyad = ttk.Entry(self)
        self.lbl_soyad.grid(row=1, column=0)
        self.entry_soyad.grid(row=1, column=1)

        self.lbl_adres = ttk.Label(self, text="Adres:")
        self.entry_adres = ttk.Entry(self)
        self.lbl_adres.grid(row=2, column=0)
        self.entry_adres.grid(row=2, column=1)

        self.lbl_vatandaslik = ttk.Label(self, text="Vatandaşlık:")
        self.entry_vatandaslik = ttk.Entry(self)
        self.lbl_vatandaslik.grid(row=3, column=0)
        self.entry_vatandaslik.grid(row=3, column=1)

        self.lbl_dogum_tarihi = ttk.Label(self, text="Doğum Tarihi (YYYY-MM-DD):")
        self.entry_dogum_tarihi = ttk.Entry(self)
        self.lbl_dogum_tarihi.grid(row=4, column=0)
        self.entry_dogum_tarihi.grid(row=4, column=1)

        self.lbl_ise_giris_tarihi = ttk.Label(self, text="İşe Giriş Tarihi (YYYY-MM-DD):")
        self.entry_ise_giris_tarihi = ttk.Entry(self)
        self.lbl_ise_giris_tarihi.grid(row=5, column=0)
        self.entry_ise_giris_tarihi.grid(row=5, column=1)

        self.lbl_gorev = ttk.Label(self, text="Görev:")
        self.entry_gorev = ttk.Entry(self)
        self.lbl_gorev.grid(row=6, column=0)
        self.entry_gorev.grid(row=6, column=1)

        self.btn_ekle = ttk.Button(self, text="Ekle", command=self.ekle_murettebat)
        self.btn_ekle.grid(row=7, column=1)

    def ekle_murettebat(self):
        ad = self.entry_ad.get().strip()
        soyad = self.entry_soyad.get().strip()
        adres = self.entry_adres.get().strip()
        vatandaslik = self.entry_vatandaslik.get().strip()
        dogum_tarihi = self.entry_dogum_tarihi.get().strip()
        ise_giris_tarihi = self.entry_ise_giris_tarihi.get().strip()
        gorev = self.entry_gorev.get().strip()

        if not (ad and soyad and adres and vatandaslik and dogum_tarihi and ise_giris_tarihi and gorev):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")  # Tüm alanların doldurulması gerekir
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    INSERT INTO Murettebat (ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                ad, soyad, adres, vatandaslik, dogum_tarihi, ise_giris_tarihi, gorev))  # Yeni mürettebat kaydı oluştur

            messagebox.showinfo("Başarılı", "Mürettebat başarıyla eklendi.")

            self.ana_uygulama.yukle_murettebatlar()
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


# Mürettebat Düzenleme Formu
class MurettebatDuzenleForm(tk.Frame):
    def __init__(self, master, Baglanti, murettebat_values, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.murettebat_values = murettebat_values
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_murettebat_id = ttk.Label(self, text="Mürettebat ıd:")
        self.entry_murettebat_id = ttk.Entry(self)
        self.entry_murettebat_id.insert(0, self.murettebat_values[0])
        self.entry_murettebat_id.config(state='readonly')  # Değiştirilemez
        self.lbl_murettebat_id.grid(row=0, column=0)
        self.entry_murettebat_id.grid(row=0, column=1)

        self.lbl_ad = ttk.Label(self, text="Ad:")
        self.entry_ad = ttk.Entry(self)
        self.entry_ad.insert(0, self.murettebat_values[1])
        self.lbl_ad.grid(row=1, column=0)
        self.entry_ad.grid(row=1, column=1)

        self.lbl_soyad = ttk.Label(self, text="Soyad:")
        self.entry_soyad = ttk.Entry(self)
        self.entry_soyad.insert(0, self.murettebat_values[2])
        self.lbl_soyad.grid(row=2, column=0)
        self.entry_soyad.grid(row=2, column=1)

        self.lbl_gorev = ttk.Label(self, text="Görev:")
        self.entry_gorev = ttk.Entry(self)
        self.entry_gorev.insert(0, self.murettebat_values[3])
        self.lbl_gorev.grid(row=3, column=0)
        self.entry_gorev.grid(row=3, column=1)

        self.btn_guncelle = ttk.Button(self, text="Güncelle", command=self.guncelle_murettebat)
        self.btn_guncelle.grid(row=4, column=1)

    def guncelle_murettebat(self):
        murettebat_id = self.entry_murettebat_id.get().strip()
        ad = self.entry_ad.get().strip()
        soyad = self.entry_soyad.get().strip()
        gorev = self.entry_gorev.get().strip()

        if not (ad and soyad and gorev):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    UPDATE Murettebat
                    SET ad = ?, soyad = ?, gorev = ?
                    WHERE murettebat_id = ?
                """, (ad, soyad, gorev, murettebat_id))  # Mürettebatı güncelle

            messagebox.showinfo("Başarılı", "Mürettebat başarıyla güncellendi.")

            # AnaUygulama daki mürettebatı yeniden yükle
            self.ana_uygulama.yukle_murettebatlar()
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


class LimanForm(tk.Frame):
    def __init__(self, master, Baglanti, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_liman_adi = ttk.Label(self, text="Liman Adı:")
        self.entry_liman_adi = ttk.Entry(self)
        self.lbl_liman_adi.grid(row=0, column=0)
        self.entry_liman_adi.grid(row=0, column=1)

        self.lbl_ulke = ttk.Label(self, text="Ülke:")
        self.entry_ulke = ttk.Entry(self)
        self.lbl_ulke.grid(row=1, column=0)
        self.entry_ulke.grid(row=1, column=1)

        self.lbl_nufus = ttk.Label(self, text="Nüfus:")
        self.entry_nufus = ttk.Entry(self)
        self.lbl_nufus.grid(row=2, column=0)
        self.entry_nufus.grid(row=2, column=1)

        self.lbl_pasaport_gerekli = ttk.Label(self, text="Pasaport Gerekli:")
        self.pasaport_var = tk.BooleanVar()
        self.chk_pasaport = ttk.Checkbutton(self, variable=self.pasaport_var)
        self.lbl_pasaport_gerekli.grid(row=3, column=0)
        self.chk_pasaport.grid(row=3, column=1)

        self.lbl_demirleme_ucreti = ttk.Label(self, text="Demirleme Ücreti:")
        self.entry_demirleme_ucreti = ttk.Entry(self)
        self.lbl_demirleme_ucreti.grid(row=4, column=0)
        self.entry_demirleme_ucreti.grid(row=4, column=1)

        self.btn_ekle = ttk.Button(self, text="Ekle", command=self.ekle_liman)
        self.btn_ekle.grid(row=5, column=1)

    def ekle_liman(self):
        liman_adi = self.entry_liman_adi.get().strip()
        ulke = self.entry_ulke.get().strip()
        nufus = int(self.entry_nufus.get().strip())
        pasaport_gerekli = self.pasaport_var.get()
        demirleme_ucreti = float(self.entry_demirleme_ucreti.get().strip())

        if not (liman_adi and ulke):
            messagebox.showerror("Hata", "Lütfen Liman Adı ve Ülke alanlarını doldurun.")  # Gereken alanlar
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    INSERT INTO Limanlar (liman_adi, ulke, nufus, pasaport_gerekli, demirleme_ucreti)
                    VALUES (?, ?, ?, ?, ?)
                """, (liman_adi, ulke, nufus, pasaport_gerekli, demirleme_ucreti))  # Yeni liman kaydı

            messagebox.showinfo("Başarılı", "Liman başarıyla eklendi.")  # Başarı mesajı

            self.ana_uygulama.yukle_limanlar()  # Limanları yeniden yükle
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


class LimanDuzenleForm(tk.Frame):
    def __init__(self, master, Baglanti, liman_values, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.liman_values = liman_values
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_liman_adi = ttk.Label(self, text="Liman Adı:")
        self.entry_liman_adi = ttk.Entry(self)
        self.entry_liman_adi.insert(0, self.liman_values[0])
        self.entry_liman_adi.config(state='readonly')  # Liman adı değiştirilemez
        self.lbl_liman_adi.grid(row=0, column=0)
        self.entry_liman_adi.grid(row=0, column=1)

        self.lbl_ulke = ttk.Label(self, text="Ülke:")
        self.entry_ulke = ttk.Entry(self)
        self.entry_ulke.insert(0, self.liman_values[1])
        self.lbl_ulke.grid(row=1, column=0)
        self.entry_ulke.grid(row=1, column=1)

        self.lbl_nufus = ttk.Label(self, text="Nüfus:")
        self.entry_nufus = ttk.Entry(self)
        self.entry_nufus.insert(0, self.liman_values[2])
        self.lbl_nufus.grid(row=2, column=0)
        self.entry_nufus.grid(row=2, column=1)

        self.lbl_pasaport_gerekli = ttk.Label(self, text="Pasaport Gerekli:")
        self.pasaport_var = ttk.BooleanVar()
        self.pasaport_var.set(self.liman_values[3])
        self.chk_pasaport = ttk.Checkbutton(self, variable=self.pasaport_var)
        self.lbl_pasaport_gerekli.grid(row=3, column=0)
        self.chk_pasaport.grid(row=3, column=1)

        self.lbl_demirleme_ucreti = ttk.Label(self, text="Demirleme Ücreti:")
        self.entry_demirleme_ucreti = ttk.Entry(self)
        self.entry_demirleme_ucreti.insert(0, self.liman_values[4])
        self.lbl_demirleme_ucreti.grid(row=4, column=0)
        self.entry_demirleme_ucreti.grid(row=4, column=1)

        self.btn_guncelle = ttk.Button(self, text="Güncelle", command=self.guncelle_liman)
        self.btn_guncelle.grid(row=5, column=1)

    def guncelle_liman(self):
        liman_adi = self.entry_liman_adi.get().strip()
        ulke = self.entry_ulke.get().strip()
        nufus = int(self.entry_nufus.get().strip())
        pasaport_gerekli = self.pasaport_var.get()
        demirleme_ucreti = float(self.entry_demirleme_ucreti.get().strip())

        if not (liman_adi and ulke):
            messagebox.showerror("Hata", "Lütfen Liman Adı ve Ülke alanlarını doldurun.")  # Gereken alanlar
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    UPDATE Limanlar
                    SET nufus = ?, pasaport_gerekli = ?, demirleme_ucreti = ?
                    WHERE liman_adi = ? AND ulke = ?
                """, (nufus, pasaport_gerekli, demirleme_ucreti, liman_adi, ulke))  # Liman kaydını güncelle

            messagebox.showinfo("Başarılı", "Liman başarıyla güncellendi.")  # Başarı mesajı

            # Limanları yeniden yükle
            self.ana_uygulama.yukle_limanlar()
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


# Sefer ekleme formu
class SeferForm(tk.Frame):
    def __init__(self, master, Baglanti, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        # Yolcu Gemisi
        self.lbl_yolcu_gemi = ttk.Label(self, text="Yolcu Gemisi:")
        self.entry_yolcu_gemi = ttk.Entry(self)
        self.lbl_yolcu_gemi.grid(row=0, column=0)
        self.entry_yolcu_gemi.grid(row=0, column=1)

        # Yola Çıkış Tarihi
        self.lbl_yola_cikis_tarihi = ttk.Label(self, text="Yola Çıkış Tarihi (YYYY-MM-DD):")
        self.entry_yola_cikis_tarihi = ttk.Entry(self)
        self.lbl_yola_cikis_tarihi.grid(row=1, column=0)
        self.entry_yola_cikis_tarihi.grid(row=1, column=1)

        # Dönüş Tarihi
        self.lbl_donus_tarihi = ttk.Label(self, text="Dönüş Tarihi (YYYY-MM-DD):")
        self.entry_donus_tarihi = ttk.Entry(self)
        self.lbl_donus_tarihi.grid(row=2, column=0)
        self.entry_donus_tarihi.grid(row=2, column=1)

        # Yola Çıkış Limanı
        self.lbl_yola_cikis_limani = ttk.Label(self, text="Yola Çıkış Limanı:")
        self.entry_yola_cikis_limani = ttk.Entry(self)
        self.lbl_yola_cikis_limani.grid(row=3, column=0)
        self.entry_yola_cikis_limani.grid(row=3, column=1)

        # Ekle Butonu
        self.btn_ekle = ttk.Button(self, text="Ekle", command=self.ekle_sefer)
        self.btn_ekle.grid(row=4, column=1)

    def ekle_sefer(self):
        yolcu_gemi = self.entry_yolcu_gemi.get().strip()
        yola_cikis_tarihi = self.entry_yola_cikis_tarihi.get().strip()
        donus_tarihi = self.entry_donus_tarihi.get().strip()
        yola_cikis_limani = self.entry_yola_cikis_limani.get().strip()

        # Girdi doğrulama
        if not (yolcu_gemi and yola_cikis_tarihi and donus_tarihi and yola_cikis_limani):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")  # Girdi doğrulama
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    INSERT INTO Seferler (yolcu_gemi, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani)
                    VALUES (?, ?, ?, ?)
                """, (yolcu_gemi, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani))  # Doğru sayıda sütun ve değer

            messagebox.showinfo("Başarılı", "Sefer başarıyla eklendi.")  # Başarı mesajı

            self.ana_uygulama.yukle_seferler()  # Seferleri yeniden yükle
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")

        # Sefer Düzenleme Formu


class SeferDuzenleForm(tk.Frame):
    def __init__(self, master, Baglanti, sefer_values, ana_uygulama):
        super().__init__(master)
        self.Baglanti = Baglanti
        self.sefer_values = sefer_values
        self.ana_uygulama = ana_uygulama
        self.sekme_olustur()

    def sekme_olustur(self):
        self.lbl_sefer_id = ttk.Label(self, text="Sefer ıd:")
        self.entry_sefer_id = ttk.Entry(self)
        self.entry_sefer_id.insert(0, self.sefer_values[0])
        self.entry_sefer_id.config(state='readonly')  # Sefer ıd si değiştirilemez
        self.lbl_sefer_id.grid(row=0, column=0)
        self.entry_sefer_id.grid(row=0, column=1)

        self.lbl_yolcu_gemi = ttk.Label(self, text="Yolcu Gemisi:")
        self.entry_yolcu_gemi = ttk.Entry(self)
        self.entry_yolcu_gemi.insert(0, self.sefer_values[1])
        self.lbl_yolcu_gemi.grid(row=1, column=0)
        self.entry_yolcu_gemi.grid(row=1, column=1)

        self.lbl_yola_cikis_tarihi = ttk.Label(self, text="Yola Çıkış Tarihi:")
        self.entry_yola_cikis_tarihi = ttk.Entry(self)
        self.entry_yola_cikis_tarihi.insert(0, self.sefer_values[2])
        self.lbl_yola_cikis_tarihi.grid(row=2, column=0)
        self.entry_yola_cikis_tarihi.grid(row=2, column=1)

        self.lbl_donus_tarihi = ttk.Label(self, text="Dönüş Tarihi:")
        self.entry_donus_tarihi = ttk.Entry(self)
        self.entry_donus_tarihi.insert(0, self.sefer_values[3])
        self.lbl_donus_tarihi.grid(row=3, column=0)
        self.entry_donus_tarihi.grid(row=3, column=1)

        self.lbl_yola_cikis_limani = ttk.Label(self, text="Yola Çıkış Limanı:")
        self.entry_yola_cikis_limani = ttk.Entry(self)
        self.entry_yola_cikis_limani.insert(0, self.sefer_values[4])
        self.lbl_yola_cikis_limani.grid(row=4, column=0)
        self.entry_yola_cikis_limani.grid(row=4, column=1)

        self.btn_guncelle = ttk.Button(self, text="Güncelle", command=self.guncelle_sefer)
        self.btn_guncelle.grid(row=5, column=1)

    def guncelle_sefer(self):
        sefer_id = self.entry_sefer_id.get().strip()
        yolcu_gemi = self.entry_yolcu_gemi.get().strip()
        yola_cikis_tarihi = self.entry_yola_cikis_tarihi.get().strip()
        donus_tarihi = self.entry_donus_tarihi.get().strip()
        yola_cikis_limani = self.entry_yola_cikis_limani.get().strip()

        if not (yolcu_gemi and yola_cikis_tarihi and donus_tarihi and yola_cikis_limani and sefer_id):
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")  # Girdi doğrulama
            return

        try:
            with self.Baglanti:
                self.Baglanti.execute("""
                    UPDATE Seferler
                    SET yolcu_gemi = ?, yola_cikis_tarihi = ?, donus_tarihi = ?, yola_cikis_limani = ?
                    WHERE sefer_id = ?
                """, (yolcu_gemi, yola_cikis_tarihi, donus_tarihi, yola_cikis_limani, sefer_id))  # Seferi güncelle

            messagebox.showinfo("Başarılı", "Sefer başarıyla güncellendi.")  # Başarı mesajı

            # Seferleri yeniden yükle
            self.ana_uygulama.yukle_seferler()
            self.pack_forget()
        except Exception as e:
            messagebox.showerror("Hata", f"Bir hata meydana geldi: {e}")


def main():
    Baglanti = Baglanti_olustur()

    tablo_olustur(Baglanti)
    root = tk.Tk()
    root.title("Gezgin Gemi Şirketi Yönetimi")
    ana_uygulama = AnaUygulama(root, Baglanti)
    ana_uygulama.pack(padx=20, pady=20)

    root.mainloop()


if __name__ == "__main__":
    main()  # Uygulamayı çalıştır
