CREATE DATABASE IF NOT EXISTS db_game_edukasi;
USE db_game_edukasi;

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

-- Saya sertakan 15 soal agar game bisa langsung dimainkan sampai menang (butuh 15 buku).
INSERT INTO soal_bahasa_arab (pertanyaan, pilihan_a, pilihan_b, pilihan_c, pilihan_d, kunci_jawaban) VALUES
('Manakah dari kata berikut yang termasuk Isim?', 'يَضْرِبُ', 'فِي', 'مَدْرَسَةٌ', 'لَمْ', 'C'),
('Huruf jar di bawah ini adalah...', 'وَ', 'مِنْ', 'ثُمَّ', 'أَوْ', 'B'),
('Apa tanda dari Fi\'il Mudhari?', 'Diawali huruf mudhara\'ah', 'Diakhiri tanwin', 'Kemasukan huruf Qad', 'Diakhiri alif lam', 'A'),
('Kata الكِتَابُ dibaca rofa\' karena...', 'Ada alif lam', 'Termasuk huruf', 'Menjadi isim', 'Mubtada', 'D'),
('Kalimat yang sempurna dalam bahasa Arab disebut...', 'Kalimat', 'Kalam', 'Isim', 'Fi\'il', 'B'),
('Pengertian dari Isim adalah...', 'Kata kerja', 'Kata depan', 'Kata benda', 'Kata hubung', 'C'),
('Apakah tanda nashab untuk Isim Mufrad?', 'Fathah', 'Kasrah', 'Dhammah', 'Sukun', 'A'),
('Contoh dari Fi\'il Madhi adalah', 'يَقْرَأُ', 'إِقْرَأْ', 'قَرَأَ', 'قِرَاءَةً', 'C'),
('Di antara ini, yang bukan merupakan tanda isim adalah...', 'Alif Lam', 'Tanwin', 'Huruf Jar', 'Huruf Mudhara\'ah', 'D'),
('Berapakah huruf jar itu menurut Jurumiyah?', '7', '8', '9', '10', 'C'),
('Ciri-ciri kalam menurut Jurumiyah ada...', '2', '3', '4', '5', 'C'),
('Fi\'il amar bermakna...', 'Masa lalu', 'Masa sekarang', 'Perintah', 'Larangan', 'C'),
('Fa\'il biasanya dibaca...', 'Nashab', 'Rofa\'', 'Khafd', 'Jazm', 'B'),
('Huruf Athof yang bermakna "dan" adalah...', 'ثُمَّ', 'أَوْ', 'أَمْ', 'وَ', 'D'),
('Isim Ghoiru Munshorif adalah isim yang tidak menerima...', 'Tanwin dan Kasrah', 'Alif Lam', 'Dhommah', 'Fathah', 'A');
