# Compressio - File Compression Web Application

Compressio adalah aplikasi web modern untuk kompresi file dengan antarmuka ramah pengguna, mendukung berbagai jenis file, pilihan metode/profil kompresi, mode sensitif, serta autentikasi Google (Firebase).

## Fitur Utama

- Kompresi berbagai file: gambar, dokumen, video, audio, arsip, dsb.
- Pilihan metode kompresi: AI Selection, Gzip, Brotli, WebP, PDF Optimize, Office Optimize, Video Optimize.
- Profil kompresi: Default, Web, Archive, Network.
- Mode sensitif untuk deteksi entitas sensitif pada file teks (NLP).
- Riwayat kompresi: lihat rasio, ukuran asli, ukuran terkompresi, dan aksi (Download, Compare, Delete).
- Komparasi file (perbandingan hasil kompresi).
- Batas kompresi untuk pengguna anonim, tanpa batas untuk pengguna login.
- Autentikasi Google (Firebase).
- UI responsif, mendukung multi-bahasa (EN/ID).

## Tech Stack

### Frontend
- HTML5, CSS3, JavaScript (Vanilla)
- Bootstrap 5
- Firebase Authentication

### Backend
- Python 3
- FastAPI, Uvicorn
- SQLAlchemy (SQLite)
- Pillow, OpenCV, scikit-image, pypdf, moviepy, brotli, gzip, python-magic, diff-match-patch, lxml, requests
- spaCy, TextBlob, NLTK (untuk mode sensitif/NLP)

## Struktur Proyek

```
Compressio/
├── backend/
│   ├── app.py
│   ├── main.py
│   ├── requirements.txt
│   └── utils/
├── docs/
│   ├── index.html
│   ├── about.html
│   ├── css/
│   ├── js/
│   └── assets/
├── tmp/
│   ├── uploads/
│   └── downloads/
├── README.md
└── requirements.txt
```

## Setup & Instalasi

1. **Clone repository:**
```bash
git clone https://github.com/yourusername/compressio.git
cd compressio
```

2. **Setup backend:**
```bash
cd backend
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

3. **Jalankan backend (FastAPI):**
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

4. **Frontend:**
   - Buka file `docs/index.html` di browser, atau
   - Jalankan static server (misal: `python -m http.server` di folder `docs/`)

5. **Konfigurasi Firebase (opsional):**
   - Buat project Firebase, aktifkan Google Authentication
   - Tambahkan konfigurasi Firebase ke `docs/js/auth.js`

## Penggunaan

1. Buka aplikasi di browser
2. (Opsional) Login dengan Google
3. Upload file untuk kompresi
4. Pilih metode & profil kompresi, aktifkan mode sensitif jika perlu
5. Proses file, lihat hasil di riwayat, download atau compare hasil kompresi

## Supported File Types
- Gambar: PNG, JPEG, WebP
- Dokumen: TXT, PDF, DOC, DOCX, XLS, XLSX, PPT, PPTX
- Arsip: ZIP, RAR
- Video: MP4, MPEG, MOV
- Audio: MP3, WAV
- Lainnya: JSON, BIN

## Limitasi
- Pengguna tanpa login: maksimal 5 kompresi per sesi
- Pengguna login: tanpa batas

## Lisensi
MIT License

## Kontribusi
Kontribusi sangat terbuka! Silakan buat Pull Request atau Issue untuk perbaikan/fitur baru. 