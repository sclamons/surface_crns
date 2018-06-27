# -*- coding: utf-8 -*-
from pygame import *
import MenuSystem

bg = image.load('python4.jpg')
scr = display.set_mode(bg.get_size())
scrrect = scr.blit(bg,(0,0))
display.flip()


#~ le module doit être initialisé après la vidéo
MenuSystem.init()
#~ change la couleur du fond
MenuSystem.BGCOLOR = Color(200,200,200,80)
MenuSystem.FGCOLOR = Color(200,200,200,255)
MenuSystem.BGHIGHTLIGHT = Color(0,0,0,180)
MenuSystem.BORDER_HL = Color(200,200,200,180)



#~ création des menus
semaine  = MenuSystem.Menu('week',      ('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday'))
couleurs = MenuSystem.Menu('colors',    ('red','blue','green','yellow','black','white'))
f_rouges = MenuSystem.Menu('berries',   ('strawberry','blackberry','blueberry'))
fruits   = MenuSystem.Menu('fruits',    ('apple','banana','pear',f_rouges,couleurs))
msoft    = MenuSystem.Menu('MicroSoft', ('XBox','XBox360'))
sony     = MenuSystem.Menu('Sony',      ('PSone','PS2','PS3'))
nintendo = MenuSystem.Menu('Nintendo',  ('SNES','GameCube','GameBoy','WII'))
consoles = MenuSystem.Menu('consoles',  ('NeoGeo','MegaDrive',msoft,sony,nintendo))
annees   = MenuSystem.Menu('*',         ('1974','1975','1976','1977'))

#~ création de la barre
bar = MenuSystem.MenuBar()
bar.set((semaine,couleurs,fruits))
display.update(bar)

#~ création du menu contextuel
#~ on le set()era plus tard au clic-droit
ms = MenuSystem.MenuSystem()

mc = MenuSystem.MenuChoice()
mc.set(annees,(10,350),w=100)
display.update(mc)


sw = MenuSystem.Button('ON',100,30)
sw.topleft =  scrrect.centerx,50
sw.set(type=MenuSystem.SWITCH,switchlabel="OFF")

bt = MenuSystem.Button('EXIT',100,30)
bt.bottomright =  scrrect.w-20,scrrect.h-20
bt.set()

while True:
    ev = event.wait()

    #~ on update l'objet MenuSystem en lui passant l'événement
    #~ si l'update retourne True on rafraîchit le display
    if ms:
        display.update(ms.update(ev))

        #~ on catch le choix de l'utilisateur
        #~ le choix sera réinitialiser au prochain update
        if ms.choice:
            print(ms.choice)
            print(ms.choice_label)
            print(ms.choice_index)

    #~ on update l'objet MenuBar en lui passant l'événement
    #~ si l'update retourne True on rafraîchit le display
    else:
        display.update(bar.update(ev))
        if bar.choice:
            print(bar.choice)
            print(bar.choice_label)
            print(bar.choice_index)

        if not bar:
            display.update(mc.update(ev))
            if mc.choice:
                print(mc.choice)
                print(mc.choice_label)
                print(mc.choice_index)



    if ev.type == MOUSEBUTTONDOWN and ev.button == 3:
        #~ on affiche le menu à la position de la souris quand on clic-droit
        #~ sans oublier d'actualiser le display
        ms.set(consoles,ev.pos)
        display.flip()

    if sw.update(ev):
        pass
    if bt.update(ev):
        if bt.clicked: break
    display.flip()