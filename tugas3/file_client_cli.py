import socket
import json
import base64
import logging

server_address = ('172.16.16.101', 11111)  # Ganti IP jika server beda

def send_command(command_str=""):
    global server_address
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(server_address)
    try:
        sock.sendall(command_str.encode())
        data_received = ""
        while True:
            data = sock.recv(16)
            if data:
                data_received += data.decode()
                if "\r\n\r\n" in data_received:
                    break
            else:
                break
        hasil = json.loads(data_received)
        return hasil
    except Exception as e:
        print("ERROR:", str(e))
        return {'status': 'ERROR', 'data': str(e)}

def remote_list():
    hasil = send_command("LIST")
    if hasil['status'] == 'OK':
        print("Daftar file:")
        for f in hasil['data']:
            print(f"- {f}")
    else:
        print("Gagal:", hasil['data'])

def remote_get(filename):
    hasil = send_command(f"GET {filename}")
    if hasil['status'] == 'OK':
        with open(hasil['data_namafile'], 'wb') as f:
            f.write(base64.b64decode(hasil['data_file']))
        print(f"File '{filename}' berhasil diunduh")
    else:
        print("Gagal:", hasil['data'])

def remote_upload(filename):
    try:
        with open(filename, 'rb') as f:
            encoded = base64.b64encode(f.read()).decode()
        hasil = send_command(f"UPLOAD {filename} {encoded}")
        if hasil['status'] == 'OK':
            print(hasil['data'])
        else:
            print("Gagal upload:", hasil['data'])
    except FileNotFoundError:
        print("File tidak ditemukan:", filename)

def remote_delete(filename):
    hasil = send_command(f"DELETE {filename}")
    if hasil['status'] == 'OK':
        print(hasil['data'])
    else:
        print("Gagal delete:", hasil['data'])

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
