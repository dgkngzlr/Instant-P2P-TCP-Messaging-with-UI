class options:

    local = False

    server_ip : str
    if local:
        server_ip = "127.0.0.1"
    else:
        server_ip = "0.0.0.0"

    server_port = 36000
    server_addr = (server_ip, server_port)

class Stack:

    def __init__(self):

        self.stack = []

    def push(self, e):
        self.stack.append(e)

    def pop(self):
        return self.stack.pop()

    def peek(self):
        return self.stack[-1]

    def size(self):
        return len(self.stack)

    def __repr__(self):
        return str(self.stack)