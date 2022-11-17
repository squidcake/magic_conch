import json

import requests
import magic_conch.config as config
# test
# import config as config


from pypinyin import lazy_pinyin, Style
from pathlib import Path
import threading
import functools
import datetime
# res=requests.get(url="http://127.0.0.1:5700/send_private_msg",params={"user_id":"2022355368",
#                                                                       "message":"哈喽"})
# print(res.content)
import os,base64
import requests as req
from PIL import Image
from io import BytesIO
import re

import random

import requests

url = "http://fanyi.youdao.com/translate"







def get_random_user(gid,top=20,random_num=49,random_flag=False):
    member_list= get_group_member_list(gid)
    if member_list:

        if len(member_list)<=random_num or random_flag:
            temp=random.randint(0,len(member_list)-1)
            target=member_list[temp]["name"]
        else:
            temp=random.randint(0,top)
            templist=[]
            for i in member_list:
                templist.append([i["user_id"],i["last_sent_time"]])

            templist.sort(key=lambda x: x[1], reverse=True)
            target=templist[temp][0]
    return target

def get_root():
    mypath = Path(__file__).resolve().parent.parent
    return str(mypath)
def download_all(gid):
    pass
def upload_all(uid):
    pass
def get_banwords():
    path=get_root()+"/data/banwords.txt"
    with open(path,encoding='UTF-8') as f:
        temp=f.readlines()
        temp="".join(temp)
        raw_list=str(temp).split()
        raw_list=[i for i in raw_list if "[" not in i]
    return raw_list

def get_banlist():
    path=get_root()+"/data/banlist.txt"
    with open(path) as f:
        temp=f.readlines()
        raw_list=[int(i.strip()) for i in temp]
    return raw_list

def get_authgroup_list():
    path=get_root()+"/data/authgroup_list.txt"
    with open(path) as f:
        temp=f.readlines()
        raw_list=[]
        for i in temp:
            i=i.strip()
            if i[0]=="#":
                continue
            else:
                raw_list.append(int(i))
    return raw_list
def get_authuser_list():
    path=get_root()+"/data/authuser_list.txt"
    with open(path) as f:
        temp=f.readlines()
        raw_list=[int(i.strip()) for i in temp]
    return raw_list
def get_user_by_name(gid,uid,name):
    # 先个人，再全局，再群列表
    key1=generate_key("nickname", type="global", gid=gid, nickname=name)
    result=get_redis(key1)
    if result is None:
        key2 = generate_key("nickname", type="global", gid=gid,uid=uid,nickname=name)
        result=get_redis(key2)
    if result is None:
        result=get_user_from_group_list(gid,name)
        if len(result)>=2 or len(result)==0:
            return None
        else:
            return result[0]
    return result


def return_not_None(*args):
    for i in args:
        if i is not None:
            return i
    return None
def AT_USER(uid):
    return "[CQ:at,qq={0}]".format(uid)
def deco_closedown(func):
    def wrapper(*args, **kwargs):
        msg=args[0]
        sendmsg_auto(msg,"神奇海螺提醒您：该功能已经暂时关闭")
        return
    return wrapper
def deco_working(func):
    def wrapper(*args, **kwargs):
        msg=args[0]
        gid=get_group(msg)
        flag=check_test_auth(msg)
        if flag:
            func(*args,**kwargs)
        else:
            sendmsg(gid,"神奇海螺提醒您：该功能正在维护中")
        return False
    return wrapper

def check_usage_auth(msg):
    if "group_id" in msg:
        gid=get_group(msg)
        grouplist=get_authgroup_list()
        if gid in grouplist:
            return True
        else:
            return False
    elif "user_id" in msg:
        uid = get_user(msg)
        userlist = get_authuser_list()
        if uid in userlist:
            return True
        else:
            return False
    return False
def deco_usage_auth(func):
    def wrapper(*args, **kwargs):
        msg=args[0]
        gid=get_group(msg)
        flag=check_usage_auth(msg)
        if flag:
            func(*args,**kwargs)
        else:
            sendmsg(gid,"神奇海螺提醒您：你所在的群组没有该功能使用权限。申请权限请找作者~")
        return False

    return wrapper

