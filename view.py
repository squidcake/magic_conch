import json
import re
import random
import time
import numpy as np
import random
import traceback
from base.myutils import *
from base.cov import *
from base.db_utils import *
from base.myredis import *
from base.myschedule import deco_threading
import config as config
from app.elseapp import *
from app.jielong import jielong
from app.ranran import ranran
from app.soviet_joke import soviet_joke
from app.menu import menu
from app.baidu import baidu
from app.tarotarot import tarotarot
from app.praise.makepraise import setpraise
from app.gua.ToChange import calculate_with_plum_flower
from app.dream import dream
from app.goodnight.say_goodnight import get_goodnight_words
from app.chouqian import chouqian
from app.whatdoing import whatdoing
from app.aipainting import aipainting
# sendmsg_private(2022355368,"[CQ:image,file=35d220d955769e33d4fc572d4b102fe8.image,subType=0]")
# sendmsg_private(2022355368," [CQ:image,file=90b45625c310e11823b724ab718d7a05.image,subType=0]")


def redraw_msg(msg,para):
    gid=get_group(msg)
    replyid=get_replyid(msg)
    if not replyid:
        sendmsg(gid,"你倒是说要撤回哪条呀？")
        return
    target_msg=get_msg(replyid)
    msgid=target_msg["message_id"]

    print(target_msg)
    if target_msg["sender"]["user_id"]==config.QQ_ID:
        make_withdraw(msgid)
    return
@deco_usage_auth
def app_aipainting(msg,para):
    gid=get_group(msg)
    uid=get_user(msg)
    name=get_group_cardname(gid,uid)
    key="aipainting"+str(gid)
    if get_redis(key) and not (gid==778505979 or gid==742112686):
        sendmsg(gid,"已经有图在绘画啦，请等上一位先画完吧~")
        return
    else:
        set_redis(key,"WORKING",ex=60)
    message=msg["message"]
    raw_message=message
    message = re.sub(".*{0}(,|，|\s|)(AI|ai)绘(图|画)".format(config.QQ_NAME),"",message)
    sendmsg(gid, "正在为【{0}】绘图中请稍后喔~".format(name))

    # 控制
    p2p_flag =False
    huge_flag = False
    translate_flag = False
    # 模式控制
    p2p_flag = "[CQ:reply" in raw_message
    # 大图控制
    huge_flag = "大图" in message
    message = message.replace("大图", "")
    # 翻译为英文
    def l_en_valiator(message):
        flag=False
        for ch in message:
            if u'\u4e00' <= ch <= u'\u9fff':
                flag = True
                break
        return flag
    def l_translate(message):
        temp = message
        url = "http://fanyi.youdao.com/translate"
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': message.encode("utf-8")
        }
        r = requests.get(url, params=data)
        result = r.json()
        try:
            message = result["translateResult"][0][0]["tgt"]
            sendmsg(gid, "原文已翻译为:" + message)
        except:
            print("英语翻译错误！！！！！")
            message = temp
        return message
    translate_flag=l_en_valiator(message)
    if translate_flag and "原文" not in message:
        message=l_translate(message)
    if l_en_valiator(message):
        message=l_translate(message)

    message = message.replace("原文", "")



    # 绘图生成
    try:
        if p2p_flag:
            replyid = get_replyid(msg)
            reply_msg = get_msg(replyid)
            pic = get_img_base_CQ(reply_msg["message"])
            pic = str(pic, "utf-8")
            raw=aipainting.pic_paint(message,pic,huge_flag)
        else:
            raw = aipainting.tags_paint(message,huge_flag)
        img=get_CQimg_base(raw)
    except Exception as e:
        traceback.print_exc()
        sendmsg(gid,"哎呀····，出错了，看来暂时还画不了哟~")
        del_redis(key)
        return
    sendmsg(gid,img,show_flag=False)
    temp="来自{0}的画作！".format(name)
    if p2p_flag:
        temp+="(novelai图转图)"
    else:
        temp+="(novelai)"
    sendmsg(gid,temp)
    dice=random.randint(1,10)
    if dice<=2:
        sendmsg(gid, "提示：描述最终都会转为英文，使用英文输入会更加准确哟")
    if 2<dice<=4:
        sendmsg(gid,"提示：回复{0}“{0}，撤回”，可以使{0}撤回该条信息！".format(config.QQ_NAME))
    del_redis(key)
    return

@deco_usage_auth
def app_aipainting_2(msg,para):
    gid=get_group(msg)
    uid=get_user(msg)
    name=get_group_cardname(gid,uid)
    key="aipainting"+str(gid)
    if get_redis(key):
        sendmsg(gid,"已经有图在绘画啦，请稍后喔~")
        return
    else:
        set_copy_redis(key,"",ex=60)
    message=msg["message"]
    message = re.sub("^{0}(,|，|)(AI|ai)绘图".format(config.QQ_NAME),"",message)
    sendmsg(gid, "正在为【{0}】绘图中请稍后喔~".format(name))

    # 翻译为英文
    temp=message
    flag=False
    for ch in message:
        if u'\u4e00' <= ch <= u'\u9fff':
            flag = True
            break

    if flag and "原文" not in message:
        url = "http://fanyi.youdao.com/translate"
        data = {
            'doctype': 'json',
            'type': 'AUTO',
            'i': message.encode("utf-8")
        }
        r = requests.get(url, params=data)
        result = r.json()
        try:
            message = result["translateResult"][0][0]["tgt"]
            sendmsg(gid,"原文已翻译为:"+message)
        except:
            print("英语翻译错误！！！！！")
            message=temp
    message=message.replace("原文","")


    try:
        raw = aipainting.tags_paint_2(message)
        img=get_CQimg_base(raw)
    except Exception as e:
        traceback.print_exc()
        sendmsg(gid,"哎呀····，出错了，看来暂时还画不了哟~")
        del_redis(key)
        return
    sendmsg(gid,img,show_flag=False)
    sendmsg(gid,"来自{0}的画作！(novelai)".format(name))
    dice=random.randint(1,10)
    if dice<=2:
        sendmsg(gid, "提示：使用英文输入会更加准确哟，输入“{0}，结束绘图”可以强制终止绘图！".format(config.QQ_NAME))
    del_redis(key)
    return
