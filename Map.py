import random
from pygame import Rect
from Player import Player
from Enemy import Enemy


class MapScreen:
    def __init__(self, screenHandler, screen, keys, clock):
        self.clock = clock
        self.screenHandler = screenHandler
        self.screen = screen
        self.keys = keys
        self.map_width = 2000
        self.map_height = 2000
        # Define regions as (x1, y1, x2, y2, color, area_name)
        self.regions = [
            (200, 200, 500, 500, (0, 0, 255, 100), 'slime_area'),        # Region1: Blue for Slime
            (1200, 200, 1500, 500, (128, 128, 128, 100), 'wolf_area'),   # Region2: Gray for Wolf
            (200, 1200, 500, 1500, (0, 255, 0, 100), 'goblin_area')      # Region3: Green for Goblin
        ]

        self.enemies = []
        self.SpawnEnemies()
        # Create player at the center of the map
        self.player = Player('player',
                            (self.map_width // 2, self.map_height // 2),
                            self.clock, self.screenHandler)
        # Track movement speed
        self.player.speed_x = 0
        self.player.speed_y = 0
        # Track pressed keys
        self.pressed_keys = set()
        # Camera
        self.camera_x = 0
        self.camera_y = 0
        # Attack cooldown (for input spam limiting)
        self.can_attack = True
        self.attack_cooldown = 0.5  # 0.5 seconds cooldown

    def SpawnEnemies(self):
        for region_bounds in self.regions:
            x1, y1, x2, y2, color, area_name = region_bounds
            if area_name == 'slime_area':
                count = 2
                name = 'slime'
            elif area_name == 'wolf_area':
                count = 3
                name = 'wolf'
            else:  # 'goblin_area'
                count = 1
                name = 'goblin'

            for i in range(count):
                x = random.randint(x1, x2)
                y = random.randint(y1, y2)
                enemy = Enemy(name, (x, y), self.clock,self)
                enemy.SetRegion((x1, y1, x2, y2))
                self.enemies.append(enemy)

    def onkeydown(self, key):
        self.pressed_keys.add(key)
        self.UpdateSpeed()

    def onkeyup(self, key):
        self.pressed_keys.discard(key)
        self.UpdateSpeed()

    def UpdateSpeed(self):
        self.player.speed_x = 0
        self.player.speed_y = 0
        if self.keys.LEFT in self.pressed_keys:
            self.player.speed_x -= self.player.speed
        if self.keys.RIGHT in self.pressed_keys:
            self.player.speed_x += self.player.speed
        if self.keys.UP in self.pressed_keys:
            self.player.speed_y -= self.player.speed
        if self.keys.DOWN in self.pressed_keys:
            self.player.speed_y += self.player.speed

    def update(self):
        # Apply speed to player position
        self.player.x += self.player.speed_x
        self.player.y += self.player.speed_y

        # Clamp player to map bounds
        self.player.x = max(0, min(self.player.x, self.map_width))
        self.player.y = max(0, min(self.player.y, self.map_height))

        # Camera follow
        self.camera_x = self.player.x - self.screen.width / 2
        self.camera_y = self.player.y - self.screen.height / 2
        # Clamp camera to map bounds
        self.camera_x = max(0, min(self.camera_x, self.map_width - self.screen.width))
        self.camera_y = max(0, min(self.camera_y, self.map_height - self.screen.height))

        # Attack with Z key
        if self.keys.Z in self.pressed_keys:
            self.attack()

        # Update enemies only if they are within a margin outside the screen
        margin = 200  # pixels
        for enemy in self.enemies:
            if (enemy.x >= self.camera_x - margin and
                enemy.x <= self.camera_x + self.screen.width + margin and
                enemy.y >= self.camera_y - margin and
                enemy.y <= self.camera_y + self.screen.height + margin):
                enemy.update((self.player.x, self.player.y), self.player)

    def attack(self):
        self.player.Attack(self.enemies)


    def draw_player_health_bar(self):
        max_health = self.player.max_health
        bar_width = 200
        bar_height = 20
        margin = 10

        # Background (border)
        bg_rect = Rect((margin, margin), (bar_width, bar_height))
        self.screen.draw.filled_rect(bg_rect, (0, 0, 0))

        # Clamp health and compute ratio
        health = max(0, min(self.player.health, max_health))
        ratio = health / max_health
        fill_width = int(bar_width * ratio)

        # Inner filled bar
        fg_rect = Rect((margin + 2, margin + 2),
                      (max(0, fill_width - 4), bar_height - 4))
        # Green bar
        self.screen.draw.filled_rect(fg_rect, (0, 200, 0))

    def draw(self):
        # Draw background color for non-region areas
        background_color = (255, 255, 200)  # Subtle yellow
        background_rect = Rect((0, 0), (self.map_width, self.map_height))
        self.screen.draw.filled_rect(background_rect, background_color)

        # Draw a grid pattern
        grid_color = (200, 200, 180)
        grid_spacing = 50
        for x in range(0, self.map_width, grid_spacing):
            self.screen.draw.line((x - self.camera_x, 0 - self.camera_y),
                                 (x - self.camera_x, self.map_height - self.camera_y),
                                 grid_color)
        for y in range(0, self.map_height, grid_spacing):
            self.screen.draw.line((0 - self.camera_x, y - self.camera_y),
                                 (self.map_width - self.camera_x, y - self.camera_y),
                                 grid_color)

        # Draw regions
        for region_bounds in self.regions:
            x1, y1, x2, y2, color, area_name = region_bounds
            rect = Rect((x1 - self.camera_x, y1 - self.camera_y), (x2 - x1, y2 - y1))
            self.screen.draw.filled_rect(rect, color[:3])

        # Draw enemies and their zones only if they are near the camera
        margin = 200
        for enemy in self.enemies:
            if (enemy.x >= self.camera_x - margin and
                enemy.x <= self.camera_x + self.screen.width + margin and
                enemy.y >= self.camera_y - margin and
                enemy.y <= self.camera_y + self.screen.height + margin):
                enemy.draw(self.screen, self.camera_x, self.camera_y)

        # Draw player and attack range
        self.player.draw(self.screen, self.camera_x, self.camera_y)

        # Draw UI: player health bar
        self.draw_player_health_bar()

    def EndGame(self):
        self.screenHandler.ChangeScreen("GameOverScreen")

    def EnemyDeath(self, enemy):
        if enemy in self.enemies:
            self.enemies.remove(enemy)
