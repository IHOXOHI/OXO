import machine
import pyb
import uasyncio
import shell_commands as sc
from micropython import const
##display lib(s)
from sh1107 import SH1107_I2C
# optionnal libs
from micropython_rfm9x import *
import ask

rtc = machine.RTC()

############################################   I2C for OLED
i2c = machine.I2C(2)
oled = SH1107_I2C(128,128,i2c,address=0x3c,rotate=90)
##  Dimensions of screen, place and style of the displayed prompt
width_screen = const(16)
step_start = const(5)
height_step = const(10)
punto = 0
texto = ""

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

#uart to communicate with keyboard1
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

    if S1.value() == 0:
        texto = "ask.copy2('test.py')"
    if S2.value() == 0:
        texto = "sc.md('redi.py','4', '    LED(1).toggle()')"
    if S3.value() == 0:
        texto = "sc.count('redi.py')"
    if S4.value() == 0:
        texto = "ask.ASK('ls')"
########## Variables to display 'correctly'
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
        n = 0
        if texto[6] == ',':
            for i in texto:
                if (i == ',') and (n == 1):
                    pl_virgule2 = texto.index(i)
                    L1 = texto[0:pl_virgule2]
                    pl_virgule2 += 1
                    L2 = texto[pl_virgule2:]
                    break
                if (i == ',') and (n == 0):
                    pl_virgule1 = texto.index(i)
                    namo = texto[0:pl_virgule1]
                    pl_virgule1 += 1
                    texto = texto[pl_virgule1:]
                    n += 1
        else:
            namo = texto
            namo = texto[1:-1]
            L1 = str(1)
            L2 = sc.count(namo)
        texto = ""
        modo = 1

    if texto[:2] == 'ls':
       import os
       try:
           textu = texto[3:-1]
       except:
           textu = ''
       texto = os.listdir(textu)
    if texto[:2] == 'rm':
       import os
       try:
           textu = texto[3:-1]
           os.remove(textu)
           texto = 'Done.'
       except NameError:
           texto = 'no file named: \n{}'.format(textu)
       except:
           texto = "No done?"

    if modo == 0:
        if texto[:6] == "import":
            module = texto[7:]
            try:
                if module == 'redi':
                    eventi = uasyncio.Event()
                    uasyncio.create_task(do_import1(eventi))
                    eventi.set()
            except:
                texto = 'no modules named: ' + module
        if texto[:3] == "RFM":
            eventu = uasyncio.Event()
            uasyncio.create_task(rfm_check1(eventu))
            eventu.set()
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
                break
        texta = texto
        if texto != "":
            try:
                com = eval(texto)
                texto = com
            except TypeError:
                texto = "Bad Type\nNo eval..."
            except AttributeError:
                texto = "Bad Attribute\nNo eval..."
            except:
                texto = ''
    await event.wait()
    event.clear()

#to make an import without stress
async def do_import1(eventi):
    import redi
    await eventi.wait()
    eventi.clear()

# To display a file
namo = "main.py" ##the default displayed file
L1, L2 = 1, 7
nl = 1

async def file_transfert(evento,namo, L1=1, L2=7):
    namo = "'" + namo + "'"
    sc.cp_view(namo,L1,L2)
    await evento.wait()
    evento.clear()
async def oled_display2(eventa, L1=1, L2=7):
    global modo, texto, nl
    if modo == 1:
        modo = 2
        fil = 'tempo.py'
        fi = open(fil, 'r')
        ligne = fi.readline()[:-1]
        oled.fill(0)
        nl = 0
        place = step_start
        L1 = int(L1) - 1
        L2 = int(L2)
        while nl < L2 :
            if nl < (L1):
                ligne = fi.readline()[:-1]
                nl += 1
            else:
                if len(ligne) > width_screen:
                    nl += 1
                    ligne = str(nl) + " " + ligne
                    ligne1 = ligne[:width_screen]
                    oled.text(ligne1, 0, place, 1)
                    ligne2 = ligne[width_screen:]
                    place = place + height_step
                    oled.text(ligne2, 0, place, 1)
                    place = place + height_step
                    ligne = fi.readline()[:-1]
                else:
                    nl += 1
                    ligne = str(nl) + " " + ligne
                    oled.text(ligne, 0, place, 1)
                    place = place + height_step
                    ligne = fi.readline()[:-1]
        oled.show()
        fi.close()
    await eventa.wait()
    eventa.clear()

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
            evento = uasyncio.Event()
            uasyncio.create_task(file_transfert(evento,namo, L1, L2))
            evento.set()
            eventa = uasyncio.Event()
            uasyncio.create_task(oled_display2(eventa, L1, L2))
            eventa.set()
        await uasyncio.sleep_ms(400)

############################################  SPI for RFM9X
RADIO_FREQ_MHZ = 433.0
CS = machine.Pin('X4', machine.Pin.OUT)
RESET = machine.Pin('X15', machine.Pin.OUT)
spi = machine.SPI(1, baudrate=2000000, polarity=0, phase=0)
rfm9x = RFM9x(spi, CS, RESET, RADIO_FREQ_MHZ)
rfm9x.hight_power = 2

async def rfm_check1(eventu):
    global texto
    text = ""
    for i in range(5):
        data = rfm9x.receive()
        if data != None:
            text = str(data, "utf-8")
    texto = text
    await eventu.wait()
    eventu.clear()

uasyncio.run(main())