@deco_usage_auth
def end_aipainting(msg,para):
    gid=get_group(msg)
    key = "aipainting" + str(gid)
    del_redis(key)
    if not get_redis(key):
        sendmsg(gid,"绘图还没开始啦")
        return

    sendmsg(gid,"绘图已经被成功取消！")
    return


def whatdoing_addone(msg,para):
    gid=get_group(msg)
    message=msg["message"]
    message = re.sub("^{0}(,|，|)".format(config.QQ_NAME),"",message)
    op_dict={"地点":"where","时间":"when","事件":"what"}
    op=re.match("(..)添加",message  )
    if op is None:

        return False
    op=op.group(1)
    if op not in op_dict:
        return
    op=op_dict[op]
    print(message)
    content=re.match("..添加(.*)",message )
    if content is None:
        return
    content=content.group(1)
    whatdoing.addone(gid,content,op)
    sendmsg(gid,"添加成功")

def whatdoing_removeone(msg,para):
    gid=get_group(msg)
    message=msg["message"]
    message = re.sub("^{0}(,|，|)".format(config.QQ_NAME),"",message)
    op_dict={"地点":"where","时间":"when","事件":"what"}
    op=re.match("(..)删除",message)
    if op is None:
        return False
    op=op.group(1)
    if op not in op_dict:
        return
    op=op_dict[op]
    content=re.match("..删除(.*)",message)
    if content is None:
        return
    content=content.group(1)
    result=whatdoing.removeone(gid,content,op)
    if result:
        sendmsg(gid,"删除成功啦")
    else:
        sendmsg(gid,"删除失败啦，没有这一条哟")
def app_whatdoing(msg,para):
    uid=get_user(msg)
    gid=get_group(msg)
    name=get_group_cardname(gid,uid)
    message=msg["message"]
    message = re.sub("^{0}(,|，|)".format(config.QQ_NAME),"",message)
    who=re.match("(.*)在干什么",message )
    group_flag=False
    if "在干什么呀" in message:
        group_flag=True
    if who is None:
        return
    who=who.group(1)
    who=who.replace("我",name)
    result=whatdoing.pickone(gid,who,group_flag)
    result=result.replace("&#93;","]")
    result=result.replace("&#91;","[")
    while ("[who]" in result):
        result=result.replace("[who]","【{0}】".format(get_group_cardname(gid,get_random_user(gid))),1)
    sendmsg(gid,result)
    return

def ban_user(msg,para):
    uid=get_user(msg)
    gid=get_group(msg)
    name=get_group_cardname(gid,uid)
    sendmsg(gid,"【{0}】是坏人！哼，不想理你~".format(name))
    message=msg["message"]
    sendmsg_private(2022355368,"被屏蔽用户发言，群:{0}。用户:{3}({1})。内容为：{2}".format(gid,uid,message,name))
    return
def app_chouqian(msg,para):
    gid=get_group(msg)
    uid=get_user(msg)
    name=get_group_cardname(gid,uid)
    result="{0}抽中了：\n".format(name)
    result+=chouqian.pickone()
    sendmsg(gid,result)
    return
def rolls(msg,para):
    gid=get_group(msg)
    message=msg["message"]
    max_roll=6
    num_dict={"一":1,"二":2,"三":3,"四":4,"五":5,"六":6}
    num=re.match(r".*投(.*)个.*",message)
    if num is not None:
        num=num.group(1)
        if num in num_dict:
            num=num_dict[num]
        try:
            num=int(num)
        except:
            num=1
        if num >=max_roll:
            num=max_roll
    else:
        num=1
    result=""
    for i in range(num):
        temp=random.randint(1,6)
        result+=get_CQimg_local("images/roll/{0}.png".format(temp))
    sendmsg(gid,result)


def broadcast(msg,para):
    print("正在发送广播信息！")
    EXCEPT=[907249237,109487457]
    uid=get_user(msg)
    message=msg["message"]
    message=message[3::]
    if uid!=2022355368:
        return False
    else:
        gid_list=get_group_list()
        for i in EXCEPT:
            if i in gid_list:
                gid_list.remove(i)
        for i in gid_list:
            sendmsg(i,message)
            time.sleep(0.5)
        sendmsg_private(2022355368,"已全部发送成功！")
    return


# def morning_sweet(msg,para):
#     words=["早安小可爱~♪(^∇^*)吃早餐吃好好哇","小可爱小可爱早安安呀~","小可爱早安安哟~goodmorning!","哦哈哟~昨天有休息好吗？",
#     "新的一天到啦！早上好哇~^_^","早上好~哦哈哟~~(#^.^#)","早上好喔小可爱~(*^▽^*)"]
#     uid=get_user(msg)
#     temp=random.randint(0,len(words)-1)
#     sendmsg_private(uid,words[temp])

