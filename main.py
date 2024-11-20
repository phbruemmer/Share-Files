import os.path
import socket
import time


class Server:
    def __init__(self):
        self.HOSTNAME = socket.gethostname()
        self.HOST = socket.gethostbyname(self.HOSTNAME)
        self.PORT = 6545
        self.BUFFER = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_sock = None
        self.client_addr = None

    def start(self):
        try:
            self.socket.bind((self.HOST, self.PORT))
            print("[start] starting...")
        except Exception as err:
            print(err)
            exit(-1)
        print("[start] listening for connections...")
        self.socket.listen(1)

    def terminate_connection(self):
        if self.client_sock:
            self.client_sock.close()
        self.socket.close()
        print("[terminate] Connection terminated")
        exit(-1)

    def accept(self):
        self.client_sock, self.client_addr = self.socket.accept()
        print(f"[accept] {self.client_addr} successfully connected to the server.")

    def handle_upload(self):
        file_path = input("[input] Please enter the file path: ")
        if not os.path.isfile(file_path):
            print("[handle_upload] No such file path found - terminating connection.")
            print("[handle_upload] stop imagining things you don't have!")
            self.terminate_connection()
        self.client_sock.send(file_path.split('\\')[-1].encode())
        with open(file_path, 'rb') as file:
            file_chunk = file.read(self.BUFFER)
            while file_chunk:
                self.client_sock.send(file_chunk)
                # print(f"[handle_upload] sending file data...\n{file_chunk.decode()}")
                file_chunk = file.read(self.BUFFER)
                time.sleep(.1)
        self.client_sock.send(b'$$$')


if __name__ == "__main__":
    server = Server()
    server.start()
    server.accept()
    server.handle_upload()
