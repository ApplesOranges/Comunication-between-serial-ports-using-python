# Comunication-between-serial-ports-using-python


# Procedimiento

 El desarrollo del proyecto consta de las siguientes partes

 principales:

 • Lectura y división de tramas

 • Obtención de la suma de verificación

 • Generación de tramas con error

 • Envío de tramas

 • Detección de errores

 • Envío de tramas con error para corregir

 • Corrección de tramas con error

 Lectura y división de tramas

 Para la lectura se creó la función divide que recibe la ruta de

 un archivo de texto y divide el contenido en 100 partes

 iguales.


 Obtención de la suma de verificación

 La siguiente implementación de checksum suma el valor

 binario de cada carácter y saca el complemento del

 resultado, luego este complemento se convierte a

 hexadecimal y ese valor se envía junto con la trama.


 Generación de tramas con error.

 A continuación podemos ver el siguiente código, dentro de

 una condicional, en la condicional se genera un numero

 entre el 0 y el 4, y si el número generado es 0 (20% de

 probabilidad de que suceda), se introduce un error al azar

 dentro de la trama, el carácter introducido es el signo de

 admiración (“!”)

 Envío de tramas

 El envío se realiza a través del puerto serial previamente

 simulado

port1 = serial.Serial('COM1')

port1.write(item.encode('utf-8'))

 se usa el Puerto de la misma forma que se utiliza cualquier

 descriptor de archivos.


 Detección de errores

 Para detectar los errores es necesario volver a realizar la

 suma de verificación y compararla con la suma recibida

 Envío de errores

 Las tramas que se rechazaron se reenvían por el puerto que

 a su vez debe iniciar el proceso de recepción

 Se recibe la información enviada al puerto 2 a través del

 puerto 1.

 Corrección de los errores

 El puerto uno ha recibido la lista de tramas con error,

 después de lo cual procede a reenviarlas correctamente.

for tr in errList1:
port1.write(tr.encode('utf-8'))
time.sleep(.1)
port1.write("EOM\r\n".encode('utf-8'))


 El Puerto 2 las recibe y se vuelven a verificar, en caso de que

 todas sean aceptadas se envía un mensaje.

while True:
strn = port2.readline()
strn = strn.decode("utf-8")
if ("EOM" in strn):
break
number = strn.split("STX", 1 )[ 0 ][ 3 :]
payload = strn.split("STX", 1 )[ 1 ]
chk1 = payload.split("ETX", 1 )[ 1 ]
payload = payload.split("ETX", 1 )[ 0 ]
i += 1
chk2 = st.checksum(payload)
if (int("0x" + chk1, 16 ) == int(chk2, 16 )):
print("TRAMA reenviada", number, "aceptada")
final[int(number, 16 )] = strn #aqui se corrigen para imprimir en el
archivo final
else:
print("TRAMA reenviada", number, "rechazada")
chkflag = 1
corrected.append(strn)
f.write(strn)

 Se envía mensaje al puerto 1

if(chkflag == 0 ):
res = "tramas corregidas satisfactoriamente\r\n"
else:
res = "error en tramas corregidas\r\n"
port2.write(res.encode('utf-8'))

 Algunos detalles adicionales:

 Para mantener un registro ordenado de los errores

 generados enviados y recibidos utilizamos los archivos de

 texto siguientes:

 Del lado que envía y luego recibe:

f = open("erroresgenerados.txt", "w")
f2 = open("erroresrecibidos.txt", "w")

 Del lado que recibe y luego envía:

f = open("erroresdetectados.txt","w")


 En estos archivos iremos escribiendo las tramas con error

 generadas, las detectadas y las reenviadas,

 respectivamente.

 Si los tres archivos son iguales nuestro código funciona

 correctamente.

 Además se muestra una interfaz sencilla cuyo propósito es

 mostrar dichos archivos.

show = f.read()
eg.textbox(title="Errores Detectados: ", msg=show)

