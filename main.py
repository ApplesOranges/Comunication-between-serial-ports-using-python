import serialtools as st
import serial
import time
import random as rnd
import easygui as eg

lst = st.divide("kafka.txt")
st.formato(lst)
port1 = serial.Serial('COM1')
f = open("erroresgenerados.txt", "w")
f2 = open("erroresrecibidos.txt", "w")
errCount = 0
errList1 = []
errList2 = []
for item in lst:
    payload = item.split("STX", 1)[1][:-3]
    hx = st.checksum(payload)#se obtiene el checksum en hexa
    item += hx[2:]+"\r\n"
    if (rnd.randint(0, 3)== 0 and errCount < 20):#si la condición se cumple se genera el error
        errList1.append(item)
        errCount += 1
        indx = rnd.randint(8, 100)#elige la posición del error
        lst = list(item)
        lst[indx] = '!'#hace el reemplazo
        item = ''.join(lst)
        print("trama con error: ", item)
        f.write(item)
    port1.write(item.encode('utf-8'))#se envia la trama
    time.sleep(.1)
port1.write("EOM\r\n".encode('utf-8'))
f.close()
port1.close()
port1 = serial.Serial('COM1')
while True:#se recibe la lista de errores
    strn = port1.readline().decode('utf-8')
    errList2.append(strn)
    if ("EOM" in strn):
        break
    f2.write(strn)
f2.close()
print("errores reportados:")
for tr in errList2:
    print(tr)
for tr in errList1:#se envian correcciones
    port1.write(tr.encode('utf-8'))
    time.sleep(.1)
port1.write("EOM\r\n".encode('utf-8'))
while True:#se recibe confirmación
    strn = port1.readline().decode('utf-8')
    if ("EOM" in strn):
        break
    print(strn)
f = open("erroresgenerados.txt", "r")
show = f.read()
eg.textbox(title="Errores Generados: ", msg=show)
f.close()
f = open("erroresrecibidos.txt", "r")
show = f.read()
eg.textbox(title="Errores Recibidos: ", msg=show)
f.close()