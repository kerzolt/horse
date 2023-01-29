import sqlite3
from sqlite3 import Error
from src.main.python.common import config

def create_connection():
    conn = None
    try:
        conn = sqlite3.connect(config["COMMON"]["DATASOURCE_URL"], check_same_thread=False)
    except Error as e:
        print(e)

    return conn