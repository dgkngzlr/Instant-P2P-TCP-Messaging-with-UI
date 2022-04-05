from encodings import utf_8
import socket
import threading
from xmlrpc.client import boolean
from inscription import Encryption
import pickle

SERVER_IP = "18.195.43.50"
SERVER_PORT = 36700


def transfer_file():
    file_name=input("Please provide the file name: ")
    with open(file_name,mode='rb') as f:
        data=pickle.dumps(f)
        s.send(data)
        
def listener(sock):
    count= False
    while True:
        
        data_temp = sock.recv(1024)
        
        if (encryption_flag and data_temp and count):
            
            data= pickle.loads(data_temp)

            nonce=data.get("nonce")
            ciphertext=data.get("ciphertext")
            print(ciphertext)
            tag=data.get("tag")

            plaintext=enc.decrypt(nonce, ciphertext, tag)

            print("Peer B: ", plaintext)

        elif(data_temp and not(encryption_flag)):
             print("Peer B:", data_temp.decode("utf-8"))

        count= True
        

enc= Encryption() # Object Decl.

connection_flag = input("Set the Connection Flag 1 to continue>")
if(int (connection_flag)== 1):
    connection_flag=True
else:
    connection_flag= False

encryption_flag = input("Set the Encryption Flag Flag 1 to start encyrpted connection>")
if(int (encryption_flag)== 1):
    encryption_flag=True
else:
    encryption_flag= False

while True:
    if (connection_flag):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((SERVER_IP, SERVER_PORT))

            listener_thread = threading.Thread(target=listener, args=(s,), daemon=True)
            listener_thread.start()
            
            while connection_flag:
                msg = input(">")
                if(msg=="connection_flag"):
                    connection_flag=False
                if msg:
                    if msg == "exit":
                        s.close()
                        break

                    elif msg=="transfer":
                        transfer_file()
        
                    if(encryption_flag):
                        nonce, ciphertext, tag= enc.encrypt(msg)

                        data_temp = {
                                "nonce": nonce,
                                "ciphertext": ciphertext,
                                "tag": tag
                            }
                        data=pickle.dumps(data_temp)
                        s.send(data)
                    else:
                        s.send(msg.encode("utf-8"))

            if(not connection_flag):
                print("Disconnecting")
                listener_thread.join()
                s.close()
    else:
        connection_flag = bool(input("Set the Connection Flag True to continue>"))
        print("Waiting For User Input")