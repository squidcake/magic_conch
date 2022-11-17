import re
import config
from base.path_handler import *
from base.myschedule import settime
import view


TIME_LIST = [
             settime("day", 1, ["12:30"], view.morning_level, gid="742112686"),
             settime("day", 1, ["12:30"], view.morning_level, gid="148597045"),
             # settime("day",1,["07:30"],view.morning_sweet,uid="2929737037"),

             settime("day",1,["10:00","16:00","23:00"],view.show_cov,gid="148597045"),

             settime("day",1,["10:00","16:00","23:00"],view.show_cov,gid="742112686"),

             settime("day",1,["14:00"],view.show_what_happened_today,gid="742112686")]
LOOP=[]
PATH=[
    path(".*【name】(,|，|\s|)撤回",view.redraw_msg,5,post_type="message"),
    path("【name】(,|，|\s|)结束绘(画|图).*",view.end_aipainting,6,post_type="message"),
    path(".*【name】(,|，|\s|)(AI|ai)绘(画|图).*",view.app_aipainting,5,post_type="message"),
    path("【name】(,|，|)(AI|ai)2绘图.*",view.app_aipainting_2,5,post_type="message"),
    path("【name】(,|，|\s|).*添加.*",view.whatdoing_addone,5,post_type="message",message_type="group"),
    path("【name】(,|，|\s|).*删除.*",view.whatdoing_removeone,5,post_type="message",message_type="group"),
    path("【name】(,|，|\s|).*在干什么(呀|)",view.app_whatdoing,5,post_type="message",message_type="group"),
    path(".*",view.ban_user,5,post_type="message",ban=True,message_type="group"),
    path("【name】(,|，|\s|)抽签",view.app_chouqian,5,post_type="message",message_type="group"),
    path("【name】(,|，|\s|)投.*(色子|骰子).*",view.rolls,5,post_type="message",message_type="group"),
    path("广播:.*",view.broadcast,5,post_type="message",message_type="private"),
    path("【name】(,|，|\s|)抽人.*",view.pick_member,5,post_type="message",message_type="group"),
    path(".*苏联笑话",view.send_soviet_joke,5,post_type="message",message_type="group"),
    path(".*help",view.get_menu,5,post_type="message",message_type="group"),
    path("【name】.*(菜单|帮助|help|功能)",view.get_menu,5,post_type="message",message_type="group"),
    path(".*接龙.*",view.make_jielong,9,post_type="message",message_type="group"),
    path("【name】(,|，|\s|).?塔罗牌",view.get_tarotarot,7,post_type="message",message_type="group"),
    path(".*发病.*",view.be_ranran,5,post_type="message",message_type="group"),
    path("【name】.*历史上的今天.*",view.show_what_happened_today,5,post_type="message",message_type="group"),
    path('.*123.*', view.mytest, 5,post_type="message",message_type="group"),
    path('(早|早安)', view.morning, 5,post_type="message",message_type="group",_msg="hello"),
    path('.*(会|会不会|可不可以|是不是|对不对|行不行|能不能|好不好|用不用|可不可爱|该不该|喜不喜欢).*',view.whether_or_not,message_type="group"),
    path('【name】.*',view.short_reply,0,post_type="message",message_type="group",_msg="我不知道呢，但我知道你一定是个好孩子啦~摸摸~"),
    path('【name】.*疫情.*', view.show_cov, 5,post_type="message",message_type="group"),
    path('哈*', view.short_reply, 5,post_type="message",message_type="group",_msg="[SAME]"),
    path('^(.)\\1{2,}$', view.short_reply, 5,post_type="message",message_type="group",_msg="[SAME]"),
    path('【name】.*算.*卦.*', view.drawgua, 5,post_type="message",message_type="group"),
    path('【name】.*念经排名.*', view.d_words_level, 5,post_type="message",message_type="group"),
    path('.*(夸夸我|求夸夸).*',view.praise,6,post_type="message",message_type="group"),
    path('【name】(,|，|\s|)夸夸.*',view.praise,6,post_type="message",message_type="group"),
    path('^#.*$',view.saytoAI,4,post_type="message",message_type="group"),
    path('【name】.*',view.sayToMe,2,post_type="message",message_type="group"),
    path(".*续写.*",view.dream_rewrite,5,post_type="message",message_type="group"),
    path(".*来点二次元",view.erciyuan,5,post_type="message",message_type="group"),
    path("晚安",view.goodnight,5,post_type="message",message_type="group"),
    path("【name】，.*提醒我.*",view.set_remind,4,post_type="message",message_type="group"),
    path("【name】，.*取消提醒.*",view.cancel_remind,1,post_type="message",message_type="group"),
    path("【name】.*早起排名",view.raw_morning_level,5,post_type="message",message_type="group"),
    # path('.*(寄吧|鸡巴|JB|叽霸|急吧|奇葩|jb|Jb|jB|\[CQ:face,id=13\]|呲牙笑).*', view.d_words, 5,post_type="message",message_type="group",group_id="952148924"),
    path('.*', view.d_words, 1, post_type="message",group_id=952148924,user_id=306168645,
         message_type="group"),
    path('(ghs|ghs -H)', view.ghs, 5, post_type="message",
         message_type="group"),
    path('.*', view.water_army, 5,post_type="message",message_type="group",group_id=952148924),
    path('.*反弹.*', view.short_reply, 7,post_type="message",message_type="group",_msg="[SAME]无效",_reloop=True)
]



