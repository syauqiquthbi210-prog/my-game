-- ================================================================
-- BATCH 2: 30 Soal Baru Kitab Amsilati (ID 31-60)
-- Jalankan setelah seed_30_soal.sql agar tidak ada duplikat.
-- ================================================================

INSERT INTO soal_bahasa_arab (kategori, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban) VALUES

-- ==============================================
-- KATEGORI BUKU: Nahwu / Shorof Dasar (10 Soal)
-- Referensi: Amsilati Jilid 1-3
-- ==============================================
('buku', 'Dalam ilmu Nahwu, Isim Nakiroh adalah isim yang...', 'Sudah tertentu maknanya', 'Belum tertentu maknanya', 'Tidak bisa diberi harakat', 'Selalu berharakat fathah', 'B'),
('buku', 'Isim Ma''rifat adalah kebalikan dari Nakiroh. Contoh Isim Ma''rifat adalah...', 'رَجُلٌ', 'كِتَابٌ', 'الرَّجُلُ', 'بَيْتٌ', 'C'),
('buku', 'Menurut Kitab Amsilati, Wazan (Timbangan/Pola) dari Fi''il Madhi adalah...', 'يَفْعَلُ', 'فَعَلَ', 'اِفْعَلْ', 'فَاعِلٌ', 'B'),
('buku', 'Huruf yang tidak memiliki tanda-tanda Isim maupun Fi''il disebut...', 'Isim Dhomir', 'Isim Isyarah', 'Huruf', 'Isim Maushul', 'C'),
('buku', 'Ada berapa macam pembagian Isim berdasarkan jumlahnya (Mufrad, Tatsniyah, Jama'')?', '2', '3', '4', '5', 'B'),
('buku', 'Isim Tatsniyah ditandai dengan akhiran huruf...', 'وَاوٌ وَ نُوْنٌ', 'أَلِفٌ وَ نُوْنٌ', 'يَاءٌ وَ نُوْنٌ', 'تَاءٌ', 'B'),
('buku', 'Jama'' Mudzakkar Salim adalah jamak untuk laki-laki dengan menambahkan akhiran...', 'اتٌ', 'انِ', 'وْنَ / يْنَ', 'ءٌ', 'C'),
('buku', 'Jama'' Muannats Salim ditandai dengan tambahan akhiran...', 'وْنَ', 'يْنَ', 'اتٌ', 'انِ', 'C'),
('buku', 'Contoh Isim Dhomir (Kata Ganti) untuk orang pertama tunggal adalah...', 'هُوَ', 'هِيَ', 'أَنْتَ', 'أَنَا', 'D'),
('buku', 'Isim Maushul (Kata Sambung) yang dipakai untuk satu orang laki-laki adalah...', 'الَّتِيْ', 'الَّذِيْ', 'الَّذِيْنَ', 'اللَّاتِيْ', 'B'),

-- ==============================================
-- KATEGORI AMMO: I''rab / Tarkib Kalimat (10 Soal)
-- Referensi: Amsilati Jilid 3-5
-- ==============================================
('ammo', 'Dalam kalimat ضَرَبَ زَيْدٌ عَمْرًا, kata عَمْرًا berkedudukan sebagai...', 'Fa''il', 'Mubtada''', 'Maf''ul Bih', 'Khobar', 'C'),
('ammo', 'Na''ibul Fa''il (Pengganti Subjek) selalu dibaca...', 'Nashab', 'Jer', 'Rofa''', 'Jazm', 'C'),
('ammo', 'Tanda Rofa'' untuk Jama'' Mudzakkar Salim adalah...', 'Dhammah', 'Alif', 'Wawu', 'Fathah', 'C'),
('ammo', 'Tanda Jer (Khafd) untuk Isim yang tidak menerima Tanwin (Ghoiru Munshorif) adalah...', 'Kasrah', 'Fathah', 'Sukun', 'Ya''', 'B'),
('ammo', 'Kalimat كَانَ زَيْدٌ مَرِيْضًا. Kata مَرِيْضًا berkedudukan sebagai...', 'Ismnya Kaana', 'Khobarnya Kaana', 'Fa''il', 'Hal', 'B'),
('ammo', 'Huruf إِنَّ (Inna) membuat Isim setelahnya dibaca...', 'Rofa''', 'Nashab', 'Jer', 'Jazm', 'B'),
('ammo', 'Dalam kalimat nominal (Jumlah Ismiyyah), susunan dasarnya adalah...', 'Fi''il + Fa''il', 'Mubtada'' + Khobar', 'Jar + Majrur', 'Hal + Dzul Hal', 'B'),
('ammo', 'Isim Majrur adalah isim yang jatuh setelah...', 'Fi''il', 'Huruf Nashab', 'Huruf Jar', 'Huruf Jazm', 'C'),
('ammo', 'Dalam kalimat ذَهَبَ التِّلْمِيْذُ إِلَى المَدْرَسَةِ, kata المَدْرَسَةِ berharakat kasrah karena...', 'Menjadi Mubtada''', 'Menjadi Khobar', 'Didahului huruf Jar إِلَى', 'Menjadi Fa''il', 'C'),
('ammo', 'Fi''il Mudhori'' yang kemasukan لَمْ (Lam Jazm) harus dibaca...', 'Rofa''', 'Nashab', 'Jazm', 'Jer', 'C'),

-- ==============================================
-- KATEGORI KUNCI: Mufrodat / Kosakata (10 Soal)
-- Referensi: Kosakata Harian Kitab Kuning
-- ==============================================
('kunci', 'Apa arti dari lafadz عِلْمٌ (''Ilmun)?', 'Amal', 'Ilmu', 'Harta', 'Dunia', 'B'),
('kunci', 'Bahasa Arab dari kata "Guru / Pengajar" adalah...', 'تِلْمِيْذٌ', 'مُعَلِّمٌ', 'طَالِبٌ', 'وَالِدٌ', 'B'),
('kunci', 'Lafadz مَسْجِدٌ (Masjidun) artinya...', 'Sekolah', 'Pasar', 'Masjid', 'Rumah Sakit', 'C'),
('kunci', 'Apa bahasa Arab dari "Murid / Pelajar"?', 'أُسْتَاذٌ', 'تِلْمِيْذٌ', 'إِمَامٌ', 'خَطِيْبٌ', 'B'),
('kunci', 'Arti dari kosakata مَاءٌ (Maa-un) adalah...', 'Api', 'Angin', 'Tanah', 'Air', 'D'),
('kunci', 'Lafadz شَمْسٌ (Syamsun) berarti...', 'Bulan', 'Matahari', 'Bintang', 'Langit', 'B'),
('kunci', 'Bahasa Arab dari "Kitab / Buku" yang bentuk jamaknya adalah...', 'كِتَابٌ', 'مَكْتَبٌ', 'كُتُبٌ', 'كَاتِبٌ', 'C'),
('kunci', 'Apa arti dari lafadz قَمَرٌ (Qomarun)?', 'Matahari', 'Bulan', 'Awan', 'Hujan', 'B'),
('kunci', 'Kosakata أَرْضٌ (Ardhun) bermakna...', 'Langit', 'Laut', 'Bumi / Tanah', 'Gunung', 'C'),
('kunci', 'Lafadz سَمَاءٌ (Samaa-un) artinya adalah...', 'Langit', 'Bumi', 'Lautan', 'Sungai', 'A');
