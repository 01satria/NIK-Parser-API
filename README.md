# 🇮🇩 NIK Parser API (Indonesia)

Aplikasi berbasis **Flask (Python)** untuk mengekstrak informasi detail dari Nomor Induk Kependudukan (NIK) Indonesia.

Selain memecah data standar (Tanggal Lahir, Jenis Kelamin, Wilayah), API ini juga dilengkapi fitur tambahan unik seperti perhitungan **Weton (Pasaran Jawa)**, **Zodiak**, **Usia**, dan **Hitung Mundur Ulang Tahun**.



## 🌐 Live Demo (Coba Sekarang)

API ini sudah dideploy dan bisa langsung diakses secara online. Klik link di bawah untuk melihat hasil respon JSON:

### **[🔗 https://satrias.pythonanywhere.com/parse_nik?nik=00000000](https://satrias.pythonanywhere.com/parse_nik?nik=00000000)**

*(Ganti angka di ujung URL dengan NIK yang ingin kamu cek)*



## ✨ Fitur Utama

* **Parsing Data Dasar:** Mengambil informasi Provinsi, Kabupaten/Kota, Kecamatan, Jenis Kelamin, dan Tanggal Lahir.
* **Data Wilayah Real-time:** Menggunakan database wilayah Indonesia terbaru (fetch dari GitHub JSON).
* **Fitur Unik:**
    * 📅 **Weton Jawa:** Menghitung hari pasaran (Legi, Pahing, Pon, Wage, Kliwon).
    * ✨ **Zodiak:** Menentukan bintang berdasarkan tanggal lahir.
    * 🎂 **Ulang Tahun:** Menghitung berapa hari/bulan lagi menuju ulang tahun berikutnya.
    * ⏳ **Kategori Usia:** Mengelompokkan usia (Balita, Remaja, Dewasa, Lansia).



## 🚀 Instalasi & Menjalankan Lokal

Jika ingin menjalankan di komputer sendiri:

1.  **Clone Repository**
    ```bash
    git clone [https://github.com/01satria/NIK-Parser-API.git](https://github.com/01satria/NIK-Parser-API.git)
    cd nik-parser
    ```

2.  **Install Dependencies**
    Pastikan Python sudah terinstall, lalu jalankan:
    ```bash
    pip install Flask requests
    ```

3.  **Jalankan Aplikasi**
    ```bash
    python app.py
    ```
    Aplikasi akan berjalan di `http://127.0.0.1:5000`.



## 📡 Dokumentasi API

### Endpoint: Parse NIK
Mendapatkan detail informasi dari 16 digit NIK.

* **URL Base:** `https://satrias.pythonanywhere.com` (Live) atau `http://localhost:5000` (Lokal)
* **Path:** `/parse_nik`
* **Method:** `GET`
* **Parameter:** `nik` (16 digit angka)

## ⚠️ Disclaimer
Aplikasi ini hanya membaca struktur nomor NIK berdasarkan algoritma standar kependudukan (Kode Wilayah + Tgl Lahir + Urut).

* Aplikasi ini TIDAK terhubung ke database Dukcapil atau pemerintah
*  Aplikasi ini TIDAK memverifikasi validitas data kependudukan (hanya validasi format).
*  Gunakan dengan bijak untuk keperluan edukasi atau validasi format input.


## 👨‍💻 Author
Dibuat oleh @01Satria.

