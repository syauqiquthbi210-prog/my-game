import os, sys
from pathlib import Path
if getattr(sys, 'frozen', False):
    os.chdir(sys._MEIPASS)

from ursina import *
from ursina import scene, color, window, Entity, Audio, PointLight, AmbientLight, SpotLight, Text, distance, destroy, time, Vec3, Vec2, camera, raycast, held_keys, application, invoke, lerp
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import math

from ursina.shaders.lit_with_shadows_shader import lit_with_shadows_shader

# Library untuk Render Teks Arab (RTL) Anti-Mojibake
import arabic_reshaper
from bidi.algorithm import get_display

from modules.jurnal_system import JurnalManager, LembarCatatan


def format_arabic(text):
    """Format teks Arab agar tersambung dan terbaca RTL di Ursina.
    Teks campuran (Arab + Latin) juga didukung."""
    try:
        reshaped = arabic_reshaper.reshape(text)
        bidi_text = get_display(reshaped)
        return bidi_text
    except Exception:
        return text  # Fallback jika gagal

# Path Font Arab Kustom
ARABIC_FONT = 'assets/fonts/Amiri-Regular.ttf'

# URL Backend Server (Ngrok Live)
SERVER_URL = "https://singular-saddlebag-scoured.ngrok-free.dev"
API_BASE = f"{SERVER_URL}/api/soal/random"

app = Ursina()




# Atmosfer Horor (Global Fog) akan dimuat setelah Player

# Ambient Light untuk cahaya minimal agar tidak benar-benar buta


# Audio
ambient_sound = Audio('ambient.wav', loop=True, autoplay=True, volume=0.5)
footstep_sound = Audio('langkah_kaki.mp3', loop=False, autoplay=False, volume=2.1)
step_triggered = False
pickup_sound = Audio('pickup.wav', autoplay=False, volume=1.0)
jumpscare_sound = Audio('kaget.wav', autoplay=False, volume=2.0)
heartbeat_sound = Audio('heartbeat.wav', loop=True, autoplay=False, volume=0.0)
panting_sound = Audio('panting.wav', loop=True, autoplay=False, volume=1.0)
unlock_sound = Audio('unlock.wav', autoplay=False, volume=1.5)
door_open_sound = Audio('pintu_buka.mp3', autoplay=False, volume=2.0)

# Random Ambient Events System
creepy_events = [
    Audio('creepy_event_1.wav', autoplay=False, volume=1.2),
    Audio('creepy_event_2.wav', autoplay=False, volume=0.7),
    Audio('creepy_event_3.wav', autoplay=False, volume=1.5)
]
ambient_event_timer = random.uniform(30.0, 90.0)
poltergeist_timer = random.uniform(45.0, 120.0)

# Player Setup
player = FirstPersonController(y=1, origin_y=-.5, scale=(1, 1, 1), mouse_sensitivity=Vec2(120, 120), height=2.7)
player.height = 2.7
player.camera_pivot.y = 2.7
player.speed = 4
player.jump_height = 0 # Game horor biasanya tidak bisa lompat tinggi
player.step_height = 0.1 # Cegah naik ke atas perabotan atau menembus celah sempit
player.stamina = 100.0
player.sanity = 100.0
player.health = 100.0
max_health = 100.0
current_day = 1
player.held_item = None # Menyimpan item khusus yang sedang dipegang

last_safe_pos = player.position
safe_timer = 0.0

stamina_bar = Entity(parent=camera.ui, model='quad', color=color.green, scale=(0.4, 0.02), position=(-0.82, -0.42), origin=(-0.5, 0))
health_bar = Entity(parent=camera.ui, model='quad', color=color.red, scale=(0.4, 0.02), position=(-0.82, -0.46), origin=(-0.5, 0))
stamina_text = Text(text='Stamina [Hold Shift]', position=(-0.82, -0.39), scale=1, color=color.white)

# ================= KOMBAT SYSTEM ==================
bullets = 1
ammo_text = Text(text=f'Ammo: {bullets}', position=(0.7, -0.42), scale=1.5, color=color.yellow)



# Senter dan Cahaya (Murky Warm White)
camera.clip_plane_far = 100 # Jangkauan render diperluas agar hantu jauh tetap terdeteksi
flashlight = SpotLight(parent=camera, position=(0, 0, 0), color=color.rgb(200, 190, 170))
flashlight_on = True

# Atmosphere: Horror Black Fog (Optimasi Jarak Pandang)
scene.fog_color = color.black
scene.fog_density = (0.01, 0.05) 
window.color = color.black

darkness_overlay = Entity(parent=camera.ui, model='quad', color=color.black, scale=(2*camera.aspect_ratio, 2), texture=load_texture('vignette.png'), transparent=True, unlit=True, alpha=1.0, z=1)

# Lantai dan Langit-langit
ground = Entity(model='plane', scale=(250, 1, 250), color=color.white, texture=load_texture('lantai.jpg'), texture_scale=(100,100), collider='box', position=(40, -0.1, 40))
ceiling = Entity(model='plane', position=(40, 5, 40), rotation=(180, 0, 0), scale=(250, 1, 250), color=color.white, texture=load_texture('tembok.png'), texture_scale=(100,100), collider='box')

# Rumah Mencekam (C = Lemari, D = Pintu, K = Kunci, 1 = Tembok, 0 = Jalan)
maze = [
    "111111111111111111111",
    "100K0C1W0K0001000C001",
    "10000100K000100000K01",
    "100001000000D0W000001",
    "11D11111110111111D111",
    "100000000000000000001",
    "1000000K0000000000001",
    "11110111111D111111111",
    "10000100C000001C00001",
    "10K001000000000D000K1",
    "10000100C00K001000001",
    "111D11111111111111111",
    "100000000D000000000C1",
    "10K00000011D111000001",
    "111111110100LL1111111",
    "1C0000010100L01A00B01",
    "100000010100LL1000B01",
    "100K000D0100L01000B01",
    "1000W0010000000000K01",
    "111111111111111111111"
]

wall_entities = []
valid_positions = []
blood_messages = []
furniture_positions = []
corner_positions = []

for z, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == '1':
            e = Entity(
                model='cube', 
                scale=(4, 5, 4), 
                texture=load_texture('tembok.png'), 
                color=color.rgb(40/255, 40/255, 45/255), 
                collider='box', 
                position=(x*4, 2.5, z*4)
            )
            wall_entities.append(e)
            
            # Pesan Berdarah Acak
            if random.random() < 0.10: # 10% peluang per balok
                msg = random.choice(["LEAVE\nNOW", "SHE IS\nWATCHING", "NOT\nALONE", "TURN\nBACK", "DEATH"])
                # Taruh teks di dinding (offset 0.51 supaya nempel di luar parent kubus)
                t_front = Text(parent=e, text=msg, color=color.red, alpha=0, scale=2, position=(0, 0.2, -0.51), origin=(0,0))
                t_back = Text(parent=e, text=msg, color=color.red, alpha=0, scale=2, position=(0, 0.2, 0.51), origin=(0,0), rotation=(0,180,0))
                t_left = Text(parent=e, text=msg, color=color.red, alpha=0, scale=2, position=(-0.51, 0.2, 0), origin=(0,0), rotation=(0,-90,0))
                t_right = Text(parent=e, text=msg, color=color.red, alpha=0, scale=2, position=(0.51, 0.2, 0), origin=(0,0), rotation=(0,90,0))
                blood_messages.extend([t_front, t_back, t_left, t_right])
        elif cell == '0':
            # Jangan taruh di tempat spawn player (1*4, 2, 1*4)
            if not (x == 1 and z == 1):
                pos = (x*4, 0.05, z*4)
                valid_positions.append(pos)
                
                # Cek apakah ini pojok (minimal ada 2 tembok atau furniture tetangga)
                neighbor_count = 0
                for dz, dx in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nz, nx = z+dz, x+dx
                    if 0 <= nz < len(maze) and 0 <= nx < len(row):
                        if maze[nz][nx] in ('1', 'C', 'L'):
                            neighbor_count += 1
                if neighbor_count >= 2:
                    corner_positions.append(pos)
        
        # Deteksi Furnitur untuk Spawn Puncak (Furniture Surface)
        elif cell == 'W': # Kitchen Table
            furniture_positions.append((x*4, 1.15, z*4 - 1.0))
        elif cell == 'B': # Bed
            furniture_positions.append((x*4 - 1.8, 0.65, z*4))
        elif cell == 'A': # Instrument
            furniture_positions.append((x*4 + 0.5, 1.35, z*4 + 0.5))
        elif cell == 'C': # Cabinet
            furniture_positions.append((x*4, 1.0, z*4)) # Letakkan di rak yang bisa dijangkau, bukan di atas atap


# Kotak Peluru
class AmmoBox(Entity):
    def __init__(self, position):
        super().__init__(
            model='quad',
            scale=(0.8, 0.8),
            texture=load_texture('horror_ammo.png'),
            double_sided=True,
            rotation_x=90,
            collider='box',
            position=(position[0], position[1] if len(position) > 1 else 0.05, position[2])
        )

