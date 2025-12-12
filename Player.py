from pgzero.actor import Actor
from pgzero.loaders import sounds
from pygame import Rect
from JsonHandler import JsonHandler


class Player(Actor):
    def __init__(self, name, pos, clock, screenHandler):
        super().__init__(name, pos)
        self.name = name
        self.image = name + '.png'
        self.anchor = ('center', 'center')
        self.statusFile = f"{self.name}_status.json"
        self.loadStatus()
        self.clock = clock
        self.screenHandler = screenHandler
        self.canAttack = True

        # sprite visual offset (does NOT affect logic)
        self.spriteOffsetX = -10
        self.spriteOffsetY = -22

        # track last sound played for this player
        self.currentSound = None

    def loadStatus(self):
        helper = JsonHandler(self.statusFile)
        status = helper.GetJson()
        self.max_health = status['health']
        self.health = self.max_health
        self.speed = status['speed']
        self.attackRange = status['attack_range']
        self.attackPower = status['attack_power']
        self.attackCooldown = status.get('attack_cooldown', 0.5)
        self.soundPrefix = status.get('name', '').lower()

    def GetAttackRect(self):
        size = self.attackRange * 2
        return Rect(
            self.x - self.attackRange,
            self.y - self.attackRange,
            size,
            size
        )

    def Attack(self, enemies):
        if not self.canAttack:
            return
        colliding = self.GetCollidingEnemies(enemies)

        if not colliding:
            return

        closestEnemy = self.FindClosestEnemyFromList(colliding)

        if closestEnemy:
            self.PerformAttack(closestEnemy)

    def GetCollidingEnemies(self, enemies):
        attackRect = self.GetAttackRect()
        return [enemy for enemy in enemies if attackRect.colliderect(enemy._rect)]

    def FindClosestEnemyFromList(self, enemies):
        closestEnemy = None
        min_distance_sq = float('inf')

        for enemy in enemies:
            dx = enemy.x - self.x
            dy = enemy.y - self.y
            distance_sq = dx * dx + dy * dy
            if distance_sq < min_distance_sq:
                min_distance_sq = distance_sq
                closestEnemy = enemy

        return closestEnemy

    def PerformAttack(self, enemy):
        print(f"Player attacks {enemy.name}!")
        enemy.TakeDamage(self.attackPower)
        self.PlaySound("attack")
        self.canAttack = False
        self.clock.schedule(self.ResetAttackTimer, self.attackCooldown)

    def ResetAttackTimer(self):
        self.canAttack = True

    def draw(self, screen, cameraX, cameraY):
        screen.blit(
            self.image,
            (self.x - cameraX + self.spriteOffsetX,
             self.y - cameraY + self.spriteOffsetY)
        )

    def TakeDamage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.Die()

    def Die(self):
        self.PlaySound("death")
        print("Player has been defeated!")
        self.screenHandler.ChangeScreen("GameOverScreen")

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
