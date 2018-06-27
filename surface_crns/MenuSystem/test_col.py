# -*- coding: utf-8 -*-
from pygame import *
import MenuSystem

scr = display.set_mode((500,500))
MenuSystem.BGCOLOR = Color(0,0,0,80)
MenuSystem.init()

colors = MenuSystem.Menu('',('red','blue','green','yellow'))
ms = MenuSystem.MenuSystem()
ms.set(colors,(200,200))


while True:
    ev = event.wait()
    if ev.type == QUIT: break
    if ms:
        display.update(ms.update(ev))
        if ms.select:
            scr.fill(Color(ms.select[-1][1]))
            ms.redraw()
            display.flip()
