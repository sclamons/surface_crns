from ..MenuSystem import *
from ..pgu import gui
import pygame

class AbstractOption(object):
    '''
    Interface for option classes. Methods to implement:

    option_event() - Do something when a menu button was clicked for 
                                this option, then return the value for that 
                                option.
    from_manifest(options)   - Do something based on a manifest file's options
                                dictionary. Usually involves calling 
                                self.option_event.
    menu()                   - Return a MenuSystem.Menu for the option. See the
                                MenuSystem pygame package by Joel Murielle for 
                                details.
    '''
    @classmethod
    def option_event(cls):
        raise NotImpelementedError("No method 'option_event' specified for " + 
                                   "option of class " + cls.__name__)

    @classmethod
    def from_manifest(cls, options):
        raise NotImpelementedError("No method 'from_manifest' specified for " + 
                                   "option of class " + cls.__name__)

    @classmethod
    def menu(cls):
        raise NotImpelementedError("No method 'menu' specified for " + 
                                   "option of class " + cls.__name__)

'''class SpeedupFactorOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'Simulation'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME>

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        return 'Speedup Factor'


class DebugOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'Simulation'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        return 'Debug on/off'
'''

class RNGSeedOpt(AbstractOption):
    menu_type = 'Simulation'

    @classmethod
    def option_event(cls):
        print("!")
        ##Using Desktop instead of App provides the GUI with a background.
        ##::
        app = gui.Desktop()
        app.connect(gui.QUIT,app.quit,None)
        ##

        ##The container is a table
        ##::
        c = gui.Table(width=200,height=120)
        ##

        ##The button CLICK event is connected to the app.close method.  The button will fill the whole table cell.
        ##::
        e = gui.Button("Quit")
        e.connect(gui.CLICK,app.quit,None)
        c.add(e,0,0)
        ##

        app.run(c)

        pygame.display.update()
        '''rng_form = Form()
        rng_input_widget = Input("Type seed here", name='rng_input')
        rng_form.open()
        try:
            print(rng_form['rng_input'].value)
            seed_value = int(rng_form['rng_input'].value)
            return seed_value
        except ValueError:
            title = Label("Error!")
            error_msg = Label("RNG seed must be an integer.")
            error_dialog = Dialog(title, error_msg)
            error_dialog.open()
            continue'''

    @classmethod
    def from_manifest(cls, options):
        if 'rng_seed' in options:
            seed_value = int(options['rng_seed'])
        else: 
            seed_value = None
        return seed_value

    @classmethod
    def menu(cls):
        return 'RNG Seed'

'''
class MaxDurationOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'Simulation'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        return 'Maximum Duration'


class CaptureRateOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'Movie'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        return 'Capture Rate'


class FPSOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'Display'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        return 'FPS'


class DisplayTextOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'Display'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        return 'State Labels On/Off'


class ColormapOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'File'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        'Load Colormap'


class SimulationTypeOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'NoMenu'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>


class UpdateRuleOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'File'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        "Load Update Rule"


class TransitionRulesOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'File'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        'Load Transition Rule Set'


class InitStateOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'File'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        'Load Initial State'


class PixelsPerNodeOpt(AbstractOption):
    def __init__(self):
        self.menu_type = 'Display'

    @classmethod
    def option_event(cls):
        <IMPLEMENT ME

    @classmethod
    def from_manifest(cls, options):
        <IMPLEMENT ME>

    @classmethod
    def menu(cls):
        'Node Display Size'
'''