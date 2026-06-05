<div align="center">

# 🚀 Parallel Network Traffic Inspection Engine

[![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20macOS-lightgrey?style=for-the-badge&logo=github)](https://github.com/Lifyhzz/Lifyhzz-Parrallel-Network-InspectionV3)
[![License](https://img.shields.io/badge/License-Academic-blueviolet?style=for-the-badge)](.)
[![Status](https://img.shields.io/badge/Status-Selesai%20✔-success?style=for-the-badge)](.)

**Mata Kuliah:** `IFB 206 — Komputasi Paralel`  
**Proyek:** Implementasi `multiprocessing` Python pada Analisis Keamanan Jaringan  
**Institusi:** Institut Teknologi Nasional Bandung

---

> *Demonstrasi empiris bahwa komputasi paralel dapat mempercepat inspeksi* ***log traffic jaringan*** *secara drastis dibandingkan pendekatan sekuensial konvensional.*

</div>

---

## 📑 Daftar Isi

| No. | Bagian | Deskripsi Singkat |
|:---:|--------|-------------------|
| 1 | [🌐 Latar Belakang](#1--latar-belakang) | Masalah bottleneck pada inspeksi log jaringan |
| 2 | [🏗️ Arsitektur Sistem](#2-️-desain-arsitektur-sistem) | Alur kerja sequential vs. parallel |
| 3 | [⚙️ Detail Implementasi](#3-️-detail-implementasi) | Penjelasan kode `main.py` |
| 4 | [⚡ Analisis Performa](#4--analisis-performa) | Perbandingan kecepatan & metrik |
| 5 | [💻 Instruksi Eksekusi](#5--instruksi-eksekusi) | Cara menjalankan simulasi |
| 6 | [📚 Konsep Kunci](#6--konsep-kunci) | Teori multiprocessing yang digunakan |
| 7 | [👥 Tim Pengembang](#-tim-pengembang) | Anggota kelompok pengembang |

---

## 1. 🌐 Latar Belakang

Dalam manajemen jaringan dan telekomunikasi modern, proses pemindaian keamanan —
seperti **vulnerability assessment** dan **packet sniffing** — harus memproses
**jutaan baris *log traffic*** setiap harinya.

### Permasalahan: Bottleneck Sequential

Metode pemrosesan **sekuensial** konvensional memproses satu entri log dalam satu waktu
menggunakan satu CPU core. Pada volume data tinggi, hal ini menyebabkan:

| ❌ Dampak Negatif | Penjelasan |
|-------------------|------------|
| **Bottleneck** | Antrian data menumpuk saat satu core kelebihan beban |
| **Latensi Tinggi** | Deteksi anomali tertunda berbanding lurus dengan jumlah data |
| **Tidak Skalabel** | Menambah data 2× langsung membuat waktu 2× lebih lama |
| **Risiko Keamanan** | Serangan bisa lolos karena detection delay terlalu besar |

### Solusi: Komputasi Paralel

Proyek ini menggunakan modul **`multiprocessing`** bawaan Python untuk mendistribusikan
beban inspeksi ke semua *logical CPU core* yang tersedia, sehingga log diproses
secara **konkuren** — bukan lagi satu-per-satu.

---

## 2. 🏗️ Desain Arsitektur Sistem

Beban *log* dibagi menjadi beberapa **chunk/batch** yang kemudian dieksekusi
secara bersamaan oleh beberapa **Worker Process** melalui `multiprocessing.Pool`.

```
  ┌──────────────────────────────────────────────┐
  │       Dataset: 50 Batch Log Jaringan         │
  └───────────────────┬──────────────────────────┘
                      │
                      ▼
  ┌──────────────────────────────────────────────┐
  │           Sistem Inspeksi (Dispatcher)       │
  └───────────┬──────────────────────┬───────────┘
              │                      │
   ┌──────────▼─────────┐   ┌────────▼──────────────┐
   │  CARA LAMA         │   │  CARA BARU             │
   │  Sequential        │   │  multiprocessing.Pool  │
   │  (1 CPU Core)      │   │  (Semua CPU Core)      │
   └──────────┬─────────┘   └──┬────┬────┬───────────┘
              │                │    │    │
              ▼             ┌──▼─┐┌─▼──┐┌▼───┐
     [Baris per baris]      │ W1 ││ W2 ││ W3 │  ← Worker Process
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
Lifyhzz-Parrallel-Network-InspectionV3/
├── main.py          # Skrip utama simulasi inspeksi paralel
├── index.html       # Halaman dokumentasi web (GitHub Pages)
├── _config.yml      # Konfigurasi tema Jekyll
└── README.md        # Dokumentasi proyek ini
```

### Fungsi Inti: `inspeksi_log_jaringan(batch_id)`

| Komponen | Detail |
|----------|--------|
| **Input** | `batch_id` — ID unik tiap batch log (integer 1–50) |
| **Beban Komputasi** | Nested loop `1500 × 1500` iterasi (simulasi regex/dekripsi paket) |
| **Delay I/O** | `random.uniform(0.1, 0.2)` detik — mensimulasikan latency pembacaan log |
| **Probabilitas Deteksi** | 90% → `"Aman"` \| 10% → `"⚠️ Anomali/Serangan Terdeteksi"` |
| **Output** | String hasil inspeksi per batch |

### Parameter Simulasi

| Parameter | Nilai | Keterangan |
|-----------|-------|------------|
| `dataset_log` | 50 batch | Jumlah batch log yang diinspeksi |
| Worker Sequential | 1 core | Satu CPU core saja |
| Worker Paralel | `cpu_count()` | Otomatis menyesuaikan jumlah core mesin |
| Pool Method | `pool.map()` | Mendistribusikan batch ke semua worker |
| Beban per batch | 1500 × 1500 iterasi | Simulasi komputasi berat per paket |
| Random seed | Tidak diset | Hasil bervariasi setiap eksekusi |

### Cuplikan Kode Kunci

```python
# ── Fungsi Inspeksi (dijalankan oleh setiap Worker) ──────────────
def inspeksi_log_jaringan(batch_id):
    beban = 1500
    _ = sum(i * j for i in range(beban) for j in range(beban))  # CPU-bound
    time.sleep(random.uniform(0.1, 0.2))                         # I/O bound sim

    status = random.choices(
        ["Aman", "⚠️ Anomali/Serangan Terdeteksi"],
        weights=[0.9, 0.1]   # Distribusi 90% Aman, 10% Anomali
    )[0]
    return f"Inspeksi Batch Log [{batch_id}] -> {status}"

# ── Paralel: Pool mendistribusikan 50 batch ke semua core ────────
cpu_cores = multiprocessing.cpu_count()
with multiprocessing.Pool(processes=cpu_cores) as pool:
    pool.map(inspeksi_log_jaringan, dataset_log)
```

---

## 4. ⚡ Analisis Performa

### Perbandingan Utama: Sequential vs. Paralel

| Aspek | 🔴 Sequential | 🟢 Paralel | Pemenang |
|-------|:-------------:|:----------:|:--------:|
| **Jumlah CPU Core** | 1 Core | N Core (semua) | 🟢 Paralel |
| **Strategi** | Baris per baris | Chunk konkuren | 🟢 Paralel |
| **Kompleksitas Waktu** | O(n) linear | O(n/core) | 🟢 Paralel |
| **Latensi Data Besar** | Tinggi | Rendah | 🟢 Paralel |
| **Risiko Bottleneck** | ❌ Tinggi | ✅ Sangat Rendah | 🟢 Paralel |
| **Skalabilitas** | ❌ Tidak skalabel | ✅ Linear per core | 🟢 Paralel |
| **Overhead Inisiasi** | ✅ Minimal | ⚠️ Ada (spawn) | 🔴 Sequential |
| **Cocok untuk Data Kecil** | ✅ Ya | ⚠️ Kurang efisien | 🔴 Sequential |
| **Cocok untuk Data Besar** | ❌ Tidak | ✅ Sangat cocok | 🟢 Paralel |
| **Penggunaan RAM** | Rendah | Lebih tinggi | 🔴 Sequential |

### Estimasi Speedup (Amdahl's Law)

| Jumlah Core | Speedup Teoritis | Speedup Praktis* | Efisiensi |
|:-----------:|:----------------:|:----------------:|:---------:|
| 1 core | 1.00× | 1.00× | 100% |
| 2 core | 2.00× | ~1.80× | ~90% |
| 4 core | 4.00× | ~3.40× | ~85% |
| 6 core | 6.00× | ~4.80× | ~80% |
| 8 core | 8.00× | ~6.00× | ~75% |
| 12 core | 12.00× | ~8.00× | ~67% |

> \* *Speedup praktis berkurang karena overhead spawn proses, koordinasi data, dan bagian kode yang tetap sekuensial.*

### Contoh Output Program

```
=== Parallel Network Traffic Inspection Engine ===
Total batch log yang akan dianalisis: 50

[1] Memulai Inspeksi Sekuensial (1 CPU Core)...
--> Waktu Eksekusi Sekuensial: 18.7321 detik

[2] Memulai Inspeksi Paralel (8 CPU Cores)...
--> Waktu Eksekusi Paralel: 4.8143 detik

==========================================================
HASIL: Pemrosesan Paralel 3.89x lebih cepat!
==========================================================
```

> ⚠️ *Hasil aktual bervariasi tergantung spesifikasi mesin. Semakin banyak core CPU, semakin besar speedup yang diperoleh.*

---

## 5. 💻 Instruksi Eksekusi

### Prasyarat

| Kebutuhan | Versi Minimum | Catatan |
|-----------|:-------------:|---------|
| Python | 3.8+ | Download di [python.org](https://python.org) |
| `multiprocessing` | Built-in | Tidak perlu instalasi tambahan |
| `time` | Built-in | Tidak perlu instalasi tambahan |
| `random` | Built-in | Tidak perlu instalasi tambahan |
| RAM | 512 MB+ | Untuk menjalankan multiple worker process |
| CPU | 2+ core | Agar paralel memberikan manfaat nyata |

### Langkah-langkah

**1. Clone repositori**
```bash
git clone https://github.com/Lifyhzz/Lifyhzz-Parrallel-Network-InspectionV3.git
cd Lifyhzz-Parrallel-Network-InspectionV3
```

**2. Jalankan simulasi**
```bash
python main.py
```

**3. Baca output**

Program akan secara otomatis:
- ✅ Menjalankan inspeksi **sequential** (1 core) dan mencatat waktunya
- ✅ Menjalankan inspeksi **paralel** (semua core) dan mencatat waktunya
- ✅ Menampilkan **perbandingan speedup** di akhir eksekusi

### Kompatibilitas Platform

| Platform | Status | Catatan |
|----------|:------:|---------|
| Windows 10/11 | ✅ | Wajib pakai `if __name__ == '__main__':` |
| Ubuntu / Debian | ✅ | Fork-based, berjalan mulus |
| macOS | ✅ | Spawn-based di Python 3.8+ |

---

## 6. 📚 Konsep Kunci

### Modul `multiprocessing` Python

| Konsep | Penjelasan |
|--------|------------|
| **`multiprocessing.Pool`** | Membuat *pool* worker process sejumlah CPU core yang tersedia |
| **`pool.map(func, iterable)`** | Mendistribusikan setiap item iterable ke worker yang tersedia |
| **Proses vs. Thread** | Proses memiliki memori **terpisah** — bebas dari GIL (Global Interpreter Lock) |
| **`cpu_count()`** | Fungsi untuk mendeteksi jumlah logical core yang dimiliki mesin |
| **Spawn vs. Fork** | Windows: spawn (lebih lambat start) \| Linux/macOS: fork (lebih cepat) |

### Mengapa `multiprocessing` dan Bukan `threading`?

| Faktor | `threading` | `multiprocessing` |
|--------|:-----------:|:-----------------:|
| GIL (Global Interpreter Lock) | ❌ Terikat GIL | ✅ Bebas dari GIL |
| Cocok untuk CPU-bound task | ❌ Tidak | ✅ Ya |
| Cocok untuk I/O-bound task | ✅ Ya | ⚠️ Berlebihan |
| Memori terpisah per worker | ❌ Shared | ✅ Isolated |
| Overhead | Rendah | Lebih tinggi |
| **Kasus proyek ini** | ❌ Kurang tepat | ✅ **Pilihan yang tepat** |

> Karena `inspeksi_log_jaringan()` melibatkan komputasi berat (nested loop CPU-bound), `multiprocessing` adalah pilihan yang **jauh lebih tepat** daripada `threading`.

---

## 👥 Tim Pengembang

| No. | Nama | NIM |
|:---:|------|-----|
| 1 | **Lifyana Nailah Azzahra** | 152024107 |
| 2 | **Nik Intan Elyana** | 152024132 |

---

<div align="center">

---

**Parallel Network Traffic Inspection Engine**  
📍 IFB 206 Komputasi Paralel &nbsp;·&nbsp; Institut Teknologi Nasional Bandung &nbsp;·&nbsp; 2025/2026

[![GitHub](https://img.shields.io/badge/GitHub-Lifyhzz-181717?style=flat-square&logo=github)](https://github.com/Lifyhzz/Lifyhzz-Parrallel-Network-InspectionV3)

</div>