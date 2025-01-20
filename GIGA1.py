import machine
import pyb
import uasyncio
from ssd1306 import SSD1306_I2C
import shell_commands as sc
from micropython import const

i2c = machine.I2C(1)
oled = SSD1306_I2C(128,64,i2c)
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

    if (len(texto)) > width_screen:
        text1 = texto[:width_screen]
        oled.text(text1, 5, step_start , 1)
        text2 = texto[width_screen:]
        p1 = step_start + height_step
        oled.text(text2, 5, p1 , 1)
    if (len(texto)) > (width_screen * 2):
        text1 = texto[:width_screen]
        oled.text(text1, 5, step_start , 1)
        t1 = width_screen *2
        text2 = texto[width_screen:t1]
        p1 = step_start + height_step
        oled.text(text2, 5, p1 , 1)
        text3 = texto[t1:]
        p2 = step_start + (height_step * 2)
        oled.text(text3, 5, p2 , 1)
    if (len(texto)) > (width_screen * 3):
        text1 = texto[:width_screen]
        oled.text(text1, 5, step_start , 1)
        t1 = width_screen *2
        text2 = texto[width_screen:t1]
        p1 = step_start + height_step
        oled.text(text2, 5, p1 , 1)
        t2 = width_screen *3
        text3 = texto[t1:t2]
        p2 = step_start + (height_step * 2)
        oled.text(text3, 5, p2 , 1)
        t3 = width_screen *4
        text4 = texto[t2:]
        p3 = step_start + (height_step * 3)
        oled.text(text4, 5, p3 , 1)
    else:
        oled.text(texto, 5, step_start , 1)
    oled.show()

#keyboard
Penter = machine.Pin('PJ12', machine.Pin.IN, machine.Pin.PULL_UP)
Pmode = machine.Pin('PG13', machine.Pin.IN, machine.Pin.PULL_UP)
Pspace = machine.Pin('PJ0', machine.Pin.IN, machine.Pin.PULL_UP)
Pdel = machine.Pin('PG12', machine.Pin.IN, machine.Pin.PULL_UP)
Pp = machine.Pin('PJ1', machine.Pin.IN, machine.Pin.PULL_UP)
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
Pprime = machine.Pin('PB4', machine. Pin.OUT)

prime = 0
texta = ""
champs1 = ""
champs2 = ""
moda = 1
async def check_keyboard():
    global texto, moda, prime
    liste1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','/',',']
    liste2 = ["sc.view",'o','p','q','r','s','t','u','v','w','x','y','z',':','.']
    liste3 = ['0','1','2','3','4','5','6','7','8','9','+','-','*',"'","="]
    liste4 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','(',')']
    liste5 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']']
    liste6 = [';','!','?','>','<','#','_','{','}','\"',"sc.md('main.py',188,\"        fil='IFI.py'\")",'`','%','', "sc.md('main.py', '167', '        L1,L2 = 3,6')"]
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
    print(texto)
    if texta == texto:
        texto = ""
    if texto[:7] == 'sc.view':
        texto = ""
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
                chmaps1 = champs1.replace(' ', '')
                pl_egal += 1
                champs2 = texto[pl_egal:]
                chmaps2 = champs2.replace(' ', '')
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
        L1, L2 = 1,3
        fil='IFI.py'
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
