import sqlite3
import pandas as pd

df_adress = pd.read_csv('/home/grigory/Local/Work/Telegram_mts/Telegram_mts/adress.csv')

# Обработка первоначального файла
#df_adress = df_adress.drop(['Бренд ОП', 'Формат салона', 'Юр.лицо', 'Легенда для проверки', 'Предмет для консультации', 'Нас.пункт признак'], axis = 1)
df_adress = df_adress.rename(columns={"Код ОП": "unique_id", "Бренд ОП": "brend", "Область":"region", "Населённый пункт название": "city", "Адрес Офиса продаж":"adress", "GPS координаты. широта":"latitude", "GPS координаты. долгота":"longitude", "Режим работы":"work_time", "Тип строения":"building", "Дата закрытия точки":"close_date", "Дата открытия точки":"open_date", "ТП":"done", "Оплата":"payment"})
df_adress['done'].fillna(0, inplace=True)
df_adress_done = df_adress.loc[df_adress['done'] != 0]
df_adress_done['done'] = 1
df_adress_not_done = df_adress.loc[df_adress['done'] == 0]
df_adress = pd.concat([df_adress_done, df_adress_not_done], ignore_index=True)
#Подключаемся к базе данных mts_adress
conn = sqlite3.connect('mts_adress.db')
c = conn.cursor()

#Создаем табличку с адресами
c.execute(
    """
    CREATE TABLE mts_newone (
       unique_id INTEGER,
       brend TEXT,
       region TEXT, 
       city TEXT,
       adress TEXT,
       latitude REAL, 
       longitude REAL,
       work_time TEXT,
       building TEXT,
       close_date TEXT,
       open_date TEXT,
       assigned INTEGER,
       payment INTEGER,
       done INTEGER,
       PRIMARY KEY(unique_id)
        )
   """
)

#Передаем в таблицу данные из экселевского файла
df_adress.to_sql('mts_newone', conn, if_exists='append', index=False)

conn.commit()

conn.close()