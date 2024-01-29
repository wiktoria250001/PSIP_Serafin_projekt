import psycopg2 as ps
import requests as rq
from tkinter import *
from tkintermapview import TkinterMapView

db_params=ps.connect(
    database='postgres',
    user='postgres',
    password='wiki3476',
    host='localhost',
    port=5433
)
cursor=db_params.cursor()

create_jednostki_policji='''
    CREATE TABLE IF NOT EXISTS jednostki_policji (
    id INT PRIMARY KEY,
    nazwa TEXT(50),
    lokalizacja TEXT(50)
    );
'''
cursor.execute(create_jednostki_policji)
db_params.commit()

create_policjanci='''
    CREATE TABLE IF NOT EXISTS policjanci (
    id INT PRIMARY KEY,
    imie TEXT(50),
    nazwisko TEXT(50),
    miejscowosc TEXT(50),
    placowka TEXT(50)
    );
'''
cursor.execute(create_policjanci)
db_params.commit()

create_incydenty='''
    CREATE TABLE IF NOT EXISTS incydenty (
    id INT PRIMARY KEY,
    lokalizacja TEXT(50),
    typ TEXT(50),
    jednostka_policji TEXT(50)
    );
'''
cursor.execute(create_incydenty)
db_params.commit()