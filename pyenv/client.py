import socket
import json
from datetime import datetime
from time import sleep

#test json
test = ''' {
    "test" : "json" 
} '''

def main():
    num = input('num:')
    s_host = 'localhost'
    s_port = 6789
    max_size = 1024
    addr = (s_host, s_port)
    print('Client Start : ', datetime.now())
    print('Client', num)
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(addr)
    
    msg = 'Client' + num
    b_send(client, num)
    msg = b_recv(client, max_size)

    for i in range(3):
        b_send(client, test)
        b_recv(client, max_size)
        sleep(2)

    client.close()

#PythonObjectに変換
#文字列変換の場合loadsではなくdumpsを利用
def b_json(msg):
    msg = json.loads(msg)
    # msg = json.dumps(msg)
    print(type(msg), msg)
    return msg
#msg bytesに変換し送信
def b_send(client, msg):
    msg = str(msg)
    msg = bytes(msg, 'utf-8')
    client.sendall(msg)
#msg 受信
def b_recv(client, max_size):
    msg = client.recv(max_size)
    print(type(msg), msg)
    return msg    

if __name__ == '__main__':
    main()