from ssd1306 import SSD1306_I2C
from machine import I2C, Pin
import uasyncio
import  pyb
from micropython import const

i2c = I2C(1)
oled = SSD1306_I2C(128,64,i2c)

name_session = const("@GIGA1:")
punto = 0
async def display_oled(texto):
    global punto
    if punto:
        texto = str(texto) + "|"
        punto = 0
    else:
        texto = str(texto)
        punto = 1
    oled.fill(0)
    oled.text(name_session, 2,2)
    oled.text(texto, 2, 22)
    oled.show()

###Keyboard #right
Penter = Pin('PJ12', Pin.IN, Pin.PULL_UP)#index
Pmode = Pin('PG13', Pin.IN,  Pin.PULL_UP)#pouce
Pspace = Pin('PJ0', Pin.IN,  Pin.PULL_UP)#majeur
Pdel = Pin('PG12', Pin.IN,  Pin.PULL_UP)#annulaire
Pp = Pin('PJ1', Pin.IN,  Pin.PULL_UP)#auriculaire
#left
P0 = Pin('PK2', Pin.IN,  Pin.PULL_UP)
P1 = Pin('PG7', Pin.IN,  Pin.PULL_UP)
P2 = Pin('PI11', Pin.IN,  Pin.PULL_UP)
P3 = Pin('PE5', Pin.IN,  Pin.PULL_UP)
P4 = Pin('PK0', Pin.IN,  Pin.PULL_UP)
P5 = Pin('PE4', Pin.IN,  Pin.PULL_UP)
P6 = Pin('PH15', Pin.IN,  Pin.PULL_UP)
P7 = Pin('PG10', Pin.IN,  Pin.PULL_UP)
P8 = Pin('PI13', Pin.IN,  Pin.PULL_UP)
P9 = Pin('PI15', Pin.IN,  Pin.PULL_UP)
P10 = Pin('PI10', Pin.IN,  Pin.PULL_UP)
P11 = Pin('PE6', Pin.IN,  Pin.PULL_UP)
P12 = Pin('PK7', Pin.IN,  Pin.PULL_UP)
P13 = Pin('PI14', Pin.IN,  Pin.PULL_UP)
P14 = Pin('PJ6', Pin.IN,  Pin.PULL_UP)

texto = ""
texta = ""
champs1 = ""
champs2 = ""
moda = 1
prime = 0
Pprime = Pin('PA7', Pin.OUT)


async def check_keyboard():
    global texto, moda, prime
    liste1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','/',',']
    liste2 = ['n','o','p','q','r','s','t','u','v','w','x','y','z',':','.']
    liste3 = ['0','1','2','3','4','5','6','7','8','9','+','-','*',"'",'=']
    liste4 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','(',')']
    liste5 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']']
    liste6 = [';','!','?','>','<','#','_','{','}','@','k','`','%','\"',"&"]

    if Penter.value() == 0:
        event = uasyncio.Event()
        uasyncio.create_task(enter(event))
        event.set()
    if Pmode.value() == 0:
        for i in range(1,4,1):
            pyb.LED(i).off()
        moda += 1
        if moda == 4:
            moda = 1
        pyb.LED(moda).on()
    if Pspace.value() == 0:
        texto = texto + " "
        #Pprime.toggle()
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
            if prime == 0:
                if moda == 1:
                    texto  = texto + liste1[i]
                if moda == 2:
                    texto  = texto + liste2[i]
                if moda == 3:
                    texto  = texto + liste3[i]
            if prime == 1:
                if moda == 1:
                    texto  = texto + liste4[i]
                if moda == 2:
                    texto  = texto + liste5[i]
                if moda == 3:
                    texto  = texto + liste6[i]

fil = open('tempo', 'w')
fil.close()
mod = 0

liste_function = ["if", "for", "while"]

async def enter(event):
    global texto, texta, champs1, champs2, fil, mod
    if mod == 2:
        if texto == "":
            fil.close()
            mod = 0
            import fil
        else:
            fil.write(texto)

    if texta == texto: #to clean the display with enter touch
        texto = ""
    if texto[:5] == "print":
        mod = 1
    if texto[:2] == "if":
        fil = open('tempo', 'w')
        fil.write('texto')
        mod = 2
    if texto[:3] == "for":
        fil = open('tempo', 'w')
        fil.write('texto')
        mod = 2
    if texto[:5] == "while":
        fil = open('tempo', 'w')
        fil.write('texto')
        mod = 2
    if texto[:6] == "import":
        textu = texto[7:]
        fil = open('fil', 'w')
        fil.write(texto[7:])
        fil.close()
        import export
        if textu == 'myscript':
            import myscript #which is placed your lib folder
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
                texto = ""
                globals()[champs1] = champs2
    if texto != "":
        if mod == 0:
            print(texto)
            com = eval(texto)
            texto = str(com)
        if mod == 1:
            texto = champs2
            mod = 0
        if mod >= 2:
            mod = 0
    texta = texto
    await event.wait()
    event.clear()

async def main():
    while 1:
        uasyncio.create_task(display_oled(texto))
        uasyncio .create_task(check_keyboard())
        await uasyncio.sleep_ms(400)
uasyncio.run(main())
