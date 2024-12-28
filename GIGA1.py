from ssd1306 import SSD1306_I2C
from machine import I2C, Pin
import uasyncio

#module1 = ""

#Oled display
i2c = I2C(2)
oled = SSD1306_I2C(128,64,i2c)
def welcome(evento):
    oled.fill(0)
    oled.text('WELCOME', 30,5)
    oled.text('GIGA1 is Ready.', 2,25)
    oled.text("Let's go!", 2,45)
    oled.show()
    await evento.wait()
    evento.clear()

##severals variables
##locals
name_session= "@GIGA1:"
##globals
texto = ""
texta = ""
champs1 = ""
champs2 = ""

async def display_oled(texto):
    texto = str(texto)
    oled.fill(0)
    oled.text(name_session, 2,2)
    oled.text(texto, 2, 22)
    oled.show()

###Keyboard
Penter = Pin('PB4', Pin.IN, Pin.PULL_UP)
Ptest = Pin('PD13', Pin.IN,  Pin.PULL_UP)
Ptest1 = Pin('PA7', Pin.IN,  Pin.PULL_UP)


async def check_keyboard():
    global texto
    ###basics commands
    if Penter.value() == 0:
        #print("Penter is pressed")
        event = uasyncio.Event()
        uasyncio.create_task(enter(event))
        event.set()

##tested commands
    if Ptest.value() == 0:
        print("Ptest is pressed")
        texto = texto + "import pyb"
    if Ptest1.value() == 0:
        print("pyb.LED(1).on()")
        texto = texto + "pyb.LED(1).on()"

fil = open('tempo', 'w')
fil.close()
mod = 0

async def enter(event):
    global texto, texta, champs1, champs2, fil, mod, module1
    if mod == 2:
        if texto == "":
            fil.close()
            mod = 0
            import fil
            texto = "print('record ok')"
        else:
            fil.write(texto)

    if texta == texto:
        texto = ""
    if texto[:5] == "print":
        mod = 1
    if texto[:2] == "if":
        fil = open('tempo', 'w')
        fil.write('texto')
        mod = 2
    if texto[:6] == "import":
        textu = texto[7:]
        print(textu)
        if textu == 'time':
            fil = open('tempo', 'w')
            fil.write('time')
            fil.close()
            import export
            print('imported time is done')
        if textu == 'pyb':
            fil = open('tempo', 'w')
            fil.write('pyb')
            fil.close()
            import export
            print('imported pyb is done')
        if textu == 'machine':
            fil = open('tempo', 'w')
            fil.write('machine')
            fil.close()
            import export
            print('imported machine is done')
        if textu == 'myscript':
            import myscript ##which is in the lib folder
            print('imported my script is done')
        if textu == 'redi':
            import redi

        texto = ""
    if mod == 0:
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
                print(champs2)
                champs2 = eval(champs2)
                try:
                    champs2 = int(champs2)
                except:
                    pass
                #print("champs1={}\nchamsp2={}".format(champs1,champs2))##for debug
                texto = ""
                globals()[champs1] = champs2
    ###save if necessary and send the result on the screen
    if texto != "":
        if mod == 0:
            print(texto)
            com = eval(texto)
            texto = com
        if mod == 1:##the print state
            texto = champs2
            mod = 0
        if (mod == 2):
            mod = 0
    texta = texto
    await event.wait()
    event.clear()

async def main():
    evento = uasyncio.Event()
    uasyncio.create_task(welcome(evento))
    evento.set()
    await uasyncio.sleep_ms(5000)
    while 1:
        uasyncio.create_task(display_oled(texto))
        uasyncio .create_task(check_keyboard())
        await uasyncio.sleep_ms(500)
uasyncio.run(main())
