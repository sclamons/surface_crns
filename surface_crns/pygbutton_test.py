import sys
import pygame as pg
import pygbutton


pg.init()
screen = pg.display.set_mode((500,500))
clock = pg.time.Clock()

button = pygbutton.PygButton((200, 200, 100, 30), "Register")

done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True
        else:
            print("Event is: " + str(event))
            print("Pygbutton says: " + str(button.handleEvent(event)))

    screen.fill(pg.Color("darkslategray"))
    button.draw(screen)
    pg.display.update()
    clock.tick(60)

pg.quit()
sys.exit()