def pick_member(msg,para):
    gid=get_group(msg)
    uid=get_user(msg)

    name=get_group_cardname(gid,uid)
    member_list= get_group_member_list(gid)
    message=msg["message"]
    result = re.search("抽人(.*)", message)
    result = result.group(1)


    if member_list:
        if len(member_list)<=49:
            temp=random.randint(0,len(member_list)-1)
            target=member_list[temp]["name"]
        else:
            temp=random.randint(0,20)
            templist=[]
            for i in member_list:
                templist.append([i["user_id"],i["last_sent_time"]])

            templist.sort(key=lambda x: x[1], reverse=True)
            target=templist[temp][0]
            target=get_group_cardname(gid,target)

    else:
        return

    result=result.replace("我","【{0}】".format(name))
    if "," in message and uid==2022355368:
        target=get_group_cardname(gid,1379366429)
    result=result.replace("谁","【{0}】".format(target))
    result=result.replace("？","")
    sendmsg(gid,result)
    return

def get_tarotarot(msg,para):

    gid = get_group(msg)
    uid = get_user(msg)
    message=msg["message"]
    new_flag = not "抽" in message
    name=get_group_cardname(gid,uid)
    result=tarotarot.app_tarotarot(new_flag)
    if not new_flag:
        pic=get_CQimg_base(result["img"])
        side=(lambda x:"正位" if x=="font" else "逆位")(result["side"])
        if sendmsg(gid,"{0}\n【{1}】{2}({3})".format(pic,result["name"],result["CHI"],side),show_flag=False):
            time.sleep(1)
            sendmsg(gid,"【牌面科普】：\n{0}\n-------------------------------------------------\n【{3}抽到了牌的{1}】\n【{1}解析】:\n{2}".format(result["exp"],side,result["content"],name))
    else:
        pic=get_CQimg_base(result["img"])
        side=(lambda x:"正位" if x=="font" else "逆位")(result["side"])
        if sendmsg(gid,pic,show_flag=False):
            temp="\n【{1}】{2}({3})".format("123",result["name"],result["CHI"],side)
            time.sleep(1)
            sendmsg(gid,"{3}抽到了:{4}\n【{1}解析】:\n{2}".format("123",side,result["content"],name,temp))
    return

def get_menu(msg,para):
    gid=get_group(msg)
    content=menu.app_get_menu()
    sendmsg(gid,content)

def show_what_happened_today(msg,para):
    gid=get_group(msg)
    sendmsg(gid,today_what_happened())
    return
def send_soviet_joke(msg,para):
    gid=get_group(msg)
    joke=soviet_joke.set_soviet_joke()
    sendmsg(gid,joke)
    return
def be_ranran(msg,para):
    message=msg["message"]
    gid=get_group(msg)
    name = re.search("发病(.*)", message)
    name = name.group(1)
    judge=ranran.LONG_POSSIBLITY
    flag=random.randint(1,10)>judge
    if flag:
        result=ranran.set_short_ran(name)
    else:
        result=ranran.set_long_ran(name)
    sendmsg(gid,result)
    return

def set_nickname(msg):
    message=msg["message"]
    temp=re.search("[,，](全局|)把.*([0-9]+)?.*的(昵称|外号|称呼|爱称|称谓|叫)[为做作]([^.,。]+)",message)
    type=temp.group(1)
    target_uid=temp.group(2)
    target_name=temp.group(4)

    uid=get_user(msg)
    gid=get_group(msg)
    flag=get_group_cardname(gid,target_uid)
    if flag is None:
        sendmsg("他好像不在这个群里")
        return

    if "全局" not in type:
        mytype="private"
        key = generate_key("nickname", type=mytype, gid=gid, uid=uid, nickname=target_uid)
    else:
        mytype="global"
        key = generate_key("nickname", type=mytype, gid=gid, nickname=target_uid)
    if target_name=="None":
        del_redis(key)
        ##
        sendmsg("已经取消")

    set_redis(key,target_name)

    if mytype=="全局":
        sendmsg("{2}记住啦！以后大家都可以以{0}来称呼{1}喔".format(target_name,AT_USER(target_uid),config.QQ_NAME))
        return


