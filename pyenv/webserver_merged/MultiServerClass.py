#-*- utf-8 -*-
import socket
import threading
import queue
import json
import re
from time import sleep

#Queue
msg_queue = queue.Queue() #待機している設定
queueLock = threading.Lock()
#Client Stack
clients = []

class ServerClass:
    def __init__(self):
        self.max_size = 1024
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.s_host = 'localhost'
        #self.s_host = '192.168.2.150'
        self.s_port = 6789
        self.server.bind((self.s_host, self.s_port))
        self.server.listen(128)

        print('--Server Start--')
        while True:
            self.con, self.addr = self.server.accept()
            clients.append((self.con, self.addr))
            print('connect:{}'.format(self.addr))
            #接続されたクライアント毎にスレッドを立てる
            handle_thread = threading.Thread(target = self.server_handler, args = (self.con, self.addr), daemon = True)
            handle_thread.start()
    
    def send_clients(self, mode, msg):
        msg = mode + ':' + msg
        print('send msg:{}'.format(msg))
        for c in clients:
            c[0].sendto(msg.encode('utf-8'), c[1])
    
    def recv_msgs(self, con):
        msg = con.recv(self.max_size)
        msg = msg.decode('utf-8')
        return msg

    def server_handler(self, con, addr):
        #clientからデータを受信する
        while True:
            try:
                msg = self.recv_msgs(con)
            except ConnectionResetError:
                #コネクションが切れたとき
                print('ConnectionResetError!')
                print('{}'.format(addr))
                con.close()
                clients.remove((con, addr))
                break

            if not msg:
                pass
            else: #msgを受け取った
                print(msg)
                self.send_clients('0', msg) 

if __name__ == '__main__':
    s_class = ServerClass()