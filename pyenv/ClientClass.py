#-*- utf-8 -*-
import socket
import threading
import queue
import json
import re

win_keep = queue.Queue() #勝ち残った設定

class ClientClass:
    def __init__(self, mode):
        self.max_size = 1024
        self.s_host = 'localhost'
        self.s_port = 6789
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.s_host, self.s_port))
        #msgの受信を待つスレッド
        if mode == '0': #UI
            print('UI mode')
            self.handler_thread = threading.Thread(target = self.UI_handler, args = (mode), daemon = True)
            self.handler_thread.start()
            try:
                #設定の追加
                self.input_msg(mode)
            finally:
                self.client.close()

        elif mode == '1': #画像
            print('screen mode')
            self.handler_thread = threading.Thread(target = self.screen_handler, args = (mode), daemon = True)
            self.handler_thread.start()

        elif mode == '2': #RaspberryPi
            print('RaspberryPi mode')
            self.handler_thread = threading.Thread(target = self.raspberry_handler, args = (mode), daemon = True)
            self.handler_thread.start()
            try:
                #設定の追加
                self.input_msg(mode)
            finally:
                self.client.close()
        else:
            print('no mode')
            self.client.close()

    def input_msg(self, mode):
        #メッセージの入力とサーバへの送信
        while True:
            msg = input()
            if msg == 'exit':
                self.client.close()
                print('close')
                break
            elif mode == '0':
                self.client.send(mode.encode('utf-8')) 
                self.client.send(msg.encode('utf-8'))
            elif mode == '2':
                self.client.send(mdoe.encode('utf-8'))
                self.client.send(msg.encode('utf-8'))

    def Raspberry_handler(self, mode):
        while True:
            msg_mode = self.client.recv(self.max_size)
            msg_mode = mdoe.decode('utf-8') 
            msg = self.client.recv(self.max_size)
            msg = msg.decode('utf-8')
            if msg_mode == mode:
                print('msg:{}:'.formta(msg))

    def screen_handler(self, mode):
        while True:
            msg_mode = self.client.recv(self.max_size)
            msg_mode = mdoe.decode('utf-8') 
            msg = self.client.recv(self.max_size)
            msg = msg.decode('utf-8')
            if msg_mode == mode:
                print('msg:{}'.format(msg))
                


    def UI_handler(self):
        while True:
            #投票結果の受け取り
            msg_mode = self.client.recv(self.max_size)
            msg_mode = msg.decode('utf-8') 
            msg = self.client.recv(self.max_size)
            msg = msg.decode('utf-8')
            if mode == msg_mode:
                print('msg:{}'.format(msg))                 
                

if __name__ == '__main__':
    mode = input('mode:') #0, 1, 2
    c_class = ClientClass(mode)