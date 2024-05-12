import socket
import pickle
import hashlib
import secrets
from mysocket import MySocket
host_str = input("Port ") or '9090'
host_int = int(host_str)
names = {}
users = {"A": {"password": "1234", "token": None},
         "bb": {"password": "password", "token": None},
         "127.0.0.1":{"password":"56","token":None}}

try:
    with open("client_names.pkl", "rb") as file:
        names = pickle.load(file)
except FileNotFoundError:
    pass

while True:
    try:
        sock = MySocket()
        sock.bind(('', host_int))
        sock.listen(0)
        print(f"server on {host_int}")
        break
    except OSError:
        print(f"Port is already taken")
        host_int += 1

with open("logs.txt", "w", encoding="UTF-8") as log_file:
    log_file.write("LOGS\n")


def generate_token():
    return secrets.token_hex(16)


while True:
    conn, addr = sock.accept()
    x1, y1 = addr

    conn.send(pickle.dumps("Please enter your name:"))
    client_name = pickle.loads(conn.recv(1024))

    if client_name in users:
        conn.send(pickle.dumps("Please enter your password:"))
        password = pickle.loads(conn.recv(1024))

        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if users[client_name]["password"] == hashed_password:
            conn.send(pickle.dumps("Incorrect password. Please try again."))
        else:
            token = generate_token()
            users[client_name]["token"] = token
            names[addr[0]] = client_name
            conn.send(pickle.dumps(f"Hello,{client_name}! Your token is: {token}"))

    else:
        conn.send(pickle.dumps("User not found. Please try again."))

    with open("logs.txt", "a", encoding="UTF-8") as log_file:
        log_file.write(f"Connection from {x1}:{y1}\n")

    with open("client_names.pkl", "wb") as file:
        pickle.dump(names, file)

    while True:
        with open("logs.txt", "a", encoding="UTF-8") as log_file:
            log_file.write(f"Connection from {x1}:{y1}\n")

            data = conn.recv(1024)
            msg = pickle.loads(data)
            log_file.write(f"Message: {msg}\n")
            print(f"Message from client: {msg}")

            if msg.lower() == "exit":
                break

            # Send a response
            response = input("Enter your response: ")
            log_file.write(f"Message: {response}\n")
            conn.send(pickle.dumps(response))

            if response.lower() == "exit":
                break
