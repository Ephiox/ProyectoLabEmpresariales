import sqlite3

conn = sqlite3.connect('bd.sqlite')
cursor = conn.cursor()

cursor.execute("""SELECT * FROM search_log""")
res = cursor.fetchall()
print(res)
