import socket
import threading
import logging

logging.basicConfig(level=logging.INFO)

# Fungsi client yang akan dijalankan oleh banyak thread
def run_client(client_id):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = ('172.16.16.101', 45000)
        logging.info(f"[Client {client_id}] Connecting to {server_address}")
        sock.connect(server_address)

        # Kirim perintah TIME
        sock.sendall("TIME\r\n".encode('utf-8'))
        response = sock.recv(1024)
        logging.info(f"[Client {client_id}] Response: {response.decode('utf-8').strip()}")

        # Kirim perintah QUIT
        sock.sendall("QUIT\r\n".encode('utf-8'))

    except Exception as e:
        logging.error(f"[Client {client_id}] ERROR: {e}")

    finally:
        logging.info(f"[Client {client_id}] Closing connection")
        sock.close()

# Menjalankan banyak thread client
if __name__ == "__main__":
    NUM_CLIENTS = 20  # ukuran jumlah client

    threads = []
    for i in range(NUM_CLIENTS):
        t = threading.Thread(target=run_client, args=(i,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    logging.info("Semua client selesai.")
