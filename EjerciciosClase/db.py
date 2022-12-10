import mysql.connector

dbconfig = { 'host' : '127.0.0.1',
             'user' : 'root',
             'password': 'ass150299',
             'database': 'search_log',}

conn = mysql.connector.connect(**dbconfig)

cursor = conn.cursor()

_SQL = """select * from log"""
cursor.execute(_SQL)
res = cursor.fetchall()
#print(res)

#for row in res:
#    print(row)

#print(res[0][1].day)

_SQL = """insert into log
          (phrase, letters, ip, browser_string,results)
          values
          ('galaxia','aeiou','127.0.0.1','Chrome',"{'a','i'}")"""
cursor.execute(_SQL)
conn.commit()

_SQL = """select * from log"""
cursor.execute(_SQL)
res = cursor.fetchall()
for row in res:
    print(row)

cursor.close()
conn.close()
