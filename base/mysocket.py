import websocket
import threading
import magic_conch.config as config
from magic_conch.urls import router,PATH,LOOP
import json


def set_socket():
    ws = websocket.WebSocket()
    ws.connect("ws://127.0.0.1:{0}/".format(config.PORT))
    return ws

def get_recv(ws):
    while True:
        msg=ws.recv()
        threading.Thread(target=router, args=(json.loads(msg), PATH, config.MINWEIGHT, [])).start()
        # router(json.loads(msg), PATH, config.MINWEIGHT, [])
        # length = len(threading.enumerate())
        # print('当前运行的线程数为：%d' % length)


def listen_socket(ws):
    t = threading.Thread(target=get_recv, args=(ws,))
    t.start()

def load_time():
    for i in LOOP:
        threading.Thread(target=i["func"],kwargs={"para":i["__para"]}).start()


