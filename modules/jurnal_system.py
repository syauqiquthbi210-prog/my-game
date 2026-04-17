from ursina import *

class JurnalManager:
    def __init__(self, player):
        self.player = player
        self.pages = [
            "Halaman 1 (Buku Pertama):\n\nJudul: Rumus 1: Mengenal Isim\n\nPenjelasan: Isim adalah kata yang menunjukkan benda, nama, atau sifat. Ciri utamanya adalah bisa menerima Tanwin (ً ٍ ٌ), diawali Alif Lam (ال), atau terletak setelah Huruf Jar (seperti min, ila, 'an).",
            "Halaman 2 (Buku Kedua):\n\nJudul: Rumus 2: Pembagian Kalimat\n\nPenjelasan: Dalam bahasa Arab, kalimat (kata) hanya ada tiga: Isim (Kata Benda), Fi'il (Kata Kerja), dan Huruf (Kata Tugas). Fi'il sendiri dibagi menjadi Madhi (Lampau), Mudhore (Sekarang/Akan), dan Amar (Perintah).",
            "Halaman 3 (Buku Ketiga):\n\nJudul: Rumus 3: Isim Isyarah & Dhomir\n\nPenjelasan: Isim Isyarah adalah kata tunjuk (seperti Haza atau Zalika). Sedangkan Dhomir adalah kata ganti orang (seperti Huwa untuk dia laki-laki atau Anta untuk kamu)."
        ]
        self.unlocked_pages = 0
        self.current_page = 0
        self.is_open = False
        
        # UI Quad Putih (Kertas)
        self.panel = Entity(parent=camera.ui, model='quad', color=color.white, scale=(1.2, 0.8), z=-20, enabled=False, ignore_paused=True)
        self.title_text = Text(parent=self.panel, text='Buku Saku (Khulasoh)', position=(0, 0.4), scale=1.3, origin=(0,0), color=color.black, z=-0.1, ignore_paused=True)
        self.content_text = Text(parent=self.panel, text=" ", position=(0, 0.2), scale=1.0, origin=(0, 0.5), color=color.black, z=-0.1, ignore_paused=True)
        self.content_text.wordwrap = 45 
        
        # Tombol Navigasi
        self.btn_prev = Button(parent=self.panel, text='< Kiri', position=(-0.35, -0.35), scale=(0.2, 0.1), color=color.gray, on_click=self.prev_page, z=-0.1, ignore_paused=True)
        self.btn_next = Button(parent=self.panel, text='Kanan >', position=(0.35, -0.35), scale=(0.2, 0.1), color=color.gray, on_click=self.next_page, z=-0.1, ignore_paused=True)
        self.btn_close = Button(parent=self.panel, text='Tutup [TAB]', position=(0, -0.35), scale=(0.3, 0.1), color=color.red, on_click=self.toggle_jurnal, z=-0.1, ignore_paused=True)
        
        self.update_content()

    def update_content(self):
        if self.unlocked_pages == 0:
            self.content_text.text = "- Belum ada halaman yang ditemukan -\n\nKumpulkan buku untuk membuka materi."
            self.btn_prev.disabled = True
            self.btn_next.disabled = True
        else:
            if self.current_page >= self.unlocked_pages:
                self.current_page = self.unlocked_pages - 1
            if self.current_page < 0:
                self.current_page = 0
                
            self.content_text.text = self.pages[self.current_page]
            self.btn_prev.disabled = (self.current_page == 0)
            self.btn_next.disabled = (self.current_page == min(self.unlocked_pages, len(self.pages)) - 1)
            
        self.btn_prev.color = color.dark_gray if self.btn_prev.disabled else color.gray
        self.btn_next.color = color.dark_gray if self.btn_next.disabled else color.gray

    def next_page(self):
        max_page = min(self.unlocked_pages, len(self.pages)) - 1
        if self.current_page < max_page:
            self.current_page += 1
            self.update_content()
            Audio('pickup.wav', volume=0.5, pitch=1.5, autoplay=True)

    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.update_content()
            Audio('pickup.wav', volume=0.5, pitch=1.5, autoplay=True)

    def open_jurnal(self):
        from ursina import mouse
        self.is_open = True
        self.update_content()
        self.panel.enabled = True
        self.player.disable()
        mouse.locked = False

    def close_jurnal(self):
        from ursina import mouse
        self.is_open = False
        self.panel.enabled = False
        self.player.enable()
        mouse.locked = True

    def toggle_jurnal(self):
        if self.is_open:
            self.close_jurnal()
        else:
            self.open_jurnal()

    def add_unlocked_page(self):
        if self.unlocked_pages < len(self.pages):
            self.unlocked_pages += 1
            self.update_content()


class LembarCatatan(Entity):
    """
    Objek 3D Lembar Catatan yang tersebar di maze. Saat dipungut, akan menambah halaman jurnal.
    """
    def __init__(self, position, content):
        super().__init__(
            model='quad', 
            color=color.rgb(250, 240, 200),
            texture='white_cube',
            scale=(0.4, 0.4),
            position=position,
            rotation_x=90,
            collider='box'
        )
        self.content = content
        # Efek pendukung (glow atau floating bisa ditambahkan)
        self.light = PointLight(parent=self, y=0.5, color=color.rgb(200, 200, 100), radius=2)
