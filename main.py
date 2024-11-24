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
                client_sock = self.accept(sock)
                file_path = self.get_file_path(client_sock)
                self.handle_upload(client_sock, file_path)
            except socket.error as e:
                logging.error("[start] Socket error: %s", e)
                raise

    def terminate_connection(self, client_sock):
        if client_sock:
            client_sock.close()
        logging.critical("[terminate] Connection terminated")

    def accept(self, sock):
        client_sock, client_addr = sock.accept()
        logging.info("[accept] %s successfully connected to the server.", client_addr)
        return client_sock

    def handle_upload(self, client_sock, path):
        try:
            with open(path, 'rb') as file:
                file_chunk = file.read(self.BUFFER)
                while file_chunk:
                    client_sock.send(file_chunk)
                    file_chunk = file.read(self.BUFFER)
            logging.info("[handle_upload] finished file upload.")
        except IOError as e:
            logging.error("[handle_upload] Failed to read file: %s", e)
            raise

    def get_file_path(self, client_sock):
        time.sleep(.1)
        file_path = input("[input] Please enter the file path: ")
        if not os.path.isfile(file_path):
            logging.error("[get_file_path] No such file path found - terminating connection.")
            self.terminate_connection(client_sock)
        else:
            client_sock.send(os.path.basename(file_path).encode())
            return file_path


if __name__ == "__main__":
    server = Server()
    server.start()
