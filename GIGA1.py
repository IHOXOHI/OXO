#importants libs
import machine
import pyb
from micropython import const
#display
from ST77352 import TFT
from seriffont import seriffont
#optional
import shell_commands as sc
import uasyncio

# display dimensions:
#width = const(128) #no necessary for moment
#height = const(128) #no necessary for moment
height_step = const(15)
step_start = const(30)

spi = machine.SPI(1, baudrate=20000000)
tft=TFT(spi,machine.Pin('PG9'),machine.Pin('PE5'),machine.Pin('PG7'))
tft.initr()
tft.rotation(0)

punto = 0
texto = ""
modo = 0

async def tft_display(texto):
    global punto, modo
    tft.fill(tft.WHITE)
    if punto:
        texto = str(texto) + "|"
        punto = 0
    else:
        texto = str(texto)
        punto = 1
    if len(texto) > height_step: #height_step is the same of (128 / space_letter = 15 in my case)
        texto1 = texto[:height_step]
        tft.text((5, step_start), texto1,tft.BLACK, seriffont, 2, nowrap=True)
        texto2 = texto[height_step:]
        tt = step_start + height_step
        tft.text((5, tt), texto2,tft.BLACK, seriffont, 2, nowrap=True)
    if len(texto) > (height_step*2):
        texto1 = texto[:height_step]
        tft.text((5, step_start), texto1,tft.BLACK, seriffont, 2, nowrap=True)
        tt = step_start + height_step
        texto2 = texto[height_step:tt]
        tft.text((5, tt), texto2,tft.BLACK, seriffont, 2, nowrap=True)
        tt = tt + height_step
        texto3 = texto[tt:]
        tft.text((5, tt), texto3,tft.BLACK, seriffont, 2, nowrap=True)
    else:
        tft.text((5, step_start), texto,tft.BLACK, seriffont, 2, nowrap=True)

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


texta = ""
champs1 = ""
champs2 = ""
moda = 1
prime = 0
Pprime = machine.Pin('PA7', machine. Pin.OUT)

async def check_keyboard():
    global texto, moda, prime
    liste1 = ["sc.view('tempo.py', 5)","sc.cp('tempo.py', 'prout.py','3','        prout')","sc.view('prout.py', 179)",'d','e','f','g','h','i','j','k','l','m','/',',']
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
            print(texto, texto[:5])
        #    if texto[:5] == 'sc.cp': # I don't understand why it works when I use repl and not there?
         #       eval(texto)
          #      texto = "Done."
           # else:
            com = eval(texto)
            texto = com
        texta = texto
    await event.wait()
    event.clear()

async def tft_display2():
    global modo, texto
    if modo == 1:
        modo = 2
        L1 = 1
        L2 = 10
        file = 'tempo.py'
        fi = open('tempo.py', 'r')
        ligne = fi.readline()
        tft.fill(tft.WHITE)
        nl = 1
        place = height_step
        while nl != L1:
            ligne = fi.readline()
        while nl != L2:
            ligne = str(nl) + ' ' + ligne
            if len(ligne) > height_step:
                ligne1 = ligne[:height_step]
                tft.text((5, place), ligne1,tft.BLACK, seriffont, 2, nowrap=True)
                ligne2 = ligne[height_step:]
                place = place + height_step
                tft.text((5, place), ligne2,tft.BLACK, seriffont, 2, nowrap=True)
            else:
                tft.text((5, place), ligne,tft.BLACK, seriffont, 2, nowrap=True)
                place = place + height_step
            ligne = fi.readline()
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
            uasyncio.create_task(tft_display2())
        uasyncio.create_task(check_keyboard())
        await uasyncio.sleep_ms(500)
uasyncio.run(main())
