# -*- coding: utf-8 -*-
import sqlite3
import time
from datetime import datetime


def search4letters(word, letters='aeiou'):
    """ Funcion que busca las letras en una palabra y las imprime"""
    return set(word).intersection(letters)


help(search4letters)
search4letters('Hola me llamo ale')


def log_request(req: 'flask_request', res: str) -> None:
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO search_log (phrase, letters, ip, browser_string, results)
                VALUES (?, ?, ?, ?, ?)""", (req.form['phrase'], req.form['letters'],
                                            req.remote_addr, str(req.user_agent),
                                            res))
    conn.commit()

    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent,
              str(datetime.today()),
              res, file=log, sep='|')


def readlog_db():
    conn = sqlite3.connect('bd.sqlite')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM search_log""")
    res = cursor.fetchall()
    return res
