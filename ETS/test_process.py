import time
from concurrent.futures import ProcessPoolExecutor
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

LOG_FILE = 'stress_test_log2.txt'

def client_worker(op, filename, nomor, client_id, server_pool):
    start = time.time()
    try:
        if op == 'UPLOAD':
            remote_upload(filename)
        elif op == 'GET':
            remote_get(filename)
        else:
            return (False, 0.0, nomor, client_id, op, filename, server_pool, "INVALID OP")

        duration = time.time() - start
        throughput = convert_size_to_bytes_by_filename(filename) / duration
        return (True, duration, nomor, client_id, op, filename, server_pool, throughput)
    except Exception as e:
        return (False, 0.0, nomor, client_id, op, filename, server_pool, f"ERROR: {e}")

def run_stress_test():
    results = []
    nomor = 1

    # Kosongkan isi file log jika ada
    open(LOG_FILE, 'w').close()

    for op in ops:
        for vol, filename in files.items():
            for client_pool in client_pools:
                for server_pool in server_pools:
                    header = f"\nRunning test #{nomor}: {op} | {vol} | client={client_pool} | server={server_pool}"
                    print(header)
                    append_log(header)

                    success = 0
                    failed = 0
                    total_time = 0.0

                    with ProcessPoolExecutor(max_workers=client_pool) as executor:
                        futures = [executor.submit(client_worker, op, filename, nomor, i+1, server_pool) for i in range(client_pool)]

                        for f in futures:
                            ok, duration, nomor_, client_id, op_, file_, sp, other = f.result()
                            if ok:
                                throughput = other
                                log_line = f"[#{nomor_}] Client-{client_id} | {op_} {file_} | Server Pool={sp} | Time={round(duration, 4)}s | Throughput={round(throughput, 2)} B/s | Status=SUKSES"
                                success += 1
                                total_time += duration
                            else:
                                log_line = f"[#{nomor_}] Client-{client_id} | {op_} {file_} | Server Pool={sp} | Status=GAGAL | Info={other}"
                                failed += 1

                            print(log_line)
                            append_log(log_line)

                    avg_time = total_time / success if success else 0
                    throughput = (convert_size_to_bytes(vol) / avg_time) if avg_time else 0

                    results.append([
                        nomor, op, vol, client_pool, server_pool,
                        round(avg_time, 4), round(throughput, 2),
                        f"{success} sukses", f"{failed} gagal"
                    ])

                    nomor += 1

    # Ringkasan
    print("\n--- Ringkasan ---")
    append_log("\n--- Ringkasan ---")
    header = "Nomor | Operasi | Volume | Jumlah client pool | Jumlah server pool | Waktu total per client (s) | Throughput per client (B/s) | Client sukses/gagal"
    print(header)
    append_log(header)

    for row in results:
        line = " | ".join(map(str, row))
        print(line)
        append_log(line)

def append_log(text):
    with open(LOG_FILE, 'a') as f:
        f.write(text + '\n')

def convert_size_to_bytes(label):
    if label == '10MB':
        return 10 * 1024 * 1024
    elif label == '50MB':
        return 50 * 1024 * 1024
    elif label == '100MB':
        return 100 * 1024 * 1024
    return 0

def convert_size_to_bytes_by_filename(filename):
    if '10mb' in filename.lower():
        return 10 * 1024 * 1024
    elif '50mb' in filename.lower():
        return 50 * 1024 * 1024
    elif '100mb' in filename.lower():
        return 100 * 1024 * 1024
    return 0

if __name__ == '__main__':
    run_stress_test()