def make_jielong(msg, para):
    gid = get_group(msg)
    if "endEvent" in msg:
        sendmsg(gid, "接龙已经过期啦！")
        if msg["VALUE"]["ai_flag"]:
            sendmsg(gid, "嘿嘿，我赢啦！")
        sendmsg(gid,jielong.get_statistics(gid,msg["VALUE"]))
        return

    message = msg["message"]
    uid = get_user(msg)
    key = generate_key("make_jielong", gid=gid)
    words = re.search("接龙(.*)", message)
    if "高级" in message:
        difficulty="2"
    else:
        difficulty="0"

    if difficulty is None:
        difficulty=jielong.jielong_DEFAULT_DIFFICULTY
    # else:
    #     difficulty = difficulty.group(1)
    if difficulty not in ["0","1","2"]:
        sendmsg(gid,"难度设置出错啦！")
        return

    value = get_redis(key)
    if "结束接龙" in message:
        if value is None:
            sendmsg(gid, "接龙还没开始啦！")
            return

        else:
            del_redis(key)
            sendmsg(gid,"收到！接龙已经结束啦！")
            value=json.loads(value)
            sendmsg(gid,jielong.get_statistics(gid,value))
            return


    if value is None:
        if "成语接龙" in message and config.QQ_NAME in message:
            # try:
            #     words = words.group(1)[:4:]
            # except:
            #     sendmsg(gid, "成语的格式都不对喔")
            #     return
            words=jielong.random_idiom()
            if "群内成语接龙" not in message:
                
                jielong.create_idiom_redis(gid, config.QQ_NAME, words, difficulty,ai_flag=True)
                sendmsg(gid, "竟敢来挑战我，哼哼！开始吧！我出的成语是【{0}】(格式：接龙XXXX)".format(words))
                sendmsg(gid, "（输入“结束接龙”可以提前结束）")
                return
            else:

                jielong.create_idiom_redis(gid,uid,words,difficulty)
                sendmsg(gid, "接龙开始！当前群内接龙是成语【{0}】(格式：接龙XXXX)".format(words))
                sendmsg(gid, "（输入“结束接龙”可以提前结束）")
                return
            # if flag:
            #     
            #     sendmsg(gid,"接龙开始啦！当前的成语是【{0}】".format(words))
            # else:
            #     sendmsg(gid, "【{0}】这个成语不存在啦！（我才不是不知道呢！）".format(words))
            #     return
        else:
            return True
    else:

        words = words.group(1)
        value=json.loads(value)
        old=value["idiom"]
        if "成语接龙" in message:
            sendmsg(gid, "接龙已经开始啦，当前成语是【{0}】(格式：接龙XXXX)".format(old))
            return
        difficulty=value["difficulty"]
        flag=jielong.check_jielong(old,words,difficulty)
        ai_flag=value["ai_flag"]
        print(ai_flag,flag)
        if flag:
            if words in value["history"]:
                sendmsg(gid,"【{0}】这个词已经用过啦！".format(words))
                return
            jielong.new_idiom_redis(key, value, uid, words)

            if ai_flag:
                words=jielong.find_next_idiom(words,difficulty)
                if words is None:
                    sendmsg(gid,"我...对不上...我...竟然输了？？？？aaaaaaaa")
                    del_redis(key)
                    sendmsg(gid, "接龙已经结束了！")
                    sendmsg(gid, jielong.get_statistics(gid, value))
                    sendmsg(gid,"输入“{0}，群内成语接龙可以进行群内对战！".format(config.QQ_NAME))
                    return
                else:
                    jielong.new_idiom_redis(key, value, config.QQ_NAME, words)
                    sendmsg(gid, "{0}接得不错！我接的成语是【{1}】".format(get_group_cardname(gid, uid), words))

            else:
                sendmsg(gid, "{0}接龙+1！当前的成语是【{1}】".format(get_group_cardname(gid,uid),words))
        else:
            sendmsg(gid,"{0}接得不对喔~".format(get_group_cardname(gid,uid)))
            return

            return True

def dream_rewrite(msg,para):
    gid=get_group(msg)
    if "endEvent" in msg:
        print(msg)
        sendmsg(gid, "续写已经过期啦！")
        return
    key=generate_key("dream_rewrite",gid=gid)

    message=msg["message"]

    words=re.search(r".*续写(.*)",message).group(1)
    val=get_redis(key)
    if "结束续写" in message:
        if val is None:
            sendmsg(gid, "续写还没开始啦！")
            return

        else:
            del_redis(key)
            sendmsg(gid,"收到！续写已经结束啦！")
            return

    if val is None:
        if "开始续写" not in message or config.QQ_NAME not in message:
            return True
        print("not key")

        last_content = "[{0}]".format(words)
        sendmsg(gid,"诶嘿~让我们开始创作吧！")
        mydata=json.dumps(dream.generate_mydata(words))

    else:
        print("has key")
        mydata=json.loads(val)
        last_content = mydata["content"]+"[{0}]".format(words)
        mydata["content"]+=words

        mydata=json.dumps(mydata)

    set_copy_redis(key,mydata,ex=dream.DREAM_EXPIRE_TIME)
    sendmsg(gid,"正在续写中....")
    result=dream.rewrite(key)
    if result is None:
        sendmsg(gid,"唔...续写失败了")
        return
    sendmsg(gid,"{0}【{1}】".format(last_content,dream.get_content(result)))
    return
@deco_working_block
def cancel_remind(msg):
    pass


def reminding(msg,para):
    REMINDING_COUNT=4
    REMINDING_REPLY=3
    print("reminding",msg)
    gid=get_group(msg)
    uid=get_user(msg)
    content=msg["VALUE"]["content"]
    mytime=msg["VALUE"]["time"]
    send_msg_A=""
    send_msg_B=""
    for i in range(REMINDING_REPLY):
        if i%2==0:
            send_msg_A+="{0}啦！".format(content)
            send_msg_B+="{0}！".format(content)
        else:
            send_msg_B += "{0}啦！".format(content)
            send_msg_A += "{0}！".format(content)

    if "endEvent" in msg:
        for i in range(REMINDING_COUNT):
            if i % 2 == 0:
                sendmsg_private(uid,send_msg_A)
                if gid is not None:
                    sendmsg(gid,AT_USER(uid)+send_msg_A)
            else:
                sendmsg_private(uid,send_msg_B)
                if gid is not None:
                    sendmsg(gid,AT_USER(uid)+send_msg_B)
            time.sleep(2)



