#-*- utf-8 -*-
import socket
import threading
import queue
import json
import re
from time import sleep
import vote_sample

class ClientClass:
    def __init__(self, mode = '0'):
        self.max_size = 1024
        self.s_host = 'localhost'
        #self.s_host = '192.168.2.150'
        self.s_port = 6789
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.s_host, self.s_port))
        #msgの受信を待つスレッド
        if mode == '0': #UI
            self.handler_thread = threading.Thread(target = self.UI_handler, args = (), daemon = True)
            self.handler_thread.start()
        elif mode == '1': #画像
            self.handler_thread = threading.Thread(target = self.screen_handler, args = (), daemon = True)
            self.handler_thread.start()
        elif mode == '2': #RaspberryPi
            self.handler_thread = threading.Thread(target = self.raspberry_handler, args = (), daemon = True)
            self.handler_thread.start()
        else:
            print('no mode')
            self.client.close()
    
    def UI_handler(self): #0
        print('UI mode')
        while True:
            msg = self.recv_msgs()
            print(msg)
            if msg != None:
                print(':'.format(msg))
            else:
                self.client.close()
            
            if msg != None:
                print(msg)
                if re.match('0:', msg):
                    msg = msg.rstrip('0:')
                    print(msg)

    
    def screen_handler(self): #1
        print('screen mode')
        while True:
            msg = self.recv_msgs()
            if msg != None:
                print(msg)
                if re.match('1:', msg):
                    msg = msg.lstrip('1:')
                    print(msg)
    
    def raspberry_handler(self): #2
        print('raspberry mode')
        while True:
            msg = self.recv_msgs()
            if msg != None:
                print(msg)
                if re.match('2:', msg):
                    msg = msg.lstrip('2:')
                    print(msg)
                    if re.search('vote', msg):
                        result = vote_sample.Vote()
                        print(result)
                        self.client.sendall(result.encode('utf-8'))
                    
    def input_msg(self, mode):
        #メッセージの入力とサーバへの送信
        while True:
            msg = input()
            if msg == 'exit':
                self.client.close()
                print('close')
                break
            elif mode == '0':
                print('mode 0: send')
                msg = mode + ':' + msg
                self.client.sendall(msg.encode('utf-8'))
            elif mode == '1':
                msg = mode + ':' + msg
                self.client.sendall(msg.encode('utf-8'))
            elif mode == '2':
                print('mode 2: send')
                msg = mode + ':' + msg
                self.client.sendall(msg.encode('utf-8'))
    
    #msg受け取り
    def recv_msgs(self):
        msg = self.client.recv(self.max_size)
        msg = msg.decode('utf-8')
        return msg

if __name__ == '__main__':
    mode = input('mode:') #0, 1, 2
    c_class = ClientClass(mode)