# Koleksi Buku
class Book(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            scale=(0.5, 0.8, 0.1),
            color=color.dark_gray,
            texture='white_cube',
            collider='box',
            position=position
        )

# Kunci
class Key(Entity):
    def __init__(self, position):
        super().__init__(
            model='quad',
            scale=(0.6, 0.6),
            texture=load_texture('horror_key.png'),
            double_sided=True,
            rotation_x=90,
            collider='box',
            position=(position[0], position[1] if len(position) > 1 else 0.05, position[2])
        )

# Pintu Terkunci
class Door(Entity):
    def __init__(self, position, rot_y=0, bloody=False):
        super().__init__(
            model='cube',
            scale=(3.9, 3.9, 0.2), # Sekarang pipih (x=lebar 3.9, y=tinggi 3.9, z=tebal 0.2)
            color=color.white,
            texture=load_texture('pintu_bloody.png') if bloody else load_texture('pintu.png'),
            collider='box',
            position=position,
            rotation_y=rot_y,
            origin_x=-0.5 # Engsel di pinggir kiri agar bisa berotasi layaknya pintu asli
        )
        self.is_open = False

# Lemari Kayu
class Cabinet(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            scale=(2.5, 3.5, 2.5),
            color=color.rgb(50/255, 20/255, 10/255), # Kayu Cokelat Tua
            texture='white_cube', # Polos tanpa error texture
            collider='box',
            position=position
        )

# Rak Buku Perpustakaan 3D
class Bookshelf(Entity):
    def __init__(self, position, rotation_y=0):
        super().__init__(
            model='cube',
            scale=(3.9, 4.0, 1.0),
            texture=load_texture('bookshelf.png'),
            position=position,
            rotation_y=rotation_y
        )
        from ursina import BoxCollider
        self.collider = BoxCollider(self, size=Vec3(1.05, 1.0, 1.05)) # Perlebar collider mencegah celah antar rak

# Meja Dapur (Kitchen Table)
class KitchenTable(Entity):
    def __init__(self, position):
        super().__init__(
            model=load_model('meja_dapur.glb'),
            scale=(1.2, 1.2, 1.2), # Diperbesar secara masif
            position=(position[0], 0, position[2] - 1.0), # Mundurkan agar tidak menembus pintu
            rotation_y=180, # Balik arah agar meja menghadap lorong
            collider='box'
        )

# Kasur Serem (Creepy Bed)
class CreepyBed(Entity):
    def __init__(self, position):
        super().__init__(
            model=load_model('kasur_serem.glb'),
            scale=(2.0, 2.0, 2.0), # Skala raksasa
            position=(position[0] - 1.8, 0, position[2]), # Rapatkan ke dinding kiri lorong secara agresif
            rotation_y=90, # Menghadap ke arah lorong terbuka
            collider='box'
        )

# Alat Music (Music Instrument)
class MusicInstrument(Entity):
    def __init__(self, position):
        super().__init__(
            model=load_model('alat_music.glb'),
            scale=(1.8, 1.8, 1.8), 
            position=(position[0] + 0.5, 1.3, position[2] + 0.5), # Diatur ke Y=1.3 untuk mengangkat pusat model agar menapak lantai
            rotation_y=135, 
            collider='box'
        )

# Pintu Keluar (Win State)
class ExitDoor(Entity):
    def __init__(self, position):
        super().__init__(
            model='cube',
            scale=(3.9, 4.0, 0.2),
            color=color.green,
            texture='white_cube',
            collider='box',
            position=position,
            enabled=False
        )

exit_door = ExitDoor(position=(4, 2, 4)) # Di posisi tempat player mulai

# Musuh (Hantu)
class Ghost(Entity):
    def __init__(self):
        super().__init__(
            model=load_model('kuntilanak_indonesian_ghost_patched.glb'),
            scale=(2.2, 2.2, 2.2), # Skala lebih besar supaya seram (sekitar 3.8m tinggi!)
            position=(0, -0.6, 0), # Berdiri di ground (agak tenggelam sedikit untuk atur kaki)
            collider='box'
        )
        self.active = False
        self.state = 'chasing' # Status awal
        self.look_timer = 0.0
        self.spawn_timer = 0.0
        self.flicker_timer = 0.0
        self.teleport_timer = 0.0
        self.blink_count = 0 # Menyimpan jumlah kedipan
        self.is_warning = False # Status sedang berkedip peringatan

ghost = Ghost()

# Tentukan posisi 15 buku secara acak - Prioritaskan meja/kasur
all_special = furniture_positions + corner_positions
random.shuffle(all_special)

books = []
# Ambil 15 buku dari pool spesial (furnitur + pojokan) jika cukup
book_pool = all_special[:15] if len(all_special) >= 15 else all_special + random.sample(valid_positions, 15 - len(all_special))
for p in book_pool:
    books.append(Book(position=p))
    if p in valid_positions: valid_positions.remove(p)
    if p in furniture_positions: furniture_positions.remove(p)
    if p in corner_positions: corner_positions.remove(p)

keys_list = []
# Pastikan ada 1 kunci di dekat area awal, tapi tetap acak posisinya
initial_key_pool = [p for p in valid_positions if p[0] < 20 and p[2] < 20]
if initial_key_pool:
    start_key_pos = random.choice(initial_key_pool)
    keys_list.append(Key(position=start_key_pos))
    if start_key_pos in valid_positions: valid_positions.remove(start_key_pos)
else:
    keys_list.append(Key(position=(12, 0.05, 4))) # Fallback jika tidak ada spot

# Spawn 8 kunci sisanya - Prioritaskan furnitur sisa
key_positions = random.sample(furniture_positions, min(len(furniture_positions), 8))
if len(key_positions) < 8:
    needed = 8 - len(key_positions)
    floor_spots = random.sample(valid_positions, min(len(valid_positions), needed))
    key_positions.extend(floor_spots)

for p in key_positions:
    keys_list.append(Key(position=p))
    if p in valid_positions: valid_positions.remove(p)

ammo_boxes_list = []
# Amunisi taruh di pojokan yang tersisa
ammo_pool = corner_positions[:4] if len(corner_positions) >= 4 else corner_positions + random.sample(valid_positions, 4 - len(corner_positions))
for p in ammo_pool:
    ammo_boxes_list.append(AmmoBox(position=p))
    if p in valid_positions: valid_positions.remove(p)


doors = []
cabinets = []
lembar_catatan_list = []

for z, row in enumerate(maze):
    for x, cell in enumerate(row):
        if cell == 'K':
            # keys_list.append(Key(position=(x*4, 1.5, z*4))) # Kunci sudah di-spawn secara acak
            pass
        elif cell == 'D':
            rot_y = 0
            pos_x, pos_y, pos_z = x*4, 2, z*4
            
            # Jika atas/bawah tembok dan kiri/kanan lorong, putar 90 agar membentang menutup celah
            if z > 0 and z < len(maze)-1 and x > 0 and x < len(row)-1:
                if (maze[z-1][x] == '1' or maze[z+1][x] == '1') and maze[z][x-1] != '1' and maze[z][x+1] != '1':
                    rot_y = 90
            
            # Geser titik asal (engsel) pintu sejauh setengah panjang 3.9 agar posisi aslinya persis di as tengah dinding
            if rot_y == 0:
                pos_x -= 1.95
            else:
                pos_z += 1.95
                
            is_bloody = random.random() < 0.40 # 40% peluang pintu berdarah
            doors.append(Door(position=(pos_x, pos_y, pos_z), rot_y=rot_y, bloody=is_bloody))
        elif cell == 'C':
            cabinets.append(Cabinet(position=(x*4, 1.75, z*4)))
        elif cell == 'W':
            KitchenTable(position=(x*4, 0, z*4))
        elif cell == 'B':
            CreepyBed(position=(x*4, 0, z*4))
        elif cell == 'A':
            MusicInstrument(position=(x*4, 0, z*4))
        elif cell == 'L':
            # Rotasi rak buku berdasarkan tetangganya (tembok/lorong)
            rot = 0
            if (z > 0 and z < len(maze)-1) and (x > 0 and x < len(row)-1):
                if maze[z][x-1] == '1' or maze[z][x+1] == '1' or maze[z][x-1] == 'L' or maze[z][x+1] == 'L':
                    rot = 0
                else:
                    rot = 90
            Bookshelf(position=(x*4, 2, z*4), rotation_y=rot)

jurnal_manager = JurnalManager(player)

# Lembar catatan telah dipindah ke dalam Buku Khulashoh

# Pintu dan balok tarkib telah dihapus

books_collected = 0
keys_collected = 0
message_timer = 0.0

