# JsonHandler.py

import json
import os

class JsonHandler:
    def __init__(self,file):
        self.File = file
        self.CheckJson()



    def CreateJson(self):
        defaultConfig = {
            "ScreenWidthOptions": [800, 1024, 1280, 1920],
            "ScreenHeightOptions": [600, 768, 720, 1080],
            "screenWidth": 800,
            "screenHeight": 600,
            "volume": 50,
            "difficulty": 1
        }
        self.config = defaultConfig
        self.SaveConfig()

    def CheckJson(self):
        json_folder = os.path.join(os.path.dirname(__file__), 'Json')
        file_path = os.path.join(json_folder, self.File)
        print(f"Checking for config file at: {file_path}")
        if os.path.exists(file_path):
            print("Config file found. Loading...")
            with open(file_path, "r") as f:
                self.config = json.load(f)
        else:
            print("Config file not found. Creating default config...")
            self.CreateJson()

    def SaveConfig(self):
        with open(self.File, "w") as f:
            json.dump(self.config, f, indent=4)

    def GetJson(self):
        return self.config

    def SetJson(self, key, value):
        self.config[key] = value
        self.SaveConfig()
