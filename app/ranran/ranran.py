from pathlib import Path
import random
import os


MAX_SENTENCE=5
MIN_SENTENCE=3
LONG_POSSIBLITY=10
#3表示30%
replace_list=["然然","嘉然"]

def get_long():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/long.txt", "r",encoding='UTF-8')
    raw_list=fo1.readlines()
    temp_flag=False
    temp = ""
    result = []
    for i in raw_list:
        if i[0]=="{":
            temp_flag=True
            continue
        if i[0]=="}":
            temp_flag=False
            result.append(temp)
            temp=""
            continue
        if temp_flag:
            temp+=i
        else:
            continue

    return result

def get_short():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/short.txt", "r",encoding='UTF-8')
    lines = [l.split()[0] for l in fo1.readlines() if l.strip()]
    return lines


def set_short_ran(name):
    body=get_short()
    count=random.randint(MIN_SENTENCE,MAX_SENTENCE)
    ran = random.sample(range(0, len(body)), count)

    raw=[body[i] for i in ran]
    raw=" ".join(raw)

    for i in replace_list:
        raw=raw.replace(i,name)
    raw=raw.replace("[name]",name)
    return raw


def set_long_ran(name):
    body=get_long()
    count=random.randint(0,len(body)-1)
    raw=body[count]
    for i in replace_list:
        raw=raw.replace(i,name)
    raw=raw.replace("[name]",name)
    return raw