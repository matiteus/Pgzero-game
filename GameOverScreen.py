from pgzero.actor import Actor
from pygame import Rect


class GameOverScreen:
    def __init__(self, screenHandler, screen, keys):
        self.screenHandler = screenHandler
        self.screen = screen
        self.keys = keys

        self.background = Actor('game_over_bg')
        self.gameOverText = "Game Over"

        # buttons centered
        cx = screen.width // 2
        cy = screen.height // 2
        self.buttons = [
            {
                "text": "MainMenu",
                "rect": Rect(cx - 100, cy, 200, 50),
                "action": "MainMenu",
            },
            {
                "text": "Exit",
                "rect": Rect(cx - 100, cy + 70, 200, 50),
                "action": "Exit",
            },
        ]

        self.selectedButton = 0       
        self.pendingEnter = False  
        self.pendingClickIndex = None 

    def update(self):
        if self.pendingEnter:
            self.pendingEnter = False
            self._buttonAction(self.buttons[self.selectedButton]["action"])

        # handle mouse click selection (if any)
        if self.pendingClickIndex is not None:
            idx = self.pendingClickIndex
            self.pendingClickIndex = None
            if 0 <= idx < len(self.buttons):
                self._buttonAction(self.buttons[idx]["action"])

    def draw(self):
        # background
        self.background.draw()

        # game over text
        self.screen.draw.text(
            self.gameOverText,
            midtop=(self.screen.width // 2, self.screen.height // 4),
            fontsize=64,
            color="black",
            owidth=1,
            ocolor="black",
        )

        # buttons
        for i, button in enumerate(self.buttons):
            rect = button["rect"]
            focused = (i == self.selectedButton)
            bg_color = (230, 230, 0) if focused else (200, 200, 200)
            text_color = (0, 0, 0)

            self.screen.draw.filled_rect(rect, bg_color)
            self.screen.draw.text(
                button["text"],
                center=rect.center,
                fontsize=40,
                color=text_color,
            )

    def onkeydown(self, key):
        # Esc quits game
        if key == self.keys.ESCAPE:
            raise SystemExit

        if key == self.keys.UP:
            if self.selectedButton > 0:
                self.selectedButton -= 1
        elif key == self.keys.DOWN:
            if self.selectedButton < len(self.buttons) - 1:
                self.selectedButton += 1
        elif key in (self.keys.RETURN, self.keys.K_RETURN, self.keys.ENTER):
            # flag handled in update()
            self.pendingEnter = True

    def onkeyup(self, key):
        pass

    def onmousedown(self, pos):
        for i, button in enumerate(self.buttons):
            if button["rect"].collidepoint(pos):
                self.pendingClickIndex = i
                break

    def onmousemove(self, pos):
        for i, button in enumerate(self.buttons):
            if button["rect"].collidepoint(pos):
                self.selectedButton = i
                break

    def _buttonAction(self, action):
        if action == "MainMenu":
            self.screenHandler.ChangeScreen("MainMenu")
        elif action == "Exit":
            raise SystemExit
