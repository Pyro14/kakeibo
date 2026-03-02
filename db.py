import sqlite3
import pandas as pd

db_path = "/home/pyro/Documents/code/repos/kakeibo/kakeibo.db"

def create_table(db_path, table_name, overwrite=False):
    with sqlite3.connect(db_path) as con:
        cur= con.cursor()

        if overwrite:
            cur.execute(f"DROP TABLE IF EXISTS {table_name}")

        query  = f""" 
        CREATE TABLE IF NOT EXISTS {table_name}(
            id INTEGER PRIMARY KEY,
            description TEXT,
            amount FLOAT NOT NULL,
            type TEXT,
            timestamp TEXT
        )"""

        cur.execute(query)

def insert_record(db_path, table_name, description, amount , type_, timestamp):
    with sqlite3.connect(db_path) as con:
        con.execute(
            f"INSERT INTO {table_name} (description, amount, type, timestamp) VALUES (?, ?, ?, ?)",
            (description, amount,type_, timestamp)
        )

def select_from_table(db_path,table_name):
    with sqlite3.connect(db_path) as con:
        res = con.execute(f"SELECT * FROM {table_name}")
        data= res.fetchall()
        columns = [c[0] for c in res.description]
        return pd.DataFrame(data,columns=columns)

if __name__ == "__main__":
    create_table(db_path, "kakeibo")
    