def set_remind(msg,para):
    uid=get_user(msg)
    gid=get_group(msg)
    now=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if gid is not None:
        key=generate_key("reminding",timetag=now,gid=gid,uid=uid)
    else:
        key=generate_key("reminding",timetag=now,gid=gid)
    message=msg["message"]
    message = message.replace("{0}，".format(config.QQ_NAME),"")
    day_recognizer={"明天":"1day","明日":"1day","后天":"2day","后日":"2day"}
    check1=re.search("[提醒我|叫我]([0-9]*)(分钟|秒|小时|天|月|年)后(.*)",message)
    check2=re.search("([0-9]*)(分钟|秒|小时|天|月|年)后.*[提醒我|叫我](.*)",message)
    check3 = re.search("([0-9]*)[点|:|：]([0-9]+|一刻|二刻|两刻|三刻|半|).*[叫我|提醒我](.*)", message)
    check4 = re.search("[提醒我|叫我]([0-9]*)[点|:|：]([0-9]+|一刻|二刻|三刻|半|)(.*)", message)
    delta_quantity={"秒":"seconds","分钟":"minutes","小时":"hours","天":"days","月":"months","年":"years"}
    minute_quantity={"一刻":15,"两刻":30,"三刻":45,"半":30,"二刻":15,"":0}
    time_content=None

    if check1 or check2:
        check=return_not_None(check1,check2)
        quantity=check.group(1)
        time_unit=check.group(2)
        content=check.group(3)

        compile_time_unit=delta_quantity[time_unit]
        ex=eval("datetime.timedelta({0}={1})".format(compile_time_unit,quantity))
        value = {"content": content}
        value.update({"time": time_content})
        value = json.dumps(value)
        set_copy_redis(key, value, ex=ex)
        sendmsg_auto(msg, "{0}收到啦！到时候会提醒你的！".format(config.QQ_NAME))
        return
    elif check3 or check4:
        check = return_not_None(check3, check4)
        hour = check.group(1)
        inhour = check.group(2)
        content = check.group(3)
        try:
            hour = int(hour)
            print(hour,"hour")
            if hour<0 or hour>24:
                sendmsg(gid, "输入了错误的时间格式啦！")
                return
        except:
            sendmsg(gid, "输入了错误的时间格式啦！")
            return

        try:
            minute=int(inhour)

            if minute>=60 or minute<0:
                sendmsg(gid,"输入了错误的时间格式啦！")
                return
        except Exception as e:
            print(e)
            minute=minute_quantity[inhour]
        print(hour,"hour")




        abs_time=datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " {0}:{1}:00".format(hour,minute),
                                                      "%Y-%m-%d %H:%M:%S")
        now_hour=int(datetime.datetime.now().strftime("%H"))
        print(hour, "hour")
        if now_hour>hour:
            if hour+12>=24:
                abs_time = datetime.datetime.strptime(
                    datetime.datetime.now().strftime("%Y-%m-%d") + " {0}:{1}:00".format(hour, minute),
                    "%Y-%m-%d %H:%M:%S")+datetime.timedelta(days=1)
            else:
                hour=hour+12
                abs_time = datetime.datetime.strptime(
                    datetime.datetime.now().strftime("%Y-%m-%d") + " {0}:{1}:00".format(hour, minute),
                    "%Y-%m-%d %H:%M:%S")

        print(hour,"hour")
        now_time=datetime.datetime.now()
        time_content=abs_time.strftime("%Y-%m-%d %H:%M:%S")
        ex=abs_time-now_time

        value = {"content": content}
        value.update({"time": time_content})
        value = json.dumps(value)

        set_copy_redis(key,value,ex=ex)
        sendmsg_auto(msg,"{1}收到啦！会在{0}提醒你的！".format(abs_time.strftime("%m月%d日 %H点%M分",config.QQ_NAME)))
        return

    sendmsg(gid, "输入了错误的时间格式啦！!")
    return


def saytoAI(msg,para):
    gid=get_group(msg)
    message=msg["message"]
    if message[0]=="#":
        message = message.replace("#", "",1)
    message = re.sub("^{0}(,|，|)".format(config.QQ_NAME),"",message)
    message = message.replace(config.QQ_NAME, "菲菲")



    result = sayToRobot(message)
    result = result.replace("菲菲",config.QQ_NAME)
    result = result.replace("{br}", "\n")
    sendmsg(gid,result,check_flag=True)

