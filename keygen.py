import random

key = ""

for i in range(32):
    key += hex(random.randint(0,15))[2:]

with open("./isa256_pseudo.key", "wb") as f:
    f.write(key.encode())

print("Key is generated !")