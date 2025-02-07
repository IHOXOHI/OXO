import machine
import uasyncio

uart = machine.UART(1, baudrate=9600)
uart.init(9600, bits=8, parity=None, stop=1)

P1 = machine.Pin('Y0', machine.Pin.IN, machine.Pin.PULL_UP)
P2 = machine.Pin('Y1', machine.Pin.IN, machine.Pin.PULL_UP)

key = ""
key_mem = ""

async def check_keyboard():
    global key, key_mem
    if key == key_mem:
        key = ""
    if P2.value() == 0:
        key = "ls"
    if P1.value() == 0:
        key = "view"
    key_mem = key

async def uart_send(key):
    data = bytearray(key)
    uart.write(data)

async def main():
    while 1:
        uasyncio.create_task(check_keyboard())
        uasyncio.create_task(uart_send(key))
        await uasyncio.sleep_ms(300)
uasyncio.run(main())
