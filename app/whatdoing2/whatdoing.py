from pathlib import Path
import os
import random


def pickone(gid,name):
    path = str(Path(__file__).resolve().parent)
    group_path=path+"\\data\\"+gid
    if not os.path.exists(group_path):
        os.mkdir(group_path)
    with open(path+"/what.txt","r",encoding="utf-8") as f:
        temp=f.readlines()
    with open(group_path+"/what.txt","r",encoding="utf-8") as f:
        temp1=f.readlines()
    print("temp1",temp1)
    temp=temp+temp1
    what=temp[random.randint(0,len(temp)-1)].strip()


    with open(path+"/where.txt","r",encoding="utf-8") as f:
        temp=f.readlines()
    with open(group_path+"/what.txt","r",encoding="utf-8") as f:
        temp1=f.readlines()
    print("temp1",temp1)
    temp=temp+temp1
    where=temp[random.randint(0,len(temp)-1)].strip()


    with open(path+"/when.txt","r",encoding="utf-8") as f:
        temp=f.readlines()
    with open(group_path+"/what.txt","r",encoding="utf-8") as f:
        temp1=f.readlines()
    print("temp1",temp1)
    temp=temp+temp1
    when=temp[random.randint(0,len(temp)-1)].strip()
    return (name+where+when+","+what)

def addone(gid,content,para):

    path = str(Path(__file__).resolve().parent)
    group_path=path+"\\data\\"+gid
    if not os.path.exists(group_path):
        os.mkdir(group_path)
    group_path=group_path+"\\"+para+".txt"
    with open(path,"a+") as f:
        f.write("\n"+content)
    return



print(pickone(2022355368,"squid"))