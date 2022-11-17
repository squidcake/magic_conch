import json
import re
import random
import time
import numpy as np
import config
import os


from_gid=952148924
target_gid=634337183
# from_gid=770268240
# target_gid=691795589
import wget
import os
import threading
def upload_thread(file_name,folder_id,group_id,path):
    res = requests.get(url=config.HTTP_URL + "upload_group_file",
                       params={"name": file_name, "folder": folder_id, "group_id": group_id,
                               "file": path})
    print("【{0}上传成功】".format(file_name))

def upload(file_name,folder_id,group_id,path):
    threading.Thread(target=upload_thread, args=(file_name,folder_id,group_id,path)).start()

def mkdir(path):
    '''
    创建指定的文件夹
    :param path: 文件夹路径，字符串格式
    :return: True(新建成功) or False(文件夹已存在，新建失败)
    '''
    # 引入模块
    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")
    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)
    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
         # 创建目录操作函数
        os.makedirs(path)
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
        return False

TEMP_URI = "D://TEMP"
res=requests.get(url=config.HTTP_URL+"get_group_root_files", params={"group_id": from_gid})
result=json.loads(res.content)
folder_data=result["data"]["folders"]
file_data=result["data"]["files"]
print(folder_data)
for folder in folder_data:
    folder_name=folder["folder_name"]
    folder_id=folder["folder_id"]
    print("开始下载文件夹：{0}".format(folder_name))
    if not mkdir(TEMP_URI+"//"+folder_name):
        print(TEMP_URI+"//"+folder_name + ' 目录已存在')
    res = requests.get(url=config.HTTP_URL + "create_group_file_folder",
                       params={"group_id": target_gid, "parent_id":"/","name": folder_name})

    res = requests.get(url=config.HTTP_URL + "get_group_files_by_folder", params={"group_id": from_gid,"folder_id":folder_id})
    result = json.loads(res.content)
    folder_files=result["data"]["files"]


    res = requests.get(url=config.HTTP_URL + "get_group_root_files", params={"group_id": target_gid})
    result = json.loads(res.content)
    folder_data = result["data"]["folders"]
    for i in folder_data:
        if i["folder_name"]==folder_name:
            new_folder_id=i["folder_id"]
            break
    for file in folder_files:
        file_name=file["file_name"]
        id=file["file_id"]
        busid=file["busid"]
        res = requests.get(url=config.HTTP_URL + "get_group_file_url",
                           params={"group_id": from_gid, "file_id": id,"busid":busid})
        result = json.loads(res.content)
        url=result["data"]["url"]
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
        }
        path=TEMP_URI+"//"+folder_name+"//"+file_name
        if os.path.exists(path):  # True/False
            print("     文件已存在，跳过")
            continue
        print("     {0}开始下载...".format(file_name))
        wget.download(url, path)  # 下载
        print("     {0}下载成功".format(file_name))
        upload(file_name,new_folder_id,target_gid,path)

        print()
    print("文件夹：{0}下载完成".format(folder_name))
    print()
    print()

for file in file_data:
    file_name=file["file_name"]
    id=file["file_id"]
    busid=file["busid"]
    res = requests.get(url=config.HTTP_URL + "get_group_file_url",
                       params={"group_id": from_gid, "file_id": id,"busid":busid})
    result = json.loads(res.content)
    url=result["data"]["url"]
    headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:99.0) Gecko/20100101 Firefox/99.0"
    }
    path=TEMP_URI+"//"+file_name
    if os.path.exists(path):  # True/False
        print("文件已存在，跳过")
        continue
    print("{0}开始下载...".format(file_name))
    wget.download(url, path)  # 下载
    print("{0}下载成功".format(file_name))
    upload(file_name,"",target_gid,path)
    print()