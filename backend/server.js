const express = require('express');
const mysql = require('mysql2');
const cors = require('cors');

const app = express();
app.use(cors());
app.use(express.json());

// ==================== KONFIGURASI ====================
// URL Resmi GitHub Releases Game Kamu
const GITHUB_RELEASE_URL = "https://github.com/syauqiquthbi210-prog/my-game/releases/download/v1.0/HuntedByKuntilanak-Windows.1.zip";

// Konfigurasi koneksi database MySQL
const db = mysql.createConnection({
    host: 'localhost',
    user: 'root',
    password: '12345',
    database: 'db_game_edukasi'
});

db.connect((err) => {
    if (err) {
        console.error('Gagal terhubung ke MySQL:', err);
        return;
    }
    console.log('Berhasil terhubung ke database MySQL db_game_edukasi.');
});

// ==================== FASE 1: LANDING PAGE HOROR ====================
app.get('/', (req, res) => {
    res.send(`
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="Misteri Kyai Abdullah — Game horor edukasi Nahwu Shorof berbasis pesantren terkutuk. Download gratis untuk Windows.">
    <title>Misteri Kyai Abdullah — Download Game Horor Edukasi</title>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel+Decorative:wght@700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&family=Amiri&display=swap" rel="stylesheet">
    <style>
        *, *::before, *::after { margin: 0; padding: 0; box-sizing: border-box; }

        body {
            min-height: 100vh;
            background: #0a0a0a;
            color: #c8c8c8;
            font-family: 'Crimson Text', 'Georgia', serif;
            overflow-x: hidden;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            position: relative;
        }

        /* ===== BACKGROUND PARTICLE EFFECT ===== */
        .particles {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0;
            overflow: hidden;
        }
        .particle {
            position: absolute;
            width: 2px; height: 2px;
            background: rgba(180, 30, 30, 0.4);
            border-radius: 50%;
            animation: float-up linear infinite;
        }
        @keyframes float-up {
            0%   { transform: translateY(100vh) scale(1); opacity: 0; }
            10%  { opacity: 1; }
            90%  { opacity: 0.6; }
            100% { transform: translateY(-10vh) scale(0.3); opacity: 0; }
        }

        /* ===== VIGNETTE OVERLAY ===== */
        .vignette {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            background: radial-gradient(ellipse at center, transparent 40%, rgba(0,0,0,0.85) 100%);
            pointer-events: none;
            z-index: 1;
        }

        /* ===== BLOOD DRIP FROM TOP ===== */
        .blood-drips {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 60px;
            pointer-events: none;
            z-index: 2;
            display: flex;
            justify-content: space-around;
        }
        .drip {
            width: 3px;
            background: linear-gradient(to bottom, #8b0000, #5a0000, transparent);
            border-radius: 0 0 50% 50%;
            animation: drip-down ease-in infinite;
            opacity: 0.6;
        }
        @keyframes drip-down {
            0%   { height: 0; opacity: 0; }
            30%  { opacity: 0.7; }
            100% { height: 120px; opacity: 0; }
        }

        /* ===== FOG MIST ===== */
        .fog {
            position: fixed;
            bottom: 0; left: -10%;
            width: 120%; height: 200px;
            background: linear-gradient(to top, rgba(20,20,20,0.9), transparent);
            pointer-events: none;
            z-index: 1;
            animation: fog-drift 8s ease-in-out infinite alternate;
        }
        @keyframes fog-drift {
            0%   { transform: translateX(-3%); }
            100% { transform: translateX(3%); }
        }

        /* ===== MAIN CONTAINER ===== */
        .container {
            position: relative;
            z-index: 10;
            max-width: 800px;
            padding: 60px 40px;
            text-align: center;
            animation: fade-in 2s ease-out;
        }
        @keyframes fade-in {
            0% { opacity: 0; transform: translateY(30px); }
            100% { opacity: 1; transform: translateY(0); }
        }

        /* ===== BISMILLAH ===== */
        .bismillah {
            font-family: 'Amiri', serif;
            font-size: 1.6rem;
            color: rgba(180, 160, 120, 0.5);
            margin-bottom: 24px;
            direction: rtl;
            letter-spacing: 2px;
        }

        /* ===== TITLE ===== */
        .title {
            font-family: 'Cinzel Decorative', serif;
            font-size: 3.2rem;
            font-weight: 900;
            color: #b91c1c;
            text-shadow:
                0 0 20px rgba(185, 28, 28, 0.5),
                0 0 60px rgba(185, 28, 28, 0.2),
                0 4px 8px rgba(0,0,0,0.8);
            letter-spacing: 3px;
            line-height: 1.2;
            margin-bottom: 12px;
            animation: pulse-glow 4s ease-in-out infinite alternate;
        }
        @keyframes pulse-glow {
            0%   { text-shadow: 0 0 20px rgba(185,28,28,0.5), 0 0 60px rgba(185,28,28,0.2), 0 4px 8px rgba(0,0,0,0.8); }
            100% { text-shadow: 0 0 40px rgba(185,28,28,0.8), 0 0 100px rgba(185,28,28,0.4), 0 4px 8px rgba(0,0,0,0.8); }
        }

        .subtitle {
            font-family: 'Cinzel Decorative', serif;
            font-size: 0.95rem;
            color: rgba(200,200,200,0.4);
            letter-spacing: 8px;
            text-transform: uppercase;
            margin-bottom: 40px;
        }

        /* ===== DIVIDER ===== */
        .divider {
            width: 200px;
            height: 1px;
            background: linear-gradient(to right, transparent, #8b0000, transparent);
            margin: 0 auto 36px;
        }

        /* ===== LORE TEXT ===== */
        .lore {
            font-size: 1.15rem;
            line-height: 1.9;
            color: rgba(200, 190, 180, 0.75);
            font-style: italic;
            max-width: 600px;
            margin: 0 auto 20px;
            text-shadow: 0 1px 3px rgba(0,0,0,0.5);
        }
        .lore .highlight {
            color: #dc2626;
            font-style: normal;
            font-weight: 600;
        }

        .lore-warning {
            font-size: 0.95rem;
            color: rgba(139, 0, 0, 0.7);
            margin-bottom: 48px;
            letter-spacing: 1px;
        }

        /* ===== DOWNLOAD BUTTON ===== */
        .download-btn {
            display: inline-flex;
            align-items: center;
            gap: 14px;
            padding: 20px 48px;
            background: linear-gradient(135deg, #7f1d1d, #991b1b, #b91c1c);
            color: #fef2f2;
            font-family: 'Cinzel Decorative', serif;
            font-size: 1.15rem;
            font-weight: 700;
            text-decoration: none;
            border: 1px solid rgba(185, 28, 28, 0.4);
            border-radius: 4px;
            letter-spacing: 2px;
            cursor: pointer;
            position: relative;
            overflow: hidden;
            transition: all 0.4s ease;
            box-shadow:
                0 4px 20px rgba(139, 0, 0, 0.4),
                inset 0 1px 0 rgba(255,255,255,0.08);
        }
        .download-btn::before {
            content: '';
            position: absolute;
            top: 0; left: -100%;
            width: 100%; height: 100%;
            background: linear-gradient(90deg, transparent, rgba(255,255,255,0.05), transparent);
            transition: left 0.6s ease;
        }
        .download-btn:hover::before {
            left: 100%;
        }
        .download-btn:hover {
            background: linear-gradient(135deg, #991b1b, #b91c1c, #dc2626);
            transform: translateY(-3px);
            box-shadow:
                0 8px 32px rgba(185, 28, 28, 0.6),
                0 0 60px rgba(185, 28, 28, 0.2),
                inset 0 1px 0 rgba(255,255,255,0.1);
        }
        .download-btn:active {
            transform: translateY(0);
        }
        .download-btn .icon {
            font-size: 1.4rem;
        }

        /* ===== PLATFORM BADGE ===== */
        .platform {
            margin-top: 16px;
            font-size: 0.8rem;
            color: rgba(150,150,150,0.5);
            letter-spacing: 3px;
            text-transform: uppercase;
        }

        /* ===== FEATURES ===== */
        .features {
            display: flex;
            justify-content: center;
            gap: 40px;
            margin-top: 56px;
            flex-wrap: wrap;
        }
        .feature {
            text-align: center;
            max-width: 160px;
        }
        .feature .icon {
            font-size: 1.8rem;
            margin-bottom: 8px;
            filter: grayscale(0.3);
        }
        .feature .label {
            font-size: 0.85rem;
            color: rgba(180,170,160,0.6);
            line-height: 1.5;
        }

        /* ===== FOOTER ===== */
        .footer {
            position: relative;
            z-index: 10;
            margin-top: 60px;
            padding: 20px;
            font-size: 0.75rem;
            color: rgba(100,100,100,0.5);
            text-align: center;
            letter-spacing: 1px;
        }

        /* ===== RESPONSIVE ===== */
        @media (max-width: 600px) {
            .title { font-size: 2rem; }
            .container { padding: 40px 20px; }
            .download-btn { padding: 16px 32px; font-size: 1rem; }
            .features { gap: 24px; }
        }

        /* ===== FLICKERING LIGHT EFFECT ===== */
        @keyframes flicker {
            0%, 95%, 100% { opacity: 1; }
            96% { opacity: 0.4; }
            97% { opacity: 0.9; }
            98% { opacity: 0.3; }
            99% { opacity: 0.8; }
        }
        .flicker { animation: flicker 6s infinite; }
    </style>
</head>
<body>

    <!-- Background Effects -->
    <div class="particles" id="particles"></div>
    <div class="vignette"></div>
    <div class="fog"></div>
    <div class="blood-drips">
        <div class="drip" style="animation-duration:4s; animation-delay:0s;"></div>
        <div class="drip" style="animation-duration:6s; animation-delay:1s;"></div>
        <div class="drip" style="animation-duration:5s; animation-delay:2.5s;"></div>
        <div class="drip" style="animation-duration:7s; animation-delay:0.5s;"></div>
        <div class="drip" style="animation-duration:4.5s; animation-delay:3s;"></div>
        <div class="drip" style="animation-duration:6.5s; animation-delay:1.5s;"></div>
        <div class="drip" style="animation-duration:5.5s; animation-delay:2s;"></div>
    </div>

    <!-- Main Content -->
    <div class="container">
        <div class="bismillah flicker">بِسْمِ اللّٰهِ الرَّحْمٰنِ الرَّحِيْمِ</div>

        <h1 class="title">Misteri<br>Kyai Abdullah</h1>
        <div class="subtitle">Ilmu Alat: Nahwu Shorof</div>

        <div class="divider"></div>

        <p class="lore">
            Tahun <span class="highlight">1998</span>, sebuah pesantren tua ditutup rapat
            pasca hilangnya seorang santri bernama <span class="highlight">Alif</span>.
            Konon, sang Kyai mencoba menembus rahasia alam ghaib menggunakan
            bacaan terlarang dari kitab <span class="highlight">Nahwu Shorof</span>...
        </p>
        <p class="lore">
            Jiwanya terperangkap dalam kutukan dimensi yang hanya bisa dibuka
            lewat kaidah bahasa Arab kuno. <span class="highlight">Kamu</span> adalah santri yang
            memberanikan diri masuk ke reruntuhan pesantren terkutuk itu.
        </p>
        <p class="lore-warning">⚠ Headphone disarankan. Bukan untuk yang lemah hati. ⚠</p>

        <a href="${GITHUB_RELEASE_URL}" id="download-btn" class="download-btn" target="_blank" rel="noopener noreferrer">
            <span class="icon">⬇</span>
            Download Game untuk Windows
        </a>
        <div class="platform">🖥 Windows 10/11 • Standalone .exe • Gratis</div>

        <div class="features">
            <div class="feature">
                <div class="icon">📖</div>
                <div class="label">15 Kitab Nahwu Shorof tersebar di pesantren gelap</div>
            </div>
            <div class="feature">
                <div class="icon">👻</div>
                <div class="label">Kuntilanak AI yang memburu setiap langkahmu</div>
            </div>
            <div class="feature">
                <div class="icon">🧠</div>
                <div class="label">Kuis I'rab, Mufrodat, & Nahwu Shorof bertingkat</div>
            </div>
        </div>
    </div>

    <footer class="footer">
        &copy; 2026 Arek Lombok — Game Horor Edukasi Bahasa Arab
    </footer>

    <!-- Particle Generator Script -->
    <script>
        (function() {
            const container = document.getElementById('particles');
            for (let i = 0; i < 40; i++) {
                const p = document.createElement('div');
                p.className = 'particle';
                p.style.left = Math.random() * 100 + '%';
                p.style.animationDuration = (6 + Math.random() * 10) + 's';
                p.style.animationDelay = Math.random() * 8 + 's';
                p.style.width = p.style.height = (1 + Math.random() * 3) + 'px';
                container.appendChild(p);
            }
        })();
    </script>
</body>
</html>
    `);
});

