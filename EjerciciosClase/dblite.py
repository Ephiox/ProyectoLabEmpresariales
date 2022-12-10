import random
import sqlite3
import datetime

connection = sqlite3.connect('coachdata.sqlite')
cursor = connection.cursor()

cursor.execute("""SELECT * FROM SQLITE_MASTER where type='table';""")
res = cursor.fetchall()
table = []

# Creamos las tablas
for i in res:
    table.append(i[1])
if 'athletes' not in table:
    cursor.execute("""CREATE TABLE athletes(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            NAME TEXT NOT NULL,
            DOB DATE NOT NULL)""")
if 'competicion' not in table:
    cursor.execute("""CREATE TABLE competicion(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            ciudad TEXT NOT NULL,
            primer_puesto INTEGER,
            segundo_puesto INTEGER,
            tercer_puesto INTEGER,
            FOREIGN KEY(primer_puesto,segundo_puesto,tercer_puesto) REFERENCES atheletes)""")
if 'timing_data' not in table:
    cursor.execute("""CREATE TABLE timing_data(
            id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
            competicion_id INTEGER NOT NULL,
            athlete_id INTEGER NOT NULL,
            value TEXT  NOT NULL,
            FOREIGN KEY(competicion_id) REFERENCES competicion,
            FOREIGN KEY(athlete_id) REFERENCES atheletes)""")

connection.commit()

# Vamos a añadir los competidores (realmente solo tendriamos que hacerlo una vez, pero lo dejamos asi)
listNames = ['Ale', 'Carlos', 'Fran', 'Alvaro', 'Adri', 'Jorge', 'Jose', 'Pepe']
for name in listNames:
    new_dob = datetime.datetime.today().date()
    cursor.execute("""INSERT INTO athletes(name, dob)
                values (?, ?)""", (name, new_dob))
connection.commit()

# Imprimimos la tabla creada
cursor.execute("""SELECT * FROM athletes""")
res = cursor.fetchall()
print(res)

# Creamos las competiciones
listaCiudades = ['Malaga', 'Sevilla', 'Baeza', 'Madrid', 'Bilbao']
for ciudad in listaCiudades:
    cursor.execute("""INSERT INTO competicion(ciudad)
                values (?)""", (ciudad,))
connection.commit()

# Imprimimos las competiciones
cursor.execute("""SELECT * FROM competicion""")
res = cursor.fetchall()
print(res)

# Ahora vamos a crear los tiempos
dob = datetime.datetime.today().date()
cursor.execute("SELECT id from competicion")
competicion_id = cursor.fetchall()
for name in listNames:
    for id in competicion_id:
        cursor.execute("SELECT id from athletes WHERE name=? AND dob=?", (name, dob))
        the_current_id = cursor.fetchone()
        time = 10 * random.random() + 20
        cursor.execute("""INSERT INTO timing_data(athlete_id, value, competicion_id)
                    values (?, ?, ?)""", (the_current_id[0], str(time), id[0]))
    connection.commit()

# Imprimimos los tiempos
cursor.execute("""SELECT * FROM timing_data""")
res = cursor.fetchall()
for i in res:
    print(i)

# Ahora vamos a ordenar los competidores en los rankings
cursor.execute("SELECT id from competicion")
res = cursor.fetchall()
for i in res:
    cursor.execute("SELECT athlete_id from timing_data WHERE competicion_id=?", (i[0],))
    athleta = cursor.fetchall()
    cursor.execute("SELECT value from timing_data WHERE competicion_id=?", (i[0],))
    tiempo = cursor.fetchall()
    tiempo = [float(t[0]) for t in tiempo]
    tiempo, athleta = [list(t) for t in zip(*sorted(zip(tiempo, athleta)))]
    cursor.execute("""UPDATE competicion 
                    SET (primer_puesto,segundo_puesto,tercer_puesto) = (?, ?, ?)
                    WHERE id = ?""", (athleta[0][0], athleta[1][0], athleta[2][0], i[0]))

# Imprimimos las competiciones
cursor.execute("""SELECT * FROM competicion""")
res = cursor.fetchall()
for i in res:
    print(i)


# Creamos una funcion para comprobar el nombre de los ganadores de una competicion
def nombre_ganador(competicion_id):
    cursor.execute("SELECT primer_puesto from competicion where id=?", (competicion_id,))
    id_competidor = cursor.fetchall()
    cursor.execute("SELECT name from athletes where id=?", (id_competidor[0][0],))
    name = cursor.fetchall()[0]
    return name


# Vemos quien gano la competicion numero 1
print(nombre_ganador(1))

cursor.close()
connection.close()
