import threading
import time
import functools
import schedule

def schedule_threading():
    threading.Thread(target=schedule_pending).start()
def schedule_pending():
    while True:
        schedule.run_pending()
        time.sleep(0.01)

def deco_threading(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        threading.Thread(target=func, args=args, kwargs=kwargs).start()
        return
    return wrapper



def settime(cycle, cycle_para, at_list, func, **kwargs):
    msg={}
    para={}
    for i in kwargs:
        if i[0]=="_":
            para.update({i[1::]:kwargs[i]})
        else:
            msg.update({i:kwargs[i]})
    if cycle=="day":
        if at_list is None:
            schedule.every(cycle_para).day.do(func, msg, para)
        else:
            for at in at_list:
                schedule.every(cycle_para).day.at(at).do(func,msg,para)
    elif cycle=="hour":
        if at_list is None:
            schedule.every(cycle_para).hour.do(func, msg, para)
        else:
            for at in at_list:
                schedule.every(cycle_para).hour.at(at).do(func, msg,para)
    elif cycle=="monday":
        if at_list is None:
            schedule.every(cycle_para).monday.do(func, msg, para)
        else:
            for at in at_list:
                schedule.every(cycle_para).monday.at(at).do(func,msg,para)
    else:
        print("error!settime")
        return
