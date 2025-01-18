
vari = {}

class VA:
    def __init__(self):
        self.vari = vari

    def ch(self,key='',value=0):
        vari = self.vari
        try:
            value = int(value)
        except:
            pass
        vari[key] = value
        re = key + '=' + str(value)
        return re


    def ifi(self, key='',comp=0):
        vari = self.vari
        print('vari:',vari)
        print('key', key)
        #print('vari[key]',vari[key])
        print("vari['a']", vari['a'])
        fil = open('IFI.py', 'w')
        for i in vari:
            text = str(i) + ' = ' + str(vari[i]) + "\n"
            fil.write(text)
        text = "if " +  key + " == " + str(comp) + ":\n"
        fil.write(text)
        fil.close()
        return "    "