def sayToMe(msg,para):
    banwords=get_banwords()

    uid=get_user(msg)

    gid=get_group(msg)
    name=get_group_cardname(gid,uid)
    message=msg["message"]
    # 违禁词检查
    for i in banwords:
        if i in message:
            sendmsg(gid,"【含违禁词，已屏蔽】")
            sendmsg_private(config.MONITOR,"出现违禁词，群:{0}。用户:{3}({1})。内容为：{2}".format(gid,uid,message,name))
            return
    if message[0]=="#":
        message = message.replace("#", "",1)
    print(message)
    message = re.sub("^{0}(,|，|)".format(config.QQ_NAME),"",message)

        # 强置处理
    if message[0:2]=="搜索":
        sendmsg(gid,"搜图请使用格式“{0}，搜图XXXX”".format(config.QQ_NAME))
        return
    if "你来自哪" in message:
        sendmsg(gid,"来自章鱼哥的一台弃用的老电脑")
        return
    if ("作者" in message or "主人" in message) and "谁" in message:
        sendmsg(gid,"{0}的作者是章鱼（扣扣2022355368），有什么意见或建议可以找他哟~只是想聊天也可以找他玩w诶嘿~".format(config.QQ_NAME))
        return
    if "开源" in message:
        sendmsg(gid,"{0}暂时没有开源的计划喔~因为很多功能还没有完成，很多地方还没打磨呢~不过最终肯定是会开源的说。【{0}的作者是章鱼（扣扣2022355368）】。".format(config.QQ_NAME))
        return
    if "你最喜欢谁" in message:
        sendmsg(gid,"当然是最喜欢{0}啦~".format(name))
        return
    if "念" in message and "诗" in message and "首" in message:
        sendmsg(gid,"啊啊啊啊啊，\n啊啊啊啊啊。\n啊啊啊啊啊，\n啊啊啊啊唉。\n")
        return
    if "花" in message and "送" in message:
        sendmsg(gid,get_CQimg_local("images/chat/flower.png"))
        return
    result=None
    message=message.strip()
    root=get_root()
    if message[0:2]=="搜图" or message[0:4]=="高清搜图":

        if message[0:2]=="搜图":
            search=message[2:]
            pic_url=baidu.app_search_pic(search)
            with open(root+"//logsearch//"+datetime.datetime.now().strftime("%Y年%m月%d日")+".txt","a+",encoding="utf-8") as f:
                f.write("{5}    群：【{0}】({1})用户《{2}》（{3}）图片：【{4}】{6}\n".format(get_group_name(gid),gid,get_group_cardname(gid,uid),\
                    uid,search,datetime.datetime.now().strftime("%H:%M:%S"),pic_url))
            
        else:
            search=message[4:]
            pic_url=baidu.app_search_pic(search,mode=6)
            with open(root+"//log//search//"+datetime.datetime.now().strftime("%Y年%m月%d日")+".txt","a+",encoding="utf-8") as f:
                f.write("{5}    群：【{0}】({1})用户《{2}》（{3}）图片：【{4}】{6}\n".format(get_group_name(gid),gid,get_group_cardname(gid,uid),\
                    uid,search,datetime.datetime.now().strftime("%H:%M:%S"),pic_url))
            

        if pic_url is None:
            sendmsg(gid,"哎呀，搜索图片失败啦...")
            return

        result=get_CQimg_url(pic_url)
        recent_count=2
        flag=sendmsg(gid, result,False)
        if not flag:
            print("图片发送失败，开始重发")
            while recent_count>0:
                recent_count-=1
                if sendmsg(gid, result,False):
                    print("图片重发成功")
                    return
                else:
                    print("图片发送失败，开始重发")
            sendmsg(gid,"哎呀，图片上传失败啦...")
        return
    elif message[0:1]!="你":
        with open(root+"//log//search//"+datetime.datetime.now().strftime("%Y年%m月%d日")+".txt","a+",encoding="utf-8") as f:
                f.write("{5}    群：【{0}】({1})用户《{2}》（{3}）搜索：【{4}】\n".format(get_group_name(gid),gid,get_group_cardname(gid,uid),\
                    uid,message,datetime.datetime.now().strftime("%H:%M:%S")))
        result=baidu.app_search(message)
        count=2
        while (result is None and count>0):
            result=baidu.app_search(message)
            count-=1

    if result is None:
        message = message.replace(config.QQ_NAME, "菲菲")
        result=sayToRobot(message)


    result=result.replace("菲菲",config.QQ_NAME)
    result = result.replace("{br}", "\n")
    sendmsg(gid,result)

def praise(msg,para):
    uid=get_user(msg)
    gid=get_group(msg)
    message=msg["message"]
    check = re.search(".*夸夸(.*)", message)
    name=check.group(1)

    if name=="我" or name=="":
        name=get_group_cardname(gid,uid)
    if name=="机器人" or name=="你":
        name="我自己"
    result=setpraise(name)
    sendmsg(gid,result)
    return


def d_words(msg,para):

    message=msg["message"]
    new_message=getfirst_words(message)

    if "JB" not in new_message and "CQ:face,id=13" not in message:
        return True
    uid=get_user(msg)
    gid=get_group(msg)
    name=get_group_cardname(gid,uid)

    count, mytime = update_d_words(uid)
    if mytime is None:
        mytime="没有记录"
    sendmsg(gid,"{3}天眼：{0}念了不该念的经！目前{0}已经念了{1}次经！上次念经时间是在:{2}".format(name,count,mytime,config.QQ_NAME))
    time.sleep(1)
    if count>=200:
        sendmsg(gid, "{0}提醒您，您念经超过了200次，罕见！已经举办！".format(config.QQ_NAME))
    sendmsg(gid,"{0}提醒您，不要念奇奇怪怪的经！哼".format(config.QQ_NAME))
    return
def timetest(para):
    while True:
        print(para["msg"])
        time.sleep(1)



@deco_threading
def morning_level(msg,*args,**kwargs):
    if "gid" in msg:
        gid=msg["gid"]
    else:
        print("error!!!<早起>")
        return
    level_list=show_morning_level(gid)
    count=1
    result="---今天早起的孩子有---\n"
    for i in level_list:
        name=get_group_cardname(gid,i[1])
        # name=i[1]
        if name is not None:
            result+="{0} {1} {2}\n".format(count,name,i[4].strftime("%H:%M"))
            count+=1

    result+="------------\n"
    sendmsg(gid,result)
    print(result)

def raw_morning_level(msg,para):
    gid=get_group(msg)
    level_list=show_morning_level(gid)
    count=1
    result="---今天本群早起的孩子有---\n"
    for i in level_list:
        name=get_group_cardname(gid,i[1])
        # name=i[1]
        if name is not None:
            result+="{0} {1} {2}\n".format(count,name,i[4].strftime("%H:%M"))
            count+=1

    result+="------------\n"
    if len(level_list)==0:
        result+="唔...好像没有记录呢\n"
    sendmsg(gid,result)
    print(result)
