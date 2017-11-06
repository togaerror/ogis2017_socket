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
                msg = client.recv(self.max_size)
                msg = msg.decode('utf-8')
            except OSError:
                break
            
            print(msg)
            msg_queue.put(msg)
            msg = 'return'
            msg = msg.encode('utf-8')
            client.sendall(msg)
            break

        client.close()

    def s_start(self):
        print('--Server Start--')
        while True:
            client, (c_addr, c_port) = self.server.accept()
            print('New Client: {0} : {1}'.format(c_addr, c_port))
            c_thread = threading.Thread(target = s_class.c_handler,
                args = (client, c_addr, c_port))
            c_thread.daemon = True
            c_thread.start()
            
            
if __name__ == '__main__':
    s_class = ServerClass()
    s_class.s_start()