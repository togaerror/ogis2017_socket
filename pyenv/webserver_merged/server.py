import tornado.ioloop
import tornado.web
import tornado.websocket
import os
import json
import threading
import time
from ClientClass import *

cl = []
class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        #print("self_info: " + self)
        if self not in cl:
            cl.append(self)
            print("open")

        self.c = ClientClass()

        #クライアント用のsocketクライアントをここで作る
        self.cl_th1 = threading.Thread(name="cl_th1", target=self.cl_threadTest)
        self.cl_th1.setDaemon(True)  # これを指定しない場合"ctrl+C"でスレッドが終了しないので注意
        self.cl_th1.start()


    def on_message(self, message):
        print(message)
        #アプリのクライアントから送られてきたJSONメッセージをsocketサーバにおくる
        self.c.client.sendall(message.encode('utf-8'))
        
    def on_close(self):
        if self in cl:
            cl.remove(self)
            print("close")

    #受け取り口
    def cl_threadTest(self):
        self.sheepCounter = 0
        '''
        while(True):
            time.sleep(3)
            print(str(self.sheepCounter) + "sheep...")
            self.sheepCounter += 1
        '''

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')

# 水槽前スクリーン用webSocketハンドラ，基本的に送るだけでよい
class ScreenWSHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        self.count = 1
        print("Connection established!! at screen")
        #以下スレッド作成とスタート
        self.th1 = threading.Thread(name="th1", target=self.threadTest)
        #self.th1 = threading.Thread(name="th1", target=self.threadTest, args=(,))
        # 引数一つの時注意!
        self.th1.setDaemon(True)  # これを指定しない場合"ctrl+C"でスレッドが終了しないので注意
        self.th1.start()
        #スクリーン用のsocketクライアントをここで作る

    def on_message(self, message):
        #ブラウザからメッセージを受け取る
        #print("recvFromBrowser: ",message)
        self.write_message(message)
        #socketのブラウザクライアントに送信

    def on_close(self):
        print("Disconnected!")

    # スレッド上での処理
    #受け取り口
    def threadTest(self):
        self.threadCounter = 0
        while(True):
            time.sleep(1)
            print("th1: " + str(self.threadCounter))
            self.threadCounter += 1

    '''
    def threadTest2(self):
        self.threadCounter2 = 0
        while(True):
            time.sleep(2)
            print("th2: " + str(self.threadCounter2))
            self.threadCounter2 += 1
    '''
class ScreenHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('screen.html')

application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/websocket", WebSocketHandler),
    (r"/screen", ScreenHandler),
    (r"/scws", ScreenWSHandler),
    ],
    static_path=os.path.join(os.path.dirname(__file__), "static"),
    template_path=os.path.join(os.path.dirname(__file__), "templates"),

)

if __name__ == "__main__":
    application.listen(8080)
    tornado.ioloop.IOLoop.current().start()
