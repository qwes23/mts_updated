import sqlite3
import json
import pandas as pd

# Получаем информацию по unique_id
def get_info(latitude1, latitude2, longitude1, longitude2):
    conn = sqlite3.connect('mts_adress.db')
    c = conn.cursor()
    c.execute("SELECT * FROM mts_adress WHERE latitude BETWEEN (?) AND (?) AND longitude BETWEEN (?) AND (?)", (latitude1, latitude2, longitude1, longitude2))
    items = c.fetchall()
    adress_dict = {}
    for item in items:
         id = item[0]
         adress = item[4]
         adress_dict[id] = adress
         
         
    print("Command executed succesfully!")
    conn.commit()
    conn.close()
    return adress_dict
