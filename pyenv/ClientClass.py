#-*- utf-8 -*-
import socket
import threading
import queue
import json

win_keep = queue.Queue() #勝ち残った設定

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
            msg = msg.decode('utf-8')
            if msg == 'start': #投票スタートを受け取った場合
                print('msg:{}'.format(msg))
                #設定を待つ
                win_msg = self.client.recv(self.max_size)
                msg = self.client.recv(self.max_size)
                win_msg.decode('utf-8')
                msg.decode('utf-8')
                print('win_msg:{}'.format(win_msg))
                print('msg:{}'.format(msg))
                win_keep.put(win_msg)
                '''
                #投票処理

                #投票結果を返す
                if win_msg < msg: #もし新しい設定になるなら
                    win_msg = msg
                self.client.senall(msg.encode('utf-8'))
                #勝ち残った設定を受け取る
                msg = self.client.recv(self.max_size)
                msg = msg.decode('utf-8')
                if win_keep.empty() != True:
                    win_keep.get()
                win_keep.put(msg)
                '''
            elif msg != None:
                print('msg:{}'.format(msg))
            else:
                self.client.close()

if __name__ == '__main__':
    c_class = ClientClass()