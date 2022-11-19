import re
import magic_conch.config as config
from magic_conch.base.myutils import get_user,get_banlist,sendmsg_private
import threading
import traceback


def path(url,func,weight=config.DEFAULT_MAX,post_type="message",**kwargs):
    url=url.replace("【name】",config.QQ_NAME)
    temp={"url":url,"func":func,"weight":weight}
    func_para={}
    match={}
    for i in kwargs:
        print(i)
        if i[0]=="_":
            func_para.update({i[1::]:kwargs[i]})
        else:
            match.update({i:kwargs[i]})
    match.update({"post_type":post_type})
    temp.update({"__match":match})
    temp.update({"__para":func_para})
    print()
    print(temp)
    return temp

def check_match_info(path,msg):
    flag=True
    for i in path["__match"]:
        if i not in msg or path["__match"][i]!=msg[i]:
            flag=False
            break
    return flag


def router(msg,PATH,minweight,except_list=[],banflag=False):
    max=minweight

    temp=None
    # 超前处理
    # 忽略心跳
    if "meta_event_type" in msg and msg["meta_event_type"]=='heartbeat':
        return
    if "message" in msg and "[CQ:at,qq={0}]".format(config.QQ_ID) in msg["message"]:
        print(msg["message"],"被@")
        msg["message"]=msg["message"].replace("[CQ:at,qq={0}]".format(config.QQ_ID),config.QQ_NAME)





    for i in PATH:
        if i in except_list:
            continue
        if not check_match_info(i,msg):
            continue
        if msg["post_type"]=="message":
            if re.fullmatch(i["url"],msg["message"]) is not None:
                if i["weight"]>max:
                    max=i["weight"]
                    temp=i
        elif msg["post_type"]=="notice":
            pass
        else:
            print("error!")

    uid=get_user(msg)
    banlist=get_banlist()
    if temp is None:
        # print("can not route:",msg)
        return
    else:
        if uid in banlist and banflag is False:
            msg["ban"] = True
            router(msg, PATH, minweight=config.MINWEIGHT, except_list=[],banflag=True)
            return
        print("routing:", temp["url"],temp["func"].__name__)
        print()
    try:
        result= temp["func"](msg,para=temp["__para"])
    except:
        sendmsg_private(config.MONITOR,traceback.format_exc())
        return

    if result:
        except_list.append(temp)
        router(msg,PATH,minweight=config.MINWEIGHT,except_list=except_list)


