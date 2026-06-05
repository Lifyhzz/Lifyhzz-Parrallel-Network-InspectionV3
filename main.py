import random
import time
import matplotlib.pyplot as plt
import numpy as np
from multiprocessing import Pool

# =========================================================================
# BLOK PEMROSESAN SINYAL (Digital Signal Processing)
# Fungsi ini dijalankan secara paralel di berbagai core CPU
# =========================================================================
def check_anomaly(data_pair):
    """
    Fungsi worker untuk mengecek apakah satu titik data adalah anomali.
    Menerima tuple (indeks, volume).
    """
    index, volume = data_pair
    # Kriteria Anomali: Di bawah 100mL (Sesak) atau di atas 1500mL (Abnormal)
    if volume < 100 or volume > 1500:
        return index
    return None

if __name__ == '__main__':
    print("==========================================================")
    print("🏥 RESPIRATORY INSPECTION SYSTEM - SPIROMETRY TRIAL")
    print("   ITENAS - IFB 206 Komputasi Paralel")
    print("   Uji Coba Distribusi Volume Pernapasan (Paralel)")
    print("==========================================================\n")

    # 1. GENERASI DATA (1000 Observasi)
    print("📊 Menggenerasi 1000 titik data observasi pernapasan...")
    respiratory_data = [random.randint(400, 600) for _ in range(1000)]
    
    # 2. PENYUNTIKAN ANOMALI (Sesuai Spesifikasi Bagian 03)
    respiratory_data[250] = 50   # Indeks 250: Napas pendek ekstrim
    respiratory_data[880] = 1800 # Indeks 880: Puncak abnormal 

    # 3. DETEKSI ANOMALI PARALEL (Menggunakan Pool)
    print("🔍 Menjalankan deteksi anomali pada Cluster Core...")
    start_time = time.time()
    
    # Menyiapkan pasangan (indeks, data) untuk diproses
    data_pairs = list(enumerate(respiratory_data))
    
    # Menggunakan Pool untuk membagi tugas ke semua CPU Core
    with Pool() as pool:
        results = pool.map(check_anomaly, data_pairs)
    
    # Menyaring hasil (hanya indeks yang tidak None)
    anomalies_detected = [res for res in results if res is not None]
    
    end_time = time.time()
    print(f"✅ Analisis Selesai dalam {end_time - start_time:.4f} detik.")
    print(f"⚠️ Ditemukan {len(anomalies_detected)} anomali pada indeks: {anomalies_detected}\n")

    # 4. VISUALISASI GRAFIK SPIROMETRI (Matplotlib)
    print("📈 Menyiapkan potret visualisasi grafik...")
    
    data_points = np.array(respiratory_data)
    plt.figure(figsize=(14, 7), facecolor='#f8fafc')
    
    # Plot utama
    plt.plot(data_points, color='#0891b2', linewidth=1, alpha=0.7, label='Volume Tidal (mL)')
    
    # Batas Normal
    plt.axhspan(400, 600, color='#16a34a', alpha=0.1, label='Rentang Normal (400-600 mL)')
    
    # Markah Anomali (Merah)
    plt.scatter(anomalies_detected, data_points[anomalies_detected], 
                color='#dc2626', s=80, edgecolors='white', linewidth=1.5, 
                zorder=5, label='Anomali Terdeteksi')

    # Anotasi Spesifik (Bagian 03)
    plt.annotate('Napas Pendek Ekstrim (Indeks 250)', xy=(250, 50), xytext=(100, 250),
                 arrowprops=dict(facecolor='#334155', shrink=0.08, width=1, headwidth=6),
                 fontsize=9, fontweight='bold', color='#dc2626')
    
    plt.annotate('Puncak Abnormal (Indeks 880)', xy=(880, 1800), xytext=(700, 1600),
                 arrowprops=dict(facecolor='#334155', shrink=0.08, width=1, headwidth=6),
                 fontsize=9, fontweight='bold', color='#dc2626')

    # Font & Styling
    plt.title('Grafik Uji Coba Spirometri - Simulasi Inspeksi Pernapasan', 
              fontsize=15, fontweight='800', pad=20, color='#0f172a')
    plt.xlabel('Indeks Observasi', fontsize=11, color='#64748b')
    plt.ylabel('Volume (mL)', fontsize=11, color='#64748b')
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    plt.show()
    
    print("==========================================================")
    print("Sistem Inspeksi Selesai: Semua anomali telah tertandai.")
    print("==========================================================")
