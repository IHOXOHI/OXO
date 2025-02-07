import machine
import pyb
import uasyncio
import shell_commands as sc
from micropython import const
##display lib(s)
#from ssd1306 import SSD1306_I2C
# optionnal libs
from micropython_rfm9x import *

texto = ""

async def send_to_oled(modo,texto):
    #print(texto)
    texto = str(texto)
    data = bytearray(modo)
    data.extend(texto)
    uart2.write(data)

##################################################    KEYBOARD


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
    try:
        pre_text = str(data)
        key = pre_text[2:-1]
        texto = texto + key
    except:
        pass

###uart to communicate with the display's board
uart2 = machine.UART(2, baudrate=9600)
uart2.init(9600, bits=8, parity=None, stop=1)

Penter = machine.Pin('Y1', machine.Pin.IN, machine.Pin.PULL_UP)
Pdel = machine.Pin('Y0', machine.Pin.IN, machine.Pin.PULL_UP)
P2 = pyb.Switch()

async def check_keyboard2():
    global texto, texta
    if Penter.value() == 0:
        if texta == texto:
            texto = ""
        try:
            texto = str(texto)
        except:
            pass
        event = uasyncio.Event()
        uasyncio.create_task(enter(event))
        event.set()

    if Pdel.value():
        texto = texto[:-1]
    if P2.value():
        texto = "a"

texta = ""
champs1 = ""
champs2 = ""
modo = 0
async def enter(event):
    global texto, texta, champs1, champs2, modo
    try:
        texto = str(texto)
    except:
        pass
    print(texto)
    if modo == 3:
        modo = 0
    if texta == texto:
        texto = ""
        modo = 3
    #if texto[:4] == 'view': # to display a file named at the line 188, mas o minos
     #   texto = ""
      #  modo = 1
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
            try:
                com = eval(texto)
                texto = com
            except TypeError:
                pass
            except:
                texto = ''
        #uasyncio.create_task(send_to_oled(modo,texto))
    await event.wait()
    event.clear()


############################    MAIN
async def main():
    global texto, modo
    while 1:
        uasyncio.create_task(send_to_oled(modo,texto))
        uasyncio.create_task(check_keyboard1())
        uasyncio.create_task(check_keyboard2())
        await uasyncio.sleep_ms(300)

############################################  SPI for RFM9X
###############################    RFM
RADIO_FREQ_MHZ = 433.0
CS = machine.Pin('X4', machine.Pin.OUT)
RESET = machine.Pin('X3', machine.Pin.OUT)
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
