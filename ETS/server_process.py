import socket
from concurrent.futures import ProcessPoolExecutor
from file_protocol import FileProtocol

def handle_client(conn_data):
    conn, addr = conn_data
    try:
        data = b""
        while True:
            chunk = conn.recv(65536)
            if not chunk:
                break
            data += chunk
            if b"\r\n\r\n" in data:
                break
        if data:
            request = data.decode().strip()
            response = FileProtocol().proses_string(request)
            conn.sendall((response + '\r\n\r\n').encode())
    except Exception as e:
        print(f"Error handling client {addr}: {e}")
    finally:
        conn.close()

def main():
    host = '0.0.0.0'
    port = 33333
    max_workers = 50  # Sesuaikan sesuai kebutuhan
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        print(f"Server berjalan di {host}:{port} dengan ProcessPoolExecutor ({max_workers} workers)")
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            while True:
                conn, addr = s.accept()
                executor.submit(handle_client, (conn, addr))

if __name__ == "__main__":
    main()
