

log = open("log",'a')
logR = open("log")
print("Esto es una prueba",file=log)
print("Espero que no haya problemas",file=log)

for task in logR:
    print(task,end='')
log.close()
logR.close()