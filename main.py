import machine
import pyb
import uasyncio
import shell_commands as sc
from micropython import const
##display lib(s)
from sh1107 import SH1107_I2C
# optionnal libs
from micropython_rfm9x import *

############################################  SPI for RFM9X
#spi = machine.SPI(5, baudrate=2_000_000)
spi = machine.SPI(5, baudrate=1_000_000, polarity=0, phase=0)
CS = machine.Pin('PK1', machine.Pin.OUT)
RE = machine.Pin('PB4', machine.Pin.OUT)
FR = 433.0
rfm9x = RFM9x(spi, CS, RE, FR)
rfm9x.hight_power = 5
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

############################################   I2C for OLED
i2c = machine.I2C(4)
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
        oled.show()
    else:
        oled.text(texto, 0, step_start , 1)
        oled.show()

##################################################    KEYBOARD
#first hand
Penter = machine.Pin('PJ12', machine.Pin.IN, machine.Pin.PULL_UP)
Pmode1 = machine.Pin('PG13', machine.Pin.IN, machine.Pin.PULL_UP)
Pmode2 = machine.Pin('PG12', machine.Pin.IN, machine.Pin.PULL_UP)
Pspace = machine.Pin('PJ0', machine.Pin.IN, machine.Pin.PULL_UP)
Pdel = machine.Pin('PJ1', machine.Pin.IN, machine.Pin.PULL_UP)
#second hand
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
PR = machine.Pin('PJ3', machine.Pin.IN, machine.Pin.PULL_UP)
PL = machine.Pin('PK2', machine.Pin.IN, machine.Pin.PULL_UP)

########## Variables to manage reactions of the keyboard
prime = 0
moda = 1
reci = ['1','2','3','4','5'] # five records of passed commands
async def check_keyboard():
    global texto, texta, prime, reci
    moda = 1
    liste1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','/',',']
    liste2 = ['n','o','p','q','r','s','t','u','v','w','x','y','z',':','.']
    liste3 = ['0','1','2','3','4','5','6','7','8','9','+','-','*',"'","="]
    liste4 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','(',')']
    liste5 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']']
    liste6 = ["sc.md('boot.py',5,\"pyb.main('SCRIPT.py')\")",'!','!','>','<','#','_','{','}','\"',"sc.md('main.py',188,\"        fil='SCRIPT.py'\")",'`','%','', "sc.md('main.py', 167, '        L1,L2 = 3,6')"]

    if Penter.value() == 0:
        if texta == texto:#to clean the display with the enter key
            texto = ""
        try:
            texto = str(texto)
            if texto[0] == '[':
                pass
            elif texto == "":
                pass
            else:
                reci.append(texto) # to record command
                reci.pop(0)
        except:
            pass
        event = uasyncio.Event()
        uasyncio.create_task(enter(event))
        event.set()

    if Pmode1.value() == 0: #when 1 key of the second hand and the key to activate the mode 2 on the first hand are pressed together
        moda = 2
    if Pmode2.value() == 0: #when 1 key of the second hand and the key to activate the mode 3 on the first hand are pressed together
        moda = 3
    if Pspace.value() == 0:
        texto = texto + " "
    if Pdel.value() == 0:
        texto = texto[:-1]

    if PL.value() == 0: # to have acces to lists 4 to 6, or not
        if prime:
            prime = 0
            pyb.LED(3).off()
        else:
            prime = 1
            pyb.LED(3).on()
    if PR.value() == 0: # the recorded commands, without argument, it display the list of alls recorded commands passed, with the number 1 on the screen, it display the last command that you can use again
        if texto == "":
            texto = str(reci)
        else:
            num = texto
            try:
                num = 5 - int(num)
                texto = reci[num]
            except TypeError:
                texto = 'not int'

    for i in range(15): 
        key = eval('P' + str(i) + ".value()")
        if key == 0:
            if moda == 1:#when just one key of the second hand is pressed
                if prime:
                    texto = texto + liste4[i]
                else:
                    texto = texto + liste1[i]
            if moda == 2: #when 1 key of the second hand and the key to activate the mode 2 on the first hand are pressed together
                if prime:
                    texto = texto + liste5[i]
                else:
                    texto = texto + liste2[i]
            if moda == 3: #when 1 key of the second hand and the key to activate the mode 3 on the first hand are pressed together
                if prime:
                    texto = texto + liste6[i]
                else:
                    texto = texto + liste3[i]

########## Variables to display text ON the screen
texta = ""
champs1 = ""
champs2 = ""
modo = 0
async def enter(event):
    global texto, texta, champs1, champs2, modo, reci
    try:
        texto = str(texto)
    except:
        pass
    if (modo == 3):
        modo = 0
    if texta == texto: # to escape when no result is returned
        texto = ""
        modo = 3
    if texto[:4] == 'view': # to display a file named at the line 188, mas o minos
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
        if texto[:6] == "import": # to execute a file that you have to add in your current folder, and his name there, below.
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
            if texto[:1] == '[': # to escape the record of the command reci (recorded commands acces)
                break
                texto = ""
            if texto[:3] == 'sc.':# to escape when a file is managed by shell_commands script
                break
            if texto[:6] == 'RFM': # to escape when a rfm communication is done
                break
            if i == '=': #to add new variables
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
        texta = texto
        if texto != "":
            try:
                com = eval(texto)
                texto = com
            except TypeError:
                pass
            #except ValueError:
             #   pass
            except:
                texto = ''
    await event.wait()
    event.clear()

# to display a file
async def oled_display2():
    global modo, texto
    if modo == 1:
        modo = 2
        L1, L2 = 1,7 ## change these numbers by a sc commands to see other lines of your file; a reset is necessary if you do it.
        fil = 'main.py' ## change these name by a sc commands to see other file; a reset is necessary if you do it.
        fi = open(fil, 'r')
        ligne = fi.readline()[:-1]
        oled.fill(0)
        nl = 1
        place = step_start
        while nl != L1:
            ligne = fi.readline()[:-1]
            nl += 1
        while nl != L2:
            if len(ligne) > width_screen:
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
        if modo == 0 or modo == 3:
            uasyncio.create_task(oled_display(texto))
        if modo == 1:
            uasyncio.create_task(oled_display2())
        uasyncio.create_task(check_keyboard())
        await uasyncio.sleep_ms(500)
uasyncio.run(main())
