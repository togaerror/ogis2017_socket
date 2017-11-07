#-*- utf-8 -*-
import socket
import threading
import queue
import json
import re

#test json
test = ''' {
    "test" : "json" 
} '''
 #Queue
msg_queue = queue.Queue() #待機している設定
win_keep = queue.Queue() #勝ち残り設定
queueLock = threading.Lock()

#Client Stack
clients = []

class ServerClass:
    def __init__(self):
        self.max_size = 1024
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        self.s_host = 'localhost'
        self.s_port = 6789
        self.server.bind((self.s_host, self.s_port))
        self.server.listen(128)

        print('--Server Start--')
        while True:
            self.con, self.addr = self.server.accept()
            print('connect:{}'.format(self.addr))
            clients.append((self.con, self.addr))
            #接続されたクライアント毎にスレッドを立てる
            handle_thread = threading.Thread(target = self.server_handler, args = (self.con, self.addr), daemon = True)
            handle_thread.start()
    
    def server_handler(self, con, addr):
        #clientからデータを受信する
        while True:
            try:
                mode = con.recv(self.max_size)
                mode = mode.decode('utf-8')
                msg = con.recv(self.max_size)
                msg = msg.decode('utf-8')
                print('from:{}'.format(con))
                print('{0} {1}'.format(mode, msg))
            except ConnectionResetError:
                #コネクションが切れたとき
                print('ConnectionResetError!')
                print('{}'.format(addr))
                con.close()
                clients.remove(con, addr)
                break

            if not msg:
                pass
            else:
                if mode == '0': #msgが設定だったらスタック 
                    queueLock.acquire()
                    msg_queue.put(msg)
                    queueLock.release()
                    mode = '0'
                    for c in clients:
                        c[0].sendto(mode.encode('utf-8'), c[1])
                        c[0].sendto(msg.encode('utf-8'), c[1])
                    
            

               
            
if __name__ == '__main__':
    s_class = ServerClass()