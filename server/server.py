import socket
import threading
from datetime import datetime

from util import *

# Messages
peer_a_msg: str = "idle"
peer_b_msg: str = "idle"

# Time stamps of messages
peer_a_msg_ts: str = ""
peer_b_msg_ts: str = ""

is_encrypted = True

def get_time_stamp():
    n = datetime.now()
    return f"{n.day}:{n.month}:{n.year}:{n.hour}:{n.minute}:{n.minute}:{n.second}"


# Peer A listener, sock = conn_a
def pa_receiver(sock):
    global peer_a_msg, peer_a_msg_ts, is_encrypted

    while True:

        try:
            data = sock.recv(4096)
            if data and sock.fileno() != -1:
                
                 # If received data is string
                try:
                    peer_a_msg = data.decode("utf-8")
                    peer_a_msg_ts = get_time_stamp()
                    is_encrypted = False

                # If received data is byte object
                except:
                    peer_a_msg = data
                    peer_a_msg_ts = get_time_stamp()
                    is_encrypted = True

        except Exception as e:
            peer_a_msg = "idle"
            peer_a_msg_ts = ""
            sock.close()
            break


# Peer B listener, sock = conn_b
def pb_receiver(sock):
    global peer_b_msg, peer_b_msg_ts, is_encrypted

    while True:

        try:
            data = sock.recv(4096)
            if data and sock.fileno() != -1:

                # If received data is string
                try:
                    peer_b_msg = data.decode("utf-8")
                    peer_b_msg_ts = get_time_stamp()
                    is_encrypted = False
                # If received data is byte object
                except:
                   peer_b_msg = data 
                   peer_b_msg_ts = get_time_stamp()
                   is_encrypted = True

        except Exception as e:

            peer_b_msg = "idle"
            peer_b_msg_ts = ""
            sock.close()
            break


# Communication handler thread, sends messages to each peer
def com_handler(peer_a_, peer_b_):
    conn_a, addr_a = peer_a_
    conn_b, addr_b = peer_b_

    # Send their addresses to each peer
    conn_b.send(f"Remote : {addr_a} Your : {addr_b}".encode())
    conn_a.send(f"Remote : {addr_b} Your : {addr_a}".encode())

    pa_recv_thread = threading.Thread(target=pa_receiver, args=(conn_a,), daemon=True)
    pb_recv_thread = threading.Thread(target=pb_receiver, args=(conn_b,), daemon=True)
    pa_recv_thread.start()
    pb_recv_thread.start()

    prev_a_ts = ""
    prev_b_ts = ""
    while True:

        # If time stamp is updated
        if peer_b_msg != "idle" and prev_b_ts != peer_b_msg_ts and conn_a.fileno() != -1:
            try:
                print(peer_b_msg)

                if is_encrypted:
                    conn_a.send(peer_b_msg)
                
                else:
                    conn_a.send(peer_b_msg.encode())

                prev_b_ts = peer_b_msg_ts

            except Exception as e:
                print(e)
                prev_b_ts = ""
                break

        if peer_a_msg != "idle" and prev_a_ts != peer_a_msg_ts and conn_b.fileno() != -1:
            try:
                print(peer_a_msg)

                if is_encrypted:
                    conn_b.send(peer_a_msg)
                    
                else:
                    conn_b.send(peer_a_msg.encode())
                
                prev_a_ts = peer_a_msg_ts

            except Exception as e:
                print(e)
                prev_a_ts = ""
                break

        # To resolve overworking
        if conn_a.fileno() == -1 or conn_b.fileno() == -1:
            conn_a.close()
            conn_b.close()
            break


if __name__ == "__main__":
    # Store the addresses temporarily
    stack = Stack()

    # The main connection of the server
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(options.server_addr)

        print("[INFO] Server status : OK ")

        # Endless loop
        while True:
            print("[INFO] Server is listening... ")
            s.listen()

            # Accept next connection
            connect, addr = s.accept()

            if connect is not None:
                print(f"Connected by {addr}")
                stack.push((connect, addr))

            # If 2 nodes are currently connected
            if stack.size() == 2:
                # Second connection
                peer_b = stack.pop()

                # First connection
                peer_a = stack.pop()

                # Start a new thread for each pair
                handler_thread = threading.Thread(target=com_handler, args=(peer_a, peer_b,), daemon=True)
                handler_thread.start()
