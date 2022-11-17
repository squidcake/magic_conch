from pathlib import Path
import random
import os
def get_txt():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/goodnight.txt", "r",encoding='UTF-8')
    lines = [l for l in fo1.readlines() if l.strip()]
    return lines

def get_goodnight_words(name):
    content=get_txt()
    length=len(content)
    count=random.randint(0,length-1)
    raw=content[count]
    return raw.replace("[name]",name)

