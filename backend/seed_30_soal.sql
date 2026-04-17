-- Jika tabel belum ada, buat terlebih dahulu:
CREATE TABLE IF NOT EXISTS soal_bahasa_arab (
    id INT AUTO_INCREMENT PRIMARY KEY,
    kategori VARCHAR(50) NOT NULL DEFAULT 'buku',
    pertanyaan TEXT NOT NULL,
    pilihan_a VARCHAR(255) NOT NULL,
    pilihan_b VARCHAR(255) NOT NULL,
    pilihan_c VARCHAR(255) NOT NULL,
    pilihan_d VARCHAR(255) NOT NULL,
    kunci_jawaban VARCHAR(1) NOT NULL
);

-- Pastikan tabel kosong sebelum inject jika tidak ingin data duplicate
-- TRUNCATE TABLE soal_bahasa_arab;

INSERT INTO soal_bahasa_arab (kategori, pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban) VALUES
-- ==============================================
-- KATEGORI BUKU: Dasar Nahwu / Shorof (10 Soal)
-- ==============================================
('buku', 'Kalimat dalam bahasa Arab secara garis besar terbagi menjadi...', '4 macam', '3 macam', '2 macam', '5 macam', 'B'),
('buku', 'Kata yang bermakna pada dirinya sendiri dan tidak berkaitan dengan waktu disebut...', 'Fi''il', 'Huruf', 'Isim', 'Fa''il', 'C'),
('buku', 'Manakah di bawah ini yang merupakan ciri-ciri Isim?', 'Diakhiri sukun', 'Menerima Tanwin', 'Diawali huruf Qod', 'Diawali huruf Sin', 'B'),
('buku', 'Tanda-tanda fi''il antara lain adalah didahului oleh kata...', 'مِنْ', 'إِلَى', 'قَدْ', 'فِي', 'C'),
('buku', 'Fi''il yang menunjukkan arti perintah (Masa Mendatang/Tuntutan) disebut...', 'Fi''il Madhi', 'Fi''il Mudhori''', 'Fi''il Amar', 'Fi''il Nahy', 'C'),
('buku', 'Kalam menurut Jurumiyah harus memenuhi 4 syarat, yaitu: Lafadz, Murokkab, Mufid, dan...', 'Wadho''', 'Isim', 'Tanwin', 'Khafd', 'A'),
('buku', 'Di antara ini, manakah yang merupakan huruf Jar?', 'هَلْ', 'بِ', 'قَدْ', 'لَمْ', 'B'),
('buku', 'Apa ciri khusus dari Fi''il Madhi?', 'Menerima Ta'' Ta''nits Sakinah', 'Menerima Alif Lam', 'Menerima Tanwin', 'Menerima huruf Nida', 'A'),
('buku', 'Jika suatu lafadz diawali dengan "Al" (ال), maka lafadz tersebut dipastikan adalah...', 'Huruf', 'Fi''il', 'Isim', 'Sifat', 'C'),
('buku', 'Manakah kata berikut yang merupakan Fi''il Mudhori''?', 'ضَرَبَ', 'يَضْرِبُ', 'إِضْرِبْ', 'ضَارِبٌ', 'B'),

-- ==============================================
-- KATEGORI AMMO: I''rab / Tarkib (10 Soal)
-- ==============================================
('ammo', 'Tanda asli untuk i''rab Rofa'' adalah...', 'Fathah', 'Kasrah', 'Sukun', 'Dhommah', 'D'),
('ammo', 'I''rab yang khusus masuk pada Isim dan tidak bisa masuk pada Fi''il adalah...', 'Rofa''', 'Nashab', 'Khafd (Jer)', 'Jazm', 'C'),
('ammo', 'Tanda asli untuk i''rab Jazm adalah...', 'Dhommah', 'Khafd', 'Fathah', 'Sukun', 'D'),
('ammo', 'Di dalam kalimat جَاءَ زَيْدٌ (Jaa-a Zaidun), lafadz زَيْدٌ berkedudukan sebagai...', 'Mubtada', 'Fa''il', 'Maf''ul Bih', 'Khobar', 'B'),
('ammo', 'Maf''ul Bih (Objek Penderita) selalu dibaca dengan i''rab...', 'Rofa''', 'Nashab', 'Khofadh', 'Jazm', 'B'),
('ammo', 'Tanda Rofa'' bagi Isim Tatsniyah (Ganda) adalah...', 'Alif', 'Wawu', 'Dhommah', 'Nun', 'A'),
('ammo', 'Jika suatu Isim kemasukan huruf Jar, maka harus dibaca...', 'Rofa''', 'Nashab', 'Jazm', 'Jer / Kasrah', 'D'),
('ammo', 'Mubtada'' dan Khobar hukum i''rab-nya selalu...', 'Nashab', 'Khafd', 'Rofa''', 'Mu''rob', 'C'),
('ammo', 'Manakah dari kalimat berikut yang susunannya adalah Fi''il dan Fa''il?', 'زَيْدٌ قَائِمٌ', 'قَامَ زَيْدٌ', 'فِي البَيْتِ', 'كِتَابٌ جَدِيْدٌ', 'B'),
('ammo', 'Tanda Nashab pada Jamak Muannats Salim adalah dengan...', 'Fathah', 'Kasrah', 'Alif', 'Ya''', 'B'),

-- ==============================================
-- KATEGORI KUNCI: Mufrodat / Kosakata (10 Soal)
-- ==============================================
('kunci', 'Apa arti dari lafadz كِتَابٌ (Kitaabun)?', 'Buku', 'Pintu', 'Kunci', 'Meja', 'A'),
('kunci', 'Apa bahasa Arab dari "Pintu"?', 'بَيْتٌ', 'بَابٌ', 'مَكْتَبٌ', 'قَلَمٌ', 'B'),
('kunci', 'Lafadz مِفْتَاحٌ (Miftaahun) artinya adalah...', 'Kunci', 'Gembok', 'Lampu', 'Jendela', 'A'),
('kunci', 'Kosakata untuk "Rumah" di bawah ini adalah...', 'سَرِيْرٌ', 'مِصْبَاحٌ', 'بَيْتٌ', 'كُرْسِيٌّ', 'C'),
('kunci', 'Apa arti dari lafadz مَكْتَبٌ (Maktabun)?', 'Pena', 'Kursi', 'Lantai', 'Meja', 'D'),
('kunci', 'Bahasa Arab dari "Kata" (secara harafiah) / Tunggal dari kalimat adalah...', 'كَلِمَةٌ', 'كَلَامٌ', 'قَوْلٌ', 'لَفْظٌ', 'A'),
('kunci', 'Lafadz خِزَانَةٌ (Khizaanatun) berarti...', 'Dapur', 'Kamar', 'Lemari', 'Ranjang', 'C'),
('kunci', 'Kosakata untuk "Pena / Pulpen" adalah...', 'كِتَابٌ', 'قَلَمٌ', 'مِفْتَاحٌ', 'طَبَاشِيْرُ', 'B'),
('kunci', 'Apa arti dari lafadz مِصْبَاحٌ (Mishbaahun)?', 'Api', 'Kaca', 'Lampu', 'Obor', 'C'),
('kunci', 'Bahasa Arab untuk "Tempat Tidur / Kasur" adalah...', 'سَرِيْرٌ', 'كُرْسِيٌّ', 'بَابٌ', 'غُرْفَةٌ', 'A');
