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
    #Webアプリケーション用クライアント
    def app_start(self):
        print('--Web Application Client Start--')
        while True:
            try:
                msg = self.client.recv(self.max_size)
                msg = msg.decode('utf-8')
            except OSError:
                break
            

                

        self.client.close()
    #Raspberry Pi用クライアント
    def rasp_start(self):
        win = ''
        print('--Raspberry Pi Client Start--')
        while True:
            try:
                msg = self.client.recv(self.max_size)
                msg = msg.decode('utf-8')
            except OSError:
                break
            
            #1回目は2つ受け取る
            if win == '':
                winn = self.client.recv(self.max_size)
                winn = win.decode('utf-8')
            #Winとmsgの設定で投票を行う
            #差分の大きい方が勝ち

            #どちらが勝ったかを返す
            if win < msg:
                win = msg
            msg = win.encode('utf-8')
            self.client.sendall(msg)
            
            #全ての水槽での結果を受け取る
            win = self.client.recv(self.max_size)
            win = win.decode('utf-8')
        self.client.close()

if __name__ == '__main__':
    c_class = ClientClass()
    comand = input('Rasb or App')
    if comand == 'Rasb':
        c_class.app_start()
    elif comand == 'App'
        c_class.app_start()