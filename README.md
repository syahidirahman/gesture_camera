# 🎥 Gesture-Controlled Camera

> **Portofolio Proyek Computer Vision Real-Time**

[![Python](https://img.shields.io/badge/Python-3.10-blue.svg)](https://www.python.org/)
[![OpenCV](https://img.shields.io/badge/OpenCV-4.8-green.svg)](https://opencv.org/)
[![MediaPipe](https://img.shields.io/badge/MediaPipe-0.10-pink.svg)](https://developers.google.com/mediapipe)

---

## 📌 Deskripsi

Proyek ini adalah aplikasi kamera interaktif yang merespons gestur tangan untuk mengaktifkan efek visual secara real-time. Dibangun dengan **MediaPipe** untuk deteksi landmark tangan dan **OpenCV** untuk pemrosesan citra.

## 🖐️ Fitur Gestur

| Jari    | Gestur            | Efek                 | Tampilan                                |
| :------ | :---------------- | :------------------- | :-------------------------------------- |
| 1 Jari  | Telunjuk Menunjuk | 🔦 **Spotlight**     | Area sekitar jari terang, sisanya gelap |
| 2 Jari  | Peace / V Sign    | 🔒 **Blur**          | Seluruh layar buram (privasi)           |
| 3 Jari  | Tiga Jari         | ✏️ **Sketsa Pensil** | Gambar menjadi sketsa hitam-putih       |
| Lainnya | -                 | ✅ **Normal**        | Tampilan jernih tanpa efek              |

## ⚙️ Instalasi

### 1. Clone Repository

```bash
git clone https://github.com/syahidirahman/gesture_camera.git  
cd gesture-camera
```

### 2. Buat Virtual Environment (Rekomendasi)

```bash
python -m venv venv_mp
source venv_mp/bin/activate  # Linux/Mac
.\venv_mp\Scripts\activate   # Windows
```

### 3. Install Dependensi

```bash
pip install -r requirements.txt
```

### 4. Jalankan Program

```bash
python gesture_camera.py
```

## 🎮 Cara Penggunaan

1. Pastikan webcam terhubung.
2. Jalankan program.
3. Tunjukkan gestur tangan di depan kamera:
   - ☝️ **1 Jari** → Spotlight
   - ✌️ **2 Jari** → Blur
   - 🖖 **3 Jari** → Sketsa
4. Tekan `ESC` atau `Q` untuk keluar.

## 🛠️ Teknologi yang Digunakan

- **Python 3.10** — Bahasa pemrograman utama
- **MediaPipe** — Deteksi landmark tangan (21 titik)
- **OpenCV** — Pemrosesan citra real-time
- **NumPy** — Manipulasi array dan matriks

## 📁 Struktur Kode

```
gesture-camera/
├── gesture_camera.py          # Kode utama
├── requirements.txt           # Daftar library
├── README.md                  # Dokumentasi proyek
├── .gitignore                 # File yang diabaikan Git
└── demo/                      # Folder untuk demo
    ├── demo_1_spotlight.gif
    ├── demo_2_blur.gif
    └── demo_3_sketch.gif
```

## 🚀 Pengembangan Selanjutnya

- [ ] Tambahkan gestur 4 jari untuk efek negatif
- [ ] Integrasi dengan screenshot otomatis
- [ ] Mode presentasi (cursor virtual)
- [ ] GUI dengan Tkinter untuk kontrol manual

## 📄 Lisensi

MIT License

---

**Dibuat dengan ❤️ oleh [Syahidi Rahman]**
