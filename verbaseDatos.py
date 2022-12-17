import sqlite3


def check_log():
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM search_log""")
    res = cursor.fetchall()
    for r in res:
        print(r)
    conn.close()


def check_users():
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM users""")
    res = cursor.fetchall()
    for r in res:
        print(r)
    conn.close()


check_log()
check_users()
