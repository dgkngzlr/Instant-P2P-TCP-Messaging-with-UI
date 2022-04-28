import socket
import threading

SERVER_IP = "127.0.0.1"
SERVER_PORT = 36000

def listener(sock):
    while True:

        data = sock.recv(1024)

        if data:
            print("Peer B:", data.decode("utf-8"))


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((SERVER_IP, SERVER_PORT))

    listener_thread = threading.Thread(target=listener, args=(s,), daemon=True)
    listener_thread.start()

    while True:
        msg = input(">")

        if msg:
            if msg == "exit":
                s.close()
                break
            s.send(msg.encode())
