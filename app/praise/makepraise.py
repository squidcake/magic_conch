from pathlib import Path
import random
import os
MAX_SENTENCE=4
MIN_SENTENCE=2
def get_body():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/body.txt", "r",encoding='UTF-8')
    lines = [l.split()[0] for l in fo1.readlines() if l.strip()]
    return lines
def get_end():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/end.txt", "r",encoding='UTF-8')
    lines = [l.split()[0] for l in fo1.readlines() if l.strip()]
    return lines

def setpraise(name):
    body=get_body()
    end=get_end()
    count=random.randint(MIN_SENTENCE,MAX_SENTENCE)
    ran = random.sample(range(0, len(body)), count)

    raw=[body[i] for i in ran]
    if len(end)!=0:
        raw.append(end[random.randint(0,len(end)-1)])
    raw=" ".join(raw)
    return raw.replace("[name]",name)

