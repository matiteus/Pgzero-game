from pgzero.actor import Actor


class MainMenu:
    def __init__(self, screenHandler, screen, keys):
        self.screenHandler = screenHandler
        self.screen = screen
        self.options = ["New Game", "Load Game", "Config", "Exit"]
        self.selectedOption = 0
        self.keys = keys
        self.background = Actor('main_menu_bg')

    def update(self):
        pass

    def draw(self):
        self.screen.clear()
        self.background.draw()
        # Main menu title centered
        title_y = self.screen.height // 2 - 100
        self.screen.draw.text("Main Menu", (self.screen.width // 2 - 100, title_y), fontsize=60, color="black")

        y = self.screen.height // 2
        for i, option in enumerate(self.options):
            if i == self.selectedOption:
                color = "yellow"
            else:
                color = "black"
            # Menu options centered
            self.screen.draw.text(option, (self.screen.width // 2 - 100, y), fontsize=40, color=color)
            y += 50

    def onkeydown(self, key):
        if key == self.keys.UP:
            self.selectedOption = (self.selectedOption - 1) % len(self.options)
        elif key == self.keys.DOWN:
            self.selectedOption = (self.selectedOption + 1) % len(self.options)
        elif key == self.keys.RETURN:
            if self.selectedOption == 0:  # New Game
                self.StartNewGame()
            elif self.selectedOption == 1:  # Load Game
                self.LoadGame()
            elif self.selectedOption == 2:  # Config
                self.OpenOptions()
            elif self.selectedOption == 3:  # Exit
                self.Exit()

    def onmousedown(self, pos):
        x, y = pos
        start_y = self.screen.height // 2
        option_height = 50

        for i, option in enumerate(self.options):
            oy = start_y + i * option_height
            if self.screen.width // 2 - 100 <= x <= self.screen.width // 2 + 100 and oy <= y <= oy + 40:
                self.selectedOption = i
                self._activate_option(i)
                break

    def _activate_option(self, index):
        if index == 0:  # new game
            self.StartNewGame()
        elif index == 1:
            self.LoadGame()
        elif index == 2:  # Config
            self.OpenOptions()
        elif index == 3:  # Exit
            self.Exit()

    def onmousemove(self, pos):
        x, y = pos
        start_y = self.screen.height // 2
        option_height = 50

        for i in range(len(self.options)):
            oy = start_y + i * option_height
            if self.screen.width // 2 - 100 <= x <= self.screen.width // 2 + 100 and oy <= y <= oy + 40:
                self.selectedOption = i
                break

    def StartNewGame(self):
        print("Starting New Game...")
        self.screenHandler.ChangeScreen("MapScreen")

    def LoadGame(self):
        print("Loading Game...")

    def OpenOptions(self):
        self.screenHandler.ChangeScreen("Options")

    def Exit(self):
        print("Exiting Game...")
        exit()
