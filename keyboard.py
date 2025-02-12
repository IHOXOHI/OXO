import machine
import uasyncio

uart = machine.UART(2, baudrate=9600)
uart.init(9600, bits=8, parity=None, stop=1)

##  2 keys from the fingers's PCB (3 others connected to the main board)
Pm1 = machine.Pin('Y1', machine.Pin.IN, machine.Pin.PULL_UP)
Pm2 = machine.Pin('Y0', machine.Pin.IN, machine.Pin.PULL_UP)

## 15 basics keys 
P0 = machine.Pin('X10', machine.Pin.IN, machine.Pin.PULL_UP)
P1 = machine.Pin('X9', machine.Pin.IN, machine.Pin.PULL_UP)
P2 = machine.Pin('X8', machine.Pin.IN, machine.Pin.PULL_UP)
P3 = machine.Pin('X7', machine.Pin.IN, machine.Pin.PULL_UP)
P4 = machine.Pin('X6', machine.Pin.IN, machine.Pin.PULL_UP)
P5 = machine.Pin('X5', machine.Pin.IN, machine.Pin.PULL_UP)
P6 = machine.Pin('X4', machine.Pin.IN, machine.Pin.PULL_UP)
P7 = machine.Pin('Y9', machine.Pin.IN, machine.Pin.PULL_UP)
P8 = machine.Pin('Y8', machine.Pin.IN, machine.Pin.PULL_UP)
P9 = machine.Pin('Y7', machine.Pin.IN, machine.Pin.PULL_UP)
P10 = machine.Pin('Y6', machine.Pin.IN, machine.Pin.PULL_UP)
P11 = machine.Pin('Y5', machine.Pin.IN, machine.Pin.PULL_UP)
P12 = machine.Pin('Y4', machine.Pin.IN, machine.Pin.PULL_UP)
P13 = machine.Pin('Y3', machine.Pin.IN, machine.Pin.PULL_UP)
P14 = machine.Pin('Y2', machine.Pin.IN, machine.Pin.PULL_UP)

## One key To double value reference of each key
Pp = machine.Pin('Y10', machine.Pin.IN, machine.Pin.PULL_UP)

## 6 extra keys for specials commands like "sc.cp(....
#S1 = machine.Pin('X0', machine.Pin.IN, machine.Pin.PULL_UP)
#S2 = machine.Pin('X1', machine.Pin.IN, machine.Pin.PULL_UP)
#S3 = machine.Pin('Y0', machine.Pin.IN, machine.Pin.PULL_UP)
#S4 = machine.Pin('Y1', machine.Pin.IN, machine.Pin.PULL_UP)

key = ""
key_mem = ""
prime = 0
moda = 1

async def check_keyboard():
    global key, key_mem, prime, moda
    moda = 1
    liste1 = ['a','b','c','d','e','f','g','h','i','j','k','l','m','/',',']
    liste2 = ['n','o','p','q','r','s','t','u','v','w','x','y','z',':','.']
    liste3 = ['0','1','2','3','4','5','6','7','8','9','+','-','*',"'","="]
    liste4 = ['A','B','C','D','E','F','G','H','I','J','K','L','M','(',')']
    liste5 = ['N','O','P','Q','R','S','T','U','V','W','X','Y','Z','[',']']
    liste6 = ['?','!',';','>','<','#','_','{','}','\"','@','`','%','|', '&']

    if Pm1.value() == 0:
        moda = 2
    if Pm2.value() == 0:
        moda = 3

    if Pp.value() == 0:
        if prime:
            prime = 0
            pyb.LED(2).off()
        else:
            prime = 1
            pyb.LED(2).on()

    for i in range(15):
        kk = eval('P' + str(i) + ".value()")
        if kk == 0:
            if moda == 1:
                if prime:
                    key = liste4[i]
                else:
                    key = liste1[i]
            if moda == 2:
                if prime:
                    key = liste5[i]
                else:
                    key = liste2[i]
            if moda == 3:
                if prime:
                    key = liste6[i]
                else:
                    key = liste3[i]
    if (moda == 4) and (key_mem != key):
        moda = 1
    if key == "":
        moda = 4
        key_mem = key

async def uart_send(key):
    data = bytearray(key)
    uart.write(data)

async def main(moda):
    global key
    while 1:
        uasyncio.create_task(check_keyboard())
        if moda != 4:
            uasyncio.create_task(uart_send(key))
            key = ""
        await uasyncio.sleep_ms(400)
uasyncio.run(main(moda))
