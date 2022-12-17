import sqlite3
from datetime import datetime
import string
import time
import random
import hashlib
import numpy as np


def log_request_bd(sessionname: str, req: 'flask_request', res: str) -> None:
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO search_log (usuario, phrase, letters, ip, browser_string, results)
                VALUES (?, ?, ?, ?, ?, ?)""", (sessionname, req.form['phrase'], req.form['letters'],
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
    resultado = True
    cursor.execute("""SELECT name FROM users Where name=(?)""", (req.form['usuario'],))
    res = cursor.fetchall()
    if res == [] and req.form['usuario'] != '':
        cursor.execute("""INSERT INTO users (name, password, dob, count)
                       VALUES (?, ?, ?, ?)""",
                       (req.form['usuario'], hashlib.md5(req.form['password'].encode()).hexdigest(),
                        str(datetime.today()), 0))
        conn.commit()
    else:
        resultado = False
    return resultado


def login_bd(req: 'flask_request'):
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()

    cursor.execute("""SELECT password FROM users WHERE name=(?)""", (req.form['usuario'],))
    res = cursor.fetchall()
    token = ''
    if not res:
        token = 'Error'
    elif hashlib.md5(req.form['password'].encode()).hexdigest() == res[0][0]:
        token = token_generator(64)
        cursor.execute("""SELECT count FROM users WHERE name=(?)""", (req.form['usuario'],))
        count = cursor.fetchall()[0][0] + 1
        cursor.execute("""UPDATE users set temporalID = (?),count=(?) WHERE name= (?)""",
                       (token, count, req.form['usuario']))
        conn.commit()
    else:
        token = 'Error'
    return token


def check_token(name: str, token: str):
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()

    cursor.execute("""SELECT temporalID FROM users WHERE name=(?)""", (name,))
    res = cursor.fetchall()
    if name == 'Anonymous':
        return False
    return token == res[0][0]


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


def crearRanking(lista):
    ranking = {}
    for frase in lista:
        for palabra in frase[0].split():
            if palabra in ranking:
                ranking[palabra] = ranking[palabra] + 1
            else:
                ranking[palabra] = 1
    return ranking


def ordenarRanking(ranking):
    key = list(ranking.keys())
    values = list(ranking.values())
    while len(key) < 3:
        key.append('')
        values.append(0)
    sorted_values_index = np.argsort(values)
    sorted_values_index = sorted_values_index[::-1]
    sorted_ranking_keys = [key[i] for i in sorted_values_index]
    sorted_ranking_values = [values[i] for i in sorted_values_index]
    suma = sum(sorted_ranking_values)
    if suma != 0:
        sorted_ranking_per = [100 * values[i] / suma for i in sorted_values_index]
    else:
        sorted_ranking_per = [0 for i in sorted_values_index]
    return [sorted_ranking_keys, sorted_ranking_values, sorted_ranking_per]


def get_stats(username: str):
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()
    cursor.execute("""SELECT phrase FROM search_log""")
    res = cursor.fetchall()
    if res:
        rankingGeneral = crearRanking(res)
    else:
        rankingGeneral = {}
    rankingGeneral_sorted = ordenarRanking(rankingGeneral)


    cursor.execute("""SELECT phrase FROM search_log WHERE usuario =(?)""", (username,))
    res = cursor.fetchall()
    if res:
        rankingPropio = crearRanking(res)
    else:
        rankingPropio = {}
    rankingPropio_sorted = ordenarRanking(rankingPropio)

    return rankingGeneral_sorted, rankingPropio_sorted
