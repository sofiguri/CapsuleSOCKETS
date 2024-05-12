import socket

class MySocket(socket.socket):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def send_message(self, message):
        msg_bytes = message.encode()
        msg_length = len(msg_bytes).to_bytes(4, byteorder='big')  # Фиксированная длина заголовка (4 байта)
        self.sendall(msg_length + msg_bytes)

    def receive_message(self):
        msg_length = int.from_bytes(self.recv(4), byteorder='big')
        msg = b''
        while len(msg) < msg_length:
            chunk = self.recv(min(msg_length - len(msg), 1024))
            if not chunk:
                raise ConnectionError("Connection closed while reading message")
            msg += chunk
        return msg.decode()

