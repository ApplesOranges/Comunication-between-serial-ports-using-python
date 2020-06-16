
import codecs


def lectxt(ruta:str)->str:
    #lectura del archivo, pide la ruta y retorna un string con el contenido de este
    with codecs.open(ruta, encoding='utf-8') as f:
        texto = f.read()
        f.close()
        return texto

def divide(ruta:str)->list:
    """divide el archivo, cada parte es  100 caracteres
    retorna una lista donde cada elemento es una cadena de 100 caracteres"""
    #leemos el archivo
    lista=[];
    mensaje=lectxt(ruta)
    divisiones=len(mensaje)//100
    for x in range(1,divisiones+1):
        superior=x*100
        lista.append(mensaje[superior-100:superior])
    if (len(mensaje)%100)!=0:
        lista.append(mensaje[superior:])
    return lista

def formato(retorno:list)->list:
    """necesita una lista de entrada,retorna la misma lista con formato en caracteres
    """
    for indice,valor in enumerate(retorno):
        retorno[indice]="SOH"+"{0:x}".format(indice)+"STX"+valor+"ETX"
    return retorno

def sustitucionVErdadera(retorno:list)->list:
    """sustituye las banderas de entrada y salida a valores exadecimales,se deja BBC pues tendria que ser la suma de verificacion"""
    for indice,valor in enumerate(retorno):
        retorno[indice]=valor.replace("SOH",chr(1)).replace("ETX",chr(3)).replace("STX",chr(2))
    return retorno

def sustituiconFalsa(retorno:list)->list:
    """funcion que realiza el intercambio de SOH,ETX y STX por valores decimales"""
    for indice,valor in enumerate(retorno):
        retorno[indice]=valor.replace("SOH","01").replace("ETX","03").replace("STX","02")
    return retorno

def converidorhexadecimal(retorno:list)->list:
    for indice,valor in enumerate(retorno):
        retorno[indice]=asqui(valor)
    return retorno

def asqui(cadena:str)->str:
    new=""
    for x in range(0,len(cadena)):
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
    i=0
    while(i<len(strn)):
        line.append(strn[i])
        if(strn[i] == "e" and strn[i+1] == "t" and strn[i+2] == "x"):
            while (strn[i] != "\n"):
                i+=1
                line.append(strn[i])
            lines.append(line)
            line=[]
        i+=1
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
    while (i >= 0):
        s = int(s1[i]) + int(s2[i])
        if s == 2:  # 1+1
            if carry == 0:
                carry = 1
                result = "%s%s" % (result, '0')
            else:
                result = "%s%s" % (result, '1')
        elif s == 1:  # 1+0
            if carry == 1:
                result = "%s%s" % (result, '0')
            else:
                result = "%s%s" % (result, '1')
        else:  # 0+0
            if carry == 1:
                result = "%s%s" % (result, '1')
                carry = 0
            else:
                result = "%s%s" % (result, '0')

        i = i - 1;

    if carry > 0:
        result = "%s%s" % (result, '1')
    return result[::-1]

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
        if (len(byt) > 8):
            byt = byt[1:]
            byt = binAdd(byt, "1")
    hx = hex(int(bCompl(byt), 2))
    return hx
