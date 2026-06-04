# Parallel Network Traffic Inspection Engine
> **Mata Kuliah:** IFB 206 Komputasi Paralel
> **Proyek:** Implementasi Multiprocessing pada Analisis Keamanan Jaringan

---

## Daftar Isi
1. [Latar Belakang](#1-latar-belakang)
2. [Desain Arsitektur Sistem](#2-desain-arsitektur-sistem)
3. [Analisis Performa](#3-analisis-performa)
4. [Instruksi Eksekusi](#4-instruksi-eksekusi)

---

## 1. Latar Belakang
Dalam manajemen jaringan dan telekomunikasi, melakukan pemindaian keamanan (*vulnerability assessment* atau *packet sniffing*) terhadap jutaan baris *log traffic* membutuhkan daya komputasi yang masif. Metode pemrosesan sekuensial konvensional seringkali memicu *bottleneck* yang menunda deteksi anomali. Proyek ini mendemonstrasikan efisiensi komputasi paralel menggunakan modul `multiprocessing` pada Python untuk mempercepat inspeksi *batch log* jaringan secara *real-time*.

## 2. Desain Arsitektur Sistem
Beban pemrosesan *log* didistribusikan secara merata ke seluruh *core logical* yang tersedia pada *server*, memecah antrean data menjadi beberapa eksekusi konkuren.

```mermaid
graph TD
    A[Dataset: Batch Log Jaringan] --> B{Sistem Inspeksi}
    B -->|Cara Lama| C[Sekuensial: 1 Core membaca baris per baris]
    B -->|Cara Baru| D[Paralel: Pool Multiprocessing]
    D --> E[Worker 1]
    D --> F[Worker 2]
    D --> G[Worker 3]
    E & F & G --> H[Agregasi Status Keamanan]
    C -.-> I[Deteksi Lambat / Bottleneck]
    H -.-> J[Deteksi Real-time & Cepat]