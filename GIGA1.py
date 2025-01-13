#importants lib
import machine
import pyb
import os
import uasyncio
#display lib
from ssd1306 import SSD1306_I2C
#optional lib
import shell_commands as sc
from micropython import const

#############  I2C for oled display
i2c = machine.I2C(1)
oled = SSD1306_I2C(128,64,i2c)

###variables for display correctly
# display dimensions: 0.96"
#width = const(128) #no necessary for moment
#height = const(128) #no necessary for moment
width_screen = const(15)
step_start = const(5)
height_step = const(10)

punto = 0
texto = ""
modo = 0

async def oled_display(texto):
    global punto
    oled.fill(0)
    if punto:
        texto = str(texto) + "|"
        punto = 0
    else:
        texto = str(texto)
        punto = 1
    if len(texto) > width_screen: # 17 is nearly the same of (128 / space_letter = 17 in my case)... it depend of the scale...
        texto1 = texto[:width_screen]
        oled.text(texto1, 5, step_start , 1)
        texto2 = texto[width_screen:]
        tt = step_start + height_step
        oled.text(texto2, 5, tt, 1)
    if len(texto) > (width_screen*2):
        texto1 = texto[:width_screen]
        oled.text(texto1, 5, step_start , 1)
        tt = step_start + height_step
        texto2 = texto[height_step:tt]
        oled.text(texto2, 5, tt, 1)
        tt = tt + height_step
        texto3 = texto[tt:]
        oled.text(texto3, 5, tt, 1)
    else:
        oled.text(texto, 5, step_start , 1)
    oled.show()

#Keyboard right
Penter = machine.Pin('PJ12', machine.Pin.IN, machine.Pin.PULL_UP)
Pmode = machine.Pin('PG13', machine.Pin.IN, machine.Pin.PULL_UP)
Pspace = machine.Pin('PJ0', machine.Pin.IN, machine.Pin.PULL_UP)
Pdel = machine.Pin('PG12', machine.Pin.IN, machine.Pin.PULL_UP)
Pp = machine.Pin('PJ1', machine.Pin.IN, machine.Pin.PULL_UP)
#left
P0 = machine.Pin('PE5', machine.Pin.IN, machine.Pin.PULL_UP)
P1 = machine.Pin('PI11', machine.Pin.IN, machine.Pin.PULL_UP)
P2 = machine.Pin('PE4', machine.Pin.IN, machine.Pin.PULL_UP)
P3 = machine.Pin('PK0', machine.Pin.IN, machine.Pin.PULL_UP)
P4 = machine.Pin('PB2', machine.Pin.IN, machine.Pin.PULL_UP)
P5 = machine.Pin('PH15', machine.Pin.IN, machine.Pin.PULL_UP)
P6 = machine.Pin('PI13', machine.Pin.IN, machine.Pin.PULL_UP)
P7 = machine.Pin('PG10', machine.Pin.IN, machine.Pin.PULL_UP)
P8 = machine.Pin('PI10', machine.Pin.IN, machine.Pin.PULL_UP)
P9 = machine.Pin('PI15', machine.Pin.IN, machine.Pin.PULL_UP)
P10 = machine.Pin('PK7', machine.Pin.IN, machine.Pin.PULL_UP)
P11 = machine.Pin('PE6', machine.Pin.IN, machine.Pin.PULL_UP)
P12 = machine.Pin('PI14', machine.Pin.IN, machine.Pin.PULL_UP)
P13 = machine.Pin('PJ7', machine.Pin.IN, machine.Pin.PULL_UP)
P14 = machine.Pin('PJ6', machine.Pin.IN, machine.Pin.PULL_UP)

Pprime = machine.Pin('PB4', machine. Pin.OUT) #to have a second list of choice on the keyboard
prime = 0
#to have a return on the screen, correctly, but be carefull with others variables inside new function
texta = ""
champs1 = ""
champs2 = ""
moda = 1

async def check_keyboard():
    global texto, moda, prime
    liste1 = ["sc.view","sc.md('tempo.py', '5', 'import machine')",'c','d','e','f','g','h','i','j','k','l','m','/',',']
    liste2 = ['n','o','p','q','r','s','t','u','v','w','x','y','z',':','.']
    liste3 = ['0','1','2','3','4','5','6','7','8','9','+','-','*',"'","="]
    liste4 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','(',')']
    liste5 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']']
    liste6 = [';','!','?','>','<','#','_','{','}','@','k','`','%','\"',"&"]

    if Penter.value() == 0:
        event = uasyncio.Event()
        uasyncio.create_task(enter(event))
        event.set()
    if Pmode.value() == 0:
        for i in range(1,4):
            pyb.LED(i).off()
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
async def enter(event):
    global texto, texta, champs1, champs2, modo
    texto = str(texto)
    #print(texto, texto[:5])
    if texta == texto:
        texto = ""
    if texto[:5] == 'print':
        texto = texto[5:-1]
    if texto[:7] == 'sc.view':
        modo = 1
    if modo == 0:
        if texto[:6] == "import":
            textu = texto[7:]
            try:
                if textu == 'redi':
                    import redi
                texto = ""
            except:
                texto = 'no modules named: ' + textu

        for i in texto:
            if texto[:5] == 'sc.cp':
                break
            if texto[:5] == 'sc.md':
                break
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

        texta = texto
        if texto != "":
            com = eval(texto)
            texto = com
    await event.wait()
    event.clear()

async def oled_display2():
    global modo, texto
    if modo == 1:
        modo = 2
        L1, L2 = 5, 6
        fil = 'tempo.py'
        fi = open(fil, 'r')
        ligne = fi.readline()
        oled.fill(0)
        nl = 1
        place = step_start
        while nl != L1:
            ligne = fi.readline()
            nl += 1
        while nl != L2:
            if len(ligne) > width_screen:
                ligne1 = ligne[:width_screen]
                oled.text(ligne1, 5, place, 1)
                ligne2 = ligne[width_screen:]
                place = place + height_step
                oled.text(ligne2, 5, place, 1)
            else:
                oled.text(ligne, 5, place, 1)
                place = place + height_step
            ligne = fi.readline()
            nl += 1
        oled.show()
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
            uasyncio.create_task(oled_display(texto))
        if modo == 1:
            uasyncio.create_task(oled_display2())
        uasyncio.create_task(check_keyboard())
        await uasyncio.sleep_ms(500)
uasyncio.run(main())
