import socket

UDP_MAX_SIZE = 65535


def listen(host: str = '127.0.0.1', port: int = 3000):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    s.bind((host, port))
    print(f'Listening at {host}:{port}')

    members = []
    while True:
        msg, addr = s.recvfrom(UDP_MAX_SIZE)

        if addr not in members:
            members.append(addr)

        if not msg:
            continue

        client_id = addr[1]
        if msg.decode('ascii') == '__join':
            print(f'Client {client_id} joined chat')
            with open("history.txt", "a", encoding="UTF-8") as history_file:
                history_file.write(f'Client {client_id} joined chat\n')

            continue

        msg = f'client{client_id}: {msg.decode("ascii")}'
        with open("history.txt", "a", encoding="UTF-8") as history_file:
            history_file.write(msg+"\n")
        for member in members:
            if member == addr:
                continue

            s.sendto(msg.encode('ascii'), member)


listen()
