import random
import json
import requests
def app_search_pic(name):
    start=random.randint(3,300)
    head = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:100.0) Gecko/20100101 Firefox/100.0'}
    url="https://pic.sogou.com/napi/pc/searchList?mode=1&start={0}&xml_len=1&query={1}".format(start,name)
    response=requests.get(url=url,headers=head)
    raw=json.loads(response.content)
    try:
        return raw["data"]["items"][0]["thumbUrl"]
    except:
        print("search pic error!")
        return None
print(app_search_pic("squid"))