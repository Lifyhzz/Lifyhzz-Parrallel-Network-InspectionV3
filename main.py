import time
import multiprocessing
import random

# Simulasi inspeksi keamanan pada paket/log jaringan
def inspeksi_log_jaringan(batch_id):
    # Simulasi beban komputasi (misal: dekripsi paket atau regex matching)
    beban = 1500
    _ = sum(i * j for i in range(beban) for j in range(beban))
    time.sleep(random.uniform(0.1, 0.2)) # Simulasi delay I/O pembacaan log
    
    # Simulasi hasil deteksi (90% Aman, 10% Anomali)
    status = random.choices(["Aman", "⚠️ Anomali/Serangan Terdeteksi"], weights=[0.9, 0.1])[0]
    return f"Inspeksi Batch Log [{batch_id}] -> {status}"

if __name__ == '__main__':
    # Simulasi 50 batch log lalu lintas jaringan
    dataset_log = list(range(1, 51))

    print("=== Parallel Network Traffic Inspection Engine ===")
    print(f"Total batch log yang akan dianalisis: {len(dataset_log)}\n")

    # ---------------------------------------------------------
    # 1. METODE SEKUENSIAL (Lambat)
    # ---------------------------------------------------------
    print("[1] Memulai Inspeksi Sekuensial (1 CPU Core)...")
    start_serial = time.time()
    for batch in dataset_log:
        inspeksi_log_jaringan(batch)
    waktu_serial = time.time() - start_serial
    print(f"--> Waktu Eksekusi Sekuensial: {waktu_serial:.4f} detik\n")

    # ---------------------------------------------------------
    # 2. METODE PARALEL (Cepat)
    # ---------------------------------------------------------
    cpu_cores = multiprocessing.cpu_count()
    print(f"[2] Memulai Inspeksi Paralel ({cpu_cores} CPU Cores)...")
    start_parallel = time.time()
    
    with multiprocessing.Pool(processes=cpu_cores) as pool:
        pool.map(inspeksi_log_jaringan, dataset_log)
        
    waktu_parallel = time.time() - start_parallel
    print(f"--> Waktu Eksekusi Paralel: {waktu_parallel:.4f} detik\n")

    # ---------------------------------------------------------
    # 3. KESIMPULAN PERFORMA
    # ---------------------------------------------------------
    print("==========================================================")
    print(f"HASIL: Pemrosesan Paralel {waktu_serial / waktu_parallel:.2f}x lebih cepat!")
    print("==========================================================")