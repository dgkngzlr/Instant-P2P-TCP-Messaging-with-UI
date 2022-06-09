from Crypto.Cipher import AES
from secrets import token_bytes

class Encryption:
    def __init__(self):
        with open ("isa256_pseudo.key", "rb") as f:
            self.key=f.read()

        
    def encrypt(self,message):
        cipher = AES.new(self.key, AES.MODE_EAX)
        
        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(message.encode('utf-8"'))
        return nonce, ciphertext, tag

    def decrypt(self,nonce, ciphertext, tag):
        cipher = AES.new(self.key, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher.decrypt(ciphertext)
        try:
            cipher.verify(tag)
            return plaintext.decode('utf-8"')
        except:
            return False
    