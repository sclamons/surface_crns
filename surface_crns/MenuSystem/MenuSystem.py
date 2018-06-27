# -*- coding: utf-8 -*-
from pygame import *
from pygame import gfxdraw
font.init()

from os.path import dirname,join

FGCOLOR      = Color(0x161212f0)
FGHIGHTLIGHT = Color(0x161212f0)
BGCOLOR      = Color(0xf2f1ebf0)
BGHIGHTLIGHT = Color(0x804a50a0)
BORDER_HL    = Color(0x804a50ff)
FGLOWLIGHT   = Color(0xbfb9b4a0)
BORDER_LEFT  = Color(0xc0c0c0f0)
BORDER_RIGHT = Color(0x303030f0)
BUTTON       = 1
SWITCH       = 0
FONT         = font.Font(join(dirname(__file__),"Roboto-Regular.ttf"),16)
try:                   Arrow        = "»".decode('utf-8')
except AttributeError: Arrow        = "»"



def init():
    global DISPLAY,DISPLAYRECT
    DISPLAY      = display.get_surface()
    if not DISPLAY: raise AttributeError('set video before init MenuSystem')
    DISPLAYRECT  = DISPLAY.get_rect()

class Menu(Rect,object):

    def __init__(self,label,itemslist,exc=()):
        self.label                  = label
        self.itemslist              = itemslist
        if self.itemslist:
            self._width,self.lineheight = max(FONT.size(x if isinstance(x,str) else x.label) for x in self.itemslist)
        else:
            self._width,self.lineheight = 0,0
        self._width                += self.lineheight*2
        self._height                = self.lineheight * len(self.itemslist)
        self.arrowRect              = Rect(0,0,*FONT.size(Arrow))
        self.exc                    = exc
        self._index                 = None
        self.itemsrect              = Rect(0,0,self._width,self._height)

    @property
    def choice(self):
        if self.index != None:
            return self.itemslist[self.index]
        return None

    @property
    def hlRect(self):
        x,y,w,h = self.itemsrect
        return Rect(x+1,self.index*self.lineheight+y+1,self.w-2,self.lineheight-2)

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self,value):
        self._index = value
        if value == None:
            self.exc_index = None
        else:
            self.exc_index = bool((1 << value)&self._exc)

    @property
    def exc(self):
        return self._exclusion

    @exc.setter
    def exc(self,value):
        self._exclusion = value
        self._exc = 0
        for i in value:
            self._exc += 2**i


    def set_at(self,x,y,w=None,h=None,force_pos=False):
        if not w:
            self.itemsrect.w = w = self._width
        else:
            self.itemsrect.w = w
        if not h: h = self._height
        r = Rect(x,y,w,h)
        if not force_pos: r.clamp_ip(DISPLAYRECT)
        Rect.__init__(self,r.clip(DISPLAYRECT))
        self.itemsrect.topleft = self.topleft
        self.index = None
        return self


    def update(self,ev):
        if ev.type == MOUSEMOTION:
            if self.itemsrect.clip(self).collidepoint(ev.pos):
                x,y = ev.pos
                index = (y-self.itemsrect.top) // self.lineheight
            else:
                index = None
            if index != self.index:
                self.index = index
                return True
        elif ev.type == MOUSEBUTTONUP:
            if self.itemsrect.clip(self).collidepoint(ev.pos):
                x,y = ev.pos
                if ev.button == 4:
                    if self.itemsrect.top < self.top:
                        self.itemsrect.top += self.lineheight
                        if self.itemsrect.top > self.top: self.itemsrect.top = self.top
                        self.index = (y-self.itemsrect.top) // self.lineheight
                        return True
                if ev.button == 5:
                    if self.itemsrect.bottom > self.bottom:
                        self.itemsrect.top -= self.lineheight
                        if self.itemsrect.bottom < self.bottom: self.itemsrect.bottom = self.bottom
                        self.index = (y-self.itemsrect.top) // self.lineheight
                        return True

    def draw(self):
        self.bg = DISPLAY.subsurface(self).copy()
        clipxy = DISPLAY.get_clip()
        DISPLAY.set_clip(self)
        gfxdraw.box(DISPLAY,self,BGCOLOR)
        x,y = self.itemsrect.topleft
        if self.index != None and not (1 << self.index)&self._exc:
            gfxdraw.box(DISPLAY,self.hlRect,BGHIGHTLIGHT)
            gfxdraw.rectangle(DISPLAY,self.hlRect,BORDER_HL)
        x += self.lineheight/3
        for idx,item in enumerate(self.itemslist):
            isExc = (1 << idx)&self._exc
            isStr = isinstance(item,str)
            text = FONT.render(item if isStr else item.label,1,FGLOWLIGHT if isExc else FGCOLOR)
            if not isStr:
                self.arrowRect.topright = self.itemsrect.right-self.lineheight/3,y
                DISPLAY.blit(FONT.render(Arrow,1,FGLOWLIGHT if isExc else FGCOLOR),self.arrowRect)
            r = DISPLAY.blit(text,(x,y))
            y += self.lineheight

        gfxdraw.vline(DISPLAY,self.left,self.top,self.bottom-1,BORDER_LEFT)
        gfxdraw.hline(DISPLAY,self.left,self.right-1,self.top,BORDER_LEFT)
        gfxdraw.vline(DISPLAY,self.right-1,self.top+1,self.bottom-1,BORDER_RIGHT)
        gfxdraw.hline(DISPLAY,self.left+1,self.right-1,self.bottom-1,BORDER_RIGHT)
        DISPLAY.set_clip(clipxy)
        return self

    def clear(self):
        DISPLAY.blit(self.bg,self)
        return self

