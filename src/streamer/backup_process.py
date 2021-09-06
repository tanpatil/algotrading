"""
Backs up all the webstreamed data by resampling and sending it over to another repository
"""


REALTIME = "./realtime/prices/"
RESAMPLED = "./nse-data/realtime_data/"
PICKLE_FILE = "data.pkl"

# IMPORTS
import pandas as pd
import os
import pickle
import datetime
from pytz import timezone

# check if the repository exists, and if it does not, clone it down.
if not os.path.isdir(RESAMPLED):
    os.system('git clone git@github.com:sumukshashidhar/nse-data.git')
if not os.path.isdir(REALTIME):
    os.system('git clone git@github.com:sumukshashidhar/realtime.git')

# update both repositories first
os.system(f'cd {REALTIME} && git pull')
os.system(f'cd {RESAMPLED} && git pull')
# load the list of actual names instrument tokens

with open(PICKLE_FILE, 'rb+') as f:
    lookup = pickle.load(f)

# itearte through the files in the collection directory

for filename in os.listdir(REALTIME):
    if filename.endswith('.csv'):
        try:
            df = pd.DataFrame(pd.read_csv(os.path.join(REALTIME, filename), header=None, index_col=0, parse_dates=True))[1].resample('1min').ohlc().dropna().drop_duplicates(subset=['open', 'high', 'low', 'close'], keep='last')
            writefile = os.path.join(RESAMPLED, lookup[int(filename[:-4])]) + '.csv'
            if not os.path.isfile(writefile):
                with open(writefile, 'w+') as f:
                    f.write('')
            df.to_csv(writefile, header=False, mode='a')
        except Exception as e:
            print(e)
            print(f'{filename}. Error is {e}. Real file is {writefile}')

# once we're done with this process, we have to go to the directory itself and back it all up
strtime = datetime.now(timezone("UTC")).astimezone(timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
os.system(f'cd nse-data/ && git add . && git commit -m "daily data: {strtime}" && git push')
exit()