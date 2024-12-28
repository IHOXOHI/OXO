fi = open('tempo', 'r')
mod = fi.readline()
fi.close()

if mod == 'pyb':
    import pyb
if mod == 'machine':
    import machine
if mod == 'network':
    import network
if mod == 'uasyncio':
    import uasyncio
