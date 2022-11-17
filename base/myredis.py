import json
import threading
import sys
import redis   # 导入redis 模块
redis_host="127.0.0.1"
redis_port=6379
import time
def get_redis(key):
    r=redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    result=r.get(key)
    return result

def set_redis(key,val,ex=None, px=None, nx=False, xx=False):
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    flag=r.set(key, val, ex=ex, px=px, nx=nx, xx=xx)
    return flag

def set_copy_redis(key,val,ex=None, px=None, nx=False, xx=False):
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    flag=r.set(key, val, ex=ex, px=px, nx=nx, xx=xx)
    flag_copy=r.set(key+"__copy", val)
    return flag and flag_copy


def del_redis(key):
    r = redis.Redis(host=redis_host, port=redis_port, decode_responses=True)
    return r.delete(key)





def setSession(gid,uid,func_name,stage,content=""):
    pass

def expire_event(message):
    if message["pattern"]!=b'__keyevent@0__:expired':
        print("error!")
        return
    # 取键
    message = str(message["data"],'UTF-8')

    # 取值
    value=get_redis(message+"__copy")
    print("key",message)
    print("val",value)
    value=json.loads(value)


    msg=json.loads(message)

    msg.update({"endEvent":True})
    msg.update({"VALUE":value})
    try:
        eval("{0}(msg,para=None)".format(msg["func"]))
    except Exception as e:
        print(e)
        print("{0}(msg,para=None)".format(msg))
        return
def generate_key(func_name,**kwargs):
    ret={"func": func_name}
    ret.update(kwargs)
    return json.dumps(ret)
# def generate_key(func_name,gid,uid=None):
#
#     if uid is not None:
#         return json.dumps({"func":func_name,"gid":gid,"uid":uid})
#     else:
#         return json.dumps({"func": func_name, "gid": gid})
def expired_loop():
    redis_conn = redis.Redis(host=redis_host, port=redis_port)
    pubsub = redis_conn.pubsub()
    pubsub.psubscribe('__keyevent@0__:expired')
    while True:
        try:
            message = pubsub.get_message()
            if message:
                expire_event(message)
            else:
                time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL + C
            break
def expired_loop_test():
    redis_conn = redis.Redis(host=redis_host, port=redis_port)
    pubsub = redis_conn.pubsub()
    pubsub.psubscribe('__keyevent@0__:expired')
    while True:
        try:
            message = pubsub.get_message()
            if message:
                print(message)
            else:
                time.sleep(0.1)
        except KeyboardInterrupt:
            # CTRL + C
            break
def expired_listening():

    t = threading.Thread(target=expired_loop)
    t.start()

#key gid uid func
#val stage content
# print(set_copy_redis('{"gid":"30088","uid":"20001","func":"hello"}','{"stage":"1","content":"hello"}',ex=1))
# expired_listening()
# set_copy_redis("123","3",ex=60)
# if get_redis("123"):
#     print("1233333")
# del_redis("123")
# if get_redis("123"):
#     print("1233333")