def d_words_level(msg,para):
    level_list=show_d_words_level()
    gid=get_group(msg)
    count=1
    result="---念经排名---\n"
    for i in level_list:
        name=get_group_cardname(gid,i[0])
        if name is not None:
            result+="{0} {1}({2}) 共{3}次\n".format(count,name,i[0],i[1])
            count+=1

    result+="------------\n"
    sendmsg(gid,result)
    time.sleep(1)
    sendmsg(gid,"平安轨迹提醒您：抵制念经邪气，共建和谐轨迹")
def short_reply(msg,para):
    uid=get_user(msg)
    message=msg["message"]
    result=para["msg"]
    result=result.replace("[SAME]",message)
    sendmsg(get_group(msg),result)
    flag =False
    # 未完成
    if "reloop" in para :
        flag=para["reloop"]

    return flag




def goodnight(msg,para):

    uid=get_user(msg)
    gid = get_group(msg)
    name=get_group_cardname(gid,uid)
    nowtime = datetime.datetime.now()
    now_hour=nowtime.hour
    one_day=datetime.timedelta(days=1)

    if 7>now_hour>=2:
        temp_pic=get_CQimg_local("images/night.jpg")
        sendmsg(gid, "唔唔...还没睡着吗？揉揉揉揉...虽然我很笨，但我会陪着你的！\n{0}".format(temp_pic))
        return


    if 12>now_hour>=7:
        sendmsg(gid, "已经是上午啦！还是，你是在陪我玩呢？那么，谢谢你啦！\n[CQ:image,file=8792fdbaa0b98c5f084ec3636a3eb815.image,url=https://gchat.qpic.cn/gchatpic_new/2022355368/809864840-2338393717-8792FDBAA0B98C5F084EC3636A3EB815/0?term=3,subType=1]")
        return
    elif 19>now_hour>=12:
        sendmsg(gid, "唔...一到下午我也容易放困呢，可以适当休息一下呢~不过,休息完后，还是要打起精神来喔！")
        return
    elif 21>now_hour>=19:
        sendmsg(gid, "唔...还有点早呢...要不再陪我玩会儿？~\n[CQ:image,file=8792fdbaa0b98c5f084ec3636a3eb815.image,url=https://gchat.qpic.cn/gchatpic_new/2022355368/809864840-2338393717-8792FDBAA0B98C5F084EC3636A3EB815/0?term=3,subType=1]")
        return
    if now_hour<12:
        temptime=nowtime-one_day
    else:
        temptime=nowtime

    nowday=temptime.strftime("%Y-%m-%d")
    res=saygoodnight(gid,uid,nowday,nowtime)
    if not res:
        sendmsg(gid,"{0}你怎么还没睡(σ｀д′)σ！亲爱的晚安喔~".format(name))
    else:
        pic= get_CQimg_erciyuan()
        sendmsg(gid,"晚安喔！{0}是本群第{1}个睡觉的好孩子~摸摸头~(,,´•ω•)ノ好梦~\n{2}".format(name,res,pic),show_flag=False)
        if 2>now_hour>=0:
            sendmsg(gid,"时间有点晚啦，还是要早点休息喔~(,,´•ω•)ノ".format(name))
        time.sleep(1)
        # sendmsg(gid,get_goodnight_words(name))




def morning(msg,para):

    time = datetime.datetime.now()
    noon_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 12:00:00",
                                           "%Y-%m-%d %H:%M:%S")
    late_morning_time=datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 6:00:00",
                                              "%Y-%m-%d %H:%M:%S")
    morning_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 5:00:00",
                                              "%Y-%m-%d %H:%M:%S")
    mid_night_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 3:00:00",
                                              "%Y-%m-%d %H:%M:%S")

    # zero_time = datetime.datetime.strptime(datetime.datetime.now().strftime("%Y-%m-%d") + " 0:00:00",
    #                                           "%Y-%m-%d %H:%M:%S")

    uid=get_user(msg)
    gid = get_group(msg)
    name=get_group_cardname(gid,uid)
    if time<mid_night_time:
        sendmsg(gid, "kora!你在熬夜对不对？对不对？快回去睡！(σ｀д′)σ！！")
        return

    if mid_night_time<=time<morning_time:
        sendmsg(gid, "你起的太早了吧kora!快回去睡！(σ｀д′)σ！！")
        return

    if time>noon_time:
        sendmsg(gid,"(σ｀д′)σ早上已经过啦！")
        return

    res=saymorning(gid,uid,time)
    if not res:
        sendmsg(gid, "忘了吗？{0}今天已经早起了喔~是可爱的孩子呢[CQ:image,file=8792fdbaa0b98c5f084ec3636a3eb815.image,url=https://gchat.qpic.cn/gchatpic_new/2022355368/809864840-2338393717-8792FDBAA0B98C5F084EC3636A3EB815/0?term=3,subType=1]".format(name))
    else:
        pic= get_CQimg_erciyuan()
        sendmsg(gid,"早上好！{0}是本群第{1}个起床的孩子~摸摸头~(,,´•ω•)ノ\n{2}".format(name,res,pic),show_flag=False)
        if time<late_morning_time:
            sendmsg(gid,"但时间还是有点早呢！还是要好好休息喔~摸摸头~(,,´•ω•)ノ\n{2}".format(name,res,pic),show_flag=False)
@deco_working_block
def mytest(msg,para):
    uid=get_user(msg)
    gid=get_group(msg)
    msg=str(msg)
    msg=msg.replace("[","【")
    msg=msg.replace("]","】")
    sendmsg(gid,msg)
    return