def deco_working_block(func):
    def wrapper(*args, **kwargs):
        msg=args[0]
        gid=get_group(msg)
        flag=check_test_auth(msg)
        if flag:
            func(*args,**kwargs)
        else:
            pass
        return True
    return wrapper

def check_test_auth(msg):
    if "group_id" in msg:
        gid=str(get_group(msg))
        if gid in config.TEST_GROUP:
            return True
        else:
            return False

    elif "user_id" in msg:
        uid = str(get_user(msg))
        if uid in config.TEST_USER:
            return True
        else:
            return False
    return False

def get_CQimg_erciyuan():
    acg_api = [api_dict("https://www.dmoe.cc/random.php?return=json", "樱花api"),
               # api_dict("https://api.vvhan.com/api/acgimg?type=json","韩小韩api"),
               api_dict("https://api.ixiaowai.cn/api/api.php?return=json", "小歪"),
               api_dict("https://api.ghser.com/random/api.php", "一叶三秋")]
    random.shuffle(acg_api)
    for i in acg_api:
        req_url = i["url"]
        print("<图片爬取>访问api:", i["name"])
        try:
            res = requests.get(req_url)
        except:
            print("<图片爬取>访问api失败！")
            continue
        print("<图片爬取>api访问成功")

        if req_url.endswith(".php"):
            pic_url = res.url
        else:
            res_data = json.loads(res.content)
            for key in ["imgurl", "acgurl"]:
                if key in res_data:
                    pic_url = res_data[key]
                    break
        try:
            basedata = str(get_img_base(pic_url), encoding="UTF-8")
            pic = "[CQ:image,file=base64://" + basedata + "]"
            return pic
        except Exception as e:
            print("图片获取出错:", e)
            continue
    return None
def get_CQimg_local(uri):
    basedata = str(get_img_base_loacl(uri), encoding="UTF-8")
    pic = "[CQ:image,file=base64://" + basedata + "]"
    return pic

def get_CQimg_base(base64):
    pic = "[CQ:image,file=base64://" + str(base64,encoding="UTF-8") + "]"
    return pic

def get_CQimg_url(url):
    pic = "[CQ:image,file=base64://" + str(get_img_base(url),encoding="UTF-8") + "]"
    return pic
def get_group_list():
    print("请求群组列表")
    res=requests.get(url=config.HTTP_URL+"get_group_list")
    result=json.loads(res.content)
    gid_list=[i["group_id"] for i in result["data"]]
    return gid_list
def get_group_member_list(gid):

    print("向群组{0}请求群员列表".format(gid))
    res=requests.get(url=config.HTTP_URL+"get_group_member_list", params={"group_id": gid})
    print("响应:", res.content[0:64])
    result=json.loads(res.content)
    result=result["data"]
    for i in result:
        name = i["card"]
        if name == "":

            name = i["nickname"]
        i["name"]=name
    return result

def get_user_from_group_list(gid,name):
    user_list=get_group_member_list(gid)
    result_list=[]
    for i in user_list:
        if name in i["nickname"] or name in i["card"]:
            result_list.append(i["user_id"])
    return result_list
def get_img_base_loacl(uri):
    try:
        png = open(uri, 'rb')
    except Exception as e:
        print(e)
        print(uri)
        return
    res = png.read()
    s = base64.b64encode(res)
    png.close()
    return s


def get_img_base(url):
    # 将这个图片保存在内存
    print("<图片爬取>获取图片中,url:",url)
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    response = requests.get(url,headers=headers)
    print("<图片爬取>获取图片成功！")
    # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
    # image = Image.open(BytesIO(response.content))
    # 得到这个图片的base64编码
    ls_f=base64.b64encode(BytesIO(response.content).read())
    return ls_f
def get_img_base_CQ(message):
    # test="[CQ:image,file=c5056485f44e260d3feae38ab850990e.image,url=https://gchat.qpic.cn/gchatpic_new/1/0-0-C5056485F44E260D3FEAE38AB850990E/0?term=2,subType=0]"
    temp=re.match(".*url=(https://.*),.*",message)
    try:
        url=temp.group(1)
    except:
        return None
    return get_img_base(url)



