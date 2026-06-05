<div align="center">

# 🚀 Distributed Respiratory Inspection Engine

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge&logo=github)](https://github.com/Lifyhzz/Respiratory-Inspection)
[![License](https://img.shields.io/badge/License-Academic-blueviolet?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Selesai%20✔-success?style=for-the-badge)](.)

**Mata Kuliah:** `IFB 206 — Komputasi Paralel`  
**Proyek:** Implementasi `multiprocessing` Python pada Analisis Grafik Pernapasan (Spirometri)  
**Institusi:** Institut Teknologi Nasional Bandung

---

> *Demonstrasi empiris bahwa komputasi paralel dapat mempercepat inspeksi* ***grafik pernapasan*** *secara drastis dibandingkan pendekatan sekuensial konvensional.*

</div>

---

## 📑 Daftar Isi

| No. | Bagian | Deskripsi Singkat |
|:---:|--------|-------------------|
| 1 | [🩺 Latar Belakang](#1--latar-belakang) | Masalah bottleneck pada inspeksi grafik pernapasan |
| 2 | [🏗️ Arsitektur Sistem](#2-️-desain-arsitektur-sistem) | Alur kerja sequential vs. parallel |
| 3 | [⚙️ Detail Implementasi](#3-️-detail-implementasi) | Penjelasan kode `main.py` |
| 4 | [⚡ Analisis Performa](#4--analisis-performa) | Perbandingan kecepatan & metrik |
| 5 | [💻 Instruksi Eksekusi](#5--instruksi-eksekusi) | Cara menjalankan simulasi |
| 6 | [📚 Konsep Kunci](#6--konsep-kunci) | Teori multiprocessing yang digunakan |
| 7 | [👥 Tim Pengembang](#-tim-pengembang) | Anggota kelompok pengembang |

---

## 1. 🩺 Latar Belakang

Dalam analisis medis modern, proses pemindaian kesehatan pasien — seperti **pengukuran volume tidal** dan **analisis spirometri** — kerap harus memproses jutaan titik data grafik pernapasan setiap harinya.

### Permasalahan: Bottleneck Sequential

Metode pemrosesan **sekuensial** konvensional memproses satu segmen data dalam satu waktu menggunakan satu CPU core. Pada volume data tinggi, hal ini menyebabkan:

| ❌ Dampak Negatif | Penjelasan |
|-------------------|------------|
| **Bottleneck** | Antrian data menumpuk saat satu core kelebihan beban |
| **Latensi Tinggi** | Deteksi anomali tertunda berbanding lurus dengan jumlah data |
| **Tidak Skalabel** | Menambah data 2× langsung membuat waktu 2× lebih lama |
| **Risiko Medis** | Deteksi kondisi kritis pasien terhambat oleh delay sistem |

### Solusi: Komputasi Paralel

Proyek ini menggunakan modul **`multiprocessing`** bawaan Python untuk mendistribusikan beban inspeksi grafik ke semua *logical CPU core* yang tersedia, sehingga data diproses secara **konkuren** — bukan lagi satu-per-satu.

---

## 2. 🏗️ Desain Arsitektur Sistem

Beban *grafik* dibagi menjadi beberapa **batch** yang kemudian dieksekusi secara bersamaan oleh beberapa **Worker Process** melalui `multiprocessing.Pool`.

```
  ┌──────────────────────────────────────────────┐
  │      Dataset: Batch Grafik Pernapasan        │
  └───────────────────┬──────────────────────────┘
                      │
                      ▼
  ┌──────────────────────────────────────────────┐
  │          Sistem Inspeksi (Dispatcher)        │
  └───────────┬──────────────────────┬───────────┘
              │                      │
    ┌──────────▼─────────┐   ┌────────▼──────────────┐
    │  CARA LAMA         │   │  CARA BARU             │
    │  Sequential        │   │  multiprocessing.Pool  │
    │  (1 CPU Core)      │   │  (Semua CPU Core)      │
    └──────────┬─────────┘   └──┬────┬────┬───────────┘
              │                │    │    │
              ▼             ┌──▼─┐┌─▼──┐┌▼───┐
      [Satu per satu]       │ W1 ││ W2 ││ W3 │  ← Worker Node
              │             └──┬─┘└─┬──┘└┬───┘
              ▼                └────┴────┘
    ┌──────────────────┐              │
    │ ⚠️ Deteksi Lambat │              ▼
    │    (Bottleneck)  │   ┌───────────────────────┐
    └──────────────────┘   │ Agregasi Status Akhir │
                           └──────────┬────────────┘
                                      ▼
                           ┌──────────────────────┐
                           │ ⚡ Deteksi Real-time  │
                           │    (Cepat & Stabil)  │
                           └──────────────────────┘
```

---

## 3. ⚙️ Detail Implementasi

Kode utama terdapat pada file **`main.py`**. Berikut rincian setiap komponennya:

### Struktur File

```
Respiratory-Inspection/
├── main.py          # Skrip utama simulasi inspeksi paralel
├── index.html       # Halaman dokumentasi web & simulator interaktif
├── _config.yml      # Konfigurasi tema
└── README.md        # Dokumentasi proyek ini
```

### Fungsi Inti: `analyze_respiratory_graph(batch_data)`

| Komponen | Detail |
|----------|--------|
| **Input** | `batch_data` — Potongan data volume pernapasan |
| **Logika** | Mengecek ambang batas normal (400-600 mL) |
| **Delay Sim** | `random.uniform(0.5, 1.5)` detik — mensimulasikan latensi komputasi |
| **Status** | `"BAHAYA"` (jika anomali ditemukan) \| `"NORMAL"` |
| **Output** | Objek hasil status dan jumlah anomali |

---

## 4. ⚡ Analisis Performa

### Perbandingan Utama: Sequential vs. Paralel

| Aspek | 🔴 Sequential | 🟢 Paralel | Pemenang |
|-------|:-------------:|:----------:|:--------:|
| **Jumlah CPU Core** | 1 Core | N Core (semua) | 🟢 Paralel |
| **Strategi** | Satu per satu | Chunk paralel | 🟢 Paralel |
| **Kompleksitas Waktu** | O(n) | O(n/core) | 🟢 Paralel |
| **Latensi Data Besar** | Tinggi | Rendah | 🟢 Paralel |
| **Skalabilitas** | ❌ Tidak | ✅ Sangat Skalabel | 🟢 Paralel |

### Contoh Output Program

```
==========================================================
🚀 DISTRIBUTED RESPIRATORY INSPECTION ENGINE
==========================================================

📡 Master Node: Menerima aliran grafik pernapasan masuk...
📥 Total Data Grafik: 1000 titik
🔀 Memecah antrean menjadi 5 batch...
🌐 Mendistribusikan beban ke Cluster Worker...

📊 HASIL REKAPITULASI CLUSTER:
  ➜ Batch #1 diproses oleh ForkPoolWorker-1 | Status: NORMAL | Anomali: 0
  ➜ Batch #2 diproses oleh ForkPoolWorker-2 | Status: BAHAYA | Anomali: 1
  ...

⏱️ Waktu Eksekusi Terdistribusi : 1.20 detik
✅ Inspeksi selesai. Sistem berjalan responsif!
```

---

## 5. 💻 Instruksi Eksekusi

### Langkah-langkah

**1. Clone repositori**
```bash
git clone https://github.com/Lifyhzz/Respiratory-Inspection.git
cd Respiratory-Inspection
```

**2. Jalankan simulasi**
```bash
python main.py
```

# --- Contoh Output ---
✔ [Sequential] Waktu pemrosesan : 4.732 detik
✔ [Parallel  ] Waktu pemrosesan : 1.201 detik
💡 Speedup Paralel               : ~3.94×

---

## 👥 Tim Pengembang

| No. | Nama | NIM |
|:---:|------|-----|
| 1 | **Lifyana Nailah Azzahra** | 152024107 |
| 2 | **Nik Intan Elyana** | 152024132 |

---

<div align="center">

**Distributed Respiratory Inspection Engine**  
📍 IFB 206 Komputasi Paralel &nbsp;·&nbsp; ITENAS Bandung &nbsp;·&nbsp; 2025/2026

</div>