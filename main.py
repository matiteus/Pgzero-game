import pgzrun
from ScreenHandler import ScreenHandler
from JsonHandler import JsonHandler

screenHandler = None

def update():
    global screenHandler
    if screenHandler is None:
        screenHandler = ScreenHandler(screen, keys, clock,music)
    screenHandler.update()

def draw():
    screenHandler.draw()

def on_key_down(key):
    screenHandler.onkeydown(key)

def on_mouse_down(pos):
    screenHandler.onmousedown(pos)

def on_mouse_move(pos):
    screenHandler.onmousemove(pos)

def on_key_up(key):
    screenHandler.onkeyup(key)

def InitialLoad():
    configs = JsonHandler("config.json")
    configs.CheckJson()
    configJson = configs.GetJson()
    WIDTH = configJson["screenWidth"]
    HEIGHT = configJson["screenHeight"]
    valid_sizes = configJson["ScreenOptions"]
    volume = configJson["volume"]
    music.set_volume(volume/100)
    music.play('game_song')
    
    if not any(size["width"] == WIDTH and size["height"] == HEIGHT for size in valid_sizes):
        print("Invalid screen size in config, reverting to default 800x600")
        WIDTH, HEIGHT = 800, 600

 

    return WIDTH, HEIGHT

WIDTH, HEIGHT = InitialLoad()
pgzrun.go()
