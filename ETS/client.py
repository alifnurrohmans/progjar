import socket
import json
import base64
import os

SERVER_ADDRESS = ('172.16.16.101', 11111)  # Sesuaikan dengan alamat server

def send_command(command_str):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(SERVER_ADDRESS)
            sock.sendall((command_str + '\r\n\r\n').encode())
            data = b""
            while True:
                chunk = sock.recv(65536)
                if not chunk:
                    break
                data += chunk
                if b"\r\n\r\n" in data:
                    break
            response = json.loads(data.decode().strip())
            return response
    except Exception as e:
        return {'status': 'ERROR', 'data': str(e)}

def remote_list():
    response = send_command("LIST")
    if response['status'] == 'OK':
        print("Daftar file:")
        for filename in response['data']:
            print(f"- {filename}")
    else:
        print("Gagal:", response['data'])

def remote_get(filename):
    response = send_command(f"GET {filename}")
    if response['status'] == 'OK':
        with open(response['data_namafile'], 'wb') as f:
            f.write(base64.b64decode(response['data_file']))
        # print(f"File '{filename}' berhasil diunduh")
    else:
        print("Gagal:", response['data'])

def remote_upload(filename):
    try:
        with open(filename, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        response = send_command(f"UPLOAD {os.path.basename(filename)} {encoded}")
        if response['status'] == 'OK':
            print(response['data'])
        else:
            print("Gagal upload:", response['data'])
    except FileNotFoundError:
        print("File tidak ditemukan:", filename)

def remote_delete(filename):
    response = send_command(f"DELETE {filename}")
    if response['status'] == 'OK':
        print(response['data'])
    else:
        print("Gagal delete:", response['data'])

def main():
    print("=== FILE CLIENT ===")
    print("Perintah yang tersedia:")
    print("- LIST")
    print("- GET <namafile>")
    print("- UPLOAD <namafile>")
    print("- DELETE <namafile>")
    print("- EXIT")

    while True:
        command = input(">> ").strip()
        if command.upper() == "LIST":
            remote_list()
        elif command.upper().startswith("GET "):
            _, filename = command.split(" ", 1)
            remote_get(filename)
        elif command.upper().startswith("UPLOAD "):
            _, filename = command.split(" ", 1)
            remote_upload(filename)
        elif command.upper().startswith("DELETE "):
            _, filename = command.split(" ", 1)
            remote_delete(filename)
        elif command.upper() == "EXIT":
            print("Keluar.")
            break
        else:
            print("Perintah tidak dikenali.")

if __name__ == '__main__':
    main()