def get_img_base_outsider(url):
    # 将这个图片保存在内存
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    proxies = {"http": "gg.bgppro.bukala.cc", "https": "127.0.0.1:64418"}
    response = req.get(url,proxies=proxies,headers=headers)
    # 将这个图片从内存中打开，然后就可以用Image的方法进行操作了
    # image = Image.open(BytesIO(response.content))
    # 得到这个图片的base64编码
    ls_f=base64.b64encode(BytesIO(response.content).read())
    return ls_f


def get_group(msg):
    if "group_id" in msg:
        return msg["group_id"]
    elif "gid" in msg:
        return msg["gid"]
    else:
        return None

def sayToRobot(message):
    res=requests.get(url="http://api.qingyunke.com/api.php?key=free&appid=0&msg="+message)
    reply=json.loads(res.content)
    return reply["content"]


def getfirst_words(str_data):
    """
       获取字符串的首字母
       :param str_data: 字符串
       :return: 返回首字母缩写(大写)
       """
    a = ''.join(lazy_pinyin(str_data, style=Style.FIRST_LETTER))
    return a.upper()
def get_user(msg):
    if "user_id" in msg:
        return msg["user_id"]
    elif "uid" in msg:
        return msg["uid"]
    else:
        return None
def get_attr(msg,attr):
    if attr in msg:
        return msg[attr]
    else:
        return None
def get_msg(msgid):
    res=requests.get(url=config.HTTP_URL+"get_msg", params={"message_id":msgid})
    result=json.loads(res.content)
    return result["data"]

def make_withdraw(msgid):
    res=requests.get(url=config.HTTP_URL+"delete_msg", params={"message_id":msgid})
    result=json.loads(res.content)
    return 

def get_replyid(msg):
    message=msg["message"]
    result=re.match(".*\[CQ:reply,id=([0-9,-]+)?\].*",message)
    try:
        result=result.group(1)
    except:
        return None
    return int(result)


def get_group_name(gid):
    res=requests.get(url=config.HTTP_URL+"get_group_info", params={"group_id": gid,
                                                                             "no_cache": "false"})
    result=json.loads(res.content)
    return result["data"]["group_name"]
def get_group_cardname(gid,uid):
    print("向群组{0}请求{1}的昵称".format(gid, uid))
    res=requests.get(url=config.HTTP_URL+"get_group_member_info", params={"group_id": gid,
                                                                             "user_id": uid})
    print("响应:", res.content)
    result=json.loads(res.content)
    if result["status"]=="failed":
        return None
    name=result["data"]["card"]
    if name=="":
        name=result["data"]["nickname"]

    return name

def sendmsg_auto(msg,content):
    if "group_id" in msg:
        gid=get_group(msg)
        flag=sendmsg(gid,content)
    elif "user_id" in msg:
        uid = get_user(msg)
        flag=sendmsg_private(uid,content)
    else:
        return False
    return flag



def sendmsg(group_id,content,show_flag=True,check_flag=False):
    banwords=get_banwords()
    if show_flag and check_flag:
        for i in banwords:
            if i in content:
                temp=list(i)
                temp[0]="***"
                temp="[报告]".join(temp)
                report=content.replace(i,temp)
                sendmsg_private(2022355368,"神奇海螺想说危险的话！群号:{0},内容是:{1}".format(group_id,report))
                content="【神奇海螺的回答存在敏感词汇，被回避掉啦】"
    if show_flag:
        print("向群组{0}发送内容：{1}".format(group_id,content))
    else:
        print("向群组{0}发送内容：含图片".format(group_id, content))
    try:
        res = requests.post(url=config.HTTP_URL+"send_group_msg", data={"group_id": group_id,
                                                                             "message": content})
        print("响应:",str(res.content,encoding="UTF-8"))

    except Exception as e:
        print("发送出错：",e,e.with_traceback())
        return False
    return True



def sendmsg_private(user_id,content):
    print("向用户{0}发送内容：{1}".format(user_id,content))
    print(config.HTTP_URL+"send_private_msg","11111111111111111")
    try:
        res = requests.get(url=config.HTTP_URL+"send_private_msg", params={"user_id": user_id,
                                                                                 "message": content})
        print("响应:",res.content)

    except Exception as e:
        print("发送出错：",e,e.with_traceback())
        return False
    return True
def api_dict(url,name):
    return {"url":url,"name":name}
