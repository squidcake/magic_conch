# {Host: fiction.cyapi.cn
# User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0
# Accept: */*
# Accept-Language: zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2
# Accept-Encoding: gzip, deflate, br
# Referer: https://if.caiyunai.com/
# Access-Control-Request-Method: POST
# Access-Control-Request-Headers: content-type,lang,ostype,testapi,uid
# Origin: https://if.caiyunai.com
# Connection: keep-alive
# Sec-Fetch-Dest: empty
# Sec-Fetch-Mode: no-cors
# Sec-Fetch-Site: cross-site
# TE: trailers
# Pragma: no-cache
# Cache-Control: no-cache}
#设置请求头
import json
from magic_conch.base.myredis import *

import requests

headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
    "uid": "6257a920f079a93649a550a7",
    "Origin":"https://fiction.cyapi.cn/v2/novel/6257a920f079a93649a550a7/novel_ai"
}

DREAM_EXPIRE_TIME=120
def generate_mydata(words):

    mydata = {"nid": "6257afb9e440c35572b8cfa9", "content": words, "uid": "6257a920f079a93649a550a7",
          "mid": "60094a2a9661080dc490f75a", "title": "", "status": "http", "storyline": "false",
          "lastnode": "6257afb9e440c35572b8cfaa", "branchid": "6257afb9e440c35572b8cfab", "ostype": "", "lang": "zh"}
    return mydata
def rewrite(key):
    mydata=get_redis(key)

    mydata=json.loads(mydata)
    print(mydata)
    # try:
    # temp=requests.post(url="https://fiction.cyapi.cn/v2/novel/6257a920f079a93649a550a7/novel_ai",headers=headers)
    # print(temp.content)
    res=requests.post(url="https://fiction.cyapi.cn/v2/novel/6257a920f079a93649a550a7/novel_ai",data=json.dumps(mydata),headers=headers)
    result=json.loads(res.content)
    dit = result["data"]["nodes"][0]
    mydata["content"] = mydata["content"] + dit["content"]
    mydata["lastnode"] = dit["_id"]
    mydata=json.dumps(mydata)
    set_copy_redis(key,mydata,ex=DREAM_EXPIRE_TIME)
    # except Exception as e:
    #     print(e)
    #     return None
    return result

def get_content(result):
    return result["data"]["nodes"][0]["values"][0]["value"]

def set_mydata(key,val):
    set_copy_redis()

def get_all_content(key):
    return json.load(get_redis(key))["content"]