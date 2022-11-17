import requests
import json
import pandas as pd

url = 'https://api.inews.qq.com/newsqa/v1/query/inner/publish/modules/list?modules=statisGradeCityDetail'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'}

resp = requests.get(url, headers=headers)
resps = resp.json()
resps = resps["data"]
datas = resps['statisGradeCityDetail']


myinput="上海"
province=["北京","天津","上海","重庆","河北","山西","辽宁","吉林","黑龙江","江苏","浙江","安徽","福建","江西","山东","河南","湖北","湖南","广东","海南","四川","贵州","云南","陕西","甘肃","青海","台湾","内蒙古","广西","西藏","宁夏","新疆","香港","澳门"]
province_flag=False
if myinput in province:
    province_flag=True

datas_list = []
datas_dict = {}

# datas_dict['地区名称'] = i['name']
datas_dict['现有确诊'] = 0
datas_dict['新增确诊'] = 0
datas_dict['累计确诊'] = 0
datas_dict['死亡人数'] = 0
datas_dict['治愈人数'] = 0
# datas_dict['风险等级'] = "NONE"
# datas_dict['省份'] = i['province']
# datas_dict['城市'] = i['city']
if province_flag:
    for i in datas:
        if myinput==i['province']:
            datas_dict['新增确诊'] += int(i['confirmAdd'])
            datas_dict['现有确诊'] += int(i['nowConfirm'])
            datas_dict['累计确诊'] += int(i['confirm'])
            datas_dict['死亡人数'] += int(i['dead'])
            datas_dict['治愈人数'] += int(i['heal'])


    # datas_dict = {}
    # datas_dict['地区名称'] = i['name']
    # datas_dict['现有确诊'] = i['nowConfirm']
    # datas_dict['新增确诊'] = i['confirmAdd']
    # datas_dict['累计确诊'] = i['confirm']
    # datas_dict['死亡人数'] = i['dead']
    # datas_dict['治愈人数'] = i['heal']
    # datas_dict['风险等级'] = i['grade']
    # datas_dict['省份'] = i['province']
    # datas_dict['城市'] = i['city']
    datas_list.append(datas_dict)

df = pd.DataFrame(datas_list)

print(df)
