# -*- coding: utf-8 -*-
from pygame import *
import MenuSystem
import os,os.path


bg = image.load('python4.jpg')
scr = display.set_mode(bg.get_size())
scr.blit(bg,(0,0))
display.flip()

MenuSystem.init()



def foo():
    if ms.select:
        m = list(zip(*ms.select))[1]
        m = '/home/'+os.path.join(*m);print(11,m)
    else:
        m = '/home/'
    f = [MenuSystem.MenuDyn(i,foo) if os.path.isdir(os.path.join(m,i)) else i for i in os.listdir(m)]
    return MenuSystem.Menu('',f)


ms = MenuSystem.MenuSystem()

while True:

    ev = event.wait()
    display.update(ms.update(ev))
    if ev.type == MOUSEBUTTONDOWN and ev.button == 3 and not ms:
        ms.set(foo(),ev.pos)
        display.flip()