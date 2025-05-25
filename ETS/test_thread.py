import time
import csv
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from client import remote_upload, remote_get

# Ukuran file dan nama yang harus tersedia
files = {
    '10MB': 'file_10mb.bin',
    '50MB': 'file_50mb.bin',
    '100MB': 'file_100mb.bin'
}

# Konfigurasi kombinasi
ops = ['GET', 'UPLOAD']
client_pools = [1, 5, 50]
server_pools = [1, 5, 50]

# Fungsi worker

def client_worker(op, filename, nomor, client_id, server_pool):
    start = time.time()
    try:
        if op == 'UPLOAD':
            remote_upload(filename)
        elif op == 'GET':
            remote_get(filename)
        else:
            return False, 0.0
        duration = time.time() - start
        throughput = convert_size_to_bytes_by_filename(filename) / duration
        print(f"[#{nomor}] Client-{client_id} | {op} {filename} | Server Pool={server_pool} | Time={round(duration, 4)}s | Throughput={round(throughput, 2)} B/s | Status=SUKSES")
        return True, duration
    except Exception as e:
        print(f"[#{nomor}] Client-{client_id} | {op} {filename} | Server Pool={server_pool} | Status=GAGAL | Error={e}")
        return False, 0.0

# Jalankan stress test
def run_stress_test():
    results = []
    nomor = 1

    for op in ops:
        for vol, filename in files.items():
            for client_pool in client_pools:
                for server_pool in server_pools:
                    print(f"\nRunning test #{nomor}: {op} | {vol} | client={client_pool} | server={server_pool}")

                    success = 0
                    failed = 0
                    total_time = 0.0

                    with ThreadPoolExecutor(max_workers=client_pool) as executor:
                        futures = [executor.submit(client_worker, op, filename, nomor, i+1, server_pool) for i in range(client_pool)]

                        for f in futures:
                            ok, t = f.result()
                            if ok:
                                success += 1
                                total_time += t
                            else:
                                failed += 1

                    avg_time = total_time / success if success else 0
                    throughput = (convert_size_to_bytes(vol) / avg_time) if avg_time else 0

                    results.append([
                        nomor, op, vol, client_pool, server_pool,
                        round(avg_time, 4), round(throughput, 2),
                        f"{success} sukses", f"{failed} gagal"
                    ])

                    nomor += 1

    print("\n--- Ringkasan ---")
    print("Nomor | Operasi | Volume | Jumlah client pool | Jumlah server pool | Waktu total per client (s) | Throughput per client (B/s) | Client sukses/gagal")
    for row in results:
        print(" | ".join(map(str, row)))

# Bantuan konversi ukuran

def convert_size_to_bytes(label):
    if label == '10MB':
        return 10 * 1024 * 1024
    elif label == '50MB':
        return 50 * 1024 * 1024
    elif label == '100MB':
        return 100 * 1024 * 1024
    return 0

def convert_size_to_bytes_by_filename(filename):
    if '10mb' in filename:
        return 10 * 1024 * 1024
    elif '50mb' in filename:
        return 50 * 1024 * 1024
    elif '100mb' in filename:
        return 100 * 1024 * 1024
    return 0

if __name__ == '__main__':
    run_stress_test()