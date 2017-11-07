#-*- utf-8 -*-
import socket
import threading
import queue
import json
import re
from time import sleep
#test json
test = ''' {
    "test" : "json" 
} '''
 #Queue
msg_queue = queue.Queue() #待機している設定
queueLock = threading.Lock()
win_keep = 'empty'
keep = 'empty'
win_list = []

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
        global win_keep
        global win_list
        global keep
        win_list = []
        #clientからデータを受信する
        while True:
            try:
                flag = False
                msg = ''
                msg = self.recv_msgs(con)
            except ConnectionResetError:
                #コネクションが切れたとき
                print('ConnectionResetError!')
                print('{}'.format(addr))
                con.close()
                clients.remove(con, addr)
                break

            if not msg:
                pass
            else: #メッセージを受け取った処理
                if re.match('0', msg) and re.search('start', msg):
                    #configの数を調べる
                    if win_keep == 'empty' and msg_queue.qsize() < 2 or msg_queue.qsize() == 0:
                        self.send_clients('2', 'empty')
                        #終了
                    else:
                        queueLock.acquire()
                        print('--start--')
                        self.send_clients('2', 'start')
                        sleep(1)
                        if win_keep == 'empty':
                            win_keep = msg_queue.get()
                        msg = msg_queue.get()
                        queueLock.release()
                        keep = msg
                        #投票を行う設定の送信
                        #win_keep 左, msg 右
                        self.send_clients('2', win_keep)
                        sleep(1)
                        self.send_clients('2', msg)
                        print('--end--')
                elif re.match('0', msg) and re.search('reset', msg):
                    print('screen reset')
                    self.send_clients('1', 'reset')
                elif re.match('0', msg) and re.search('result', msg): #結果
                    win_list.sort()
                    num = len(win_list)
                    print(win_list[num // 2])
                    if re.search('left', win_list[num // 2]):
                        print('win left')
                    else:
                        print('win right')
                        win_list = keep
                    print('--end--')
                elif re.match('0', msg):
                    print('--stack--')
                    queueLock.acquire()
                    msg_queue.put(msg)
                    queueLock.release()
                    self.send_clients('0', 'stack')
                elif re.match('2', msg):
                    print('Raspberry Pi')
                    queueLock.acquire()
                    if re.search('left', msg) or re.search('right', msg):
                        win_list.append(msg)
                    queueLock.release()
        
                if flag == True:
                    print('Ture')
                    
                    


if __name__ == '__main__':
    s_class = ServerClass()