from ursina import *

class BalokTarkib(Entity):
    """
    Item berbentuk balok yang bisa diambil oleh pemain (Held Item).
    Digunakan untuk membuka Pintu Tarkib tertentu.
    """
    def __init__(self, position, kata_arab, tipe_kedudukan):
        super().__init__(
            model='cube',
            scale=(0.5, 0.5, 0.5),
            color=color.rgb(50, 150, 200),
            texture='white_cube',
            position=position,
            collider='box' # Agar bisa dideteksi oleh distance/raycast
        )
        self.kata_arab = kata_arab
        self.tipe_kedudukan = tipe_kedudukan
        self.is_held = False
        
        # Teks bahasa Arab di atas balok
        self.label = Text(parent=self, text=kata_arab, color=color.white, scale=2, position=(0, 0.7, 0), origin=(0,0), billboard=True)
        # Menghitamkan pinggiran teks agar mudah dibaca di tempat terang
        self.label_shadow = Text(parent=self, text=kata_arab, color=color.black, scale=2.01, position=(0, 0.68, 0.05), origin=(0,0), billboard=True)

    def pickup(self, player):
        from ursina import camera
        self.is_held = True
        self.parent = camera # Parent ke kamera agar ikut bergerak layaknya FPS
        self.position = Vec3(0.6, -0.5, 1.0) # Taruh di kanan bawah layar
        self.rotation = Vec3(0, -20, 0) # Sedikit miring
        self.collider = None # Nonaktifkan collider saat dipegang
        self.label.enabled = False
        self.label_shadow.enabled = False
        Audio('pickup.wav', autoplay=True, volume=1.0)

    def drop(self, player):
        from ursina import scene
        self.is_held = False
        self.parent = scene
        # Turunkan di depan player, jatuh ke lantai
        self.position = player.position + player.forward * 1.5 + Vec3(0, 0.25, 0)
        self.rotation = Vec3(0, 0, 0)
        self.collider = 'box'
        self.label.enabled = True
        self.label_shadow.enabled = True
        Audio('pickup.wav', autoplay=True, volume=0.5, pitch=0.8)


class PintuTarkib(Entity):
    """
    Pintu khusus (Magic Door) yang tertutup sihir.
    Hanya bisa terbuka jika pemain berinteraksi sambil memegang Balok Tarkib yang benar.
    """
    def __init__(self, position, rot_y=0, kalimat_soal="[ __ ] ضرب زيد", syarat_id="kalban"):
        super().__init__(
            model='cube',
            scale=(3.9, 3.9, 0.2), # Standard ukuran pintu di game ini
            color=color.rgb(100, 30, 100), # Warna magis
            texture='white_cube',
            collider='box',
            position=position,
            rotation_y=rot_y,
            origin_x=-0.5 # Engsel di pinggir kiri
        )
        self.syarat_id = syarat_id
        self.is_open = False
        
        # Teks soal yang melayang di pintu
        self.soal_label = Text(parent=self, text=kalimat_soal, color=color.yellow, scale=3, position=(0, 2.5, -0.15), origin=(0,-0.5), z=-0.15)
        self.soal_label_back = Text(parent=self, text=kalimat_soal, color=color.yellow, scale=3, position=(0, 2.5, 0.15), origin=(0,-0.5), rotation=(0,180,0), z=0.15)
        
        # Audio
        self.error_sound = Audio('kaget.wav', autoplay=False, volume=1.5, pitch=0.8)
        self.success_sound = Audio('unlock.wav', autoplay=False, volume=1.5)
        self.door_open_sound = Audio('pintu_buka.mp3', autoplay=False, volume=2.0)

    def try_open(self, held_item):
        """Mengecek apakah item yang dipegang cocok untuk membuka pintu ini."""
        if held_item and getattr(held_item, 'tipe_kedudukan', None) == self.syarat_id:
            # BENAR! Pintu Terbuka
            self.success_sound.play()
            self.door_open_sound.play()
            self.is_open = True
            self.collider = None
            
            # Matikan teks
            self.soal_label.enabled = False
            self.soal_label_back.enabled = False
            
            # Animasikan buka perlahan sebesar 90 derajat
            from ursina import curve
            self.animate_rotation_y(self.rotation_y + 90, duration=1.5, curve=curve.in_out_sine)
            return True
        else:
            # SALAH!
            self.error_sound.play()
            return False
