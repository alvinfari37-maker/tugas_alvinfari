import json
import os
from datetime import datetime, timedelta

from kivy.app import App
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.graphics import Color, RoundedRectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup


Window.size = (1200, 750)
Window.minimum_width = 1000
Window.minimum_height = 650
Window.clearcolor = (0.035, 0.055, 0.09, 1)


BG = (0.035, 0.055, 0.09, 1)
CARD = (0.065, 0.095, 0.15, 1)
CARD2 = (0.09, 0.13, 0.20, 1)

BLUE = (0.0, 0.55, 0.80, 1)
BLUE_DARK = (0.0, 0.35, 0.55, 1)

GREEN = (0.05, 0.65, 0.30, 1)
ORANGE = (0.90, 0.55, 0.10, 1)
RED = (0.85, 0.18, 0.20, 1)

WHITE = (1, 1, 1, 1)
GRAY = (0.65, 0.70, 0.78, 1)


MENU = [
    ("Nasi Goreng", 15000),
    ("Mie Goreng", 12000),
    ("Ayam Geprek", 18000),
    ("Ayam Bakar", 20000),
    ("Es Teh", 5000),
    ("Es Jeruk", 6000),
    ("Kopi", 7000),
    ("Air Mineral", 4000),
    ("Kentang Goreng", 10000),
    ("Roti Bakar", 12000),
]