@deco_working
def ghs(msg,para):
    gid=get_group(msg)

    message=msg["message"]
    sendmsg(gid,"正在ghs中...")
    try:
        proxies = {"http": None, "https": None}
        req_url = "https://api.lolicon.app/setu/"

        r18_para=0
        if "-H" in message:
            r18_para=1
        res = requests.get(req_url,params={"r18":r18_para})
        setu_title = res.json()['data'][0]['title']
        setu_url = res.json()['data'][0]['url']
        setu_pid = res.json()['data'][0]['pid']
        setu_author = res.json()['data'][0]['author']

        setu_url=setu_url.replace("https","http")
        basedata=get_img_base(setu_url)
        basedata=str(basedata,encoding="UTF-8")
        local_img_url = "title:" + setu_title + "[CQ:image,file=base64://" + basedata + "]" + "pid:" + str(
            setu_pid) + " 画师:" + setu_author
        sendmsg(gid,local_img_url,show_flag=False)
    except Exception as e:
        print("出错:",e)
        sendmsg(gid,"访问出错啦！（装死）")
    return
def erciyuan(msg,para):
    gid=get_group(msg)
    acg_api=[api_dict("https://www.dmoe.cc/random.php?return=json","樱花api"),
             # api_dict("https://api.vvhan.com/api/acgimg?type=json","韩小韩api"),
             api_dict("https://api.ixiaowai.cn/api/api.php?return=json","小歪"),
             api_dict("https://api.ghser.com/random/api.php","一叶三秋")]
    random.shuffle(acg_api)
    for i in acg_api:
        req_url = i["url"]
        print("<图片爬取>访问api:",i["name"])
        try:
            res = requests.get(req_url)
        except:
            print("<图片爬取>访问api失败！")
            continue
        print("<图片爬取>api访问成功")


        if req_url.endswith(".php"):
            pic_url=res.url
        else:
            res_data = json.loads(res.content)
            for key in ["imgurl","acgurl"]:
                if key in res_data:
                    pic_url=res_data[key]
                    break
        # 下载图片
        try:
            basedata=str(get_img_base(pic_url),encoding="UTF-8")
            pic = "[CQ:image,file=base64://" + basedata + "]"
            sendmsg(gid,pic,show_flag=False)
            sendmsg(gid,"来自api:"+i["name"])
            return
        except Exception as e:
            print("图片发送出错:",e)
            continue
    sendmsg(gid, "唔...出错啦！章鱼的网络又出问题啦！")
    return
def drawgua(msg,para):
    result=""
    gid = get_group(msg)
    uid = get_user(msg)
    name = get_group_cardname(gid,uid)

    message=msg["message"]
    if "请" not in message and "please" not in message:
        sendmsg(gid, "请说请，哼！")
        return
    try:
        sendmsg(gid, "{0}正在计算中...".format(config.QQ_NAME))

        result=calculate_with_plum_flower()
        result="{1}为{0}算的卦：".format(name,config.QQ_NAME)+result
        time.sleep(3)
        sendmsg(gid,result)
    except Exception as e:
        print(e)
        sendmsg(gid,"唔...算错啦")
        return
    return

def show_cov(msg,para):
    gid=get_group(msg)
    result=get_yiqing()
    sendmsg(gid,result)
    return
def water_army(msg,para):
    message=msg["message"]
    gid=get_group(msg)
    dialog={"上单":6,"叔叔":6,"你所热爱的":6,"cherry":6,"陈睿":6,"厉害了我的国":5,"感恩":5,"越南":5,"搬起石头":5,"稳中向好":5,"润":5,"华为":3,"5G":2,"刻晴":1,"钟离":1,"可莉":1,"派蒙":1,"原神":1,"5g":2,"胸部":4,"妹子":4,"美女":4,"女拳":4,"女权":4}
    reply={6:"陈睿，柠檬什么时候酸啊？",5:"yygq不懂得感恩，50w已举办！",4:"郭楠收收味😅😅😅",2:"5G就是骗局！",3:"华为又贵又差，全靠吹",1:"原p差不多得了"}
    flag=False
    for i in dialog:
        if message.find(i)!=-1:
            flag=True
            sendmsg(gid,reply[dialog[i]])
    if not flag:
        return True

    return
def whether_or_not(msg,para):
    uid=get_user(msg)
    gid=get_group(msg)
    if not uid:
        return
    message=msg["message"]
    if "不知道" in message:
        message=re.match(r"不知道(.*)",message).group(1)
    result=re.search(r"([^，,。.\s]*(会不会|可不可以|是不是|对不对|行不行|能不能|好不好|用不用|可不可爱|该不该|喜不喜欢)[^，,。.\s]*)",message)
    if result is None:
        return True


    temp=result.group(1)
    judge=random.randint(0,1)
    # 嘿嘿
    special_list=["阿廖","莫斯科","红星","松子","文欣","无忧","章鱼","马洛","酱布"]
    spe_flag=False
    for i in special_list:
        if i in temp:
            spe_flag=True
            break
    if result.group(2)=="可不可爱" and spe_flag:
        judge=1

    # 作弊

    if message.count("wink")==1:
        judge=1

    elif message.count("wink")>1:
        judge=0
    else:
        pass


    if judge==1:
        temp=temp.replace(result.group(2),result.group(2)[2::])
    else:
        temp=temp.replace(result.group(2), result.group(2)[1::])


    if temp[0]=="你":
        temp=temp[1::]
    temp = temp.replace("我", "你")
    temp=temp.replace("?","！")
    temp = temp.replace("？", "！")
    temp = temp.replace(config.QQ_NAME,"")
    temp="{1}为{0}裁决——".format(get_group_cardname(gid,uid),config.QQ_NAME)+temp
    sendmsg(gid,temp,check_flag=True)
    print(message)