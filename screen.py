import machine
import pyb
import uasyncio
from micropython import const
##display lib(s)
from ssd1306 import SSD1306_I2C
# optionnal libs

uart = machine.UART(2, baudrate=9600)
uart.init(9600, bits=8, parity=None, stop=1)

texto = ""


async def check_uart():
    global texto, modo
    data = ""
    result = uart.any()
    if result == 0:
        pass
    else:
        data = uart.read()
    try:
        pre_text = str(data)
        modo = pre_text[1]
        texto = pre_text[2:-1]
    except:
        texto = ""
############################################   I2C for OLED
i2c = machine.I2C(1)
oled = SSD1306_I2C(64,64,i2c)
##  Variables to display text FROM the keyboard
width_screen = const(8)
step_start = const(32)
height_step = const(5)
punto = 0

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

modo = 0
# For display a file
async def oled_display2(event):
    global modo, texto
    if modo == 1:
        modo = 2
        L1, L2 = 1,7
        fil = 'main.py'
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
    await event.wait()
    event.set()
############################    MAIN
async def main(modo):
    while 1:
        uasyncio.create_task(check_uart())
        if modo == 0:
            uasyncio.create_task(oled_display(texto))
        if modo == 1:
            event = uasyncio.Event()
            uasyncio.create_task(oled_display2(event,texto))
            event.clear()
        await uasyncio.sleep_ms(300)
uasyncio.run(main(modo))
