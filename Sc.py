import socket
import threading

UDP_MAX_SIZE = 65535


def listen(s):
    while True:
        msg = s.recv(UDP_MAX_SIZE)
        print('\r\r' + msg.decode('ascii') + '\n' + f'you: ', end='')


def connect(host='127.0.0.1', port=3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.connect((host, port))

    threading.Thread(target=listen, args=(s,), daemon=True).start()

    s.send('__join'.encode('ascii'))

    while True:
        msg = input(f'you: ')
        s.send(msg.encode('ascii'))


connect()
