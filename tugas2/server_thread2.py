from socket import *
import socket
import threading
import logging
from datetime import datetime

class ProcessTheClient(threading.Thread):
    def __init__(self, connection, address):
        self.connection = connection
        self.address = address
        threading.Thread.__init__(self)

    def run(self):
        while True:
            try:
                data = self.connection.recv(1024).decode('utf-8')
                if not data:
                    break

                data = data.strip()

                if data == "TIME":
                    now = datetime.now()
                    jam = now.strftime("%H:%M:%S")
                    response = f"JAM {jam}\r\n"
                    self.connection.sendall(response.encode('utf-8'))

                elif data == "QUIT":
                    break

                else:
                    self.connection.sendall("Perintah tidak dikenali\r\n".encode('utf-8'))

            except Exception as e:
                logging.warning(f"Error handling client {self.address}: {e}")
                break

        logging.warning(f"Koneksi ditutup dari {self.address}")
        self.connection.close()

class Server(threading.Thread):
    def __init__(self):
        self.the_clients = []
        self.my_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        threading.Thread.__init__(self)

    def run(self):
        self.my_socket.bind(('0.0.0.0', 45000))  # Ganti port ke 45000
        self.my_socket.listen(5)
        logging.warning("Server berjalan di port 45000...")

        while True:
            self.connection, self.client_address = self.my_socket.accept()
            logging.warning(f"Connection from {self.client_address}")

            clt = ProcessTheClient(self.connection, self.client_address)
            clt.start()
            self.the_clients.append(clt)

def main():
    svr = Server()
    svr.start()

if __name__ == "__main__":
    main()
