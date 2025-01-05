import machine
import pyb
from machine import I2C, Pin, SPI
from ST77352 import TFT
from seriffont import seriffont
from time import sleep_ms
import os
import shell_commands as sc
import uasyncio

spi = SPI(1, baudrate=20000000)
tft=TFT(spi,Pin('PG9'),Pin('PE5'),Pin('PG7'))
tft.initr()
tft.rotation(0)

name_session= "@GIGA1:"
punto = 0
texto = ""
modo = 0

async def tft_display(texto):
    global punto, modo
    if punto:
        texto = str(texto) + "|"
        punto = 0
    else:
        texto = str(texto)
        punto = 1
    tft.fill(tft.WHITE)
    tft.text((5, 30), name_session,tft.BLACK, seriffont, 2, nowrap=True)
    tft.text((15, 80), texto,tft.BLACK, seriffont, 2, nowrap=True)

#Keyboard right
Penter = Pin('PJ12', Pin.IN, Pin.PULL_UP)
Pmode = Pin('PG13', Pin.IN, Pin.PULL_UP)
Pspace = Pin('PJ0', Pin.IN, Pin.PULL_UP)
Pdel = Pin('PG12', Pin.IN, Pin.PULL_UP)
Pp = Pin('PJ1', Pin.IN, Pin.PULL_UP)
#left
P0 = Pin('PE5', Pin.IN, Pin.PULL_UP)
P1 = Pin('PI11', Pin.IN, Pin.PULL_UP)
P2 = Pin('PE4', Pin.IN, Pin.PULL_UP)
P3 = Pin('PK0', Pin.IN, Pin.PULL_UP)
P4 = Pin('PB2', Pin.IN, Pin.PULL_UP)
P5 = Pin('PH15', Pin.IN, Pin.PULL_UP)
P6 = Pin('PI13', Pin.IN, Pin.PULL_UP)
P7 = Pin('PG10', Pin.IN, Pin.PULL_UP)
P8 = Pin('PI10', Pin.IN, Pin.PULL_UP)
P9 = Pin('PI15', Pin.IN, Pin.PULL_UP)
P10 = Pin('PK7', Pin.IN, Pin.PULL_UP)
P11 = Pin('PE6', Pin.IN, Pin.PULL_UP)
P12 = Pin('PI14', Pin.IN, Pin.PULL_UP)
P13 = Pin('PJ7', Pin.IN, Pin.PULL_UP)
P14 = Pin('PJ6', Pin.IN, Pin.PULL_UP)


texta = ""
champs1 = ""
champs2 = ""
moda = 1
prime = 0
Pprime = Pin('PA7', Pin.OUT)

async def check_keyboard():
    global texto, moda, prime
    liste1 = ["sc.view('tempo.py', 3)","sc.cp('tempo.py', 'prout')","sc.view('prout', 3)",'d','e','f','g','h','i','j','k','l','m','/',',']
    liste2 = ["print('tempo.py')","sc.count('tempo.py')",'p','q','r','s','t','u','v','w','x','y','z',':','.']
    liste3 = ['0','1','2','3','4','5','6','7','8','9','+','-','*',"'","="]
    liste4 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','(',')']
    liste5 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']']
    liste6 = [';','!','?','>','<','#','_','{','}','@','k','`','%','\"',"&"]

    if Penter.value() == 0:
        event = uasyncio.Event()
        uasyncio.create_task(enter(event))
        event.set()
    if Pmode.value() == 0:
        pyb.LED(1).off()
        pyb.LED(2).off()
        pyb.LED(3).off()
        moda +=1
        if moda == 4:
            moda = 1
        pyb.LED(moda).on()
    if Pspace.value() == 0:
        texto = texto + " "
    if Pdel.value() == 0:
        texto = texto[:-1]
    if Pp.value() == 0:
        if prime:
            prime = 0
            Pprime.off()
        else:
            prime = 1
            Pprime.on()

    for i in range(15):
        key = eval('P' + str(i) + ".value()")
        if key == 0:
            print(key)
            if moda == 1:
                if prime:
                    texto = texto + liste4[i]
                else:
                    texto = texto + liste1[i]
            if moda == 2:
                if prime:
                    texto = texto + liste5[i]
                else:
                    texto = texto + liste2[i]
            if moda == 3:
                if prime:
                    texto = texto + liste6[i]
                else:
                    texto = texto + liste3[i]
modo = 0
fi = ""
L1=1
async def enter(event):
    global texto, texta, champs1, champs2, modo, fi, L1
    texto = str(texto)
    if texta == texto:
        texto = ""
    if texto[:5] == 'print': #less than 10 pages
        fi = texto[6:-1]
        print(fi)
        modo = 1
    if modo == 0:
        if texto[:6] == "import":
            textu = texto[7:]
            try:
                if textu == 'sh':
                    import shell_commands as sh
                if textu == 'redi':
                    import redi
                texto = ""
            except:
                texto = 'no modules named: ' + textu

        for i in texto:
            if i == '=':
                pl_egal = texto.index(i)
                champs1 = texto[0:pl_egal]
                for i in champs1:
                    if i == " ":
                        pl_i = champs1.index(i)
                        pl_j = pl_i + 1
                        champs1 = champs1[:pl_i] + champs1[pl_j:]
                pl_egal += 1
                champs2 = texto[pl_egal:]
                for i in champs2:
                    if i == " ":
                        pl_i = champs2.index(i)
                        pl_j = pl_i + 1
                        champs2 = champs2[:pl_i] + champs2[pl_j:]
                champs2 = eval(champs2)
                try:
                    champs2 = int(champs2)
                except:
                    pass
                texto = ""
                globals()[champs1] = champs2

        if texto != "":
            print(texto)
            com = eval(texto)
            texto = com
        texta = texto
    await event.wait()
    event.clear()

async def tft_display2(fi):#the name of the file dosen't pass???
    global modo, texto
    if modo == 1:
        modo = 2
        #L2 = int(count)
        L2 = 10
        print('fi: '.format(fi))
        fi = open('tempo.py', 'r')
        ligne = fi.readline()
        tft.fill(tft.WHITE)
        nb = 1
        nl = 1
        while nl != L1:
            ligne = fi.readline()
        while nl != L2:
            ligne = str(nl) + ' ' + ligne
            if len(ligne) > 15:
                ligne1 = str(nl) + ' ' + ligne[:15]
                ligne2 = ligne[15:]
                tft.text((5, nb), ligne1,tft.BLACK, seriffont, 2, nowrap=True)
                nb += 15
                tft.text((5, nb), ligne2,tft.BLACK, seriffont, 2, nowrap=True)
            else:
                tft.text((5, nb), ligne,tft.BLACK, seriffont, 2, nowrap=True)
            ligne = fi.readline()
            nb += 15
            nl += 1
        fi.close()
    if modo == 2:
        while modo == 2:
            if Penter.value() == 0:
                modo = 0
                texto = ""
            await uasyncio.sleep_ms(200)
async def main():
    while 1:
        if modo == 0:
            uasyncio.create_task(tft_display(texto))
        else:
            uasyncio.create_task(tft_display2(fi))
        uasyncio.create_task(check_keyboard())
        await uasyncio.sleep_ms(500)
uasyncio.run(main())
