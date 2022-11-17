import datetime
import requests
import json
import re
from base.myutils import *



def today_what_happened():
    date=datetime.datetime.now().strftime("%m%d")
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0",
        "referer": "https://baike.baidu.com/calendar/"

    }
    month=date[0]+date[1]
    url="https://baike.baidu.com/cms/home/eventsOnHistory/{0}.json".format(month)
    res = requests.get(url, headers=headers)
    res=json.loads(res.content)
    content=datetime.datetime.now().strftime("【%m月%d日】历史上的今天\n")
    res=res[month][date]

    for i in res:
        sentence=""
        sentence+=i["year"]+"年："
        title=re.sub("(<.*?>)","",i["title"])
        desc=re.sub("(<.*?>)","",i["desc"])

        sentence+=(title+"\n")
        sentence+="({0}...)\n\n".format(desc)
        content+=sentence
    return content