// ==================== API ENDPOINTS ====================

// Endpoint GET /api/soal/random
// Mendukung parameter query ?kategori=buku|ammo|kunci
// Tanpa parameter → ambil semua soal acak (backward compatible)
app.get('/api/soal/random', (req, res) => {
    const kategori = req.query.kategori;
    const limit = parseInt(req.query.limit) || 15; // default limit 15 soal
    
    let query;
    let params = [];
    
    if (kategori && ['buku', 'ammo', 'kunci'].includes(kategori)) {
        // Ambil soal berdasarkan kategori tertentu dengan LIMIT dinamis
        query = 'SELECT * FROM soal_bahasa_arab WHERE kategori = ? ORDER BY RAND() LIMIT ?';
        params = [kategori, limit];
    } else {
        // Ambil semua soal secara acak jika tanpa kategori
        query = 'SELECT * FROM soal_bahasa_arab ORDER BY RAND() LIMIT ?';
        params = [limit];
    }
    
    db.query(query, params, (err, results) => {
        if (err) {
            console.error('Error saat mengambil soal:', err);
            res.status(500).json({ error: 'Gagal mengambil data dari database' });
            return;
        }
        res.json(results);
    });
});

const PORT = 3000;
app.listen(PORT, () => {
    console.log(`Server Node.js berjalan di http://localhost:${PORT}`);
    console.log(`Landing Page  : http://localhost:${PORT}/`);
    console.log(`API Soal      : http://localhost:${PORT}/api/soal/random`);
    console.log(`GitHub Release: ${GITHUB_RELEASE_URL}`);
});
