import pgzrun
from JsonHandler import JsonHandler

class Options:
    def __init__(self, screenHandler, screen, keys, music):
        self.screen = screen
        self.screenHandler = screenHandler
        self.keys = keys
        self.music = music
        self.jsonHandler = JsonHandler("config.json")
        self.configs = self.jsonHandler.GetJson()
        self.screenOptions = self.configs["ScreenOptions"]
        self.currentScreenIndex = next((i for i, opt in enumerate(self.screenOptions) if opt["width"] == self.configs["screenWidth"] and opt["height"] == self.configs["screenHeight"]), 0)
        self.difficulty_labels = ["Easy", "Medium", "Difficult"]
        self.difficulty_values = [1, 2, 3]
        self.options = [
            {"name": "screenSize", "label": "Screen Size", "value": self.currentScreenIndex, "options": self.screenOptions},
            {"name": "volume", "label": "Volume", "value": self.configs["volume"], "min": 0, "max": 100},
            {"name": "difficulty", "label": "Difficulty", "value": self.difficulty_values.index(self.configs["difficulty"]), "options": self.difficulty_labels}
        ]
        self.selectedOption = 0
        self.buttons = ["Save", "Cancel"]

    def draw(self):
        self.screen.clear()
        self.screen.draw.text("Options", (100, 50), fontsize=40, color="white")
        y = 100
        for i, opt in enumerate(self.options):
            color = "yellow" if i == self.selectedOption else "white"
            if "options" in opt:
                selected = opt["options"][opt["value"]]
                if opt["name"] == "screenSize":
                    value = f"{selected['width']}x{selected['height']}"
                else:
                    value = selected
            else:
                value = opt["value"]
            self.screen.draw.text(f"{opt['label']}: {value}", (100, y), fontsize=30, color=color)
            self.screen.draw.text("<", (400, y), fontsize=30, color=color)
            self.screen.draw.text(">", (450, y), fontsize=30, color=color)
            y += 40
        save_color = "yellow" if self.selectedOption == len(self.options) else "white"
        self.screen.draw.text("Save", (100, 500), fontsize=30, color=save_color)
        cancel_color = "yellow" if self.selectedOption == len(self.options) + 1 else "white"
        self.screen.draw.text("Cancel", (self.screen.width - 150, 500), fontsize=30, color=cancel_color)

    def onkeydown(self, key):
        if key == self.keys.UP:
            self.selectedOption = (self.selectedOption - 1) % (len(self.options) + len(self.buttons))
        elif key == self.keys.DOWN:
            self.selectedOption = (self.selectedOption + 1) % (len(self.options) + len(self.buttons))
        elif key == self.keys.LEFT:
            if self.selectedOption < len(self.options):
                opt = self.options[self.selectedOption]
                if "options" in opt:
                    opt["value"] = (opt["value"] - 1) % len(opt["options"])
                else:
                    opt["value"] = max(opt["min"], min(opt["max"], opt["value"] - 10))
                self.update_volume()
            elif self.selectedOption >= len(self.options):
                self.selectedOption = (self.selectedOption - 1) % (len(self.options) + len(self.buttons))
        elif key == self.keys.RIGHT:
            if self.selectedOption < len(self.options):
                opt = self.options[self.selectedOption]
                if "options" in opt:
                    opt["value"] = (opt["value"] + 1) % len(opt["options"])
                else:
                    opt["value"] = max(opt["min"], min(opt["max"], opt["value"] + 10))
                self.update_volume()
            elif self.selectedOption >= len(self.options):
                self.selectedOption = (self.selectedOption + 1) % (len(self.options) + len(self.buttons))
        elif key == self.keys.RETURN:
            if self.selectedOption == len(self.options):  # Save
                for opt in self.options:
                    if opt["name"] == "screenSize":
                        selected = opt["options"][opt["value"]]
                        self.jsonHandler.SetJson("screenWidth", selected["width"])
                        self.jsonHandler.SetJson("screenHeight", selected["height"])
                    elif opt["name"] == "difficulty":
                        self.jsonHandler.SetJson("difficulty", self.difficulty_values[opt["value"]])
                    else:
                        self.jsonHandler.SetJson(opt["name"], opt["value"])
                self.screenHandler.ReturnToPreviousScreen()
            elif self.selectedOption == len(self.options) + 1:  # Cancel
                self.screenHandler.ReturnToPreviousScreen()
        elif key == self.keys.ESCAPE:
            self.screenHandler.ReturnToPreviousScreen()

    def onmousedown(self, pos):
        y = 100
        for i, opt in enumerate(self.options):
            if 100 <= pos[0] <= 500 and y <= pos[1] <= y + 40:
                self.selectedOption = i
                if 400 <= pos[0] <= 430:  # Left arrow
                    if "options" in opt:
                        opt["value"] = (opt["value"] - 1) % len(opt["options"])
                    else:
                        opt["value"] = max(opt["min"], min(opt["max"], opt["value"] - 10))
                    self.update_volume()
                elif 450 <= pos[0] <= 480:  # Right arrow
                    if "options" in opt:
                        opt["value"] = (opt["value"] + 1) % len(opt["options"])
                    else:
                        opt["value"] = max(opt["min"], min(opt["max"], opt["value"] + 10))
                    self.update_volume()
                return
            y += 40
        # Handle Save and Cancel buttons
        if 100 <= pos[0] <= 250 and 500 <= pos[1] <= 540:
            self.selectedOption = len(self.options)
        elif self.screen.width - 150 <= pos[0] <= self.screen.width - 10 and 500 <= pos[1] <= 540:
            self.selectedOption = len(self.options) + 1


    def update_volume(self):
        volume = self.options[1]["value"] / 100
        self.music.set_volume(volume)

