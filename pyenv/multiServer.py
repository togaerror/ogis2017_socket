import socket
import threading
import json
import queue

#test json
test = ''' {
    "test" : "json" 
} '''
 #Queue
msg_queue = queue.Queue()
queueLock = threading.Lock()

class ServerClass:
    def c_handler(client, c_addr, c_port):
        max_size = 1024
        num = b_recv(client, max_size)
        num = int(num)
        b_send(client, num)
        
        for i in range(3):
            try:
                print(num)
                msg = b_recv(client, max_size)
            except OSError:
                break

            msg = b_json(msg)
            json_queue_put(msg)
            msg = 'return'
            b_send(client, msg)

            if len(msg) == 0:
                break
            
        client.close()
        print('bey')

        print('queue')
        while not msg_queue.empty():
            print(msg_queue.get())

    def start_server():
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
        s_host = 'localhost'
        s_port = 6789
        server.bind((s_host, s_port))
        server.listen(128)
        print('Server Start')

        while True:
            client, (c_addr, c_port) = server.accept()
            print('New Client: {0} : {1}'.format(c_addr, c_port))
            c_thread = threading.Thread(target = c_handler,
                args = (client, c_addr, c_port))
            c_thread.daemon = True
            c_thread.start()


    #queueから削除
    def json_queue_get():
        return msg_queue.get()
    #queueに追加
    def json_queue_put(msg):
        queueLock.acquire()
        msg_queue.put(msg)
        queueLock.release()
    #PythonObjectに変換
    def b_json(msg):
        msg = msg.decode('utf-8')
        msg = json.loads(msg)
        print(msg)
        return msg
    #msg bytesに変換し送信
    def b_send(client, msg):
        msg = str(msg)
        msg = bytes(msg, 'utf-8')
        client.sendall(msg)
    #msg 受信
    def b_recv(client, max_size):
        msg = client.recv(max_size)
        print(msg)
        return msg 

if __name__ == '__main__':
    ServerClass.start_server()