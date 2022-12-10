import sqlite3

conn = sqlite3.connect('log.sqlite')
cursor = conn.cursor()

_SQL = """insert into log
          (phrase, letters, ip, browser_string,results)
          values
          ('galaxia','aeiou','127.0.0.1','Chrome',"{'a','i'}")"""
cursor.execute(_SQL)
conn.commit()