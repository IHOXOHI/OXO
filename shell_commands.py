import os

def view(ori,L=1):
    fil_ori = open(ori, "r")
    if L != 1:
        n = 1
        L -= 1
        while n != L:
            l = fil_ori.readline()
            n+=1
    l = fil_ori.readline()
    fil_ori.close()
    return l

def cp(ori, des,ch_lg=0, ch_txt="\n"):
    fil_ori = open(ori, "r")
    fil_des = open(des, "w")
    l = fil_ori.readline()
    n = 1
    ch_txt = ch_txt + '\n'
    while l != "":
        if n == int(ch_lg):
            text = str(ch_txt)
        else:
            text = str(l)
        fil_des.write(text)
        l = fil_ori.readline()
        n += 1
    fil_ori.close()
    fil_des.close()
    return "ok"

def count(ori):
    fil_ori = open(ori, "r")
    n = 0
    l = fil_ori.readline()
    while l != "":
        n += 1
        l = fil_ori.readline()
    fil_ori.close()
    return str(n)

def md(ori,ch_lg=0, ch_txt=""):
    fil_ori = open(ori, "r")
    fil_des = open('tempo.py', "w")
    l = fil_ori.readline()
    n = 1
    ch_txt = ch_txt + '\n'
    while l != "":
        if n == int(ch_lg):
            text = str(ch_txt)
        else:
            text = str(l)
        fil_des.write(text)
        l = fil_ori.readline()
        n += 1
    fil_ori.close()
    fil_des.close()

    fil_ori = open('tempo.py', "r")
    fil_des = open(ori, "w")
    l = fil_ori.readline()
    n = 1
    while l != "":
        if n == int(ch_lg):
            text = str(ch_txt)
        else:
            text = str(l)
        fil_des.write(text)
        l = fil_ori.readline()
        n += 1
    fil_ori.close()
    fil_des.close()

    os.remove('tempo.py')
    return "ok"
