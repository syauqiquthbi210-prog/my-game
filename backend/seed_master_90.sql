-- ================================================================
-- MASTER SEED: 90 Soal Kitab Amsilati (Batch 1 + 2 + 3)
-- Drop tabel lama, buat ulang, dan inject semua sekaligus.
-- ================================================================

DROP TABLE IF EXISTS soal_bahasa_arab;

CREATE TABLE soal_bahasa_arab (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kategori VARCHAR(50) NOT NULL DEFAULT 'buku',
    pertanyaan TEXT NOT NULL,
    pilihan_a VARCHAR(255) NOT NULL,
    pilihan_b VARCHAR(255) NOT NULL,
    pilihan_c VARCHAR(255) NOT NULL,
    pilihan_d VARCHAR(255) NOT NULL,
    kunci_jawaban VARCHAR(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO soal_bahasa_arab (kategori, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban) VALUES

-- ██████████████████████████████████████████████████
-- ██  BATCH 1: BUKU - Nahwu/Shorof Dasar (10)    ██
-- ██████████████████████████████████████████████████
('buku', 'Kalimat dalam bahasa Arab secara garis besar terbagi menjadi...', '4 macam', '3 macam', '2 macam', '5 macam', 'B'),
('buku', 'Kata yang bermakna pada dirinya sendiri dan tidak berkaitan dengan waktu disebut...', 'Fi''il', 'Huruf', 'Isim', 'Fa''il', 'C'),
('buku', 'Manakah di bawah ini yang merupakan ciri-ciri Isim?', 'Diakhiri sukun', 'Menerima Tanwin', 'Diawali huruf Qod', 'Diawali huruf Sin', 'B'),
('buku', 'Tanda-tanda Fi''il antara lain adalah didahului oleh kata...', 'مِنْ', 'إِلَى', 'قَدْ', 'فِي', 'C'),
('buku', 'Fi''il yang menunjukkan arti perintah disebut...', 'Fi''il Madhi', 'Fi''il Mudhori''', 'Fi''il Amar', 'Fi''il Nahi', 'C'),
('buku', 'Kalam menurut Jurumiyah harus memenuhi 4 syarat: Lafadz, Murokkab, Mufid, dan...', 'Wadho''', 'Isim', 'Tanwin', 'Khafd', 'A'),
('buku', 'Di antara ini, manakah yang merupakan Huruf Jar?', 'هَلْ', 'بِ', 'قَدْ', 'لَمْ', 'B'),
('buku', 'Apa ciri khusus dari Fi''il Madhi?', 'Menerima Ta'' Ta''nits Sakinah', 'Menerima Alif Lam', 'Menerima Tanwin', 'Menerima huruf Nida', 'A'),
('buku', 'Jika suatu lafadz diawali dengan Al (ال), maka dipastikan ia adalah...', 'Huruf', 'Fi''il', 'Isim', 'Sifat', 'C'),
('buku', 'Manakah kata berikut yang merupakan Fi''il Mudhori''?', 'ضَرَبَ', 'يَضْرِبُ', 'اِضْرِبْ', 'ضَارِبٌ', 'B'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 1: AMMO - I'rab / Tarkib (10)        ██
-- ██████████████████████████████████████████████████
('ammo', 'Tanda asli untuk I''rab Rofa'' adalah...', 'Fathah', 'Kasrah', 'Sukun', 'Dhommah', 'D'),
('ammo', 'I''rab yang khusus masuk pada Isim dan tidak bisa pada Fi''il adalah...', 'Rofa''', 'Nashab', 'Khafd (Jer)', 'Jazm', 'C'),
('ammo', 'Tanda asli untuk I''rab Jazm adalah...', 'Dhommah', 'Khafd', 'Fathah', 'Sukun', 'D'),
('ammo', 'Dalam kalimat جَاءَ زَيْدٌ, lafadz زَيْدٌ berkedudukan sebagai...', 'Mubtada''', 'Fa''il', 'Maf''ul Bih', 'Khobar', 'B'),
('ammo', 'Maf''ul Bih selalu dibaca dengan I''rab...', 'Rofa''', 'Nashab', 'Khofadh', 'Jazm', 'B'),
('ammo', 'Tanda Rofa'' bagi Isim Tatsniyah (Ganda) adalah...', 'Alif', 'Wawu', 'Dhommah', 'Nun', 'A'),
('ammo', 'Jika suatu Isim kemasukan huruf Jar, maka harus dibaca...', 'Rofa''', 'Nashab', 'Jazm', 'Jer / Kasrah', 'D'),
('ammo', 'Mubtada'' dan Khobar hukum I''rabnya selalu...', 'Nashab', 'Khafd', 'Rofa''', 'Mabni', 'C'),
('ammo', 'Susunan Fi''il + Fa''il terdapat pada kalimat...', 'زَيْدٌ قَائِمٌ', 'قَامَ زَيْدٌ', 'فِي البَيْتِ', 'كِتَابٌ جَدِيْدٌ', 'B'),
('ammo', 'Tanda Nashab pada Jama'' Muannats Salim adalah...', 'Fathah', 'Kasrah', 'Alif', 'Ya''', 'B'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 1: KUNCI - Mufrodat (10)             ██
-- ██████████████████████████████████████████████████
('kunci', 'Apa arti dari lafadz كِتَابٌ (Kitaabun)?', 'Buku', 'Pintu', 'Kunci', 'Meja', 'A'),
('kunci', 'Apa bahasa Arab dari "Pintu"?', 'بَيْتٌ', 'بَابٌ', 'مَكْتَبٌ', 'قَلَمٌ', 'B'),
('kunci', 'Lafadz مِفْتَاحٌ (Miftaahun) artinya adalah...', 'Kunci', 'Gembok', 'Lampu', 'Jendela', 'A'),
('kunci', 'Kosakata untuk "Rumah" di bawah ini adalah...', 'سَرِيْرٌ', 'مِصْبَاحٌ', 'بَيْتٌ', 'كُرْسِيٌّ', 'C'),
('kunci', 'Apa arti dari lafadz مَكْتَبٌ (Maktabun)?', 'Pena', 'Kursi', 'Lantai', 'Meja', 'D'),
('kunci', 'Bahasa Arab dari "Kata" secara harafiah adalah...', 'كَلِمَةٌ', 'كَلَامٌ', 'قَوْلٌ', 'لَفْظٌ', 'A'),
('kunci', 'Lafadz خِزَانَةٌ (Khizaanatun) berarti...', 'Dapur', 'Kamar', 'Lemari', 'Ranjang', 'C'),
('kunci', 'Kosakata untuk "Pena / Pulpen" adalah...', 'كِتَابٌ', 'قَلَمٌ', 'مِفْتَاحٌ', 'طَبَاشِيْرُ', 'B'),
('kunci', 'Apa arti dari lafadz مِصْبَاحٌ (Mishbaahun)?', 'Api', 'Kaca', 'Lampu', 'Obor', 'C'),
('kunci', 'Bahasa Arab untuk "Tempat Tidur / Kasur" adalah...', 'سَرِيْرٌ', 'كُرْسِيٌّ', 'بَابٌ', 'غُرْفَةٌ', 'A'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 2: BUKU - Nahwu/Shorof Lanjut (10)   ██
-- ██████████████████████████████████████████████████
('buku', 'Dalam ilmu Nahwu, Isim Nakiroh adalah isim yang...', 'Sudah tertentu maknanya', 'Belum tertentu maknanya', 'Tidak bisa diberi harakat', 'Selalu berharakat fathah', 'B'),
('buku', 'Contoh Isim Ma''rifat adalah...', 'رَجُلٌ', 'كِتَابٌ', 'الرَّجُلُ', 'بَيْتٌ', 'C'),
('buku', 'Wazan (Pola) dari Fi''il Madhi Tsulasi Mujarrad adalah...', 'يَفْعَلُ', 'فَعَلَ', 'اِفْعَلْ', 'فَاعِلٌ', 'B'),
('buku', 'Huruf yang tidak memiliki tanda Isim maupun Fi''il disebut...', 'Isim Dhomir', 'Isim Isyarah', 'Huruf', 'Isim Maushul', 'C'),
('buku', 'Pembagian Isim berdasarkan jumlah ada berapa macam?', '2', '3', '4', '5', 'B'),
('buku', 'Isim Tatsniyah ditandai dengan akhiran huruf...', 'وَاوٌ وَ نُوْنٌ', 'أَلِفٌ وَ نُوْنٌ', 'يَاءٌ وَ نُوْنٌ', 'تَاءٌ', 'B'),
('buku', 'Jama'' Mudzakkar Salim ditambahkan akhiran...', 'اتٌ', 'انِ', 'وْنَ / يْنَ', 'ءٌ', 'C'),
('buku', 'Jama'' Muannats Salim ditandai dengan tambahan...', 'وْنَ', 'يْنَ', 'اتٌ', 'انِ', 'C'),
('buku', 'Isim Dhomir untuk orang pertama tunggal (Saya) adalah...', 'هُوَ', 'هِيَ', 'أَنْتَ', 'أَنَا', 'D'),
('buku', 'Isim Maushul untuk satu orang laki-laki adalah...', 'الَّتِيْ', 'الَّذِيْ', 'الَّذِيْنَ', 'اللَّاتِيْ', 'B'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 2: AMMO - I'rab / Tarkib (10)        ██
-- ██████████████████████████████████████████████████
('ammo', 'Dalam ضَرَبَ زَيْدٌ عَمْرًا, kata عَمْرًا berkedudukan sebagai...', 'Fa''il', 'Mubtada''', 'Maf''ul Bih', 'Khobar', 'C'),
('ammo', 'Na''ibul Fa''il selalu dibaca...', 'Nashab', 'Jer', 'Rofa''', 'Jazm', 'C'),
('ammo', 'Tanda Rofa'' untuk Jama'' Mudzakkar Salim adalah...', 'Dhammah', 'Alif', 'Wawu', 'Fathah', 'C'),
('ammo', 'Tanda Jer untuk Isim Ghoiru Munshorif adalah...', 'Kasrah', 'Fathah', 'Sukun', 'Ya''', 'B'),
('ammo', 'Dalam كَانَ زَيْدٌ مَرِيْضًا, kata مَرِيْضًا berkedudukan...', 'Ismnya Kaana', 'Khobarnya Kaana', 'Fa''il', 'Hal', 'B'),
('ammo', 'Huruf إِنَّ membuat Isim setelahnya dibaca...', 'Rofa''', 'Nashab', 'Jer', 'Jazm', 'B'),
('ammo', 'Susunan dasar Jumlah Ismiyyah adalah...', 'Fi''il + Fa''il', 'Mubtada'' + Khobar', 'Jar + Majrur', 'Hal + Dzul Hal', 'B'),
('ammo', 'Isim Majrur adalah isim yang jatuh setelah...', 'Fi''il', 'Huruf Nashab', 'Huruf Jar', 'Huruf Jazm', 'C'),
('ammo', 'Dalam إِلَى المَدْرَسَةِ, kata المَدْرَسَةِ dibaca kasrah karena...', 'Menjadi Mubtada''', 'Menjadi Khobar', 'Didahului huruf Jar إِلَى', 'Menjadi Fa''il', 'C'),
('ammo', 'Fi''il Mudhori'' yang kemasukan لَمْ harus dibaca...', 'Rofa''', 'Nashab', 'Jazm', 'Jer', 'C'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 2: KUNCI - Mufrodat (10)             ██
-- ██████████████████████████████████████████████████
('kunci', 'Apa arti dari lafadz عِلْمٌ (Ilmun)?', 'Amal', 'Ilmu', 'Harta', 'Dunia', 'B'),
('kunci', 'Bahasa Arab dari "Guru / Pengajar" adalah...', 'تِلْمِيْذٌ', 'مُعَلِّمٌ', 'طَالِبٌ', 'وَالِدٌ', 'B'),
('kunci', 'Lafadz مَسْجِدٌ (Masjidun) artinya...', 'Sekolah', 'Pasar', 'Masjid', 'Rumah Sakit', 'C'),
('kunci', 'Apa bahasa Arab dari "Murid / Pelajar"?', 'أُسْتَاذٌ', 'تِلْمِيْذٌ', 'إِمَامٌ', 'خَطِيْبٌ', 'B'),
('kunci', 'Arti dari kosakata مَاءٌ (Maa-un) adalah...', 'Api', 'Angin', 'Tanah', 'Air', 'D'),
('kunci', 'Lafadz شَمْسٌ (Syamsun) berarti...', 'Bulan', 'Matahari', 'Bintang', 'Langit', 'B'),
('kunci', 'Bentuk jamak dari كِتَابٌ adalah...', 'كِتَابٌ', 'مَكْتَبٌ', 'كُتُبٌ', 'كَاتِبٌ', 'C'),
('kunci', 'Apa arti dari lafadz قَمَرٌ (Qomarun)?', 'Matahari', 'Bulan', 'Awan', 'Hujan', 'B'),
('kunci', 'Kosakata أَرْضٌ (Ardhun) bermakna...', 'Langit', 'Laut', 'Bumi / Tanah', 'Gunung', 'C'),
('kunci', 'Lafadz سَمَاءٌ (Samaa-un) artinya...', 'Langit', 'Bumi', 'Lautan', 'Sungai', 'A'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 3: BUKU - Nahwu/Shorof Mahir (10)    ██
-- ██████████████████████████████████████████████████
('buku', 'Isim Isyarah (Kata Tunjuk) untuk benda dekat laki-laki adalah...', 'ذَلِكَ', 'تِلْكَ', 'هَذَا', 'هَؤُلَاءِ', 'C'),
('buku', 'Isim Isyarah untuk benda jauh perempuan adalah...', 'هَذِهِ', 'ذَلِكَ', 'تِلْكَ', 'هَذَانِ', 'C'),
('buku', 'Wazan Fi''il Mudhori'' dari فَعَلَ adalah...', 'فَاعِلٌ', 'مَفْعُوْلٌ', 'يَفْعَلُ', 'اِفْعَلْ', 'C'),
('buku', 'Isim Fa''il dari fi''il نَصَرَ adalah...', 'مَنْصُوْرٌ', 'نَاصِرٌ', 'نَصْرٌ', 'يَنْصُرُ', 'B'),
('buku', 'Isim Maf''ul dari fi''il كَتَبَ adalah...', 'كَاتِبٌ', 'مَكْتُوْبٌ', 'كِتَابَةٌ', 'يَكْتُبُ', 'B'),
('buku', 'Mashdar (Kata Dasar) dari fi''il عَلِمَ adalah...', 'عَالِمٌ', 'مَعْلُوْمٌ', 'عِلْمٌ', 'يَعْلَمُ', 'C'),
('buku', 'Fi''il Tsulatsi Mujarrad artinya fi''il yang huruf aslinya berjumlah...', '2 huruf', '3 huruf', '4 huruf', '5 huruf', 'B'),
('buku', 'Tashrif Istilahi disebut juga dengan istilah...', 'Shorof Lughowi', 'Shorof Istilahi', 'Nahwu I''rob', 'Balaghoh', 'B'),
('buku', 'Isim Dhomir هُمَا artinya...', 'Dia (lk)', 'Mereka berdua', 'Mereka (lk)', 'Kamu berdua', 'B'),
('buku', 'Isim Dhomir yang disebut Dhomir Mukhotob (Lawan Bicara Laki-laki) adalah...', 'هُوَ', 'أَنَا', 'أَنْتَ', 'هِيَ', 'C'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 3: AMMO - I'rab / Tarkib Mahir (10)  ██
-- ██████████████████████████████████████████████████
('ammo', 'Tanda Nashab untuk Fi''il Mudhori'' adalah...', 'Dhommah', 'Fathah', 'Kasrah', 'Sukun', 'B'),
('ammo', 'Fi''il Mudhori'' yang kemasukan أَنْ dibaca...', 'Rofa''', 'Nashab', 'Jazm', 'Jer', 'B'),
('ammo', 'Dalam kalimat رَأَيْتُ الرَّجُلَ, kata الرَّجُلَ berharakat fathah karena...', 'Menjadi Fa''il', 'Menjadi Mubtada''', 'Menjadi Maf''ul Bih', 'Menjadi Khobar', 'C'),
('ammo', 'Khobar dari إِنَّ harus dibaca...', 'Nashab', 'Jer', 'Rofa''', 'Jazm', 'C'),
('ammo', 'Isim dari كَانَ harus dibaca...', 'Nashab', 'Jer', 'Rofa''', 'Jazm', 'C'),
('ammo', 'Dalam kalimat الطَّالِبُ مُجْتَهِدٌ, kata مُجْتَهِدٌ berkedudukan sebagai...', 'Mubtada''', 'Khobar', 'Fa''il', 'Na''at', 'B'),
('ammo', 'Huruf لَنْ membuat Fi''il Mudhori'' dibaca...', 'Rofa''', 'Nashab', 'Jazm', 'Jer', 'B'),
('ammo', 'Isim yang dibaca Nashab karena menjelaskan keadaan Fa''il disebut...', 'Tamyiz', 'Hal', 'Maf''ul Bih', 'Maf''ul Fih', 'B'),
('ammo', 'Tanda I''rab Rofa'' untuk Fi''il Mudhori'' adalah...', 'Fathah', 'Sukun', 'Dhammah', 'Kasrah', 'C'),
('ammo', 'Dalam كَتَبَ الوَلَدُ الدَّرْسَ, kata الوَلَدُ berkedudukan sebagai...', 'Maf''ul Bih', 'Khobar', 'Fa''il', 'Mubtada''', 'C'),

-- ██████████████████████████████████████████████████
-- ██  BATCH 3: KUNCI - Mufrodat Lanjut (10)      ██
-- ██████████████████████████████████████████████████
('kunci', 'Apa arti dari كُرْسِيٌّ (Kursiyyun)?', 'Meja', 'Kursi', 'Rak', 'Papan', 'B'),
('kunci', 'Bahasa Arab dari "Jendela" adalah...', 'بَابٌ', 'نَافِذَةٌ', 'جِدَارٌ', 'سَقْفٌ', 'B'),
('kunci', 'Lafadz جِدَارٌ (Jidaarun) berarti...', 'Lantai', 'Atap', 'Dinding', 'Tangga', 'C'),
('kunci', 'Apa arti dari نُوْرٌ (Nuurun)?', 'Gelap', 'Api', 'Cahaya', 'Bayangan', 'C'),
('kunci', 'Bahasa Arab dari "Tinta" adalah...', 'قَلَمٌ', 'حِبْرٌ', 'وَرَقَةٌ', 'كِتَابٌ', 'B'),
('kunci', 'Lafadz وَرَقَةٌ (Waroqotun) artinya...', 'Buku', 'Kertas', 'Papan Tulis', 'Pena', 'B'),
('kunci', 'Apa bahasa Arab dari "Papan Tulis"?', 'سَبُّوْرَةٌ', 'مِمْحَاةٌ', 'طَبَاشِيْرُ', 'دَفْتَرٌ', 'A'),
('kunci', 'Arti dari مِمْحَاةٌ (Mimhaatun) adalah...', 'Penggaris', 'Penghapus', 'Pena', 'Tinta', 'B'),
('kunci', 'Kosakata دَفْتَرٌ (Daftarun) bermakna...', 'Kertas', 'Buku Catatan', 'Map', 'Tas', 'B'),
('kunci', 'Lafadz حَقِيْبَةٌ (Haqiibatun) artinya...', 'Sepatu', 'Baju', 'Tas', 'Topi', 'C');