class MenuDyn(Rect,object):

    def __init__(self,label,func):
        self.label = label
        self.func = func

    def __call__(self):
        return self.func()

class MenuSystem(list,object):

    def clear(self):
        if self:
            self.boxindex = None
            return [self.pop().clear() for _ in range(len(self))]
        return []

    def set(self,menu,pos,w=None,h=None,force_pos=False):
        ret = []
        if self:
            ret = self.clear()
        menu.set_at(*pos,w=w,h=h,force_pos=force_pos)
        self.append(menu)
        self.boxindex = None
        self.choice  = None
        event.pump()
        menu.draw()
        self.update(event.Event(MOUSEMOTION,{'pos':mouse.get_pos()}))
        return ret+[menu]

    @property
    def choice(self):
        return self._choice

    @choice.setter
    def choice(self,value):
        self._choice = value
        if value:
            self.choice_index,self.choice_label = list(zip(*self._choice))
        else:
            self.choice_index,self.choice_label = None,None

    @property
    def select(self):
        return [(b.index,b.choice if isinstance(b.choice,str) else b.choice.label) for b in self if b.index!=None]

    def update(self,ev):

        if self:
            if self.choice: self.choice = None
            if ev.type in (MOUSEMOTION,MOUSEBUTTONUP):
                boxindexlist = Rect(ev.pos,(0,0)).collidelistall(self)
                if boxindexlist:
                    self.boxindex = boxindexlist[-1]
                    box           = self[self.boxindex]
                    if ev.type == MOUSEBUTTONUP and ev.button == 1 and isinstance(box.choice,str) and not box.exc_index and self[-1].index != None:
                        self.choice = self.select
                        return self.clear()
                    if box.update(ev) or (len(self)-1 != boxindexlist[-1] and self[-1].index != None):
                        ret = [self.pop().clear()for _ in range(self.boxindex+1,len(self))]+[box.clear()]
                        box.draw()
                        if not box.exc_index:
                            if callable(box.choice):
                                dyn = box.choice()
                                dyn.set_at(*box.hlRect.inflate(2,2).topright)
                                self.append(dyn)
                                return ret+[dyn.draw()]
                            if isinstance(box.choice,Menu):
                                box.choice.set_at(*box.hlRect.inflate(2,2).topright)
                                self.append(box.choice)
                                return ret+[box.choice.draw()]
                        return ret

                else:
                    if ev.type == MOUSEBUTTONUP:
                        return self.clear()
                    self.boxindex = None
                    if self[-1].index != None:
                        self[-1].index = None
                        self[-1].clear()
                        self[-1].draw()
                        return [self[-1]]
        return []

    def redraw(self):
        for menu in self:
            menu.draw()
            return self

class MenuFix(MenuSystem,object):

    def clear(self):
        if len(self) > 1:
            ret = [self.pop().clear() for _ in range(1,len(self))]
            self.boxindex = None
            self[0].index = None
            self[0].clear()
            return ret+[self[0].draw()]
        return []

