import random
from pgzero.actor import Actor
from pgzero.loaders import sounds
from pygame import Rect
from JsonHandler import JsonHandler


class Enemy(Actor):
    def __init__(self, name, pos, clock,mapScreen):
        super().__init__(name, pos)
        self.clock = clock
        self.name = name
        self.image = name + '.png'
        self.anchor = ('center', 'center')
        self.statusFile = f"{self.name}_status.json"
        self.loadStatus()
        self.region = None
        self.regionCenter = None
        self.moveDirection = None
        self.passive = True
        self.canAttack = True
        self.mapScreen = mapScreen

        # sprite visual offset (does not affect logic)
        self.spriteOffsetX = -10
        self.spriteOffsetY = -22

        # track last sound played for this enemy
        self.currentSound = None

        # Schedule direction change every 1.5 seconds
        self.clock.schedule_interval(self.PickRandomRegion, self.attackCooldown)

    # public called by Map
    def SetRegion(self, region):
        self.region = region
        self.regionCenter = (
            (region[0] + region[2]) / 2,
            (region[1] + region[3]) / 2
        )

    # private
    def loadStatus(self):
        helper = JsonHandler(self.statusFile)
        status = helper.GetJson()
        self.speed = status['speed']
        self.detectionArea = status['detection_area']
        self.battleArea = status['battle_area']
        self.health = status['health']
        self.attackPower = status['attack_power']
        self.attackCooldown = status.get('attack_cooldown')
        self.soundPrefix = status.get('name', '').lower()

    # attack collider (box) around enemy, size based on battleArea
    def GetAttackRect(self):
        size = self.battleArea * 2
        return Rect(
            self.x - self.battleArea,
            self.y - self.battleArea,
            size,
            size
        )

    # ------------------- Movement and AI controls ------------------------
    def PickRandomRegion(self):
        if not self.region or not self.regionCenter:
            self.moveDirection = random.choice(['left', 'right', 'up', 'down'])
        else:
            dx = self.regionCenter[0] - self.x
            dy = self.regionCenter[1] - self.y
            distance = (dx**2 + dy**2)**0.5
            if distance > 100:
                self.moveDirection = 'left' if abs(dx) > abs(dy) and dx < 0 else \
                                    'right' if abs(dx) > abs(dy) else \
                                    'up' if dy < 0 else 'down'
            else:
                self.moveDirection = random.choice(['left', 'right', 'up', 'down'])

    def Wander(self):
        if self.moveDirection == 'left':
            self.x -= self.speed
        elif self.moveDirection == 'right':
            self.x += self.speed
        elif self.moveDirection == 'up':
            self.y -= self.speed
        elif self.moveDirection == 'down':
            self.y += self.speed

        if self.region:
            x1, y1, x2, y2 = self.region
            self.x = max(x1, min(self.x, x2))
            self.y = max(y1, min(self.y, y2))


    def MoveTowardsTarget(self, targetPos):
        dx = targetPos[0] - self.x
        dy = targetPos[1] - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance > 0:
            self.x += (dx / distance) * self.speed
            self.y += (dy / distance) * self.speed
            if self.region:
                x1, y1, x2, y2 = self.region
                self.x = max(x1, min(self.x, x2))
                self.y = max(y1, min(self.y, y2))

    # ------------ Detection and Battle ------------------------
    def CheckBattle(self, player):
        if self.region:
            x1, y1, x2, y2 = self.region
            if not (x1 <= player.x <= x2 and y1 <= player.y <= y2):
                return False

        attackRect = self.GetAttackRect()
        if attackRect.colliderect(player._rect):
            self.Battle(player)
            self.passive = False
            return True

        return False

    def CheckDetection(self, playerPos):
        if self.region:
            x1, y1, x2, y2 = self.region
            if not (x1 <= playerPos[0] <= x2 and y1 <= playerPos[1] <= y2):
                return False

        dx = playerPos[0] - self.x
        dy = playerPos[1] - self.y
        distance = (dx**2 + dy**2)**0.5
        if distance <= self.detectionArea:
            self.MoveTowardsTarget(playerPos)
            self.passive = False
            return True

        return False

    def Battle(self, player):
        if self.canAttack:
            print(f"{self.name} attacks player!")
            self.PlaySound("attack")
            player.TakeDamage(self.attackPower)
            self.canAttack = False
            self.clock.schedule(self.ResetAttackTimer, self.attackCooldown)

    def ResetAttackTimer(self):
        self.canAttack = True

    def TakeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.Die()

    def Die(self):
        print(f"{self.name} has been defeated!")
        self.PlaySound("death")
        self.mapScreen.EnemyDeath(self)
        

    # ----------------------------------------------------------
    def update(self, playerPos, player):
        # 1) Check battle (attack collider)
        if self.CheckBattle(player):
            return

        # 2) Check detection (follow player)
        if self.CheckDetection(playerPos):
            return

        # 3) Wander in the chosen direction
        self.Wander()

    def draw(self, screen, cameraX, cameraY):
        screen.blit(
            self.image,
            (self.x - cameraX + self.spriteOffsetX,
             self.y - cameraY + self.spriteOffsetY)
        )

    # Sounds
    ###########################################################
    def PlaySound(self, action):
        soundName = f"{self.soundPrefix}_{action}"
        print(f"Playing sound: {soundName}")
        self.StopSound()
        self.StartNewSound(soundName)

    def StopSound(self):
        if self.currentSound is not None:
            self.currentSound.stop()

    def StartNewSound(self, soundName):
        snd = getattr(sounds, soundName)
        snd.play()
        self.currentSound = snd
    ###########################################################
