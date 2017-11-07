#-*- utf-8 -*-
import socket
import threading
import queue
import json
import re
win_keep = ''

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
            try:
                self.input_msg(mode)
            finally:
                self.client.close()
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
                print('mode 0: send')
                msg = mode + ':' + msg
                self.client.sendall(msg.encode('utf-8'))
            elif mode == '2':
                print('mode 2: send')
                msg = mode + ':' + msg
                self.client.send(msg.encode('utf-8'))
    
    def recv_msgs(self):
        msg = self.client.recv(self.max_size)
        msg = msg.decode('utf-8')
        return msg

    def raspberry_handler(self, mode): #2
        global win_keep
        while True:
            msg = self.recv_msgs()
            if msg != None:
                if re.match(mode, msg): #先頭が2
                    print('match')
                    #投票の場合
                    if re.search('start', msg):
                        print('--start--')
                        msg = self.recv_msgs() #config check
                        if re.search('ok', msg):
                            #投票を行う設定の受信
                            print(msg)
                            print('wait win_msg and msg')
                            win_keep = self.recv_msgs()
                            msg = self.recv_msgs()
                            print(win_keep)
                            print(msg)
                        print('--end--')
                    else:
                        print('not start')
                else:
                    print('no match')
            else:
                self.client.close()



    def screen_handler(self, mode): #1
        while True:
            msg = self.recv_msgs()
            if msg != None:
                if re.match(mode, msg):
                    print('match')
                else:
                    print('no match')
            else:
                self.client.close()

    def UI_handler(self, mode): #0
        while True:
            #投票結果の受け取り
            msg = self.recv_msgs()
            if msg != None:    
                if re.match(mode, msg):
                    print('match')
                else:
                    print('no match')
            else:
                self.client.close()

if __name__ == '__main__':
    mode = input('mode:') #0, 1, 2
    c_class = ClientClass(mode)