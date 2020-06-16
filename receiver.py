import serialtools as st
import serial
import easygui as eg

f = open("erroresdetectados.txt","w")
port2 = serial.Serial('COM2')
i = 0
corrected = []
final = []
while True:#recepcion de tramas
    strn = port2.readline()
    strn = strn.decode("utf-8")
    if("EOM" in strn):
        break
    final.append(strn)
    payload = strn.split("STX", 1)[1]
    chk1 = payload.split("ETX", 1)[1]
    payload = payload.split("ETX", 1)[0]
    i += 1
    chk2 = st.checksum(payload)
    if(int("0x"+chk1, 16) == int(chk2, 16)):
        print("TRAMA", hex(i)[2:], "aceptada")
    else:
        print("TRAMA", hex(i)[2:], "rechazada")
        f.write(strn)
    #print(payload)

f.close()
f = open("erroresdetectados.txt","r")
send = f.readlines()
f.close()
for l in send:#envia la lista de errores
    port2.write(l.encode('utf-8'))
port2.write("EOM\r\n".encode('utf-8'))
chkflag = 0
while True:#recibe correcciones de dichos ers
    strn = port2.readline()
    strn = strn.decode("utf-8")
    if ("EOM" in strn):
        break
    number = strn.split("STX", 1)[0][3:]
    payload = strn.split("STX", 1)[1]
    chk1 = payload.split("ETX", 1)[1]
    payload = payload.split("ETX", 1)[0]
    i += 1
    chk2 = st.checksum(payload)
    if (int("0x" + chk1, 16) == int(chk2, 16)):
        print("TRAMA reenviada", number, "aceptada")
        final[int(number, 16)] = strn #aqui se corrigen para imprimir en el archivo final
        print("corregida:", strn)
    else:
        print("TRAMA reenviada", number, "rechazada")
        chkflag = 1
if(chkflag == 0):
    res = "tramas corregidas satisfactoriamente\r\n"
else:
    res = "error en tramas corregidas\r\n"
port2.write(res.encode('utf-8'))
port2.write("EOM\r\n".encode('utf-8'))
print(res)
f = open("archivofinal.txt", "w")
for item in final:#envia confirmacion
    f.write(item)
f.close()
f = open("erroresdetectados.txt","r")
show = f.read()
eg.textbox(title="Errores Detectados: ", msg=show)
f.close()
f = open("archivofinal.txt","r")
show = f.read()
eg.textbox(title="Archivo recibido y corregido: ", msg=show)
f.close()