import os.path
import socket


class Client:
    def __init__(self):
        self.SERVER_IP = '192.168.115.200'
        self.PORT = 6545
        self.BUFFER = 1024
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        print(f"[connect] trying to connect to {self.SERVER_IP}...")
        try:
            self.socket.connect((self.SERVER_IP, self.PORT))
            print(f"[connect] successfully connected to {self.SERVER_IP} on port {self.PORT}.")
        except Exception as err:
            print(err)
            exit(-1)

    def listen(self):
        print(f"[listen] waiting for data from {self.SERVER_IP}...")
        data = self.socket.recv(self.BUFFER)
        print(f"Data: {data.decode()} received.")


if __name__ == "__main__":
    client = Client()
    client.connect()
    client.listen()

