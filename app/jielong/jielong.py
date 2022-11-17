import json
import random
from pathlib import Path

import pypinyin
from magic_conch.base.myredis import *
from magic_conch.base.myutils import *
idiom_path = str(Path(__file__).resolve().parent)+"\idiom2.txt"

jielong_EX=60
jielong_DEFAULT_DIFFICULTY="0"
def query_idiom(words):
    first_word=words[0]
    if first_word in [chr(i) for i in range(65,91)]:
        return False
    with open(idiom_path, 'r') as f:
        for i in set(f.readlines()):
            if words == i.strip():

                return True
    return False


def find_next_idiom(old, difficulty):
    old = old[-1]
    with open(idiom_path, 'r') as f:
        for i in set(f.readlines()):
            if i.strip()[0] == old:
                flag=check_jielong(old, i.strip(), difficulty)
                if flag:
                    return i.strip()
    return None


def random_idiom():
    print("random")
    with open(idiom_path, 'r') as f:
        res=f.readlines()
        index=random.randint(0,len(res)-1)

    return res[index].strip()

def check_jielong(old,new,difficulty):
    flag=query_idiom(new)
    if not flag:
        return False
    print("going")
    if difficulty=="0":
        old_para=pypinyin.lazy_pinyin(old[-1])
        new_para=pypinyin.lazy_pinyin(new[0])
        for i in new_para:
            if i in old_para:
                return True
        return False
    elif difficulty=="1":
        old_para=pypinyin.pinyin(old[-1])
        new_para=pypinyin.pinyin(new[0])
        for i in new_para:
            if i in old_para:
                return True
        return False
    elif difficulty == "2":
        old_para=old[-1]
        new_para=new[0]
        return old_para==new_para
    else:
        print("error")
    return False

def create_idiom_redis(gid,uid,idiom,difficulty,ai_flag=False):
    key=generate_key("make_jielong",gid=gid)
    value={uid:1,"idiom":idiom,"difficulty":difficulty,"history":[idiom],"last_uid":uid,"ai_flag":ai_flag}
    value = json.dumps(value)
    return set_copy_redis(key, value, ex=jielong_EX)


def new_idiom_redis(key,value,uid,idiom):
    uid=str(uid)
    if uid in value:
        value[uid]+=1
    else:
        value.update({uid:1})
    value["history"].append(idiom)
    value["last_uid"]=uid
    value["idiom"]=idiom
    value=json.dumps(value)
    return set_copy_redis(key,value,ex=jielong_EX)

def get_statistics(gid,value):
    last_idiom=value.pop("idiom")
    value.pop("difficulty")
    value.pop("history")
    value.pop("ai_flag")
    uid=value.pop("last_uid")
    name = get_group_cardname(gid, uid)
    if name is None:
        name=uid
    content="最后一个成语是【{0}】，由{1}完成\n".format(last_idiom,name)
    content+="【接龙统计】\n"
    temp_list=[]
    for i in value:
        name=get_group_cardname(gid, i)
        if name is None:
            name=i
        temp_list.append([name,value[i]])
    print(temp_list)
    temp_list.sort(key=lambda x: x[1],reverse=True)
    for i in temp_list:
        content+="{0}:{1}次\n".format(i[0],i[1])
    print(content,type(content))
    return content





# def check_state(gid):
#     key = generate_key("make_jielong", gid=gid)
#     temp=get_redis(key)
#     if temp is
#