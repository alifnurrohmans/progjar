import socket
import logging

# Set ke server lokal
server_address = ('172.16.16.101', 8889)  # atau 8885 untuk thread pool

def make_socket(destination_address='localhost', port=8889):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((destination_address, port))
        return sock
    except Exception as e:
        logging.warning(f"Socket error: {str(e)}")
        return None

def send_command(command_str):
    sock = make_socket(server_address[0], server_address[1])
    if not sock:
        print("Gagal koneksi ke server.")
        return ""
    try:
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(1024)
            if not data:
                break
            data_received += data.decode()
            if "\r\n\r\n" in data_received:
                break
        return data_received
    except Exception as e:
        print(f"Error saat komunikasi: {e}")
        return ""
    finally:
        sock.close()

# CLI testing
if __name__ == "__main__":
    while True:
        print("""
Pilih operasi:
1. Lihat daftar file
2. Upload file dummy
3. Hapus file
4. Keluar
""")
        pilih = input("Pilihan Anda [1-4]: ")
        if pilih == '1':
            cmd = "GET /list HTTP/1.0\r\n\r\n"
        elif pilih == '2':
            cmd = "POST /upload HTTP/1.0\r\n\r\n"
        elif pilih == '3':
            filename = input("Nama file yang ingin dihapus: ")
            cmd = f"DELETE /hapus/{filename} HTTP/1.0\r\n\r\n"
        elif pilih == '4':
            print("Keluar dari program.")
            break
        else:
            print("Pilihan tidak valid.")
            continue

        hasil = send_command(cmd)
        print("\nResponse dari server:\n", hasil)
