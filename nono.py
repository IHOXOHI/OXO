import machine
import pyb
import uasyncio
import shell_commands as sc
from micropython import const
##display lib(s)
from sh1107 import SH1107_I2C
# optionnal libs
from micropython_rfm9x import *
#TO DO: an import which stop the uasyncio.run, so create a loop.main
rtc = machine.RTC()
############################################   I2C for OLED
i2c = machine.I2C(2)
oled = SH1107_I2C(128,128,i2c,address=0x3c,rotate=90)
##  Variables to display text FROM the keyboard
width_screen = const(16)
step_start = const(5)
height_step = const(10)
punto = 0
texto = ""
modo = 0

async def oled_display(texto):
    global punto, ori, fin, place
    oled.fill(0)
    if punto:
        texto = str(texto) + "|"
        punto = 0
    else:
        texto = str(texto)
        punto = 1
    nn = len(texto)
    pp = nn // width_screen
    if pp >= 1:
        ori = 0#horizontal place
        place = step_start  #vertical place
        ss = texto[ori:width_screen]
        oled.text(ss, 0, step_start, 1)
        ori =  ori + width_screen
        fin = ori + width_screen
        if (len(texto)) > (width_screen*2): # 3 lines on the screen
            uu = texto[ori:fin]
            ori += width_screen
            fin += width_screen
            place += height_step
            oled.text(uu, 0, place, 1)
            if (len(texto)) > (width_screen*3): # 4 lines
                qq = texto[ori:fin]
                ori += width_screen
                fin += width_screen
                place += height_step
                oled.text(qq, 0, place, 1)
                if (len(texto)) > (width_screen*4): # 5
                    kk = texto[ori:fin]
                    ori += width_screen
                    fin += width_screen
                    place += height_step
                    oled.text(kk, 0, place, 1)
                    ##if: add other paragraph like the last one 'if:', change numbers to add a new line on the screen. Again and again if you need it.
        vv = texto[ori:]  #the last line
        place += height_step
        oled.text(vv, 0, place, 1)
        t = rtc.datetime()
        ho, mi = t[4], t[5]
        oled.text("{}: {}".format(ho,mi), 88, 110, 1)
        oled.show()
    else:
        oled.text(texto, 0, step_start , 1)
        t = rtc.datetime()
        ho, mi = t[4], t[5]
        oled.text("{}:{}".format(ho,mi), 88, 110, 1)
        oled.show()

#uart to communicate with the keyboard's board
uart1 = machine.UART(1, baudrate=9600)
uart1.init(9600, bits=8, parity=None, stop=1)

key = ""

async def check_keyboard1():
    global texto
    data = ""
    result = uart1.any()
    if result == 0:
        pass
    else:
        data = uart1.read()
        print(data)
        try:
            pre_text = str(data)
            key = pre_text[2:-1]
            texto = texto + key
        except:
            pass

## Control keys from NONO
Penter = machine.Pin('X1', machine.Pin.IN, machine.Pin.PULL_UP)
Pspace = machine.Pin('X2', machine.Pin.IN, machine.Pin.PULL_UP)
Pdel = machine.Pin('X3', machine.Pin.IN, machine.Pin.PULL_UP)
PR = machine.Pin('Y4', machine.Pin.IN, machine.Pin.PULL_UP)
## 4 extra keys for specials commands like "sc.cp(....
S1 = machine.Pin('Y5', machine.Pin.IN, machine.Pin.PULL_UP)
S2 = machine.Pin('Y7', machine.Pin.IN, machine.Pin.PULL_UP)
S3 = machine.Pin('Y1', machine.Pin.IN, machine.Pin.PULL_UP)
S4 = machine.Pin('Y0', machine.Pin.IN, machine.Pin.PULL_UP)

moda = 1
reci = ['1','2','3','4','5'] # five records of passed commands

async def check_keyboard2():
    global texto, texta, reci
    try:
        texto = str(texto)
    except:
        pass
    if Penter.value() == 0:
        if texta == texto:
            texto = ""
        try:
            if texto[0] == '[':
                pass
            elif texto == "":
                pass
            else:
                reci.append(texto)
                reci.pop(0)
        except:
            pass
        event = uasyncio.Event()
        uasyncio.create_task(enter(event))
        event.set()

    if Pspace.value() == 0:
        texto = texto + " "
    if Pdel.value() == 0:
        texto = texto[:-1]

    if PR.value() == 0:
        if texto == "":
            texto = str(reci)
        else:
            num = texto
            try:
                num = 5 - int(num)
                texto = reci[num]
            except TypeError:
                texto = 'not int'

