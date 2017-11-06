#-*- utf-8 -*-
import socket
import threading
import queue
import json

#test json
test = ''' {
    "test" : "json" 
} '''
 #Queue
msg_queue = queue.Queue()
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

    #ここでClientとのやりとりを書いていく
    def c_handler(self, client, c_addr, c_port):
        while True:
            try:
                msg = client.recv(self.max_size).decode('utf-8')
            except OSError:
                break
                
                print(msg)
                       
        client.close()
    
    def input_msg(self):
        while True:
            msg = input('command wait:')
            #全てのクライアントに向けて発信
            for c in clients:
                c[0].sendall(msg.encode('utf-8'), c[1])

    def s_start(self):
        print('--Server Start--')
        while True:
            client, (c_addr, c_port) = self.server.accept()
            clients.append((client, c_addr))
            print('New Client: {0} : {1}'.format(c_addr, c_port))
            #接続してきたクライアントを処理するスレッドを用意する
            c_thread = threading.Thread(target = s_class.c_handler,
                args = (client, c_addr, c_port))
            
            #標準入力(コマンド)待ち
            self.input_msg()
            #親スレッドが死んだら子も道連れにする
            c_thread.daemon = True
            #スレッドを起動する
            c_thread.start()
            
            
if __name__ == '__main__':
    s_class = ServerClass()
    s_class.s_start()