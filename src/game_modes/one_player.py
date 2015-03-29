__author__ = 'conor'

import random
from pgtools.utils import *
from sprites import tank, game_items, enemy
import game_mode


class OnePlayer(game_mode.GameMode):
    """Class representing one player game mode"""

    def __init__(self, screen, difficulty):
        pygame.init()
        self.screen = screen
        self.difficulty = difficulty
        game_mode.GameMode.__init__(self, screen)

        # Set difficulty rules. Set for generation speed and aggression
        if difficulty == 'easy':
            self.enemyMin, self.enemyMax = 50, 300
            self.spriteHP = 100
        elif difficulty == 'medium':
            self.enemyMin, self.enemyMax = 40, 250
            self.spriteHP = 150
        elif difficulty == 'hard':
            self.enemyMin, self.enemyMax = 20, 150
            self.spriteHP = 200
        self.ENEMY_INTERVAL = random.randint(self.enemyMin, self.enemyMax)

        # Set up initial game state
        self.HEALTH_INTERVAL = random.randint(800, 1200)
        self.AMMO_INTERVAL = random.randint(800, 1200)
        self.PLAYER_1_HP = 1000
        self.P1_SCORE = 0
        self.enemyHP = 100

        # Finally, load the sprites & sprite groups required for this game
        self.playerTank = tank.Player1Tank(self.screen)
        self.explosions = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle(self.playerTank)
        self.enemies = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()

    def get_score(self):
        return self.P1_SCORE

    def display_game_message(self):
        # Update game message for points, HP, etc, and flip the display
        self.message = self.font.render('Player 1: Score: ' + str(self.P1_SCORE) +
                                        " Health: " + str(self.PLAYER_1_HP) +
                                        " Ammo: " + str(self.playerTank.ammo), True, (0, 0, 0))
        self.rectm = self.message.get_rect()
        self.rectm.bottomleft = (20, 50)
        self.screen.blit(self.message, self.rectm)

    def update_sprites(self):
        self.player_group.update()
        self.enemies.update()
        self.upgrades.update()
        self.playerTank.bullets.update()
        self.upgrades.update()
        self.explosions.update()
        for Sprite in self.enemies:
            Sprite.bullets.update()

    def generate_game_items(self):
        self.HEALTH_INTERVAL -= 1
        self.AMMO_INTERVAL -= 1
        if self.HEALTH_INTERVAL == 0:
            self.upgrades.add(game_items.HealthBox(self.screen))
            self.HEALTH_INTERVAL = random.randint(800, 1200)
        if self.AMMO_INTERVAL == 0:
            self.upgrades.add(game_items.AmmoBox(self.screen))
            self.AMMO_INTERVAL = random.randint(800, 1200)
        self.ENEMY_INTERVAL -= 1
        if self.ENEMY_INTERVAL == 0:
            self.enemies.add(enemy.Enemy(self.screen, self.spriteHP))
            self.ENEMY_INTERVAL = random.randint(self.enemyMin, self.enemyMax)
            self.enemyMax -= 1

    def handle_collisions(self):
        # Check if the tank has hit an upgrade, and make changes necessary
        for Sprite in self.upgrades:
            if pygame.sprite.spritecollide(Sprite, self.player_group, False, pygame.sprite.collide_mask):
                if Sprite.get_name() == "health":
                    self.PLAYER_1_HP += Sprite.healthboost
                    Sprite.kill()
                elif Sprite.get_name() == "ammo":
                    self.playerTank.ammo += Sprite.ammoboost
                    Sprite.kill()

        # Check each enemy for collision with tank, or to be destroyed if HP is 0  
        for Sprite in self.enemies:
            if Sprite.HP<=0:
                self.explosions.add(game_items.Explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()
            if pygame.sprite.spritecollide(Sprite, self.player_group, False, pygame.sprite.collide_mask):
                self.P1_SCORE += 100
                self.PLAYER_1_HP -= Sprite.HP
                self.explosions.add(game_items.Explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()

            # Also check if this sprite's bullets have hit the tank
            for bullet in Sprite.bullets:
                if pygame.sprite.spritecollide(bullet, self.player_group, False, pygame.sprite.collide_mask):
                    self.PLAYER_1_HP -= 25
                    self.explosions.add(game_items.Explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                    bullet.kill()

        if self.player_group.sprite is not None:
            # Check if the tank's bullets have hit anything (check for tank not being killed here)
            for bullet in self.player_group.sprite.bullets:
                for Sprite in self.enemies:
                    if pygame.sprite.collide_mask(bullet, Sprite):
                        self.explosions.add(game_items.Explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                        Sprite.HP -= 10
                        self.P1_SCORE += 100
                        bullet.kill()

    def draw_changes(self):
        self.enemies.draw(self.screen)
        self.player_group.draw(self.screen)
        self.upgrades.draw(self.screen)
        self.playerTank.bullets.draw(self.screen)
        for Sprite in self.enemies:
            Sprite.bullets.draw(self.screen)
        self.explosions.draw(self.screen)

    def check_for_game_over(self):
        # Check the player has died, and if so, signal game over
        if self.PLAYER_1_HP <= 0:
            self.playerTank.kill()
            self.GAME_OVER = True
            self.PLAYER_1_HP = 0

    def get_game_mode(self):
        return "1player"