from ..pgu.gui.input import *
from ..MenuSystem import *
from option_types import *

class MainOptionMenu:
    def __init__(self):
        MenuSystem.init()
        self.menu_bar = MenuSystem.MenuBar()
        self.display_height = self.menu_bar.rect.height

        self.option_list = [RNGSeedOpt]
        self.menu_dict = dict()
        self.option_actions = dict()
        for option in self.option_list:
            menu_type = option.menu_type
            if not menu_type in self.menu_dict.keys():
                self.menu_dict[menu_type] = []
            self.menu_dict[menu_type].append(option)
            self.option_actions[option.menu()] = option.option_event
        menu_top_level = map(lambda header: 
                           MenuSystem.Menu(header, 
                           map(lambda opt: opt.menu(), self.menu_dict[header])), 
                         self.menu_dict.keys())
        self.menu_bar.set(menu_top_level)

    def process_event(self, event):
        self.menu_bar.update(event)
        self.update()
        if self.menu_bar.choice:
            choice_label = self.menu_bar.choice_label
            self.option_actions[choice_label[1]]()

    def update(self):
        pygame.display.update(self.menu_bar)