from pathlib import Path
import random
import os

def pickone():
    mypath = Path(__file__).resolve().parent
    fo1 = open(str(mypath)+"/chouqian.txt", "r",encoding='UTF-8')
    raw_list=fo1.readlines()
    index=random.randint(1,100)
    end_index=str(index+1)
    index=str(index)

    catch_flag=False
    result = ""
    for i in raw_list:
        if i.strip()==index:
            catch_flag=True
            result+=i
            continue
        elif i.strip()==end_index:
        	break
        if catch_flag:
            result+=i
    return result
