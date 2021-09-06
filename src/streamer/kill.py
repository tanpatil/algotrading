"""
Script invoked upon cronjob to kill all python processess.
"""
import os
import datetime
import time
from pytz import timezone
time.sleep(50)
strtime = datetime.now(timezone("UTC")).astimezone(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
os.system(f'cd realtime && git add . && git commit -m "{strtime}" && git push')
os.system('pkill -9 python3')
