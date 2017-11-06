import socket
import json
from datetime import datetime
from time import sleep

class ClientClass:
    def __init__(self):
        self.max_size = 1024
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s_host = 'localhost'
        self.s_port = 6789
        self.addr = (self.s_host, self.s_port)
        self.client.connect(self.addr)

    #ここにServerとのやりとりを書いていく
    def c_start(self):
        print('--Client Start--')
        while True:
            msg = '''{ "test" : "json" }'''
            msg = msg.encode('utf-8')
            self.client.sendall(msg)
            msg = self.client.recv(self.max_size)
            print(msg)
            break
        
        self.client.close()


if __name__ == '__main__':
    c_class = ClientClass()
    c_class.c_start()