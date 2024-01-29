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