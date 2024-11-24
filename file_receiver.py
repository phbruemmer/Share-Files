import os.path
import socket
import logging


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


class Client:
    DEFAULT_SERVER_IP = '192.168.115.200'
    DEFAULT_PORT = 6545
    DEFAULT_BUFFER = 8192

    DEFAULT_PATH = f"C:\\tmp\\"

    END_OF_FILE_MARKER = b'$$$'

    def __init__(self, server_ip=None, port=None, buffer=None, path=None):
        self.SERVER_IP = server_ip or self.DEFAULT_SERVER_IP
        self.PORT = port or self.DEFAULT_PORT
        self.BUFFER = buffer or self.DEFAULT_BUFFER
        self.PATH = path or self.DEFAULT_PATH

    def connect(self):
        logging.info("[connect] Connecting to %s on port %d...", self.SERVER_IP, self.PORT)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(10)
            try:
                sock.connect((self.SERVER_IP, self.PORT))
                logging.info("[connect] Successfully connected.")
                filename = self.receive_data(sock)
                self.receive_file(sock, filename)
            except socket.timeout:
                logging.error("[connect] Connection timed out.")
            except socket.error as e:
                logging.error("[connect] Socket error: %s", e)
                raise
            except Exception as e:
                logging.error("[connect] Unexpected error: %s", e)
                raise

    def receive_data(self, sock):
        logging.info("[receive_data] waiting for data from %s ...", self.SERVER_IP)
        data = sock.recv(self.BUFFER)

        logging.info("[receive_data] raw data received: %s", data.decode())

        if not data:
            logging.error("[receive_data] No data received from server.")
            raise ValueError("No data received.")

        filename = data.decode().strip()
        logging.info("[receive_data] received data: %s", filename)

        sanitized_filename = os.path.basename(filename)
        return sanitized_filename

    def receive_file(self, sock, filename):
        full_path = os.path.join(self.PATH, filename)
        logging.info("[receive_file] Saving file to %s ...", full_path)

        try:
            self.check_directory()

            with open(full_path, 'wb') as file:
                while True:
                    data = sock.recv(self.BUFFER)
                    if data.find(self.END_OF_FILE_MARKER):
                        logging.info("[receive_file] End of file marker received.")
                        break
                    file.write(data)
            logging.info("[receive_file] File saved successfully.")
        except IOError as e:
            logging.error("[receive_file] Failed to write file: %s", e)
            raise

    def check_directory(self):
        if not os.path.exists(self.PATH):
            logging.info("[check_directory] Directory does not exist. Creating: %s", self.PATH)
            os.makedirs(self.PATH, exist_ok=True)
        else:
            logging.info("[check_directory] Directory already exists: %s", self.PATH)


if __name__ == "__main__":
    client = Client()
    client.connect()

