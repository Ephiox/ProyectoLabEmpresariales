import sqlite3

conn = sqlite3.connect('bd.sqlite')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE search_log (
                id INTEGER auto_increment primary key unique not null,
                ts timestamp default current_timestamp,
                phrase varchar(128) not null,
                letters varchar(32) not null,
                ip varchar(16) not null,
                browser_string varchar(256) not null,
                results varchar(64) not null );""")

cursor.execute("""CREATE TABLE usuario (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name TEXT NOT NULL,
                dob DATE NOT NULL )""")
conn.commit()