class MenuBar(MenuSystem,object):

    def __init__(self):
        self.lineheigth = FONT.get_height()
        self.rect = Rect(0,0,DISPLAYRECT.width,self.lineheigth)

    def set(self,menuboxlist=None):
        self.bg = DISPLAY.subsurface(self.rect).copy()
        if menuboxlist:
            self.menuboxlist = menuboxlist
            x = 0
            self.rects = []
            for item in self.menuboxlist:
                w,h = FONT.size(item.label)
                self.rects.append(Rect(x,0,w+self.lineheigth,h))
                x = self.rects[-1].right
        self.index = -1
        self.draw()
        self.choice = None
        return self.rect



    def update(self,ev):
        if self.choice: self.choice = None
        ret = super(MenuBar,self).update(ev)
        if ret and self.choice:
            self.choice = [(self.index,self.menuboxlist[self.index].label)]+self.choice

        if "pos" in ev.dict:
            if not self or self.boxindex == None:
                if ev.type == MOUSEBUTTONUP:
                    if self.index > -1 and ev.button == 1:
                        if not ret:
                            ret = super(MenuBar,self).set(self.menuboxlist[self.index],self.rects[self.index].bottomleft)
                    elif ret:
                        ret += [self.draw()]
                index = Rect(ev.pos,(0,0)).collidelist(self.rects)
                if index != self.index:
                    if not self:
                        self.index = index
                        ret += [self.draw()]
                    elif index > -1:
                        self.index = index
                        ret = self.clear()
                        ret += [self.draw()]
                        ret += super(MenuBar,self).set(self.menuboxlist[self.index],self.rects[self.index].bottomleft)
            return ret

    def undraw(self):
        DISPLAY.blit(self.bg,self.rect)
        return self.rect

    def draw(self):
        DISPLAY.blit(self.bg,self.rect)
        gfxdraw.box(DISPLAY,self.rect,BGCOLOR)
        gfxdraw.vline(DISPLAY,self.rect.left,self.rect.top,self.rect.bottom-1,BORDER_LEFT)
        gfxdraw.hline(DISPLAY,self.rect.left,self.rect.right-1,self.rect.top,BORDER_LEFT)
        gfxdraw.vline(DISPLAY,self.rect.right-1,self.rect.top+1,self.rect.bottom-1,BORDER_RIGHT)
        gfxdraw.hline(DISPLAY,self.rect.left+1,self.rect.right-1,self.rect.bottom-1,BORDER_RIGHT)
        x = self.rect.x + self.lineheigth/3
        if self.index > -1:
            gfxdraw.box(DISPLAY,self.rects[self.index].inflate(-2,-2),BGHIGHTLIGHT)
        for item in self.menuboxlist:
            x = DISPLAY.blit(FONT.render(item.label,1,FGCOLOR),(x,self.rect.y)).right+self.lineheigth
        return self.rect


class MenuChoice(MenuSystem,object):

    def __init__(self):
        self.lineheigth = FONT.get_height()


    def set(self,menu,pos,w=None):
        if w == None:
            self.wd = max((menu._width,FONT.size(menu.label)[0]+menu.lineheight*2))
        else:
            self.wd = w
        self.rect = Rect(pos,(self.wd,self.lineheigth))
        self.bg = DISPLAY.subsurface(self.rect).copy()
        self.menu = menu
        self.index = -1
        #self.update(event.Event(MOUSEMOTION,{'pos':mouse.get_pos()}))
        self.mouse_in = self.rect.collidepoint(mouse.get_pos())
        self.draw()
        self.choice = None
        return self.rect


    def update(self,ev):
        ret = super(MenuChoice,self).update(ev)
        if ret and self.choice:
            self.menu.label = self.choice[-1][1]
        if "pos" in ev.dict:
            t = self.mouse_in
            self.mouse_in = self.rect.collidepoint(ev.pos)
            if (t != self.mouse_in or ret) and not self:
                ret += [self.draw()]
            if ev.type == MOUSEBUTTONUP and ev.button == 1 and self.mouse_in and not ret:
                ret = super(MenuChoice,self).set(self.menu,self.rect.bottomleft,w=self.wd,force_pos=True)
        return ret

    def draw(self):
        DISPLAY.blit(self.bg,self.rect)
        gfxdraw.box(DISPLAY,self.rect,BGCOLOR)
        gfxdraw.vline(DISPLAY,self.rect.left,self.rect.top,self.rect.bottom-1,BORDER_LEFT)
        gfxdraw.hline(DISPLAY,self.rect.left,self.rect.right-1,self.rect.top,BORDER_LEFT)
        gfxdraw.vline(DISPLAY,self.rect.right-1,self.rect.top+1,self.rect.bottom-1,BORDER_RIGHT)
        gfxdraw.hline(DISPLAY,self.rect.left+1,self.rect.right-1,self.rect.bottom-1,BORDER_RIGHT)
        x = self.rect.x + self.lineheigth/3
        if self.mouse_in or self: gfxdraw.box(DISPLAY,self.rect.inflate(-2,-2),BGHIGHTLIGHT)
        clipxy = DISPLAY.get_clip()
        DISPLAY.set_clip(self.rect.inflate(-self.lineheigth/3*2,-2))
        DISPLAY.blit(FONT.render(self.menu.label,1,FGCOLOR),(x,self.rect.y))
        DISPLAY.set_clip(clipxy)
        return self.rect

    def undraw(self):
        DISPLAY.blit(self.bg,self.rect)
        return self.rect




