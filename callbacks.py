from sqlite3 import connect
import dearpygui.dearpygui as dpg
import socket
import threading
import pickle
from inscription import Encryption

class Callback:
    def __init__(self) -> None:
        self.is_encrypted= True
        self.enc= Encryption()
        self.global_socket=None
        self.global_listener_thread= None

    def listener(self,sock):

        first_flag= False
        while True:
            data_temp = sock.recv(4096)
            
            if (self.is_encrypted and data_temp and first_flag):
                
                data= pickle.loads(data_temp)

                nonce=data.get("nonce")
                ciphertext=data.get("ciphertext")
                #print(ciphertext)
                tag=data.get("tag")

                plaintext=self.enc.decrypt(nonce, ciphertext, tag)

                previous_text = dpg.get_value("history_text")
                msg_text = f"\n> Remote : {plaintext}"
                out=previous_text+ msg_text
                dpg.set_value("history_text", f"{out}")
                #print("Peer A: ", plaintext)

            elif(data_temp and not(self.is_encrypted) and first_flag):
                plaintext= data_temp.decode("utf-8")
                previous_text = dpg.get_value("history_text")
                msg_text = f"\n> Remote : {plaintext}" 
                out=previous_text+ msg_text
                dpg.set_value("history_text", f"{out}")   
                #print("Peer A:", data_temp.decode("utf-8"))
            elif(data_temp and not(first_flag)):
                temp_data= data_temp.decode("utf-8")
                
                temp_data_array= temp_data.split(" ")
    
                
                remote_ipv4, remote_port= temp_data_array[2], temp_data_array[3]
                host_ipv4, host_port=temp_data_array[6], temp_data_array[7]
                
                self.set_host_info(host_ipv4[1:-1],host_port[0:-1])
                self.set_remote_info(remote_ipv4[1:-1],remote_port[0:-1])
            first_flag= True
    def connect_to_server(self,server_ip,server_port):
        s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((server_ip, server_port))
        self.global_socket=s
        listener_thread = threading.Thread(target=self.listener, args=(s,), daemon=True)
        listener_thread.start()
        self.global_listener_thread= listener_thread

    def connect_button_callback(self,sender, app_data, user_data):
        if dpg.get_item_configuration("connect_button")["label"] == "Connect":

            sock= self.connect_to_server("18.195.43.50",36000)
            dpg.configure_item("connect_button", label="Disconnect")

        else:
            #global_listener_thread.join()
            self.global_socket.close()
            dpg.configure_item("connect_button", label="Connect")

        self.set_host_info()
        self.set_remote_info()    

    def send_button_callback(self,sender, app_data, user_data):
        previous_text = dpg.get_value("history_text")
        msg_text = f"\n> Host : {dpg.get_value('message_text')}"
        msg_package = dpg.get_value('message_text')

        if(self.is_encrypted):
            nonce, ciphertext, tag= self.enc.encrypt(msg_package)

            data_temp = {
                    "nonce": nonce,
                    "ciphertext": ciphertext,
                    "tag": tag
                }
            data=pickle.dumps(data_temp)
            self.global_socket.send(data)
        else:
            self.global_socket.send(msg_package.encode("utf-8"))

        out = previous_text + msg_text
        dpg.set_value("history_text", f"{out}")
        dpg.set_value("message_text", "")

    def radio_button_callback(self,sender, app_data, user_data):
        # If radio button value is encrypted
        if dpg.get_value("radio_button") == "Encrypted":
            self.is_encrypted=True

        else:
            self.is_encrypted=False

    def set_host_info(self,ipv4="0.0.0.0", port="00000"):
        dpg.set_value("host_info", f"Host - Ipv4 : {ipv4}\nHost - Ipv4 : {port}")

    def set_remote_info(self,ipv4="0.0.0.0", port="00000"):
        dpg.set_value("remote_info", f"Remote - Ipv4 : {ipv4}\nRemote - Ipv4 : {port}")

    def about_callback(self,sender, app_data, user_data):
        dpg.configure_item("modal_about", show=True)
