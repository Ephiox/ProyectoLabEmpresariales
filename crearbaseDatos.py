import sqlite3

conn = sqlite3.connect('bd.sqlite')
cursor = conn.cursor()

cursor.execute("""CREATE TABLE search_log (
                id INTEGER primary key AUTOINCREMENT unique not null,
                ts timestamp default current_timestamp,
                usuario varchar(128),
                phrase varchar(128) not null,
                letters varchar(32) not null,
                ip varchar(16) not null,
                browser_string varchar(256) not null,
                results varchar(64) not null,
                FOREIGN KEY (usuario) REFERENCES users);""")

cursor.execute("""CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
                name TEXT UNIQUE NOT NULL,
                password varchar(16) not null,
                dob DATE NOT NULL,
                count INTEGER NOT NULL,
                temporalID varchar(64) UNIQUE)""")
conn.commit()
conn.close()
