# Manual Book Compressio

---

## 1. Sampul

**Nama Aplikasi:** Compressio  
**Logo Aplikasi:**  
![Compressio Logo](docs/assets/logo.png)  
**Versi Aplikasi:** 1.0.0  
**Tanggal Rilis Manual:** 30 Juni 2024

---

## 2. Kata Pengantar / Pendahuluan
Compressio adalah aplikasi web modern untuk kompresi file yang memudahkan pengguna mengurangi ukuran file tanpa mengorbankan kualitas. Aplikasi ini cocok untuk pelajar, profesional, maupun masyarakat umum yang ingin menghemat ruang penyimpanan atau mempercepat pengiriman file.

Manual book ini bertujuan membantu pengguna memahami cara kerja Compressio, mulai dari instalasi, penggunaan, hingga pemecahan masalah umum.

---

## 3. Daftar Isi
1. Sampul
2. Kata Pengantar / Pendahuluan
3. Daftar Isi
4. Deskripsi Aplikasi
5. Fitur Utama Aplikasi
6. Spesifikasi Minimum
7. Panduan Instalasi
8. Panduan Penggunaan
9. Contoh Kasus / Studi Kasus
10. Troubleshooting (Pemecahan Masalah Umum)
11. Catatan Keamanan dan Privasi
12. Kontak Dukungan
13. Lampiran

---

## 4. Deskripsi Aplikasi
- **Fungsi Utama:** Kompresi dan dekompresi berbagai jenis file (gambar, dokumen, video, audio, arsip, dsb.) secara online.
- **Platform:** Web (akses via browser di PC, laptop, tablet, maupun smartphone)
- **Bahasa yang Digunakan:**
  - Antarmuka: Bahasa Indonesia & Inggris
  - Backend: Python (FastAPI)
  - Frontend: HTML, CSS, JavaScript

---

## 5. Fitur Utama Aplikasi
- **Login dengan Google:** Autentikasi aman menggunakan Firebase.
- **Upload File:** Mendukung drag & drop atau pilih file manual.
- **Pilih Metode & Profil Kompresi:** AI Selection, Gzip, Brotli, WebP, PDF Optimize, Office Optimize, Video Optimize. Profil: Default, Web, Archive, Network.
- **Mode Sensitif:** Deteksi konten sensitif pada file teks.
- **Riwayat Kompresi:** Lihat daftar file yang pernah dikompresi, rasio, ukuran, dan aksi (Download, Compare, Delete).
- **Compare:** Bandingkan file asli dan hasil kompresi.
- **Multi-bahasa:** UI mendukung Bahasa Indonesia & Inggris.
- **Batasan Kompresi:** 5 file per sesi untuk pengguna tanpa login, tanpa batas untuk pengguna login.

---

## 6. Spesifikasi Minimum
- **OS/Browser:**
  - Chrome, Firefox, Edge, Safari (versi terbaru)
  - Windows, macOS, Linux, Android, iOS
- **RAM:** Minimal 1 GB
- **Penyimpanan:** Cukup untuk file yang diunggah (maks. 5 MB per file)
- **Koneksi Internet:** Diperlukan untuk akses dan proses kompresi

---

## 7. Panduan Instalasi
- **Versi Web:**
  - Tidak perlu instalasi. Cukup buka [Compressio](http://localhost:8000) di browser.
  - Untuk developer: ikuti petunjuk di README.md untuk menjalankan backend dan frontend secara lokal.

---

## 8. Panduan Penggunaan

### Fitur: Login dengan Google
- **Deskripsi:** Masuk untuk mengakses fitur tanpa batas.
- **Langkah:**
  1. Klik tombol "Sign in with Google" di pojok kanan atas.
  2. Pilih akun Google Anda.
  3. Setelah login, nama Anda akan muncul di aplikasi.
- **Tips:** Login untuk menghilangkan batas 5 kompresi per sesi.

### Fitur: Upload & Kompresi File
- **Deskripsi:** Kompres file dengan mudah.
- **Langkah:**
  1. Klik "Pilih File" atau seret file ke area upload.
  2. Pilih metode dan profil kompresi sesuai kebutuhan.
  3. (Opsional) Aktifkan Mode Sensitif untuk deteksi konten sensitif.
  4. Klik "Process File".
  5. Tunggu proses selesai, file akan muncul di riwayat.
- **Tips:** Gunakan AI Selection untuk hasil optimal secara otomatis.

### Fitur: Riwayat Kompresi & Aksi
- **Deskripsi:** Lihat dan kelola hasil kompresi.
- **Langkah:**
  1. Buka tabel "Compression History".
  2. Klik "Download" untuk mengunduh hasil.
  3. Klik "Compare" untuk membandingkan file asli dan hasil kompresi.
  4. Klik "Delete" untuk menghapus riwayat.

### Fitur: Multi-bahasa
- **Deskripsi:** Ganti bahasa aplikasi.
- **Langkah:**
  1. Pilih bahasa di pojok kanan bawah.

---

## 9. Contoh Kasus / Studi Kasus
**Skenario:** Seorang mahasiswa ingin mengirim file PDF tugas akhir yang ukurannya 10MB ke email dosen (maksimal 5MB).
- **Langkah:**
  1. Upload file PDF ke Compressio.
  2. Pilih metode "PDF Optimize".
  3. Proses file, download hasil kompresi.
  4. File siap dikirim ke email dosen.

---

## 10. Troubleshooting (Pemecahan Masalah Umum)
- **Lupa password:** Login hanya menggunakan Google, tidak perlu password.
- **Tidak bisa login:** Pastikan koneksi internet stabil dan akun Google aktif.
- **Aplikasi tidak memuat:** Cek koneksi internet, refresh halaman, atau coba browser lain.
- **Data tidak tersimpan:** Pastikan browser tidak dalam mode private/incognito.
- **File gagal diproses:** Pastikan ukuran dan tipe file sesuai ketentuan.

---

## 11. Catatan Keamanan dan Privasi
- **Kebijakan Data:** File yang diunggah hanya disimpan sementara dan akan dihapus otomatis setelah beberapa waktu.
- **Tips Keamanan:** Jangan bagikan akun Google Anda ke orang lain. Selalu logout jika menggunakan komputer bersama.
- **Yang boleh/tidak boleh:**
  - Boleh: Menggunakan aplikasi untuk keperluan pribadi/pekerjaan.
  - Tidak boleh: Mengunggah file ilegal atau berisi konten terlarang.

---

## 12. Kontak Dukungan
- **Email:** support@compressio.app (contoh)
- **FAQ:** [Link FAQ](#) (belum tersedia)
- **Website:** [https://github.com/yourusername/compressio](https://github.com/yourusername/compressio)
- **Sosial Media:** @compressioapp (Instagram, Twitter)

---

## 13. Lampiran
- **Glosarium:**
  - *Kompresi*: Proses memperkecil ukuran file.
  - *Profil Kompresi*: Pengaturan optimasi sesuai kebutuhan (web, arsip, dsb).
  - *Mode Sensitif*: Fitur deteksi konten sensitif pada file teks.
- **Diagram Alur Kerja:**
  ![Alur Kerja Compressio](docs/assets/logo.png) <!-- Ganti dengan diagram jika tersedia -->
- **Link Desain Figma:** [Figma Compressio](#) (link placeholder)