book_text = Text(text='Books: 0/15', position=(-0.85, 0.45), scale=2, color=color.white)
key_text = Text(text='Keys: 0', position=(-0.85, 0.38), scale=2, color=color.yellow)
flashlight_text = Text(text='[Right Click] Toggle Flashlight', position=(-0.80, 0.31), scale=1.5, color=color.light_gray)
message_text = Text(text='', position=(0, 0), scale=3, color=color.red, origin=(0,0))
message_text.enabled = False
jumpscare_text = Text(text='CAUGHT!', position=(0, 0), scale=5, color=color.red, origin=(0,0))
jumpscare_text.enabled = False
interaction_text = Text(text='', position=(0, -0.15), scale=2, color=color.white, origin=(0,0))
interaction_text.enabled = False

win_bg = Entity(parent=camera.ui, model='quad', color=color.black, scale=(3, 3), z=-10, enabled=False)
win_text = Text(parent=camera.ui, text='YOU SURVIVED!\nYOU HAVE ESCAPED.', position=(0, 0), scale=4, color=color.green, origin=(0,0), z=-11, enabled=False)
game_won = False

# ================= HARI KEDUA (DAY 2) =================
day_transition_bg = Entity(parent=camera.ui, model='quad', color=color.black, scale=(3, 3), z=-10, enabled=False)
day_transition_text = Text(parent=camera.ui, text='HARI KEDUA', origin=(0,0), scale=3, color=color.red, z=-11, enabled=False)

class Chalkboard(Entity):
    def __init__(self, position, rotation_y=0):
        super().__init__(
            model='quad',
            color=color.dark_gray,
            scale=(4, 2),
            position=position,
            rotation_y=rotation_y,
            collider='box'
        )
        self.text_entity = Text(parent=self, text='Mereka bilang dia bunuh diri...\nTapi kitab itu bersimbah darah di bawah rak.', color=color.light_gray, origin=(0,0), z=-0.1, scale=1.5)

class WhiteLetter(Entity):
    def __init__(self, position):
        super().__init__(
            model='quad',
            color=color.white,
            scale=(0.5, 0.5),
            position=position,
            rotation_x=90,
            collider='box'
        )

chalkboard = Chalkboard(position=(30, 2, 30), rotation_y=0) # Place it somewhere around the center
chalkboard.enabled = False
white_letter = WhiteLetter(position=(28, 0.1, 30))
white_letter.enabled = False

letter_ui_bg = Entity(parent=camera.ui, model='quad', color=color.white, scale=(0.8, 1.2), z=-10, enabled=False, ignore_paused=True)
letter_ui_text = Text(parent=letter_ui_bg, text='لقد قتلوه\n\n(Mereka telah membunuhnya)\n\nGuru kami dibunuh di sini.', color=color.black, origin=(0,0), scale=2, position=(0,0), z=-0.1, font=ARABIC_FONT, ignore_paused=True)

def close_letter_ui():
    letter_ui_bg.enabled = False
    player.enable()
    mouse.locked = True
    global current_day
    if current_day == 2:
        exit_door.enabled = True
        message_text.text = 'YOU FOUND THE TRUTH. ESCAPE NOW!'
        message_text.color = color.green
        message_text.enabled = True
        global message_timer
        message_timer = 5.0

def start_day_2():
    global current_day, flashlight_on
    current_day = 2
    player.position = (1*4, 2, 1*4)
    player.health = max_health
    player.stamina = 100.0
    player.sanity = 100.0
    flashlight_on = True
    
    ghost.active = False
    ghost.position = (0, -10, 0)
    
    chalkboard.enabled = True
    valid_chalkboard_positions = [(x,y,z) for (x,y,z) in valid_positions if x > 10 and z > 10]
    chalkboard.position = valid_chalkboard_positions[0] if valid_chalkboard_positions else (30, 2, 30)
    chalkboard.y = 2.0
    
    white_letter.enabled = True
    white_letter.position = valid_chalkboard_positions[1] if len(valid_chalkboard_positions) > 1 else (28, 0.1, 30)
    white_letter.y = 0.5 # Put letter slightly above ground
    
    day_transition_bg.enabled = False
    day_transition_text.enabled = False
    player.enable()
    
    message_text.text = 'Cari petunjuk tentang Sang Guru...'
    message_text.color = color.red
    message_text.enabled = True
    global message_timer
    message_timer = 5.0
# ======================================================


# (Dihapus: Foto Besar / Objek Putih Raksasa yang menyebabkan visual glitch)

# ==== SISTEM EDUKASI NAHWU SHOROF (AMSILATI JILID 1-5) ====
import requests
import threading

# Data soal per kategori: {'buku': [...], 'ammo': [...], 'kunci': [...]}
qa_data = {'buku': [], 'ammo': [], 'kunci': []}

def fetch_questions_by_category(kategori, limit=15):
    """Fetch soal dari backend berdasarkan kategori (buku/ammo/kunci).
    Menggunakan timestamp untuk mencegah cache browser/proxy."""
    global qa_data
    try:
        import time as _time
        cache_bust = int(_time.time() * 1000)
        url = f"{API_BASE}?kategori={kategori}&limit={limit}&t={cache_bust}"
        req = requests.get(url, timeout=5)
        if req.status_code == 200:
            new_soal = req.json()
            qa_data[kategori].extend(new_soal)
            print(f"[FETCH] Berhasil memuat {len(new_soal)} soal kategori '{kategori}' (total pool: {len(qa_data[kategori])})")
        else:
            print(f"[FETCH] Gagal fetch soal kategori '{kategori}', HTTP status: {req.status_code}")
    except Exception as e:
        print(f"[FETCH] Error koneksi ke backend (kategori: {kategori}):", e)

def reload_questions():
    """Kosongkan seluruh pool soal lama, lalu fetch batch baru dari database.
    Dipanggil saat game pertama kali jalan DAN saat restart/game over."""
    global qa_data
    # 1. Kosongkan pool lama agar tidak ada soal sisa dari sesi sebelumnya
    qa_data['buku'].clear()
    qa_data['ammo'].clear()
    qa_data['kunci'].clear()
    print("[RELOAD] Pool soal dikosongkan. Menarik batch baru dari server...")
    
    # 2. Fetch batch baru untuk setiap kategori
    for kat in ['buku', 'ammo', 'kunci']:
        fetch_questions_by_category(kat, 15)

# Fetch data via API in background saat inisialisasi game
threading.Thread(target=reload_questions).start()

quiz_panel = Entity(parent=camera.ui, model='quad', color=color.rgba32(15, 15, 15, 245), scale=(1.4, 0.9), z=-10, enabled=False, ignore_paused=True)
quiz_title = Text(parent=quiz_panel, text='— P E R T A N Y A A N   M A U T —', position=(0, 0.35), scale=0.9, origin=(0, 0), color=color.red, z=-0.1, ignore_paused=True)
quiz_question_text = Text(parent=quiz_panel, text='', position=(0, 0.15), scale=0.8, origin=(0, 0), color=color.white, z=-0.1, font=ARABIC_FONT, ignore_paused=True)
quiz_category_label = Text(parent=quiz_panel, text='', position=(0, 0.43), scale=0.6, origin=(0, 0), color=color.yellow, z=-0.1, ignore_paused=True)
quiz_buttons = []

from ursina import Button, Func, mouse
for i in range(4):
    btn = Button(parent=quiz_panel, text=' ', position=(0, 0.04 - i*0.12), scale=(0.9, 0.10), color=color.rgba32(70, 45, 45, 230), highlight_color=color.rgba32(150, 40, 40, 240), text_color=color.white, z=-0.1, ignore_paused=True)
    if btn.text_entity: btn.text_entity.ignore_paused = True
    quiz_buttons.append(btn)

current_item_entity = None  # Entity item yang sedang di-quiz
current_item_type = None    # Tipe item: 'buku', 'ammo', atau 'kunci'
quiz_active = False
current_correct_idx = None