class Card(BoxLayout):

    def __init__(self, color=CARD, radius=18, **kwargs):
        super().__init__(**kwargs)

        with self.canvas.before:
            Color(*color)
            self.background = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(radius)]
            )

        self.bind(
            pos=self.update_background,
            size=self.update_background
        )

    def update_background(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size


class MenuButton(Button):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.background_normal = ""
        self.background_color = CARD2
        self.color = WHITE
        self.font_size = dp(13)
        self.bold = True


class KasirLayout(BoxLayout):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)

        self.orientation = "vertical"
        self.padding = dp(18)
        self.spacing = dp(12)

        self.cart = []

        header = Card(
            orientation="horizontal",
            size_hint_y=None,
            height=dp(75),
            padding=[dp(20), dp(10)]
        )

        title_box = BoxLayout(
            orientation="vertical"
        )

        title = Label(
            text="[b]WARUNG INI[/b]",
            markup=True,
            font_size=dp(25),
            color=WHITE,
            halign="left"
        )

        subtitle = Label(
            text="Aplikasi Kasir & Manajemen Transaksi",
            font_size=dp(12),
            color=GRAY,
            halign="left"
        )

        title_box.add_widget(title)
        title_box.add_widget(subtitle)

        header.add_widget(title_box)

        status = Label(
            text="[color=#20C997]● SISTEM AKTIF[/color]",
            markup=True,
            font_size=dp(13),
            size_hint_x=None,
            width=dp(150)
        )

        header.add_widget(status)

        self.add_widget(header)


        main = BoxLayout(
            orientation="horizontal",
            spacing=dp(12)
        )


        left = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_x=0.36
        )


        input_card = Card(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(8),
            size_hint_y=None,
            height=dp(300)
        )

        input_title = Label(
            markup=True,
            font_size=dp(19),
            color=WHITE,
            size_hint_y=None,
            height=dp(32),
            halign="left"
        )

        input_card.add_widget(input_title)

      
        input_card.add_widget(
            self.label_kecil("Nama Barang")
        )

        self.input_nama = TextInput(
            hint_text="Masukkan nama barang",
            multiline=False,
            background_normal="",
            background_color=CARD2,
            foreground_color=WHITE,
            hint_text_color=GRAY,
            cursor_color=PUTIH,
            padding=[dp(12), dp(10)],
            size_hint_y=None,
            height=dp(40)
        )

        input_card.add_widget(self.input_nama)

       
        input_card.add_widget(
            self.label_kecil("Harga")
        )

        self.input_harga = TextInput(
            hint_text="Contoh: 15000",
            multiline=False,
            input_filter="int",
            background_normal="",
            background_color=CARD2,
            foreground_color=WHITE,
            hint_text_color=GRAY,
            cursor_color=PUTIH,
            padding=[dp(12), dp(10)],
            size_hint_y=None,
            height=dp(40)
        )

        input_card.add_widget(self.input_harga)

        
        input_card.add_widget(
            self.label_kecil("Jumlah")

        )

        self.input_jumlah = TextInput(
            text="1",
            multiline=False,
            input_filter="int",
            background_normal="",
            background_color=CARD2,
            foreground_color=WHITE,
            hint_text_color=GRAY,
            cursor_color=PUTIH,
            padding=[dp(12), dp(10)],
            size_hint_y=None,
            height=dp(40)
        )

        input_card.add_widget(self.input_jumlah)

        btn_tambah = Button(
            text="+  TAMBAH KE KERANJANG",
            background_normal="",
            background_color=BLUE_DARK,
            color=WHITE,
            bold=True,
            size_hint_y=None,
            height=dp(45)
        )

        btn_tambah.bind(
            on_press=self.tambah_keranjang
        )

        input_card.add_widget(btn_tambah)

        left.add_widget(input_card)

        menu_card = Card(
            orientation="vertical",
            padding=dp(12),
            spacing=dp(7)
        )

        menu_title = Label(
            text="[b]Daftar Menu[/b]",
            markup=True,
            font_size=dp(17),
            color=WHITE,
            size_hint_y=None,
            height=dp(30),
            halign="left"
        )

        menu_card.add_widget(menu_title)

        menu_scroll = ScrollView()

        menu_grid = GridLayout(
            cols=2,
            spacing=dp(7),
            size_hint_y=None
        )

        menu_grid.bind(
            minimum_height=menu_grid.setter("height")
        )

        for nama, harga in MENU:

            tombol = MenuButton(
                text=f"{nama}\nRp {harga:,}".replace(",", "."),
                size_hint_y=None,
                height=dp(55)
            )

            tombol.bind(
                on_press=lambda instance,
                n=nama,
                h=harga: self.pilih_menu(n, h)
            )

            menu_grid.add_widget(tombol)

        menu_scroll.add_widget(menu_grid)
        menu_card.add_widget(menu_scroll)

        left.add_widget(menu_card)

        main.add_widget(left)

        right = Card(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10),
            size_hint_x=0.64
        )

        

        cart_header = BoxLayout(
            size_hint_y=None,
            height=dp(38)
        )

        cart_title = Label(
            text="[b]Keranjang Belanja[/b]",
            markup=True,
            font_size=dp(20),
            color=WHITE,
            halign="left"
        )

        cart_header.add_widget(cart_title)

        self.jumlah_item = Label(
            text="0 item",
            font_size=dp(13),
            color=GRAY,
            size_hint_x=None,
            width=dp(90)
        )

        cart_header.add_widget(self.jumlah_item)

        right.add_widget(cart_header)

       

        table_header = BoxLayout(
            size_hint_y=None,
            height=dp(35)
        )

        header_names = [
            "Barang",
            "Harga",
            "Qty",
            "Subtotal",
            "Aksi"
        ]

        for nama in header_names:

            table_header.add_widget(
                Label(
                    text=f"[b]{nama}[/b]",
                    markup=True,
                    color=GRAY,
                    font_size=dp(11)
                )
            )

        right.add_widget(table_header)


        self.scroll = ScrollView()

        self.layout_keranjang = GridLayout(
            cols=1,
            spacing=dp(7),
            size_hint_y=None
        )

        self.layout_keranjang.bind(
            minimum_height=self.layout_keranjang.setter(
                "height"
            )
        )

        self.scroll.add_widget(
            self.layout_keranjang
        )

        right.add_widget(self.scroll)

        total_card = Card(
            orientation="horizontal",
            padding=[dp(15), dp(8)],
            size_hint_y=None,
            height=dp(65),
            color=(0.03, 0.16, 0.18, 1)
        )

        total_card.add_widget(
            Label(
                text="TOTAL PEMBAYARAN",
                color=GRAY,
                font_size=dp(13),
                halign="left"
            )
        )

        self.label_total = Label(
            text="Rp 0",
            color=GREEN,
            font_size=dp(24),
            bold=True,
            halign="right"
        )

        total_card.add_widget(
            self.label_total
        )

        right.add_widget(total_card)


        action = GridLayout(
            cols=3,
            spacing=dp(8),
            size_hint_y=None,
            height=dp(48)
        )

        btn_simpan = Button(
            text="CETAK STRUK",
            background_normal="",
            background_color=GREEN,
            color=WHITE,
            bold=True,
            font_size=dp(12)
        )

        btn_simpan.bind(
            on_press=self.simpan_dan_cetak
        )

        btn_laporan = Button(
            text="LAPORAN MINGGUAN",
            background_normal="",
            background_color=ORANGE,
            color=WHITE,
            bold=True,
            font_size=dp(12)
        )

        btn_laporan.bind(
            on_press=self.tampilkan_laporan
        )

        btn_bersihkan = Button(
            text="KOSONGKAN",
            background_normal="",
            background_color=RED,
            color=WHITE,
            bold=True,
            font_size=dp(12)
        )

        btn_bersihkan.bind(
            on_press=self.kosongkan_keranjang
        )

        action.add_widget(btn_simpan)
        action.add_widget(btn_laporan)
        action.add_widget(btn_bersihkan)

        right.add_widget(action)

        main.add_widget(right)

        self.add_widget(main)


        self.label_status = Label(
            text="Status: Silakan pilih menu atau masukkan barang...",
            color=GRAY,
            font_size=dp(12),
            italic=True,
            size_hint_y=None,
            height=dp(22)
        )

        self.add_widget(
            self.label_status
        )


    def label_kecil(self, teks):

        return Label(
            text=teks,
            color=GRAY,
            font_size=dp(12),
            size_hint_y=None,
            height=dp(20),
            halign="left"
        )


    def pilih_menu(self, nama, harga):

        self.input_nama.text = nama
        self.input_harga.text = str(harga)
        self.input_jumlah.text = "1"

        self.label_status.text = (
            f"Menu '{nama}' dipilih."
        )

   
    def tambah_keranjang(self, instance):

        nama = self.input_nama.text.strip()
        harga = self.input_harga.text.strip()
        jumlah = self.input_jumlah.text.strip()

        if not nama or not harga or not jumlah:

            self.label_status.text = (
                "Error: Lengkapi nama, harga dan jumlah!"
            )

            return

        try:

            harga = int(harga)
            jumlah = int(jumlah)

            if harga <= 0 or jumlah <= 0:
                raise ValueError

        except ValueError:

            self.label_status.text = (
                "Harga dan jumlah harus berupa angka yang benar."
            )

            return

        subtotal = harga * jumlah

        item = {
            "nama": nama,
            "harga": harga,
            "jumlah": jumlah,
            "subtotal": subtotal
        }

        self.cart.append(item)

        self.update_keranjang_ui()

        self.input_nama.text = ""
        self.input_harga.text = ""
        self.input_jumlah.text = "1"

        self.label_status.text = (
            f"{nama} berhasil ditambahkan."
        )


    def update_keranjang_ui(self):

        self.layout_keranjang.clear_widgets()

        total = 0

        for index, item in enumerate(self.cart):

            row = Card(
                orientation="horizontal",
                size_hint_y=None,
                height=dp(55),
                padding=[dp(5), dp(5)],
                color=CARD2
            )

            
            row.add_widget(
                Label(
                    text=item["nama"],
                    color=WHITE,
                    font_size=dp(12)
                )
            )

            
            row.add_widget(
                Label(
                    text=self.rupiah(item["harga"]),
                    color=GRAY,
                    font_size=dp(11)
                )
            )

          
            row.add_widget(
                Label(
                    text=str(item["jumlah"]),
                    color=WHITE,
                    font_size=dp(12)
                )
            )

           
            row.add_widget(
                Label(
                    text=self.rupiah(item["subtotal"]),
                    color=GREEN,
                    font_size=dp(12),
                    bold=True
                )
            )

           
            hapus = Button(
                text="HAPUS",
                background_normal="",
                background_color=RED,
                color=WHITE,
                font_size=dp(10),
                bold=True
            )

            hapus.bind(
                on_press=lambda instance,
                i=index: self.hapus_item(i)
            )

            row.add_widget(hapus)

            self.layout_keranjang.add_widget(row)

            total += item["subtotal"]

        self.label_total.text = self.rupiah(total)

        self.jumlah_item.text = (
            f"{len(self.cart)} item"
        )

    def hapus_item(self, index):

        if 0 <= index < len(self.cart):

            nama = self.cart[index]["nama"]

            self.cart.pop(index)

            self.update_keranjang_ui()

            self.label_status.text = (
                f"{nama} dihapus dari keranjang."
            )

    def kosongkan_keranjang(self, instance):

        self.cart = []

        self.update_keranjang_ui()

        self.label_status.text = (
            "Keranjang telah dikosongkan."
        )

    def rupiah(self, angka):

        return "Rp " + f"{angka:,}".replace(",", ".")

    def simpan_dan_cetak(self, instance):

        if not self.cart:

            self.label_status.text = (
                "Keranjang masih kosong."
            )

            return

        sekarang = datetime.now()

        total = sum(
            item["subtotal"]
            for item in self.cart
        )

        transaksi = {

            "tanggal": sekarang.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),

            "items": self.cart.copy(),

            "total": total
        }

        file_name = "riwayat_transaksi.json"

        data = []

        if os.path.exists(file_name):

            try:

                with open(
                    file_name,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

            except:

                data = []

        data.append(transaksi)

        with open(
            file_name,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=4,
                ensure_ascii=False
            )

        struk = ""

        struk += "================================\n"
        struk += "          WARUNG INI             \n"
        struk += "       STRUK PEMBAYARAN         \n"
        struk += "================================\n"

        struk += (
            f"Tanggal : "
            f"{sekarang.strftime('%d-%m-%Y %H:%M:%S')}\n"
        )

        struk += "--------------------------------\n"

        for item in self.cart:

            struk += (
                f"{item['nama']}\n"
                f"{item['jumlah']} x "
                f"{self.rupiah(item['harga'])}"
                f" = {self.rupiah(item['subtotal'])}\n"
            )

        struk += "--------------------------------\n"

        struk += (
            f"TOTAL : {self.rupiah(total)}\n"
        )

        struk += "================================\n"
        struk += "       TERIMA KASIH :)          \n"
        struk += "================================"


        receipt_name = (
            "struk_"
            + sekarang.strftime("%Y%m%d_%H%M%S")
            + ".txt"
        )

        with open(
            receipt_name,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(struk)

        popup_layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        popup_layout.add_widget(
            Label(
                text=struk,
                font_size=dp(13),
                color=WHITE
            )
        )

        btn_tutup = Button(
            text="TUTUP",
            size_hint_y=None,
            height=dp(45),
            background_normal="",
            background_color=GREEN,
            color=WHITE,
            bold=True
        )

        popup = Popup(
            title="Struk Pembayaran",
            content=popup_layout,
            size_hint=(0.75, 0.75)
        )

        btn_tutup.bind(
            on_press=popup.dismiss
        )

        popup_layout.add_widget(
            btn_tutup
        )

        popup.open()

        self.cart = []

        self.update_keranjang_ui()

        self.label_status.text = (
            f"Transaksi berhasil disimpan. "
            f"Struk: {receipt_name}"
        )

    def tampilkan_laporan(self, instance):

        file_name = "riwayat_transaksi.json"

        total_mingguan = 0
        jumlah_transaksi = 0

        sekarang = datetime.now()

        tujuh_hari = (
            sekarang - timedelta(days=7)
        )

        data = []

        if os.path.exists(file_name):

            try:

                with open(
                    file_name,
                    "r",
                    encoding="utf-8"
                ) as file:

                    data = json.load(file)

            except:

                data = []

        for transaksi in data:

            try:

                tanggal = datetime.strptime(
                    transaksi["tanggal"],
                    "%Y-%m-%d %H:%M:%S"
                )

                if tujuh_hari <= tanggal <= sekarang:

                    total_mingguan += transaksi["total"]

                    jumlah_transaksi += 1

            except:

                continue

        
        laporan = ""

        laporan += "================================\n"
        laporan += "       LAPORAN MINGGUAN         \n"
        laporan += "================================\n\n"

        laporan += (
            "Periode: 7 Hari Terakhir\n\n"
        )

        laporan += (
            f"Jumlah Transaksi : "
            f"{jumlah_transaksi}\n"
        )

        laporan += (
            f"Total Pemasukan  : "
            f"{self.rupiah(total_mingguan)}\n"
        )

        laporan += "\n"
        laporan += "================================"

        popup_layout = BoxLayout(
            orientation="vertical",
            padding=dp(15),
            spacing=dp(10)
        )

        popup_layout.add_widget(
            Label(
                text=laporan,
                font_size=dp(15),
                color=WHITE
            )
        )

        tombol = BoxLayout(
            spacing=dp(8),
            size_hint_y=None,
            height=dp(45)
        )

        btn_cetak = Button(
            text="SIMPAN LAPORAN",
            background_normal="",
            background_color=GREEN,
            color=WHITE,
            bold=True
        )

        btn_tutup = Button(
            text="TUTUP",
            background_normal="",
            background_color=RED,
            color=WHITE,
            bold=True
        )

        tombol.add_widget(btn_cetak)
        tombol.add_widget(btn_tutup)

        popup_layout.add_widget(tombol)

        popup = Popup(
            title="Laporan Pemasukan Mingguan",
            content=popup_layout,
            size_hint=(0.70, 0.55)
        )

        btn_tutup.bind(
            on_press=popup.dismiss
        )

        btn_cetak.bind(
            on_press=lambda x: self.simpan_laporan(
                laporan
            )
        )

        popup.open()

    def simpan_laporan(self, teks):

        nama_file = (
            "laporan_"
            + datetime.now().strftime(
                "%Y%m%d_%H%M%S"
            )
            + ".txt"
        )

        with open(
            nama_file,
            "w",
            encoding="utf-8"
        ) as file:

            file.write(teks)

        self.label_status.text = (
            f"Laporan berhasil disimpan: {nama_file}"
        )

class KasirApp(App):

    def build(self):

        self.title = "Kasir Pro"

        return KasirLayout()

if __name__ == "__main__":

    KasirApp().run()