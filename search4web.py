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
    with open('vsearch.log', 'a') as log:
        print(req.form, req.remote_addr, req.user_agent,
              str(datetime.today()),
              res, file=log, sep='|')