import schedule
import time
from quickstart import main

import sqlite3 as sq
import pandas as pd

def updating_closed():
    global base, cur
    base = sq.connect('mts_adress.db')
    cur = base.cursor()
    data = pd.read_csv('/home/grigory/Local/Work/Telegram_mts/Telegram_mts/now_closed.csv')
    #data = data.loc[data['date_close'] != '']
    for i in range(len(data)):
        unique_id = int(data['unique_id'][i])
        close_date = data['date_close'][i]
        open_date = data['date_open'][i]
        oplata = data['oplata'][i]
        cur.execute("UPDATE mts_adress SET close_date = (?), open_date = (?), oplata = (?) WHERE unique_id = (?)", (close_date, open_date, oplata, unique_id,))
    base.commit()
    print('yes')
    
def getting_table():
    main()
    updating_closed()
    print("I'm working...")

getting_table()

#schedule.every(30).seconds.do(getting_table)

#schedule.every().day.at("12:00").do(getting_table)

while True:
    schedule.run_pending()
    time.sleep(1)