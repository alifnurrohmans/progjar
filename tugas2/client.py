import socket
import logging

logging.basicConfig(level=logging.INFO)

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = ('172.16.16.101', 45000)
    logging.info(f"Connecting to {server_address}")
    sock.connect(server_address)

    while True:
        user_input = input("Ketik 'TIME\\r\\n' untuk waktu, 'QUIT\\r\\n' untuk keluar: ").strip().upper()

        if user_input == "QUIT\\R\\N":
            sock.sendall("QUIT\r\n".encode('utf-8'))
            break

        elif user_input == "TIME\\R\\N":
            sock.sendall("TIME\r\n".encode('utf-8'))
            response = sock.recv(1024)
            logging.info(f"{response.decode('utf-8').strip()}")

        else:
            logging.warning("Perintah Salah, Inputkan Sesuai Instruksi")

except Exception as e:
    logging.error(f"ERROR: {e}")

finally:
    logging.info("Closing connection")
    sock.close()
