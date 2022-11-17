import sys,os

import schedule

sys.path.append(os.path.dirname(__file__) + os.sep + '../')
from base.mysocket import *
from base.myredis import expired_listening
from base.myschedule import schedule_threading
print("\n【等待API开启中...】")
ws=None
ws=set_socket()
while ws is None:
	try:
		ws=set_socket()
	except:
		ws=None
print("\n【成功连接API，机器人开始运行】")
listen_socket(ws)
load_time()
expired_listening()
schedule_threading()



