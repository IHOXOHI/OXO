from machine import UART, I2C, freq
from pyb import delay, LED, RTC, stop, ADC, Pin
from ssd1306 import  SSD1306_I2C
import uasyncio
from time import sleep_ms
import os

rtc = RTC()

r = LED(1)

adc = ADC(Pin('X1'))

i2c = I2C(1)
oled = SSD1306_I2C(128,64,i2c)

uart = UART(1, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

text = ""
response = 0
liste_responses = ['cp', 'ls', 'vo', 'te', 'ti',]

def check_uart():
    global text, response
    text = ""
    data = bytearray()
    result = uart.any()
    if result == 0:
        oled.fill(0)
        oled.text('NO', 5, 37, 1)
        oled.show()
    else:
        data = uart.read()
        oled.fill(0)
        oled.text('YES', 5, 37, 1)
        oled.show()

        try:
            text = str(data)
        except:
            print("problem bytes/string translation")
        #for i in liste_responses:
         #   print(i,text[2:4])
          #  if i == text[2:4]:
           #    response = 1
        response = 1

def respond():
    global response, text
####################   LS function #################
    if text[2:4] == "ls":
        if not text[5:-2]:
            listi = os.listdir()
        else:
            listi = os.listdir(text[5:-2])
        texto = ""
        for i in listi:
            texto = texto + str(i)
        data = bytearray()
        for i in texto:
            data.extend(i)
        uart.write(data)
        oled.fill(0)
        oled.text(texto, 0, 37, 1)
        oled.show()
        response = 0

####################   voltage check #################
    if text[2:4] == "vo":
        val = adc.read()
        volt = (val * 3.3) / 4095 
        texto = ("{} Volt".format(volt))
        data = bytearray()
        for i in texto:
            data.extend(i)
        uart.write(data)
        oled.fill(0)
        oled.text(texto, 0, 37, 1)
        oled.show()
        response = 0

####################   time clock #################
    if text[2:4] == "ti":
        t = rtc.datetime()
        texto = str(t)
        data = bytearray()
        for i in texto:
            data.extend(i)
        uart.write(data)
        oled.fill(0)
        oled.text(texto, 0, 37, 1)
        oled.show()
        response = 0

##################### COPY a file FROM this board
    if text[2:4] == "cp":
        response = 2
##################### COPY a file ON this board
    if text[2:4] == "c2":
        response = 3

def main():
    while 1:
        global text, response
        if response == 0:
            check_uart()
        if response == 1:
            for i in range(2):
                respond()
            sleep_ms(50)
        if response == 2:
            copy(text)
            response = 0
        if response == 3:
            copy2(text)
            response = 0
        sleep_ms(500)

respi = 0

def copy(text):
    global respi
    file_name = text[5:-2]
    print(file_name)
    while respi != 3:
        if respi == 0:
            uart_start(file_name)
        if respi == 1:
            uart_write()
        if respi == 2:
            uart_close()
        sleep_ms(100)

def uart_start(file_name):
    global respi, fil
    fil = open(file_name, 'r')
    respi = 1

def uart_write():
    global respi, fil
    text = "1"
    while text != "":
        text = fil.readline()
        data = bytearray(text)
        uart.write(data)
        sleep_ms(100)
    respi = 2

def uart_close():
    global respi, fil
    fil.close()
    respi = 3

##################### COPY2 a file ON this board from other board
def copy2(nam):
    global respi
    file_name = nam[5:-2]
    while respi != 3:
        if respi == 0:
            uart_start2(file_name)
        if respi == 1:
            uart_write2()
        if respi == 2:
            uart_close()
        sleep_ms(100)

def uart_start2(file_name):
    global respi, fil
    fil = open(file_name, 'w')
    respi = 1

def resp():
    data = bytearray()
    result = uart.any()
    if result == 0:
        pass
    else:
        data = uart.read()
        return data

def uart_write2():
    global respi, fil
    text = resp()
    text = str(text)
    text = text[2:-3]
    text = str(text) + "\n"
    if text != "Do\n":
        if text == "":
            pass
        else:
            fil.write(text)
    else:
        respi = 2

main()
