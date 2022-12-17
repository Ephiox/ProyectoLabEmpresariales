import sqlite3
from datetime import datetime
import string
import time
import random


def check_bd():
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()

    cursor.execute("""SELECT * FROM users""")
    res = cursor.fetchall()
    return res


def log_request_bd(req: 'flask_request', res: str) -> None:
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO search_log (phrase, letters, ip, browser_string, results)
                VALUES (?, ?, ?, ?, ?)""", (req.form['phrase'], req.form['letters'],
                                            req.remote_addr, str(req.user_agent),
                                            res))
    conn.commit()


def readlog_bd():
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM search_log""")
    res = cursor.fetchall()
    return res


def register_bd(req: 'flask_request'):
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (name, password, dob)
                VALUES (?, ?, ?)""", (req.form['usuario'], req.form['password'], str(datetime.today())))
    conn.commit()


def login_bd(req: 'flask_request'):
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()

    cursor.execute("""SELECT password FROM users WHERE name=(?)""", (req.form['usuario'],))
    res = cursor.fetchall()
    token = ''
    if not res:
        token = 'Error'
    elif res[0][0] == req.form['password']:
        token = token_generator(64)
        cursor.execute("""UPDATE users set temporalID = (?) WHERE name= (?)""", (token, req.form['usuario']))
        conn.commit()
    return token


def token_generator(longitud):
    alphabet = list(string.ascii_lowercase) + list(string.ascii_uppercase)
    specials = [',', '.', '*', '?', '%', '$', '!']
    numbers = list(range(0, 100))

    # Se ha sumado varias veces el alfabeto y los caracteres especiales
    # para aumentar la probabilidad de estos
    alphabet = alphabet + alphabet + specials + specials + specials + numbers

    semilla = round(time.time())
    random.seed(semilla)

    password = []
    for i in range(0, longitud):
        index = random.randint(0, len(alphabet) - 1)
        password.append(str(alphabet[index]))
    password = ''.join(password)
    return password