########## Variables to display text ON the screen
texta = ""
champs1 = ""
champs2 = ""
modo = 0
async def enter(event):
    global texto, texta, champs1, champs2, modo, reci, namo, L1, L2
    try:
        texto = str(texto)
    except:
        pass
    if (modo == 3):
        modo = 0
    if texta == texto:
        texto = ""
        modo = 3
    if texto[:4] == 'view':
        texto = texto[5:-1]
        print(texto)
        n = 0
        for i in texto:
            if i == ',':
                pl_virgule1 = texto.index(i)
                namo = texto[0:pl_virgule1]
                texto = texto[pl_virgule1:]
                print(texto)
                break
        for i in texto:
            if i == ',':
                pl_virgule2 = texto.index(i)
                L1 = texto[0:pl_virgule2]
                L2 = texto[pl_virgule2:]
                print(namo,L1,L2)
                break
        texto = ""
        modo = 1
    if texto[:2] == 'ls': # to list alls files
       import os
       try:
           textu = texto[3:-1]
       except:
           textu = ''
       texto = os.listdir(textu)
    if modo == 0:
        if texto[:6] == "import":
            textu = texto[7:]
            try:
                if textu == 'myscript':
                    import myscript
                texto = ""
            except:
                texto = 'no modules named: ' + textu
        if texto[:3] == "RFM":
            evento = uasyncio.Event()
            uasyncio.create_task(rfm_check1(evento))
            evento.set()
        for i in texto:
            if texto[:1] == '[':
                break
                texto = ""
            if texto[:3] == 'sc.':
                break
            if texto[:6] == 'RFM':
                break
            if i == '=':
                texto = texto.replace(' ', '')
                pl_egal = texto.index(i)
                champs1 = texto[0:pl_egal]
                pl_egal += 1
                champs2 = texto[pl_egal:]
                champs2 = eval(champs2)
                try:
                    champs2 = int(champs2)
                except:
                    pass
                texto = ""
                globals()[champs1] = champs2
                break#down!!:!!! the firmware??? YEAH¡¡¡¡
        texta = texto
        if texto != "":
            try:
                com = eval(texto)
                texto = com
            except TypeError:
                pass
            except:
                texto = ''
    await event.wait()
    event.clear()

# To display a file
namo = "main.py" ##the default displayed file
L1, L2 = 1, 7
async def oled_display2(namo, L1=1, L2=7):
    global modo, texto
    if modo == 1:
        sc.cp_view(namo,L1,L2)
        modo = 2
        fil = 'tempo.py' #for security better to change this name by your's!
        fi = open(fil, 'r')
        ligne = fi.readline()[:-1]
        oled.fill(0)
        nl = 1
        place = step_start
        while nl != L1:
            ligne = fi.readline()[:-1]
            nl += 1
        while nl != L2:
            if len(ligne) > width_screen: #no more than a double ligne
                ligne1 = ligne[:width_screen]
                oled.text(ligne1, 0, place, 1)
                ligne2 = ligne[width_screen:]
                place = place + height_step
                oled.text(ligne2, 0, place, 1)
                place = place + height_step
            else:
                oled.text(ligne, 0, place, 1)
                place = place + height_step
            ligne = fi.readline()[:-1]
            nl += 1
        oled.show()
        fi.close()
    if modo == 2:
        while modo == 2:
            if Penter.value() == 0:
                modo = 0
                texto = ""
            await uasyncio.sleep_ms(200)

############################    MAIN
async def main():
    while 1:
        uasyncio.create_task(check_keyboard1())
        uasyncio.create_task(check_keyboard2())
        if modo == 0 or modo == 3:
            uasyncio.create_task(oled_display(texto))
        if modo == 1:
            uasyncio.create_task(oled_display2(namo, L1, L2))
        await uasyncio.sleep_ms(400)

############################################  SPI for RFM9X
###############################    RFM
RADIO_FREQ_MHZ = 433.0
CS = machine.Pin('X4', machine.Pin.OUT)
RESET = machine.Pin('X15', machine.Pin.OUT)
spi = machine.SPI(1, baudrate=2000000, polarity=0, phase=0)
rfm9x = RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.hight_power = 2
## possibles commands: rfm9x.send(b'MessageToSend'), data = rfm9x.receive(), text = str(data, "utf-8"), text

async def rfm_check1(evento):
    global texto
    text = ""
    for i in range(5):
        data = rfm9x.receive()
        if data != None:
            text = str(data, "utf-8")
    texto = text
    await evento.wait()
    evento.clear()

uasyncio.run(main())