class Button(Rect,object):

    def __init__(self,label,w,h):
        self.label = label
        Rect.__init__(self,0,0,w,h)

    def update(self,ev):
        if self.active:
            if ev.type == MOUSEMOTION:
                if not self._over and self.collidepoint(ev.pos):
                    self._over = True
                    if ev.buttons[0]:
                        self.pressed = True
                    self.draw()
                    return True
                elif self._over and not self.collidepoint(ev.pos):
                    self._over   = False
                    self.pressed = False
                    self.draw()
                    return True
            if ev.type == MOUSEBUTTONDOWN and ev.button == 1 and self.collidepoint(ev.pos):
                self.pressed = True
                self.draw()
                return True
            elif ev.type == MOUSEBUTTONUP and ev.button == 1 and self.collidepoint(ev.pos):
                self.pressed = False
                self.clicked   = True
                self._switch = not self._switch
                self.draw()
                return True
            elif ev.type == ACTIVEEVENT and self._over:
                self.pressed = False
                self._over = False
                self.draw()
                return True

    def set(self,type=BUTTON,active=True,switch=False,switchlabel=None):
        self._bg = DISPLAY.subsurface(self).copy()
        self.type = type
        self.switchlabel = switchlabel if switchlabel != None else self.label
        if not hasattr(self,"_switch"): self._switch = switch
        if not hasattr(self,"_active"): self.active = active
        else: self.draw()

    def draw(self):
        def draw(bgcolor,fgcolor,topleftcolor,bottomrightcolor):
            gfxdraw.box(DISPLAY,self,bgcolor)
            gfxdraw.vline(DISPLAY,self.left,self.top,self.bottom-1,topleftcolor)
            gfxdraw.hline(DISPLAY,self.left,self.right-1,self.top,topleftcolor)
            gfxdraw.vline(DISPLAY,self.right-1,self.top+1,self.bottom-1,bottomrightcolor)
            gfxdraw.hline(DISPLAY,self.left+1,self.right-1,self.bottom-1,bottomrightcolor)
            clipxy = DISPLAY.get_clip()
            DISPLAY.set_clip(self.inflate(-2,-2))
            if self.type == SWITCH:
                label = FONT.render(self.label if not self.switch else self.switchlabel,1,fgcolor)
            else:
                label = FONT.render(self.label,1,fgcolor)
            DISPLAY.blit(label,label.get_rect(center=self.center))
            DISPLAY.set_clip(clipxy)

        DISPLAY.blit(self._bg,self)
        if not self.active:
            draw(BGCOLOR,FGCOLOR,BORDER_LEFT,BORDER_RIGHT)
        elif self.pressed:
            draw(BGHIGHTLIGHT,FGCOLOR,BORDER_RIGHT,BORDER_LEFT)
        elif self._over:
            if self.type == SWITCH and self.switch:
                draw(BGHIGHTLIGHT,FGCOLOR,BORDER_RIGHT,BORDER_LEFT)
            else:
                draw(BGHIGHTLIGHT,FGCOLOR,BORDER_LEFT,BORDER_RIGHT)
        elif self.type == SWITCH and self.switch:
            draw(BGCOLOR,FGCOLOR,BORDER_RIGHT,BORDER_LEFT)
            #draw(BORDER_LEFT,FGCOLOR,BORDER_RIGHT,BGCOLOR)
        else:
            draw(BGCOLOR,FGCOLOR,BORDER_LEFT,BORDER_RIGHT)
        display.update(self)

    @property
    def active(self):
        return self._active
    @active.setter
    def active(self,value):
        self._active = value
        self.pressed = False
        self.clicked = False
        event.pump()
        self._over   = self.collidepoint(mouse.get_pos())
        if self._over and mouse.get_pressed()[0]:
            self.pressed = True
        if hasattr(self,"_bg"):
            self.draw()

    @property
    def clicked(self):
        if self._click:
            self._click = False
            return True
    @clicked.setter
    def clicked(self,value):
        self._click = value

    @property
    def switch(self):
        return self._switch
    @switch.setter
    def switch(self,value):
        self._switch = value
        self.draw()


