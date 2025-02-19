from machine import UART
from time import sleep_ms

uart = UART(2, 9600)
uart.init(9600, bits=8, parity=None, stop=1)

def ASK(question):
    uart.write(question)

def resp():
    data = bytearray()
    result = uart.any()
    if result == 0:
        pass
    else:
        data = uart.read()
        return data

state = 0

def file_start(file_name):
    global fil, state
    fil = open(file_name, 'w')
    text = "cp(" + str(file_name) + ")"
    uart.write(text)
    state = 1
def file_copy():
    global fil, state
    text = resp()
    text = str(text)
    text = text[2:-3]
    text = str(text) + "\n"
    if text != "Do\n":
        #if text == "ne":
         #   pass
        if text == "":
            pass
        else:
            fil.write(text)
        #fil.write(text)
    else:
        state = 2
def file_end():
    global fil, state
    fil.close()
    state = 3
    uart.write(b'Done')

def copy(file_name):
    global state
    while state != 3:
        if state == 0:
            file_start(file_name)
        if state == 1:
            file_copy()
        if state == 2:
            file_end()
        sleep_ms(100)

def copy2(file_name):
    global state
    while state != 3:
        if state == 0:
            file_start2(file_name)
        if state == 1:
            file_copy2()
        if state == 2:
            file_end()
        sleep_ms(100)


def file_start2(file_name):
    global fil, state
    fil = open(file_name, 'r')
    nam = "c2(" + str(file_name) + ")"
    uart.write(nam)
    state = 1
    sleep_ms(200)
def file_copy2():
    global fil, state
    text = "1"
    while text != "":
        text = fil.readline()
        data = bytearray(text)
        uart.write(data)
        sleep_ms(100)
    state = 2