f = open("erroresgenerados.txt", "r")
show = f.read()
eg.textbox(title="Errores Generados: ", msg=show)
f.close()
f = open("erroresrecibidos.txt", "r")
show = f.read()
eg.textbox(title="Errores Recibidos: ", msg=show)

 Aquí se muestra un ejemplo de errores generados,

 detectados y recibidos nuevamente en el otro puerto.

 Las capturas incluyen 8 tramas con error de muestra, sin

 embargo el programa muestra el total de ellas (20% de las

 100 tramas).


 Y un archivo recibido final, con cada trama corregida:

 Programa 1 (puerto1):

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
payload = item.split("STX", 1 )[ 1 ][:- 3 ]
hx = st.checksum(payload)#se obtiene el checksum en hexa
item += hx[ 2 :]+"\r\n"
if (rnd.randint( 0 , 3 )== 0 and errCount < 20 ):#si la condición se cumple se
genera el error
errList1.append(item)
errCount += 1
indx = rnd.randint( 8 , 100 )#elige la posición del error
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
while True:
strn = port1.readline().decode('utf-8')
errList2.append(strn)
if ("EOM" in strn):
break
f2.write(strn)
f2.close()
for tr in errList1:
port1.write(tr.encode('utf-8'))
time.sleep(.1)
port1.write("EOM\r\n".encode('utf-8'))
while True:
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


 Programa 2 (puerto2):

import serialtools as st
import serial
import easygui as eg

f = open("erroresdetectados.txt","w")
port2 = serial.Serial('COM2')
i = 0
corrected = []
final = []
while True:
strn = port2.readline()
strn = strn.decode("utf-8")
if("EOM" in strn):
break
final.append(strn)
payload = strn.split("STX", 1 )[ 1 ]
chk1 = payload.split("ETX", 1 )[ 1 ]
payload = payload.split("ETX", 1 )[ 0 ]
i += 1
chk2 = st.checksum(payload)
if(int("0x"+chk1, 16 ) == int(chk2, 16 )):
print("TRAMA", hex(i)[ 2 :], "aceptada")
else:
print("TRAMA", hex(i)[ 2 :], "rechazada")
f.write(strn)
#print(payload)

f.close()
f = open("erroresdetectados.txt","r")
send = f.readlines()
f.close()
for l in send:
port2.write(l.encode('utf-8'))
port2.write("EOM\r\n".encode('utf-8'))
f = open("tramasreenviadas.txt","w")
chkflag = 0
while True:
strn = port2.readline()
strn = strn.decode("utf-8")
if ("EOM" in strn):
break
number = strn.split("STX", 1 )[ 0 ][ 3 :]
payload = strn.split("STX", 1 )[ 1 ]
chk1 = payload.split("ETX", 1 )[ 1 ]
payload = payload.split("ETX", 1 )[ 0 ]
i += 1
chk2 = st.checksum(payload)
if (int("0x" + chk1, 16 ) == int(chk2, 16 )):
print("TRAMA reenviada", number, "aceptada")
final[int(number, 16 )] = strn #aqui se corrigen para imprimir en el
archivo final
else:


print("TRAMA reenviada", number, "rechazada")
chkflag = 1
corrected.append(strn)
f.write(strn)
f.close()
if(chkflag == 0 ):
res = "tramas corregidas satisfactoriamente\r\n"
else:
res = "error en tramas corregidas\r\n"
port2.write(res.encode('utf-8'))
port2.write("EOM\r\n".encode('utf-8'))
print(res)
f = open("archivofinal.txt", "w")
for item in final:
f.write(item)
f.close()
f = open("erroresdetectados.txt","r")
show = f.read()
eg.textbox(title="Errores Detectados: ", msg=show)
f = open("archivofinal.txt","r")
show = f.read()
eg.textbox(title="Archivo recibido y corregido: ", msg=show)

 Funciones creadas para uso en los programas anteriores:

import codecs

def lectxt(ruta:str)->str:
#lectura del archivo, pide la ruta y retorna un string con el contenido de
este
with codecs.open(ruta, encoding='utf-8') as f:
texto = f.read()
f.close()
return texto

