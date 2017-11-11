#-*- utf-8 -*-
import socket
import threading
import re
from time import sleep
import vote_sample

class ClientClass:
    def __init__(self, mode = '0'):
        self.max_size = 1024
        self.s_host = 'localhost'
        #self.s_host = '192.168.2.150'
        self.s_port = 6789
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.s_host, self.s_port))
        if mode == '2':
           self.raspberry_lisner() 
        """
        #msgの受信を待つスレッド
        if mode == '0': #UI
            self.handler_thread = threading.Thread(target = self.UI_handler, args = (), daemon = True)
            self.handler_thread.start()
        elif mode == '1': #画像
            self.handler_thread = threading.Thread(target = self.screen_handler, args = (), daemon = True)
            self.handler_thread.start()
        elif mode == '2': #RaspberryPi
            '''
            self.handler_thread = threading.Thread(target = self.raspberry_handler, args = (), daemon = True)
            self.handler_thread.start()
            '''
            self.raspberry_handler()
        else:
            print('no mode')
            self.client.close()
        """
    def UI_lisner(self):
        while True:
            msg = self.recv_msgs()
            if msg != None:
                pass
            else:
                self.client.close()
            
            if msg != None:
                if re.match('0:', msg):
                    msg = msg.lstrip('0:')
                    return msg 
    '''
    def UI_handler(self): #0
        while True:
            msg = self.recv_msgs()
            if msg != None:
                pass
            else:
                self.client.close()
            
            if msg != None:
                if re.match('0:', msg):
                    msg = msg.lstrip('0:')
                    return msg
    '''
    def screen_lisner(self): #1
        while True:
            msg = self.recv_msgs()
            if msg != None:
                pass
            else:
                self.client.close()

            if re.match('1:', msg):
                msg = msg.lstrip('1:')
                return msg
    '''
    def screen_handler(self): #1
        while True:
            msg = self.recv_msgs()
            if msg != None:
                pass
            else:
                self.client.close()

            if re.match('1:', msg):
                msg = msg.lstrip('1:')
                return msg
    '''
    def raspberry_handler(self): #2
        while True:
            msg = self.recv_msgs()
            if msg != None:
                pass
            else:
                self.client.close()
            
            if re.match('2:', msg):
                msg = msg.lstrip('2:')
                if re.search('@', msg):
                    conf = msg.split('@')
                    print('left:  {}'.format(conf[0]))
                    print('right: {}'.format(conf[1]))
                    print('--start--')
                    #ここにRaspberryPIの処理を書いていく
                    self.client.sendall('screen0'.encode('utf-8'))
                    print('--end--')
                    #RaspberryPIの処理が終わったらServerに結果を返す
                    result = vote_sample.Vote() 
                    self.client.sendall(result.encode('utf-8'))
                    print('--vote end--') 
    '''
    def raspberry_handler(self): #2
        while True:
            msg = self.recv_msgs()
            if msg != None:
                pass
            else:
                self.client.close()
            
            if re.match('2:', msg):
                msg = msg.lstrip('2:')
                if re.search('@', msg):
                    conf = msg.split('@')
                    print('left:  {}'.format(conf[0]))
                    print('right: {}'.format(conf[1]))
                    print('--start--')
                    #ここにRaspberryPIの処理を書いていく
                    self.client.sendall('screen0'.encode('utf-8'))
                    print('--end--')
                    #RaspberryPIの処理が終わったらServerに結果を返す
                    result = vote_sample.Vote() 
                    self.client.sendall(result.encode('utf-8'))
                    print('--vote end--')
    '''
    #msg受け取り
    def recv_msgs(self):
        msg = self.client.recv(self.max_size)
        msg = msg.decode('utf-8')
        return msg

if __name__ == '__main__':
    mode = input('mode:') #0, 1, 2
    c_class = ClientClass(mode)