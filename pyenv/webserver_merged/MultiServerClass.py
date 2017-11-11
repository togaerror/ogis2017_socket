#-*- utf-8 -*-
import socket
import threading
import queue
import re

#Queue
msg_queue = queue.Queue() #待機している設定
threadLock = threading.Lock()
#Client Stack
clients = []
result_stack = []
win_keep = ''

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
        if re.match('0:', msg):
            msg = msg.rsplit('0:', msg)
        elif re.match('1:', msg):
            msg = msg.rsplit('1:', msg)  
        elif re.match('2:', msg):
            msg = msg.rsplit('2:', msg)
        return msg

    def server_handler(self, con, addr):
        #clientからデータを受信する
        global win_keep
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
                if msg == 'start': #投票の開始
                    threadLock.acquire()
                    if msg_queue.qsize() == 0:
                        print('empty')
                    else:
                        msg = msg_queue.get()
                        msg = win_keep + '@' + msg
                        self.send_clients('2', msg)
                    threadLock.release()
                elif msg == 'left' or msg == 'right':
                    threadLock.acquire()
                    result_stack.append(msg)
                    threadLock.release()
                else:
                    #設定のスタック
                    threadLock.acquire()
                    if win_keep == '':
                        win_keep = msg
                    else:
                        msg_queue.put(msg)
                    threadLock.release()


if __name__ == '__main__':
    s_class = ServerClass()