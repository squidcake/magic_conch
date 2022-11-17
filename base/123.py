import threading
import time
import functools
import schedule
def test():
    print("123")
schedule.every(1).second.do(test)

schedule.every(1).second.do(test)
def schedule_pending():
    while True:
        schedule.run_pending()
        time.sleep(0.01)
schedule_pending()