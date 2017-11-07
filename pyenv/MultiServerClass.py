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
                msg = con.recv(self.max_size)
                msg = msg.decode('utf-8')
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
                if msg == 'start':
                    print('msg:{}'.format(msg))
                    #投票開始
                    #全clientに設定を送る
                    win_msg = 'empty'
                    queueLock.acquire()
                    if win_keep.empty() != True:
                        if msg_queue.empty() != True:
                            msg = msg_queue.get()
                        else:
                            msg = 'Message empty!'
                    else:
                        if msg_queue.qsize() < 2:
                            msg = '設定数が足りません'
                        else:
                            win_msg = msg_queue.get()
                            msg = msg_queue.get()
                    queueLock.release()
                    print('--send all client--')
                    for c in clients:
                        c[0].sendto(win_msg.encode('utf-8'), c[1])
                        c[0].sendto(msg.encode('utf-8'), c[1])
                else:
                    #メッセージをスタックする
                    queueLock.acquire()
                    msg_queue.put(msg)
                    queueLock.release()
                    print('msg:{}'.format(msg))
                    msg = 'return'
                    for c in clients:
                        c[0].sendto(msg.encode('utf-8'), c[1])
                    
            

               
            
if __name__ == '__main__':
    s_class = ServerClass()