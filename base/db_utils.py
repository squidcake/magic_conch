import datetime
from pathlib import Path
import magic_conch.config as config

import sqlite3

mypath = Path(__file__).resolve().parent.parent
def makesql():
    db = sqlite3.connect(str(mypath)+"/data/database/kiseki.db")
    return db
def commit_sql(db,sql):
    try:
        # 执行SQL语句
        cursor = db.cursor()
        cursor.execute(sql)
        # 提交修改
        db.commit()
    except Exception as e:
        print(e)
        db.rollback()
def show_morning_level(gid):
    db = makesql()
    cursor = db.cursor()
    day=datetime.datetime.now().strftime("%Y-%m-%d")
    sql = 'select * FROM morning where day="{0}" and gid="{1}" order by day desc'.format(day,gid)
    print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    return result


# 发生错误时回滚
def show_d_words_level():
    db = makesql()
    cursor = db.cursor()
    sql = 'select * FROM d_words order by count desc'
    cursor.execute(sql)
    result=cursor.fetchall()
    return result



def update_d_words(uid):
    db=makesql()
    cursor=db.cursor()
    sql='SELECT * FROM d_words where uid="{0}"'.format(uid)
    cursor.execute(sql)
    result=cursor.fetchone()
    if result==None:
        count=1
        lasttime=None
        mytime=datetime.datetime.now()
        sql = """INSERT INTO d_words
                 VALUES ({0}, {1}, "{2}")""".format(uid,count,mytime)
        commit_sql(db, sql)

    else:
        count=result[1]+1
        lasttime=result[2].strftime('%Y-%m-%d %H:%M:%S')
        mytime=datetime.datetime.now()
        sql='update d_words set count={0},last_time="{2}" where uid="{1}"'.format(count,uid,mytime)
        commit_sql(db,sql)

    return [count,lasttime]


def saygoodnight(gid,uid,nowday,mytime):
    flag=ischecked_goodnight(uid,nowday)
    if flag:
        return False
    else:
        db = makesql()
        sql = """INSERT INTO goodnight(uid,day,time,gid)
                 VALUES("{0}", "{1}","{2}","{3}")""".format(uid,nowday,mytime,gid)
        commit_sql(db, sql)

        return count_goodnight(gid,nowday)

def ischecked_goodnight(uid,nowday):
    db = makesql()
    cursor = db.cursor()
    sql='SELECT * FROM goodnight where uid="{0}" and day="{1}"'.format(uid,nowday)
    cursor.execute(sql)
    result=cursor.fetchall()
    if len(result)>0:
        return True
    else:
        return False


def count_goodnight(gid,day):
    db = makesql()
    cursor = db.cursor()
    sql='SELECT * FROM goodnight where gid="{0}" and day="{1}"'.format(gid,day)
    cursor.execute(sql)
    result=cursor.fetchall()
    return len(result)



def saymorning(gid,uid,mytime):
    day=mytime.strftime("%Y-%m-%d")
    flag=ischeckedmorning(gid,uid,day)
    if flag:
        return False
    else:
        db = makesql()
        sql = """INSERT INTO morning(uid,day,time,gid)
                 VALUES("{0}", "{1}","{2}","{3}")""".format(uid,day,mytime,gid)
        commit_sql(db, sql)

        return count_morning(gid,day)


def count_morning(gid,day):
    db = makesql()
    cursor = db.cursor()
    sql='SELECT * FROM morning where gid="{0}" and day="{1}"'.format(gid,day)
    cursor.execute(sql)
    result=cursor.fetchall()
    return len(result)
def ischeckedmorning(gid,uid,day):
    db = makesql()
    cursor = db.cursor()
    sql='SELECT * FROM morning where uid="{0}" and day="{1}" and gid="{2}"'.format(uid,day,gid)
    print(sql)
    cursor.execute(sql)
    result=cursor.fetchall()
    if len(result)>0:
        return True
    else:
        return False
if __name__ == '__main__':
    makesql()
    print(show_d_words_level())