def show_quiz(item_entity, kategori='buku'):
    """Tampilkan kuis berdasarkan kategori item yang diambil.
    kategori: 'buku' (Nahwu), 'ammo' (I'rab), 'kunci' (Mufrodat)"""
    global current_item_entity, current_item_type, quiz_active, current_correct_idx, qa_data
    current_item_entity = item_entity
    current_item_type = kategori
    quiz_active = True
    player.disable()
    mouse.locked = False
    
    # Ambil soal dari pool kategori yang sesuai
    pool = qa_data.get(kategori, [])
    
    # Fallback darurat jika soal benar-benar kosong:
    if len(pool) == 0:
        print(f"[FALLBACK] Soal kategori '{kategori}' kosong! Melakukan fetch darurat sinkron...")
        try:
            import time as _time
            cache_bust = int(_time.time() * 1000)
            url = f"{API_BASE}?kategori={kategori}&limit=10&t={cache_bust}"
            req = requests.get(url, timeout=3)
            if req.status_code == 200:
                pool.extend(req.json())
                print(f"[FALLBACK] Berhasil tarik {len(req.json())} soal darurat kategori '{kategori}'")
        except Exception as e:
            print("[FALLBACK] Fetch darurat gagal", e)

    if len(pool) > 0:
        q = pool.pop(0)  # Menarik soal dan menghapusnya dari list
        
        # Peringatan dini: Jika stok sisa <= 2, fetch diam-diam di background untuk stok selanjutnya
        if len(pool) <= 2:
            threading.Thread(target=fetch_questions_by_category, args=(kategori, 10)).start()
    else:
        q = {
            "pertanyaan": "Koneksi terputus! Lanjutkan saja permainannya.",
            "pilihan_a": "-", "pilihan_b": "-", "pilihan_c": "-", "pilihan_d": "-",
            "kunci_jawaban": "A"
        }
    
    # Label kategori kuis
    category_labels = {
        'buku': '📖 NAHWU / SHOROF DASAR',
        'ammo': '⚔️ I\'RAB / KEDUDUKAN KALIMAT',
        'kunci': '🔑 MUFRODAT / ARTI KATA'
    }
    quiz_category_label.text = category_labels.get(kategori, 'KUIS')
        
    jawaban_map = {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    current_correct_idx = jawaban_map.get(str(q["kunci_jawaban"]).upper(), 0)
    
    # Format teks Arab agar tidak Mojibake (RTL + reshaping)
    pertanyaan_text = format_arabic(q["pertanyaan"])
    quiz_question_text.text = pertanyaan_text
    quiz_question_text.wordwrap = 50
    
    prefixes = ['A.', 'B.', 'C.', 'D.']
    opsi = [q.get("pilihan_a", "-"), q.get("pilihan_b", "-"), q.get("pilihan_c", "-"), q.get("pilihan_d", "-")]
    
    for i, btn in enumerate(quiz_buttons):
        # Format teks Arab pada pilihan jawaban
        formatted_opsi = format_arabic(opsi[i])
        btn.text = f"{prefixes[i]} {formatted_opsi}"
        if btn.text_entity:
            btn.text_entity.wordwrap = 55
            btn.text_entity.font = ARABIC_FONT
            if not hasattr(btn.text_entity, 'original_scale_set'):
                btn.text_entity.scale *= 0.7
                btn.text_entity.original_scale_set = True
            btn.text_entity.color = color.white
        btn.on_click = Func(check_answer, i, current_correct_idx)
        
    quiz_panel.enabled = True
    
    # Mencekam suasana selama kuis, dan detak jantung makin kencang
    if panting_sound.playing: panting_sound.stop()
    if footstep_sound.playing: footstep_sound.stop()
    if not heartbeat_sound.playing:
        heartbeat_sound.play()
    heartbeat_sound.volume = 1.0  # Jantung berdebar keras saat kuis

def check_answer(selected_idx, correct_idx):
    """Cek jawaban kuis. Handle 3 tipe item: buku, ammo, kunci."""
    global books_collected, keys_collected, bullets, quiz_active, message_timer
    
    if selected_idx == correct_idx:
        pickup_sound.play()
        
        # === JAWABAN BENAR: Berikan reward sesuai tipe item ===
        if current_item_type == 'buku':
            books_collected += 1
            jurnal_manager.add_unlocked_page()
            book_text.text = f'Books: {books_collected}/15'
            if current_item_entity in books:
                books.remove(current_item_entity)
            destroy(current_item_entity)
            
            if books_collected >= 15:
                exit_door.enabled = True
                message_text.text = 'SCROLLS COMPLETED!\nFIND THE GREEN EXIT AT THE START!'
                message_text.color = color.green
                message_text.enabled = True
                message_timer = 5.0
            else:
                message_text.text = 'JAWABAN BENAR! Buku diperoleh!'
                message_text.color = color.green
                message_text.enabled = True
                message_timer = 2.0
                
        elif current_item_type == 'ammo':
            bullets += 2
            ammo_text.text = f'Ammo: {bullets}'
            if current_item_entity in ammo_boxes_list:
                ammo_boxes_list.remove(current_item_entity)
            destroy(current_item_entity)
            message_text.text = 'JAWABAN BENAR! Peluru diperoleh!'
            message_text.color = color.green
            message_text.enabled = True
            message_timer = 2.0
            
        elif current_item_type == 'kunci':
            keys_collected += 1
            key_text.text = f'Keys: {keys_collected}'
            if current_item_entity in keys_list:
                keys_list.remove(current_item_entity)
            destroy(current_item_entity)
            message_text.text = 'JAWABAN BENAR! Kunci diperoleh!'
            message_text.color = color.green
            message_text.enabled = True
            message_timer = 2.0
            
        close_quiz()
    else:
        # === JAWABAN SALAH: Item tidak terambil, darah berkurang ===
        Audio('creepy_event_2.wav', autoplay=True, volume=2.0)
        player.sanity -= 20
        player.health -= 30  # Darah berkurang
        if player.health < 0: player.health = 0
        message_text.text = 'SALAH! Darah Berkurang! Item gagal diambil!'
        message_text.color = color.red
        message_text.enabled = True
        message_timer = 2.0
        
        quiz_panel.shake(duration=0.5, magnitude=0.02)
        if player.sanity < 0:
             player.sanity = 0 
        close_quiz()

def close_quiz():
    global quiz_active
    quiz_panel.enabled = False
    player.enable()
    mouse.locked = True
    quiz_active = False
    if heartbeat_sound.playing: heartbeat_sound.stop()  # Hentikan detak jantung, update loop akan nyalakan lagi jika hantu dekat
# ================= SISTEM LORE (CATATAN KIAI) =================
lore_panel = Entity(parent=camera.ui, model='quad', scale=(0.8, 0.8), color=color.rgb(230, 220, 200), enabled=False, z=-20, ignore_paused=True)
wasiat_text = (
    "WASIAT YANG TERPUTUS\n\n"
    "Muridku... Jika kau membaca tulisan yang kutorehkan dengan sisa darahku ini... berlarilah. "
    "Alif tidak hilang, dia ditarik oleh 'mereka'. Seseorang telah menanam buhul santet di sudut pesantren ini, "
    "menggunakan ayat-ayat suci yang diputarbalikkan menjadi ilmu hitam.\n\n"
    "Perutku terasa robek, paku dan kawat berduri memaksa keluar dari tenggorokanku setiap kali aku melafalkan doa pelindung. "
    "Kutukan sihir mereka terlalu kuat. Aku telah mengunci sisa penawarnya dalam 15 kitab Khulashoh. "
    "Temukan kitab-kitab itu... sebelum entitas yang membawa Alif menemukanmu.\n\n"
    "Ingat, jangan sampai salah menyusun kalimat penangkal pada pintu kayu di lorong itu, "
    "atau kau akan merasakan lehermu dirobek dari dalam sepertiku..."
)
lore_text_entity = Text(parent=lore_panel, text=wasiat_text, color=color.black, scale=1.1, position=(-0.35, 0.35), z=-0.1, ignore_paused=True)
lore_text_entity.wordwrap = 50
lore_instruction_text = Text(parent=lore_panel, text='[F] / [Klik Kiri] untuk Menutup', color=color.dark_gray, position=(0, -0.45), origin=(0, 0), scale=1, z=-0.1, ignore_paused=True)
lore_close_btn = Button(parent=lore_panel, text='Tutup [F]', position=(0, -0.35), scale=(0.3, 0.1), color=color.red, z=-0.1, ignore_paused=True)

def toggle_lore():
    from ursina import mouse
    if lore_panel.enabled:
        lore_panel.enabled = False
        player.enable()
        mouse.locked = True
    else:
        p_x, _, p_z = player.position
        if p_x < 12 and p_z < 12:
            lore_panel.enabled = True
            player.disable()
            mouse.locked = False

lore_close_btn.on_click = toggle_lore
lore_notes_list = [] # Dikosongkan, dipindah ke sistem lore_panel

# ========================================================
# ========================================================

headbob_timer = 0.0
walk_timer = 0.0

# Jumpscare overlay menggunakan gambar 2D di UI layar penuh
jumpscare_bg = Entity(parent=camera.ui, model='quad', color=color.black, scale=(3, 3), z=1, enabled=False)
jumpscare_overlay = Entity(parent=camera.ui, model='quad', texture=load_texture('kuntilanak_1.png'), scale=(1.778 * 1.5, 1.5), z=0, color=color.white, transparent=True, enabled=False)
jumpscare_blood = Entity(parent=camera.ui, model='quad', texture=load_texture('blood_splatter.png'), scale=(1.778 * 2, 2), z=-2, transparent=True, enabled=False)
game_over = False
in_menu = True

# Mulai player di jalan kosong (1, 1) x 4
player.position = (1*4, 2, 1*4)

# ================= SISTEM KABUT VOLUMETRIK (DRIFTING FOG) =================
fog_particles = []
for _ in range(55): # Turunkan sedikit dari 80 ke 55
    p = Entity(
        parent=scene,
        model='quad',
        texture='radial_gradient', # Built-in Ursina soft circle
        scale=(random.uniform(30, 60), random.uniform(30, 60)), 
        color=color.rgba32(200, 200, 200, random.randint(8, 20)), # Sedikit ditebalkan warnanya
        position=(player.x + random.uniform(-30, 30), random.uniform(-1, 5), player.z + random.uniform(-30, 30)),
        double_sided=True,
    )
    p.drift_speed_x = random.uniform(-0.8, 0.8)
    p.drift_speed_z = random.uniform(-0.8, 0.8)
    fog_particles.append(p)

# ================= MENU UTAMA & STORY =================
menu_parent = Entity(parent=camera.ui, z=-10)
menu_bg = Entity(parent=menu_parent, model='quad', texture=load_texture('menu_bg.png'), scale=(1.778*2, 2), color=color.white)
menu_vignette = Entity(parent=menu_parent, model='quad', texture=load_texture('vignette.png'), scale=(1.778*2, 2), color=color.rgba32(100, 0, 0, 200), z=-0.05)

# Text dengan drop shadow merayap
menu_title_shadow = Text(parent=menu_parent, text='Ilmu Alat:\nMisteri Nahwu Shorof', position=(0.005, 0.295), scale=3, origin=(0, 0), color=color.black, z=-0.08)
menu_title_ar = Text(parent=menu_parent, text='Ilmu Alat:\nMisteri Nahwu Shorof', position=(0, 0.3), scale=3, origin=(0, 0), color=color.red, z=-0.1)

menu_subtitle_shadow = Text(parent=menu_parent, text='BY: AREK LOMBOK', position=(0.003, 0.177), scale=1.5, origin=(0, 0), color=color.black, z=-0.08)
menu_subtitle = Text(parent=menu_parent, text='BY: AREK LOMBOK', position=(0, 0.18), scale=1.5, origin=(0, 0), color=color.white, z=-0.1)

story_bg = Entity(parent=camera.ui, model='quad', color=color.clear, scale=(1.778*2, 2), z=-15)
story_dirty = Entity(parent=camera.ui, model='quad', texture=load_texture('vignette.png'), color=color.clear, scale=(1.778*2, 2), z=-15.5)
story_text = Text(parent=camera.ui, text='', position=(0, 0), origin=(0,0), scale=2, color=color.clear, z=-16)
story_audio = None

def actual_start():
    global in_menu, story_audio
    if not in_menu: return # Hindari pemanggilan ganda
    in_menu = False
    destroy(story_bg)
    destroy(story_dirty)
    destroy(story_text)
    destroy(menu_parent)
    destroy(skip_button)
    if story_audio:
        destroy(story_audio)
    player.enable()
    mouse.locked = True
    Audio('door_slam.wav', autoplay=True, volume=2.0)

def sequence_6():
    if not in_menu: return
    story_text.text = "Namun berhati-hatilah.\nAlif tidak lagi sendiri di dalam kegelapan ini..."
    story_text.color = color.clear
    story_text.animate_color(color.red, duration=2.0)
    story_text.shake(duration=4.0, magnitude=0.005) # Efek gemetar horor
    invoke(story_text.animate_color, color.clear, duration=1.0, delay=3.5)
    invoke(actual_start, delay=5.0)

def sequence_5():
    if not in_menu: return
    story_text.text = "Satu-satunya jalan keluar adalah menyelesaikan\nteka-teki kitab yang ia tinggalkan..."
    story_text.color = color.clear
    story_text.animate_color(color.rgb(200, 50, 50), duration=1.5)
    invoke(story_text.animate_color, color.clear, duration=1.0, delay=3.0)
    invoke(sequence_6, delay=4.5)

def sequence_4():
    if not in_menu: return
    story_text.text = "Malam ini... kamu memberanikan diri\nmasuk ke dalam reruntuhan tersebut."
    story_text.color = color.clear
    story_text.animate_color(color.light_gray, duration=1.5)
    invoke(story_text.animate_color, color.clear, duration=1.0, delay=2.5)
    invoke(sequence_5, delay=4.0)

def sequence_3():
    if not in_menu: return
    story_text.text = "Jiwanya konon terperangkap dalam kutukan dimensi...\nyang hanya bisa dibuka lewat kaidah Nahwu Shorof."
    story_text.color = color.clear
    story_text.animate_color(color.light_gray, duration=1.5)
    invoke(story_text.animate_color, color.clear, duration=1.0, delay=3.5)
    invoke(sequence_4, delay=5.0)

def sequence_2():
    if not in_menu: return
    story_text.text = "Konon, ia mencoba menembus rahasia alam ghaib...\nmenggunakan bacaan terlarang dari kitab Nahwu Shorof."
    story_text.color = color.clear
    story_text.animate_color(color.white, duration=1.5)
    invoke(story_text.animate_color, color.clear, duration=1.0, delay=3.5)
    invoke(sequence_3, delay=5.0)

def sequence_1():
    if not in_menu: return
    story_text.text = "Tahun 1998...\nSebuah pesantren tua ditutup rapat pasca\nhilangnya seorang santri bernama Alif."
    story_text.color = color.clear
    story_text.animate_color(color.white, duration=1.5)
    invoke(story_text.animate_color, color.clear, duration=1.0, delay=3.5)
    invoke(sequence_2, delay=5.0)

def start_game():
    global story_audio
    play_button.enabled = False
    quit_button.enabled = False
    skip_button.enabled = True
    Audio('ambient.wav', autoplay=True, volume=1.0) # Mainkan suara ambient awal pembuka
    story_audio = Audio('heartbeat.wav', autoplay=True, volume=0.7, loop=True) # Tambah detak jantung pelan merinding
    story_bg.animate_color(color.black, duration=2.0)
    story_dirty.animate_color(color.rgba32(150, 0, 0, 100), duration=20.0) # Pelan-pelan vignette merah merayap menjadi lebih gelap
    invoke(sequence_1, delay=3.0)
    
def quit_game():
    application.quit()

from ursina import Button
play_button = Button(parent=menu_parent, text='—   M U L A I   —', position=(0, -0.1), scale=(0.55, 0.09), color=color.rgba32(100, 30, 30, 240), highlight_color=color.rgba32(220, 30, 30, 200), pressed_color=color.rgba32(255, 50, 50, 255), text_color=color.white, on_click=start_game, z=-0.1)
quit_button = Button(parent=menu_parent, text='—   K E L U A R   —', position=(0, -0.22), scale=(0.55, 0.09), color=color.rgba32(100, 30, 30, 240), highlight_color=color.rgba32(220, 30, 30, 200), pressed_color=color.rgba32(255, 50, 50, 255), text_color=color.white, on_click=quit_game, z=-0.1)
skip_button = Button(text='Skip Story >>', position=(0.75, -0.45), scale=(0.2, 0.05), color=color.black66, enabled=False, on_click=actual_start, z=-20)

# Atur ukuran teks agar lebih proporsional elegan dan memastikan warnanya terang
if play_button.text_entity: 
    # Gunakan *= agar teks tidak gepeng (inverse scale dari button terjaga)
    play_button.text_entity.scale *= 1.3
    play_button.text_entity.color = color.white
if quit_button.text_entity: 
    quit_button.text_entity.scale *= 1.3
    quit_button.text_entity.color = color.white
if skip_button.text_entity:
    skip_button.text_entity.color = color.white

# Saat pertama kali game dibuka, tahan pergerakan
player.disable()
mouse.locked = False
# ===============================================
handgun = Entity(
    parent=camera.ui,
    model='quad',
    texture=load_texture('123.png'),
    scale=(0.6 * camera.aspect_ratio, 0.6), # Diperkecil sedikit
    position=(0.3, -0.4, 0), # Agak ke kanan, di sebelah kiri Ammo
    color=color.white # Jangan digelapkan
)

# Crosshair bidikan sederhana
crosshair = Entity(parent=camera.ui, model='circle', color=color.rgba(255, 255, 255, 100), scale=0.01)

def update():
    global books_collected, keys_collected, bullets
    global message_timer, ambient_event_timer, poltergeist_timer
    global game_over, flashlight_on, walk_timer, in_menu, game_won, step_triggered
    
    if in_menu:
        pulse_scale = 3.0 + math.sin(time.time() * 2) * 0.05
        menu_title_ar.scale = pulse_scale
        menu_title_shadow.scale = pulse_scale
        
        pulse_sub = 1.5 + math.sin(time.time() * 2) * 0.02
        menu_subtitle.scale = pulse_sub
        menu_subtitle_shadow.scale = pulse_sub
        return

    if game_over:
        return

    if game_won:
        return
        
    jumpscare_active_now = False
        
    # Update Kabut Volumetrik
    for p in fog_particles:
        p.look_at_2d(camera.position, 'y') # Billboarding wajah ke arah pemain
        p.x += p.drift_speed_x * time.dt
        p.z += p.drift_speed_z * time.dt
        
        # Teleport jika terlalu jauh dari player agar partikel tidak habis dan selalu mengelilingi pemain
        dist_p = math.hypot(p.x - player.x, p.z - player.z)
        if dist_p > 35:
            p.x = player.x + random.uniform(-30, 30)
            p.z = player.z + random.uniform(-30, 30)
            p.y = random.uniform(-1, 5)

    if exit_door.enabled and distance(player, exit_door) < 3.0:
        if current_day == 1:
            day_transition_bg.enabled = True
            day_transition_text.enabled = True
            player.disable()
            invoke(start_day_2, delay=3.0)
            exit_door.enabled = False
        else:
            win_bg.enabled = True
            win_text.enabled = True
            player.disable()
            game_won = True
        return

    # --- SISTEM KEAMANAN POSISI (ANTI TRAAPPED) ---
    global last_safe_pos, safe_timer
    safe_timer += time.dt
    if safe_timer > 0.5:
        safe_timer = 0
        # Cek jika player terjepit di dalam tembok maze
        x_idx = int(round(player.x / 4))
        z_idx = int(round(player.z / 4))
        
        is_in_wall = False
        if 0 <= z_idx < len(maze) and 0 <= x_idx < len(maze[0]):
            if maze[z_idx][x_idx] == '1':
                is_in_wall = True
        
        # Jika di luar batas maze atau jatuh ke jurang dalam, kembalikan ke posisi aman
        if is_in_wall or player.y < -5.0 or player.y > 10:
            player.position = last_safe_pos
            print(f"[DEBUG] Player Out of Bounds/Fell! Resetting to {last_safe_pos}")
        else:
            # Update posisi aman jika sedang berpijak di area yang masuk akal
            if player.y > -0.5 and player.y < 3:
                last_safe_pos = player.position
    
    # Floor snapping manual: Pastikan kaki tidak amblas di bawah lantai (lantai ada di -0.1, kita kunci di 0.0)
    if player.y < 0.0:
        player.y = 0.0
    # -----------------------------------------------
        
    if quiz_active or getattr(jurnal_manager, 'is_open', False):
        return # Pause segala elemen permainan (hantu, ketahanan, dll) selama kuis/jurnal!
    
    if message_timer > 0:
        message_timer -= time.dt
        if message_timer <= 0:
            message_text.enabled = False

    # Deklarasikan is_moving di awal supaya tidak terjadi UnboundLocalError
    # Deteksi pergerakan (Hanya tombol, untuk menghindari AttributeError)
    moving_keys = held_keys['w'] or held_keys['a'] or held_keys['s'] or held_keys['d'] or \
                  held_keys['up arrow'] or held_keys['down arrow'] or held_keys['left arrow'] or held_keys['right arrow']
    is_moving = moving_keys # Kembali ke tombol saja untuk kompatibilitas

    # Alternatif kontrol arah pandangan menggunakan tombol Panah (Kiri, Kanan, Atas, Bawah) 
    # untuk mengatasi Touchpad yang tidak merespon saat menekan tombol WASD secara bersamaan
    if held_keys['left arrow']:
        player.rotation_y -= 150 * time.dt
    if held_keys['right arrow']:
        player.rotation_y += 150 * time.dt
    if held_keys['up arrow']:
        camera.rotation_x -= 100 * time.dt
    if held_keys['down arrow']:
        camera.rotation_x += 100 * time.dt
    camera.rotation_x = max(-90, min(90, camera.rotation_x))

    # Logika Sistem Detak Jantung Jarak Dekat & Vignette Merah
    dist_to_ghost = distance(player, ghost) if ghost.active else 999
    
    # Logika Sistem Detak Jantung Jarak Dekat
    if ghost.active and dist_to_ghost < 15:
        if not heartbeat_sound.playing:
            heartbeat_sound.play()
        heartbeat_sound.volume = 1.0 - (dist_to_ghost / 15.0)
        heartbeat_sound.pitch = 1.0 + (1.0 - (dist_to_ghost / 15.0)) * 0.5
        
        # Efek Pulsing Vignette Darah HANYA BILA senter tidak sedang kedap-kedip mati
        if not getattr(ghost, 'is_warning', False) and flashlight_on:
            pulse = (math.sin(time.time() * 5) + 1) / 2 # Nilai berayun 0 sampai 1
            darkness_overlay.color = color.rgba32(120, int(50 * pulse), int(50 * pulse), 255) # Vignette Silent Hill merah kusam
            
    # Efek Senter (Menyala/Mati)
    if held_keys['right mouse'] or held_keys['q'] or held_keys['f']:
        pass # Handle dengan fungsi input agar tidak nyala matikan terus saat tombol ditahan
    # Senter secara normal disesuaikan dengan state 'flashlight_on'
    # KECUALI jika sedang dalam fase flicker (kedap-kedip berkedip mati)
    if not getattr(ghost, 'is_warning', False):
        if flashlight_on:
            flashlight.enabled = True
        else:
            flashlight.enabled = False
        
    # Senter Flicker jika hantu dekat
    if flashlight_on:
        scene.fog_density = 0.05
        
        if (ghost.active and dist_to_ghost < 15):
            # Dynamic fog: semakin dekat, kabut semakin pekat
            scene.fog_density = (max(2, dist_to_ghost/2), max(5, dist_to_ghost*1.5))
            
            # Sistem 3-kedipan peringatan
            if ghost.blink_count < 3:
                ghost.flicker_timer -= time.dt
                if ghost.flicker_timer <= 0:
                    if not ghost.is_warning: # Jika sedang nyala, matikan sekejap
                        darkness_overlay.texture = None
                        darkness_overlay.color = color.black
                        darkness_overlay.alpha = 1.0
                        flashlight.enabled = False
                        ghost.is_warning = True
                        ghost.flicker_timer = 0.8 # Matinya diperlama menjadi nyaris 1 detik
                    else: # Jika sedang mati, nyalakan kembali dan tambah hitungan
                        darkness_overlay.texture = 'vignette.png'
                        darkness_overlay.color = color.black
                        darkness_overlay.alpha = 0.95
                        flashlight.enabled = True
                        ghost.is_warning = False
                        ghost.blink_count += 1
                        ghost.flicker_timer = 0.4 # Nyala selama 0.4 detik (jeda antar kedip)
            else:
                # Setelah 3 kali kedip, senter stabil menyala
                darkness_overlay.texture = 'vignette.png'
                darkness_overlay.color = color.black
                darkness_overlay.alpha = 0.95
                flashlight.enabled = True
                
        else:
            scene.fog_density = (8, 30)
            darkness_overlay.texture = 'vignette.png'
            darkness_overlay.color = color.black
            darkness_overlay.alpha = 0.98
            # Reset ukuran efek senter saat jauh
            darkness_overlay.scale = (2*camera.aspect_ratio, 2)
            # Reset penghitung kedipan jika hantu menjauh/hilang
            ghost.blink_count = 0
            ghost.is_warning = False
            ghost.flicker_timer = 0
            
    else:
        # JANGANKAN JAUH, SEKAT SAJA SUDAH GELAP TOTAL JIKA SENTER MATI
        scene.fog_density = (2, 10) if (ghost.active and dist_to_ghost < 15) else (1, 8) 
        darkness_overlay.texture = None
        darkness_overlay.color = color.black
        darkness_overlay.alpha = 1.0 # Benar-benar hitam pekat
        flashlight.enabled = False
        
        # Volume langkah kaki diatur secara global dalam blok pergerakan di bawah
        pass

    # Flashlight beam shrinking effect (Vignette mengecil)
    if flashlight_on and ghost.active and dist_to_ghost < 12:
        # Semakin dekat, skala vignette semakin mengecil membatasi pandangan periferal
        shrink_factor = max(1.0, dist_to_ghost / 10.0)
        # Skala original 2, minimum 1.0
        darkness_overlay.scale = (2 * shrink_factor * camera.aspect_ratio, 2 * shrink_factor)
        
    # Layar bergetar jika hantu sangat dekat
    if ghost.active and dist_to_ghost < 8:
        # Shake intensity berdasarkan jarak
        shake_amt = (8 - dist_to_ghost) * 0.005
        camera.x += random.uniform(-shake_amt, shake_amt)
        camera.y += random.uniform(-shake_amt, shake_amt)

    # Pesan Berdarah Teror (Muncul ketika sudah mengambil minimal 3 buku)
    if books_collected > 2:
        for bm in blood_messages:
            if bm.alpha < 0.8: # Maksimal kepudaran 80% mirip rembesan darah
                bm.alpha += time.dt * 0.05
                
    # Logika Stamina & Sprint
    if is_moving and held_keys['left shift'] and player.stamina > 0:
        player.speed = 5.8 # Sprint speed sedikit diperlambat
        player.stamina -= time.dt * 20
        if player.stamina < 0: player.stamina = 0
    else:
        player.speed = 3.2 # Walk speed sedikit diperlambat
        if player.stamina < 100:
            player.stamina += time.dt * 10
            if player.stamina > 100: player.stamina = 100
            
    # Goyangan Kamera Berjalan (Handled in immersion block)
    pass

            
    # Update UI Stamina Bar
    stamina_bar.scale_x = (player.stamina / 100.0) * 0.4
    if player.stamina < 30:
        stamina_bar.color = color.red
    else:
        stamina_bar.color = color.green
    
    # Update ukuran bar darah & kedip-kedip saat kritis
    health_bar.scale_x = max(0, (player.health / max_health) * 0.4)
    if player.health > 0 and player.health < 30:
        # Kedap-kedip
        health_bar.color = color.red if (time.time() * 5) % 2 < 1 else color.clear
    else:
        health_bar.color = color.red

    # Logika Sanity (Mental)
    if not flashlight_on:
        player.sanity -= time.dt * 3.0 # Turun jika di kegelapan (sekitar 33 detik untuk habis)
        if player.sanity < 0: player.sanity = 0
    else:
        player.sanity += time.dt * 10 # Cepat pulih jika senter menyala
        if player.sanity > 100: player.sanity = 100
        
    # Efek Kritis / Sanity Rendah (Kamera Miring Goyang Kanan-Kiri Oleng)
    if player.health < 30:
        # Darah kritis membuat sangat oleng
        camera.rotation_z = math.sin(time.time() * 3.0) * ((30 - player.health) / 1.5)
    elif player.sanity < 50:
        # Semakin gila, semakin miring sumbu Z
        camera.rotation_z = math.sin(time.time() * 3.5) * (50 - player.sanity) / 8.0
    else:
        # Stabilkan perlahan jika waras
        camera.rotation_z += (0 - camera.rotation_z) * time.dt * 5

    # Logika Panting Audio (Karena capek lari ATAU panik ketakutan)
    if player.stamina < 30 or player.sanity < 50:
        if not panting_sound.playing: panting_sound.play()
    else:
        if panting_sound.playing: panting_sound.stop()



    # Deteksi koleksi buku (Kuis Nahwu Shorof — kategori 'buku')
    for b in list(books):
        if distance(player, b) < 2:
            if not quiz_active:
                show_quiz(b, 'buku')

                
    # Logika Audio Ambien Acak (Creepy Events)
    ambient_event_timer -= time.dt
    if ambient_event_timer <= 0:
        event_audio = random.choice(creepy_events)
        if not event_audio.playing:
            event_audio.pitch = random.uniform(0.8, 1.2) # Beri sedikit variasi frekuensi
            event_audio.play()
        # Reset timer 30 sampai 90 detik
        ambient_event_timer = random.uniform(30.0, 90.0)

    # Jumpscare Halus (Poltergeist Door Slam)
    poltergeist_timer -= time.dt
    if poltergeist_timer <= 0:
        # Cari pintu yang tertutup di radius menengah (cukup jauh agar tak terlihat langsung tapi kedengaran)
        closed_doors = [d for d in doors if not d.is_open and 15 < distance(player, d) < 40]
        if closed_doors:
            target_door = random.choice(closed_doors)
            from ursina import curve
            # Banting buka dengan sangat cepat (0.15 detik)
            target_door.animate_rotation_y(target_door.rotation_y + 90, duration=0.15, curve=curve.linear)
            target_door.is_open = True
            
            # Putar suara bantingan keras (pitch dinaikkan sedikit agar melengking/keras)
            slam_sound = Audio('door_slam.wav', autoplay=False, volume=2.0)
            slam_sound.pitch = random.uniform(0.9, 1.1)
            slam_sound.play()
            
        # Reset timer
        poltergeist_timer = random.uniform(60.0, 180.0)

    # Deteksi Pintu Terkunci
    near_door = None
    for d in doors:
        if getattr(d, 'is_open', False):
            continue
            
        # Pakai jarak dari posisi bawah agar radius collider box bisa terjangkau tanpa ter-block oleh ketinggian player_origin
        d_pos = Vec3(d.position.x, 0, d.position.z)
        p_pos = Vec3(player.position.x, 0, player.position.z)
        
        if distance(d_pos, p_pos) < 5.0:
            near_door = d
            break # Cukup deteksi 1 pintu terdekat
            
    if near_door:
        if keys_collected > 0:
            interaction_text.text = '[E] Unlock Door'
            interaction_text.enabled = True
            if held_keys['e']:
                keys_collected -= 1
                key_text.text = f'Keys: {keys_collected}'
                unlock_sound.play()
                door_open_sound.play()
                near_door.is_open = True
                near_door.collider = None
                from ursina import curve
                near_door.animate_rotation_y(near_door.rotation_y + 90, duration=1.0, curve=curve.in_out_sine)
                interaction_text.enabled = False
        else:
            interaction_text.text = 'LOCKED (Need a Key)'
            interaction_text.enabled = True
    else:
        # Cek Interaksi Ambil Kunci (Kuis Mufrodat — kategori 'kunci')
        near_key = None
        for k in keys_list:
            if distance(player, k) < 2.5:
                near_key = k
                break
        
        if near_key:
            interaction_text.text = '[E] Ambil Kunci (Kuis Mufrodat)'
            interaction_text.enabled = True
            if held_keys['e']:
                if not quiz_active:
                    show_quiz(near_key, 'kunci')
                interaction_text.enabled = False
        else:
            # Cek Interaksi Ambil Ammo (Kuis I'rab — kategori 'ammo')
            near_ammo = None
            for a in ammo_boxes_list:
                if distance(player, a) < 2.5:
                    near_ammo = a
                    break
            
            if near_ammo:
                interaction_text.text = '[E] Ambil Peluru (Kuis I\'rab)'
                interaction_text.enabled = True
                if held_keys['e']:
                    if not quiz_active:
                        show_quiz(near_ammo, 'ammo')
                    interaction_text.enabled = False
            else:
                interaction_text.enabled = False

    # Lembar catatan telah dipindah ke dalam Buku Khulasoh

    # Blok interaksi puzzle Tarkib lama dihapus

    # Deteksi Interaksi Dokumen Lore
    
    # Day 2 interactions
    if current_day == 2 and white_letter.enabled and distance(player, white_letter) < 3.0:
        interaction_text.text = '[F] Baca Surat'
        interaction_text.enabled = True
        if held_keys['f'] and not letter_ui_bg.enabled:
            letter_ui_bg.enabled = True
            player.disable()
            mouse.locked = False

    p_x, _, p_z = player.position
    if p_x < 12 and p_z < 12 and not lore_panel.enabled and not quiz_active and not getattr(jurnal_manager, 'is_open', False):
        if not interaction_text.enabled:
            interaction_text.text = '[F] Baca Catatan Kyai'
            interaction_text.enabled = True

    # Hantu semakin lincah dan haus darah seiring bertambahnya kitab yang diambil
    difficulty_multiplier = books_collected / 8.0 # 0.0 sampai 1.0
    spawn_delay_limit = 4.0 - (difficulty_multiplier * 3.7) # Dari 4s turun drastis ke 0.3s (Sangat cepat muncul)
    creep_move_speed = 1.5 + (difficulty_multiplier * 3.5) # Dari 1.5 naik drastis melampaui lari player (max 5.0!)
    jumpscare_threshold = 3.0 - (difficulty_multiplier * 2.5) # Dari 3.0s turun drastis ke 0.5s (Sangat mematikan)

    # ============ LOGIKA HANTU (DO NOT MOVE) ============
    if not ghost.active:
        ghost.spawn_timer += time.dt
        if ghost.spawn_timer > spawn_delay_limit: 
            spawn_p = random.choice(valid_positions)
            if distance(player, spawn_p) > 15 and distance(player, spawn_p) < 30: # Jarak muncul lebih jauh
                ghost.position = spawn_p
                ghost.active = True
                ghost.look_timer = 0
                ghost.spawn_timer = 0
                ghost.state = 'chasing'
    else:
        p_to_g = ghost.position - player.position
        p_to_g_dir = p_to_g.normalized()
        dist = distance(player, ghost)
        p_to_g_2d = Vec3(p_to_g.x, 0, p_to_g.z).normalized()
        cam_forward_2d = Vec3(camera.forward.x, 0, camera.forward.z).normalized()
        
        is_looking = cam_forward_2d.dot(p_to_g_2d) > 0.65 # Deteksi mata lebih sempit (harus lebih tepat menatap hantu agar terhitung)
        
        if ghost.active and random.random() < 0.02:
             print(f"[STATUS] Jarak: {dist:.1f}, Menatap: {is_looking}, Timer Mati: {ghost.look_timer:.1f}, Timer Merayap: {ghost.teleport_timer:.1f}")
        
        ghost.y = 0.0
        ghost.look_at_2d(player.position, 'y')

        if is_looking or dist < 4.0:
            head_pos = player.position + Vec3(0, 2.7, 0) # Tinggi Pandangan Mata (Fisik)
            target_pos = ghost.position + Vec3(0, 2.7, 0) # Target Mata Hantu (Fisik)
            ray_dir = (target_pos - head_pos).normalized()
            ui_ignores = (handgun, darkness_overlay, jumpscare_bg, jumpscare_overlay, jumpscare_blood, crosshair, stamina_bar, health_bar, stamina_text, ammo_text, book_text, key_text, flashlight_text, message_text, jumpscare_text, interaction_text)
            hit = raycast(head_pos, ray_dir, distance=max(0.1, dist - 2.5), ignore=(player, ghost, ground, ceiling) + ui_ignores)
            
            is_blocked = False
            if hit.hit:
                if hit.entity in wall_entities or isinstance(hit.entity, (Door, Cabinet, Bookshelf)):
                    if not getattr(hit.entity, 'is_open', False):
                        is_blocked = True
            
            if dist < 3.5:
                is_blocked = False
                    
            if not is_blocked:
                if is_looking:
                    ghost.look_timer += time.dt
                    ghost.teleport_timer = 0.0
                
                if dist < 3.5:
                    ghost.look_timer += time.dt * 2.0
                
                is_jumpscare = is_looking and (ghost.look_timer > jumpscare_threshold or dist < 2.0)
                if is_jumpscare:
                    jumpscare_active_now = True
                    player.health -= time.dt * 60.0
                    if not jumpscare_overlay.enabled:
                        jumpscare_sound.play()
                        footstep_sound.stop()
                        ambient_sound.stop()
                        if heartbeat_sound.playing: heartbeat_sound.stop()
                        if panting_sound.playing: panting_sound.stop()
                        jumpscare_overlay.enabled = True
                        jumpscare_overlay.color = color.white
                        jumpscare_overlay.scale = (1.778 * 1.3, 1.3)
                        jumpscare_overlay.animate_scale((1.778 * 1.5, 1.5), duration=2)
                        darkness_overlay.enabled = True
                        darkness_overlay.texture = 'vignette.png'
                        darkness_overlay.color = color.red
                        darkness_overlay.alpha = 0.95
                        darkness_overlay.z = -1
                        jumpscare_blood.enabled = True
                        jumpscare_blood.color = color.white
                        jumpscare_blood.scale = (1.778 * 1.8, 1.8)
                        jumpscare_blood.animate_scale((1.778 * 2.2, 2.2), duration=1.5)
                        jumpscare_overlay.shake(duration=2.0, magnitude=0.05)
                        
                    if player.health <= 0 and not game_over:
                        player.health = 0
                        player.disable()
                        mouse.locked = False
                        game_over = True
                        window.color = color.black
                        jumpscare_overlay.enabled = False
                        jumpscare_blood.enabled = False
                        
                        import sys, os
                        def restart_game():
                            # Kosongkan soal lama sebelum restart proses
                            qa_data['buku'].clear()
                            qa_data['ammo'].clear()
                            qa_data['kunci'].clear()
                            print("[RESTART] Pool soal dikosongkan. Memulai ulang game...")
                            os.execl(sys.executable, sys.executable, *sys.argv)
                            
                        Button(parent=camera.ui, text="KEMBALI KE MENU", scale=(0.4, 0.1), position=(0, -0.2), color=color.dark_gray, text_color=color.red, highlight_color=color.black, on_click=restart_game, z=-20)
                        Text(parent=camera.ui, text="KAMU MATI", scale=5, color=color.red, origin=(0, 0), position=(0, 0.1), z=-20)
            else:
                ghost.look_timer -= time.dt * 0.3
        else:
            ghost.look_timer -= time.dt * 1.0
            if dist > 2.0 and dist < 100.0:
                ghost.teleport_timer += time.dt
                if ghost.teleport_timer > 3.0: 
                    move_speed = creep_move_speed
                    move_dir = Vec3(-p_to_g.x, 0, -p_to_g.z).normalized()
                    tp_hit = raycast(ghost.position + Vec3(0,2.7,0), move_dir, distance=0.5, ignore=(player, ghost, ground, ceiling))
                    if not tp_hit.hit:
                        ghost.position += move_dir * move_speed * time.dt
                        ghost.look_at_2d(player.position, 'y')
                        
            if held_keys['left shift'] and ghost.active and dist < 25 and camera.forward.dot(p_to_g_dir) < -0.2:
                ghost.active = False
                ghost.position = (0, -10, 0)
                ghost.look_timer = 0
                ghost.teleport_timer = 0
                
        if ghost.look_timer < 0:
            ghost.look_timer = 0
            
        if dist > 100:
            ghost.active = False
            ghost.position = (0, -10, 0)
            ghost.look_timer = 0
            ghost.teleport_timer = 0
            
    if not jumpscare_active_now:
        jumpscare_overlay.enabled = False
        jumpscare_overlay.color = color.clear
        jumpscare_blood.enabled = False
        jumpscare_blood.color = color.clear

    # ================= PENGUNCI TINGGI & IMMERSION AKHIR =================
    # Skala harus tetap normal
    player.scale = (1, 1, 1)

    # Pemicu Bobbing: Hanya jika menekan tombol jalan DAN sedang menyentuh tanah (grounded)
    is_walking = is_moving and getattr(player, 'grounded', True)
    
    if is_walking and not quiz_active:
        # 1. Hitung Bobbing
        # Gunakan time.dt yang dibatasi untuk kestabilan saat lag
        dt = min(time.dt, 0.05)
        bob_speed = 7 if held_keys['left shift'] else 5
        walk_timer += dt * bob_speed
        
        bob_offset = math.sin(walk_timer) * 0.12 # Efek naik turun diperkuat
        tilt_offset = math.sin(walk_timer * 0.5) * 0.05
        
        # 2. Terapkan ke Kamera (Naik-Turun & Miring)
        if hasattr(player, 'camera_pivot'):
            player.camera_pivot.y = 2.7 + bob_offset
        camera.y = tilt_offset
        
        # 3. Audio Langkah Kaki Sinkron (Mainkan saat kaki menghujam tanah / trough sin wave)
        # Gunakan threshold sin < -0.8 untuk memicu suara langkah sekali per ayunan
        sin_val = math.sin(walk_timer)
        if sin_val < -0.8:
            if not step_triggered:
                footstep_sound.volume = 2.5 # Pastikan volume cukup keras
                footstep_sound.play()
                step_triggered = True
        elif sin_val > 0:
            # Reset trigger saat kaki sudah di posisi atas
            step_triggered = False
    else:
        # Kembali ke baseline saat diam atau saat melompat/jatuh
        walk_timer = 0
        step_triggered = False
        if hasattr(player, 'camera_pivot'):
            # Interpolasi smooth kembali ke 2.7
            player.camera_pivot.y = lerp(player.camera_pivot.y, 2.7, time.dt * 10)
        camera.y = lerp(camera.y, 0, time.dt * 10)
        
        if footstep_sound.playing:
            footstep_sound.stop()
    
    # Debug logic removed for cleaner gameplay
    pass

def input(key):
    global bullets, flashlight_on, quiz_active, current_correct_idx, in_menu
    
    if lore_panel.enabled:
        if key == 'left mouse down' or key == 'f':
            toggle_lore()
        return

    if key == 'f' and not in_menu and not quiz_active:
        p_x, _, p_z = player.position
        if p_x < 12 and p_z < 12:
            toggle_lore()
            return

    
    if letter_ui_bg.enabled:
        if key == 'left mouse down':
            close_letter_ui()
        return

    if in_menu:

        return
        
    if key == 'tab':
        if not quiz_active and not in_menu:
            jurnal_manager.toggle_jurnal()

    if quiz_active:
        if key in ['1', 'a']:
            check_answer(0, current_correct_idx)
        elif key in ['2', 'b']:
            check_answer(1, current_correct_idx)
        elif key in ['3', 'c']:
            check_answer(2, current_correct_idx)
        elif key in ['4', 'd']:
            check_answer(3, current_correct_idx)
        return

    # Toggle Senter pakai Klik Kanan atau Q
    if key == 'right mouse down' or key == 'q':
        flashlight_on = not flashlight_on
        print(f"Senter di-toggle! Status Senter: {'NYALA' if flashlight_on else 'MATI'}")

    # Logika Menembak Pistol pakai Klik Kiri
    if key == 'left mouse down' and bullets > 0:
        bullets -= 1
        ammo_text.text = f'Ammo: {bullets}'
        
        # Audio Tembakan
        s = Audio('mrfriends-pistol-shot-233473.mp3', autoplay=True, volume=1.5)
        destroy(s, delay=2.0)
        
        # Efek Recoil
        handgun.animate_position((0.3, -0.3, 0), duration=0.05)
        invoke(handgun.animate_position, (0.3, -0.4, 0), duration=0.1, delay=0.05)
        
        # Efek Layar Kejut
        darkness_overlay.color = color.white
        invoke(setattr, darkness_overlay, 'color', color.rgba(255, 0, 0, 0), delay=0.1)
        
        # Raycast Tembakan
        hit_info = raycast(camera.world_position, camera.forward, distance=100, ignore=(player, ground, ceiling, handgun))
        
        if hit_info.hit and hit_info.entity == ghost:
            ghost.color = color.orange
            Audio('creepy_event_3.wav', autoplay=True, volume=2.0, pitch=1.8)
            ghost.active = False
            ghost.position = (0, -50, 0)
            ghost.spawn_timer = -30.0
            invoke(setattr, ghost, 'color', color.white, delay=30)

class GameController(Entity):
    def input(self, key):
        if key == 'escape':
            application.quit()

game_controller = GameController()

app.run()
