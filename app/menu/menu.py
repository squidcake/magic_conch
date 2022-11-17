from pathlib import Path
import random
import os

def read_txt():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/menu.txt", "r",encoding='UTF-8')
    raw_list=fo1.readlines()
    return raw_list
def app_get_menu():
    raw_list=read_txt()
    content="".join(raw_list)
    return content

