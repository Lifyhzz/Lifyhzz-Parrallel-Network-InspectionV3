import time
import multiprocessing
import random
import sys

# Simulasi inspeksi keamanan pada paket/log jaringan
def inspeksi_log_jaringan(batch_id):
    # Simulasi beban komputasi (misal: dekripsi paket atau regex matching)
    beban = 1500
    _ = sum(i * j for i in range(beban) for j in range(beban))
    time.sleep(random.uniform(0.1, 0.2)) # Simulasi delay I/O pembacaan log
    
    # Simulasi hasil deteksi (90% Aman, 10% Anomali)
    status = random.choices(["✓ Aman", "⚠ Anomali/Serangan"], weights=[0.9, 0.1])[0]
    return (batch_id, status)

def print_box(text, char="="):
    """Print text dalam box"""
    width = max(len(line) for line in text.split('\n'))
    print(char * (width + 4))
    for line in text.split('\n'):
        print(f"{char} {line.ljust(width)} {char}")
    print(char * (width + 4))

def print_header(title):
    """Print section header"""
    width = 60
    print(f"\n{'='*width}")
    print(f"  {title}")
    print(f"{'='*width}")

if __name__ == '__main__':
    # Simulasi 50 batch log lalu lintas jaringan
    dataset_log = list(range(1, 51))

    print("\n" + "█" * 70)
    print("█  🔒 Parallel Network Traffic Inspection Engine".ljust(69) + "█")
    print("█  Implementasi Python Multiprocessing untuk Inspeksi Log Jaringan".ljust(69) + "█")
    print("█" * 70)
    
    print(f"\n  📊 Total batch log yang akan dianalisis: {len(dataset_log)} batch")
    print()

    # ---------------------------------------------------------
    # 1. METODE SEKUENSIAL (Lambat)
    # ---------------------------------------------------------
    print_header("[1] INSPEKSI SEKUENSIAL (1 CPU Core)")
    print(f"  ⏳ Memulai pemrosesan sequentially...\n")
    
    start_serial = time.time()
    results_serial = []
    for i, batch in enumerate(dataset_log):
        result = inspeksi_log_jaringan(batch)
        results_serial.append(result)
        # Tampilkan progress setiap 10 batch
        if (i + 1) % 10 == 0:
            print(f"  ✓ Selesai {i + 1}/{len(dataset_log)} batch diproses")
    
    waktu_serial = time.time() - start_serial
    print(f"\n  ⏱️  Waktu Eksekusi Sekuensial: {waktu_serial:.4f} detik")
    print(f"     ({waktu_serial/len(dataset_log):.4f} detik per batch)\n")

    # ---------------------------------------------------------
    # 2. METODE PARALEL (Cepat)
    # ---------------------------------------------------------
    cpu_cores = multiprocessing.cpu_count()
    print_header(f"[2] INSPEKSI PARALEL ({cpu_cores} CPU Cores)")
    print(f"  ⚡ Memulai pemrosesan dengan {cpu_cores} CPU cores...\n")
    
    start_parallel = time.time()
    
    with multiprocessing.Pool(processes=cpu_cores) as pool:
        results_parallel = pool.map(inspeksi_log_jaringan, dataset_log)
        
    waktu_parallel = time.time() - start_parallel
    print(f"  ✓ Semua batch selesai diproses!")
    print(f"\n  ⏱️  Waktu Eksekusi Paralel: {waktu_parallel:.4f} detik")
    print(f"     ({waktu_parallel/len(dataset_log):.4f} detik per batch)\n")

    # ---------------------------------------------------------
    # 3. KESIMPULAN PERFORMA
    # ---------------------------------------------------------
    print_header("📈 HASIL ANALISIS PERFORMA")
    
    speedup = waktu_serial / waktu_parallel
    efficiency = (speedup / cpu_cores) * 100
    
    print(f"\n  Kecepatan Sequential:  {waktu_serial:.4f} detik")
    print(f"  Kecepatan Parallel:    {waktu_parallel:.4f} detik")
    print(f"  {'─' * 50}")
    print(f"  ⚡ SPEEDUP: {speedup:.2f}x lebih cepat!")
    print(f"  📊 EFFICIENCY: {efficiency:.1f}% (terhadap CPU cores)")
    
    # Visualisasi bar chart sederhana
    print(f"\n  Perbandingan Waktu Eksekusi:")
    bar_length = 40
    serial_bar = int((waktu_serial / max(waktu_serial, waktu_parallel)) * bar_length)
    parallel_bar = int((waktu_parallel / max(waktu_serial, waktu_parallel)) * bar_length)
    
    print(f"  Sequential: [{'█' * serial_bar}{'─' * (bar_length - serial_bar)}] {waktu_serial:.4f}s")
    print(f"  Parallel:   [{'█' * parallel_bar}{'─' * (bar_length - parallel_bar)}] {waktu_parallel:.4f}s")
    
    print("\n" + "█" * 70)
    print("█ ✅ Analisis selesai!".ljust(69) + "█")
    print("█" * 70 + "\n")