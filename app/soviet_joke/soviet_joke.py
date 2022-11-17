import re
from pathlib import Path
import random
import os


def get_soviet_joke():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/joke.txt", "r",encoding='UTF-8')
    raw_list=fo1.readlines()

    temp = ""
    result = []
    for i in raw_list:
        if re.match("[0-9]+\)",i):
            result.append(temp)
            temp=i
            continue
        if i=="\n":
            continue
        temp+=i

    return result

def set_soviet_joke():
    content_list=get_soviet_joke()
    index=random.randint(1,len(content_list)-1)
    return content_list[index]


