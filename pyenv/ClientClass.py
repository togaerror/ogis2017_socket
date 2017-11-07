#-*- utf-8 -*-
import socket
import json
import threading
from datetime import datetime
from time import sleep

class ClientClass:
    def __init__(self):
        self.max_size = 1024
        self.s_host = 'localhost'
        self.s_port = 6789
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.s_host, self.s_port))
        #msgの受信を待つスレッド
        self.handler_thread = threading.Thread(target = self.client_handler, args = (), daemon = True)
        self.handler_thread.start()
        try:
            self.input_msg()
        finally:
            self.client.close()

    def input_msg(self):
        #メッセージの入力とサーバへの送信
        while True:
            msg = input()
            if msg == 'exit':
                self.client.close()
                print('close')
                break
            else:
                self.client.send(msg.encode('utf-8'))

    def client_handler(self):
        while True:
            msg = self.client.recv(self.max_size)
            if msg != None:
                print('msg:{}'.format(msg.decode('utf-8')))
            else:
                self.client.close()

if __name__ == '__main__':
    c_class = ClientClass()