-- =====================================================
-- MIGRASI DATABASE v2: Amsilati Quiz System
-- Jalankan file ini di MySQL untuk update tabel
-- =====================================================

USE db_game_edukasi;

-- Langkah 1: Tambahkan kolom kategori
-- (Jika kolom sudah ada, MySQL akan error -> abaikan saja)
ALTER TABLE soal_bahasa_arab 
ADD COLUMN kategori ENUM('buku', 'ammo', 'kunci') NOT NULL DEFAULT 'buku';

-- Langkah 2: Hapus semua data lama
TRUNCATE TABLE soal_bahasa_arab;

-- Langkah 3: Insert 15 soal baru berdasarkan Kitab Amsilati Jilid 1-5
-- =====================================================
-- KATEGORI 'buku' — Nahwu/Shorof Dasar (Amsilati Jilid 1-2)
-- =====================================================
INSERT INTO soal_bahasa_arab (pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban, kategori) VALUES

('Menurut kitab Amsilati, salah satu tanda Isim (kata benda) adalah bisa kemasukan Al. Manakah contoh Isim berikut?',
 'يَكْتُبُ', 'الْكِتَابُ', 'مِنْ', 'لَمْ', 'B', 'buku'),

('Dalam Amsilati Jilid 1, Fi''il Madhi bisa dikenali dengan adanya Ta'' Ta''nits Sakinah di akhirnya. Manakah contoh Fi''il Madhi?',
 'يَجْلِسُ', 'جَلَسَتْ', 'اُجْلُسْ', 'جُلُوْسٌ', 'B', 'buku'),

('Menurut Amsilati, kata dalam bahasa Arab dibagi menjadi tiga bagian. Apa saja pembagiannya?',
 'Isim, Fi''il, Huruf', 'Mubtada, Khobar, Haal', 'Fa''il, Maf''ul, Mashdar', 'Rofa, Nashab, Jar', 'A', 'buku'),

('Dalam Amsilati Jilid 2, wazan dasar Fi''il Tsulasi Mujarrod adalah...',
 'فَعَلَ - يَفْعُلُ', 'اِنْفَعَلَ - يَنْفَعِلُ', 'تَفَعَّلَ - يَتَفَعَّلُ', 'اِسْتَفْعَلَ - يَسْتَفْعِلُ', 'A', 'buku'),

('Tanwin adalah salah satu tanda Isim menurut Amsilati. Kata manakah yang bertanwin?',
 'ذَهَبَ', 'كِتَابًا', 'فِيْ', 'لَنْ', 'B', 'buku'),

-- =====================================================
-- KATEGORI 'ammo' — I'rab / Kedudukan Kalimat (Amsilati Jilid 3-4)
-- =====================================================

('Dalam kalimat: جَاءَ الطَّالِبُ (Pelajar itu datang), apa kedudukan kata الطَّالِبُ?',
 'Maf''ul Bih', 'Fa''il', 'Mubtada', 'Khobar', 'B', 'ammo'),

('Dalam kalimat: قَرَأَ التِّلْمِيْذُ الْقُرْآنَ (Murid itu membaca Al-Quran), apa kedudukan kata الْقُرْآنَ?',
 'Fa''il', 'Mubtada', 'Maf''ul Bih', 'Khobar', 'C', 'ammo'),

('Dalam kalimat: الْعِلْمُ نُوْرٌ (Ilmu itu cahaya), apa kedudukan kata نُوْرٌ?',
 'Fa''il', 'Maf''ul Bih', 'Mubtada', 'Khobar', 'D', 'ammo'),

('Dalam kalimat: جَاءَ رَجُلٌ كَرِيْمٌ (Datang seorang laki-laki yang mulia), apa kedudukan kata كَرِيْمٌ?',
 'Khobar', 'Badal', 'Haal', 'Na''at/Sifat', 'D', 'ammo'),

('Dalam kalimat: ذَهَبَ إِلَى الْمَسْجِدِ (Dia pergi ke masjid), apa kedudukan kata الْمَسْجِدِ?',
 'Fa''il', 'Majrur bi Huruf Jar', 'Maf''ul Bih', 'Mubtada', 'B', 'ammo'),

-- =====================================================
-- KATEGORI 'kunci' — Mufrodat / Arti Kata (Amsilati Jilid 1-5)
-- =====================================================

('Apa arti kata عِلْمٌ?',
 'Buku', 'Ilmu', 'Pena', 'Cahaya', 'B', 'kunci'),

('Apa arti kata كَتَبَ?',
 'Membaca', 'Menulis', 'Duduk', 'Berdiri', 'B', 'kunci'),

('Apa arti kata مَدْرَسَةٌ?',
 'Masjid', 'Perpustakaan', 'Sekolah', 'Rumah', 'C', 'kunci'),

('Apa arti dari مُعَلِّمٌ?',
 'Murid', 'Guru', 'Dokter', 'Petani', 'B', 'kunci'),

('Apa arti kata قَلَمٌ?',
 'Buku', 'Meja', 'Pena', 'Kursi', 'C', 'kunci');