def divide(ruta:str)->list:
_"""divide el archivo, cada parte es 100 caracteres
retorna una lista donde cada elemento es una cadena de 100 caracteres"""_
#leemos el archivo
lista=[];
mensaje=lectxt(ruta)
divisiones=len(mensaje)// 100
for x in range( 1 ,divisiones+ 1 ):
superior=x* 100
lista.append(mensaje[superior- 100 :superior])
if (len(mensaje)% 100 )!= 0 :
lista.append(mensaje[superior:])
return lista

def formato(retorno:list)->list:
_"""necesita una lista de entrada,retorna la misma lista con formato en
caracteres
"""_


for indice,valor in enumerate(retorno):
retorno[indice]="SOH"+"{0:x}".format(indice)+"STX"+valor+"ETX"
return retorno

def sustitucionVErdadera(retorno:list)->list:
_"""sustituye las banderas de entrada y salida a valores exadecimales,se deja
BBC pues tendria que ser la suma de verificacion"""_
for indice,valor in enumerate(retorno):

retorno[indice]=valor.replace("SOH",chr( 1 )).replace("ETX",chr( 3 )).replace("STX",
chr( 2 ))
return retorno

def sustituiconFalsa(retorno:list)->list:
_"""funcion que realiza el intercambio de SOH,ETX y STX por valores
decimales"""_
for indice,valor in enumerate(retorno):

retorno[indice]=valor.replace("SOH","01").replace("ETX","03").replace("STX","02"
)
return retorno

def converidorhexadecimal(retorno:list)->list:
for indice,valor in enumerate(retorno):
retorno[indice]=asqui(valor)
return retorno

def asqui(cadena:str)->str:
new=""
for x in range( 0 ,len(cadena)):
new+=str(ord(cadena[x]))
return new

def escritura(nombre:str,retorno:list)->None:
mensaje=""
f=open(nombre,"w")
for valor in retorno:
mensaje+=valor+"\n"
f.write(mensaje)
f.close()

def lineReader(path):
lines = []
line = []
sLines = []
j = 0
strn = lectxt(path)
i= 0
while(i<len(strn)):
line.append(strn[i])
if(strn[i] == "e" and strn[i+ 1 ] == "t" and strn[i+ 2 ] == "x"):
while (strn[i] != "\n"):
i+= 1
line.append(strn[i])
lines.append(line)


line=[]
i+= 1
for x in lines:
s = "".join(x)
sLines.append(s)
return sLines

def binAdd(s1, s2):
if not s1 or not s2:
return ''

maxlen = max(len(s1), len(s2))

s1 = s1.zfill(maxlen)
s2 = s2.zfill(maxlen)

result = ''
carry = 0

i = maxlen - 1
while (i >= 0 ):
s = int(s1[i]) + int(s2[i])
if s == 2 : # 1+
if carry == 0 :
carry = 1
result = "%s%s" % (result, '0')
else:
result = "%s%s" % (result, '1')
elif s == 1 : # 1+
if carry == 1 :
result = "%s%s" % (result, '0')
else:
result = "%s%s" % (result, '1')
else: # 0+
if carry == 1 :
result = "%s%s" % (result, '1')
carry = 0
else:
result = "%s%s" % (result, '0')

i = i - 1 ;

if carry > 0 :
result = "%s%s" % (result, '1')
return result[::- 1 ]

def bCompl(s):
st=""
for c in s:
if (c == "0"):
st += "1"
if (c == "1"):
st += "0"
return st


def checksum(strn:str):
byts = []
li = list(strn)
li = list(map(ord, li))
for x in li:
byts.append('{0:08b}'.format(x))
byt = "0"
for b in byts:
byt = binAdd(byt, b)
if (len(byt) > 8 ):
byt = byt[ 1 :]
byt = binAdd(byt, "1")
hx = hex(int(bCompl(byt), 2 ))
return hx

