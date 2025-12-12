# ScreenHandler.py

from OptionsMenu import Options
from MainMenu import MainMenu
from Map import MapScreen
from GameOverScreen import GameOverScreen

class ScreenHandler:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(ScreenHandler, cls).__new__(cls)
        return cls._instance

    def __init__(self, screen, keys,clock,music):
        if not hasattr(self, 'initialized'):
            self.screen = screen
            self.currentScreen = None
            self.keys = keys
            self.clock = clock
            self.music = music
            self.startup()
            self.previousScreen = None
            self.initialized = True

    def startup(self):
        self.currentScreen = MainMenu(self, self.screen, self.keys)

    def update(self):
        if hasattr(self.currentScreen, 'update'):
            self.currentScreen.update()

    def draw(self):
        if self.currentScreen:
            self.currentScreen.draw()

    def onkeydown(self, key):
        if hasattr(self.currentScreen, 'onkeydown'):
            self.currentScreen.onkeydown(key)

    def onkeyup(self, key):
        if hasattr(self.currentScreen, 'onkeyup'):
            self.currentScreen.onkeyup(key)

    def onmousedown(self, pos):
        if hasattr(self.currentScreen, 'onmousedown'):
            self.currentScreen.onmousedown(pos)

    def onmousemove(self, pos):
        if hasattr(self.currentScreen, 'onmousemove'):
            self.currentScreen.onmousemove(pos)

    def ChangeScreen(self, screen):
        newScreen = self.InitiateNewScreen(screen)
        self.previousScreen = self.currentScreen
        self.currentScreen = newScreen
        if hasattr(newScreen, 'screenHandler'):
            newScreen.screenHandler = self

    def ReturnToPreviousScreen(self):
        if self.previousScreen:
            self.currentScreen = self.previousScreen
            self.previousScreen = None

    def InitiateNewScreen(self, screen):
        if screen == "Options":
            newScreen = Options(self, self.screen, self.keys, self.music)
        elif screen == "MainMenu":
            newScreen = MainMenu(self, self.screen, self.keys)
        elif screen == "MapScreen":
            newScreen = MapScreen(self, self.screen, self.keys,self.clock)
        elif screen == "GameOverScreen":
            newScreen = GameOverScreen(self, self.screen, self.keys)
        else:
            print(f"Unknown screen: {screen}, defaulting to MainMenu")
            newScreen = MainMenu(self, self.screen, self.keys)
        return newScreen