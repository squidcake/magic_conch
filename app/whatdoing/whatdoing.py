from pathlib import Path
import os
import random


def pickone(gid,name,flag):
    path = str(Path(__file__).resolve().parent)
    group_path=path+"\\data\\"+str(gid)
    if not os.path.exists(group_path):
        os.mkdir(group_path)

    if not flag:
        with open(path+"/what.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            temp=f.readlines()
    else:
        temp=[]
    if os.path.exists(group_path+"/what.txt"):
        with open(group_path+"/what.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            temp1=f.readlines()
    else:
        temp1=[]
    temp=temp+temp1
    what=temp[random.randint(0,len(temp)-1)].strip()

    if not flag:
        with open(path+"/where.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            temp=f.readlines()
    else:
        temp=[]
    if os.path.exists(group_path+"/where.txt"):
        with open(group_path+"/where.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            temp1=f.readlines()
    else:
        temp1=[]
    temp=temp+temp1
    where=temp[random.randint(0,len(temp)-1)].strip()

    if not flag:
        with open(path+"/when.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            temp=f.readlines()
    else:
        temp=[]
    if os.path.exists(group_path+"/when.txt"):
        with open(group_path+"/when.txt","a+",encoding="utf-8") as f:
            f.seek(0)
            temp1=f.readlines()
    else:
        temp1=[]
    temp=temp+temp1
    when=temp[random.randint(0,len(temp)-1)].strip()
    return ("【{0}】{1}{2}，{3}".format(name,where,when,what))

def addone(gid,content,para):

    path = str(Path(__file__).resolve().parent)
    group_path=path+"\\data\\"+str(gid)
    if not os.path.exists(group_path):
        os.mkdir(group_path)
    group_path=group_path+"\\"+para+".txt"
    with open(group_path,"a+",encoding="utf-8") as f:
        f.seek(0)
        if len(f.readlines())==0:
            f.write(content)
        else:
            f.write("\n"+content)
    return

def removeone(gid,content,para):

    path = str(Path(__file__).resolve().parent)
    group_path=path+"\\data\\"+str(gid)
    data=""
    flag=False
    if not os.path.exists(group_path):
        os.mkdir(group_path)
    group_path=group_path+"\\"+para+".txt"
    with open(group_path,"a+",encoding="utf-8") as f:
        f.seek(0)
        temp=f.read()
        if content in temp:
            flag=True
            data=temp.replace("\n"+content,"")
    if flag is False:
        return False
    else:
        with open(group_path, "w", encoding="utf-8") as f:
            f.write(data)
        return  True
