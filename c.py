import socket
import pickle
import hashlib

sock = socket.socket()

name = input("Server name: ") or 'localhost'
port = int(input("Port number: ") or '9090')

sock.connect((name, port))
data = sock.recv(1024)
print("Message from the server:", pickle.loads(data))

authenticated = False

while not authenticated:
    print("Enter your username:")
    username = input()
    sock.send(pickle.dumps(username))

    response = sock.recv(1024)
    print(pickle.loads(response))

    if "Please enter your password:" in pickle.loads(response):
        print("Enter your password:")
        password = input()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        sock.send(pickle.dumps(hashed_password))

        auth_response = sock.recv(1024)
        print(pickle.loads(auth_response))

        if "Hello" in pickle.loads(auth_response):
            authenticated = True

while True:

    message = input("Enter a message: ")
    sock.send(pickle.dumps(message))
    data = sock.recv(1024)
    print("Message from the server:", pickle.loads(data))

    if data.lower() == "exit":
        break
    if message.lower() == "exit":
        print("Connection is closed")
        break

sock.close()
