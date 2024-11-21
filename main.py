import os.path
import socket
import time
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Server:
    DEFAULT_PORT = 6545
    DEFAULT_BUFFER = 8192

    def __init__(self, port=None, buffer=None):
        self.HOSTNAME = socket.gethostname()
        self.HOST = socket.gethostbyname(self.HOSTNAME)
        self.PORT = port or self.DEFAULT_PORT
        self.BUFFER = buffer or self.DEFAULT_BUFFER

    def start(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                sock.bind((self.HOST, self.PORT))
                logging.info("[start] starting...")
                logging.info("[start] listening for connections...")
                sock.listen(1)
                self.accept(sock)
                file_path = self.get_file_path(sock)
                self.handle_upload(sock, file_path)
            except socket.error as e:
                logging.error("[start] Socket error: %s", e)
                raise

    def terminate_connection(self, sock):
        if sock:
            sock.close()
        logging.critical("[terminate] Connection terminated")

    def accept(self, sock):
        client_sock, client_addr = sock.accept()
        logging.info("[accept] %s successfully connected to the server.", client_addr)

    def handle_upload(self, sock, path):
        try:
            with open(path, 'rb') as file:
                file_chunk = file.read(self.BUFFER)
                while file_chunk:
                    sock.send(file_chunk)
                    file_chunk = file.read(self.BUFFER)
            sock.send(b'$$$')
        except IOError as e:
            logging.error("[handle_upload] Failed to read file: %s", e)

    def get_file_path(self, sock):
        time.sleep(.1)
        file_path = input("[input] Please enter the file path: ")
        if not os.path.isfile(file_path):
            logging.error("[get_file_path] No such file path found - terminating connection.")
            self.terminate_connection(sock)
        else:
            sock.send(os.path.basename(file_path).encode())
            return file_path


if __name__ == "__main__":
    server = Server()
    server.start()
