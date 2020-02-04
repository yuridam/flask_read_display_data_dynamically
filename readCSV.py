import sqlite3
from sqlite3 import Error
import os
import pandas as pd

FILE_NAME = "task_data.csv"

try:
    ## open connection to database
    conn = sqlite3.connect('database.db')
    cur = conn.cursor()
    print("Database connected successfully")

    ### check if logs table exists, if not, create one
    cur.execute("SELECT count(name) FROM sqlite_master WHERE type='table' AND name='logs'")
    if cur.fetchone()[0] == 1:
        pass
    else:
        cur.execute("""CREATE TABLE IF NOT EXISTS logs (
                                        id integer PRIMARY KEY,
                                        method text NOT NULL,
                                        client text,
                                        datetime text
                                    )""")
        print("logs table doesn't exist, created one")

except Error as e:
    print(e)

### read file and insert the content into database
if os.path.isfile(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
    df.to_sql("data", conn, if_exists='replace', index=False)
    print("Data inserted into database successfully")
else:
    print(FILE_NAME + " not found.")

if conn:
    conn.commit()
    conn.close()
