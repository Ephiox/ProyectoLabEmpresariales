import sqlite3

conn = sqlite3.connect('bd.sqlite')
cursor = conn.cursor()

cursor.execute("""INSERT INTO search_log (name, dob)
            VALUES (?, ?)""", (new_name, new_dob))


