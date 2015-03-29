__author__ = 'conor'

import random
from pgtools.utils import *
from sprites import tank, game_items, enemy
import game_mode


class Cooperative(game_mode.GameMode):

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
        self.HEALTH_INTERVAL = random.randint(8, 12)
        self.AMMO_INTERVAL = random.randint(800, 1200)
        self.PLAYER_1_HP = 1000
        self.PLAYER_2_HP = 1000
        self.SCORE = 0

        # Finally, load the sprites & sprite groups required for this game
        self.playerTank = tank.Player1Tank(self.screen)
        self.player2Tank = tank.Player2Tank(self.screen)
        self.explosions = pygame.sprite.Group()
        self.player1_group = pygame.sprite.GroupSingle(self.playerTank)
        self.player2_group = pygame.sprite.GroupSingle(self.player2Tank)
        self.enemies = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()

    def game_is_over(self):
        return self.GAME_OVER

    def get_score(self):
        return self.SCORE

    def display_game_message(self):
        self.message = self.font.render('Player 1: Health: '+str(self.PLAYER_1_HP)+" Ammo: "+str(self.playerTank.ammo)+" Score: "+str(self.SCORE), True, (0, 0, 0))
        self.message2 = self.font.render('Player 2: Health: '+str(self.PLAYER_2_HP)+" Ammo: "+str(self.player2Tank.ammo), True, (0, 0, 0))
        self.rectm = self.message.get_rect()
        self.rectm2 = self.message2.get_rect()
        self.rectm.bottomleft = (25, 40)
        self.rectm2.bottomleft = (25, 80)
        self.screen.blit(self.message, self.rectm)
        self.screen.blit(self.message2, self.rectm2)

    def update_sprites(self):
        self.player1_group.update()
        if pygame.sprite.spritecollide(self.playerTank, self.player2_group, False, pygame.sprite.collide_mask):
            self.playerTank.move_back(self.player2_group)
        self.player2_group.update()
        if pygame.sprite.spritecollide(self.player2Tank, self.player1_group, False, pygame.sprite.collide_mask):
            self.player2Tank.move_back(self.player1_group)

        self.enemies.update()
        self.upgrades.update()
        self.upgrades.update()
        self.playerTank.bullets.update()
        self.player2Tank.bullets.update()
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
        # Check if a tank has hit an upgrade, and make changes necessary
        for Sprite in self.upgrades:
            if pygame.sprite.spritecollide(Sprite, self.player1_group, False, pygame.sprite.collide_mask):
                if Sprite.get_name() == "health":
                    self.PLAYER_1_HP += Sprite.healthboost
                    Sprite.kill()
                elif Sprite.get_name() == "ammo":
                    self.playerTank.ammo += Sprite.ammoboost
                    Sprite.kill()
            elif pygame.sprite.spritecollide(Sprite, self.player2_group, False, pygame.sprite.collide_mask):
                if Sprite.get_name() == "health":
                    self.PLAYER_2_HP += Sprite.healthboost
                    Sprite.kill()
                elif Sprite.get_name() == "ammo":
                    self.player2Tank.ammo += Sprite.ammoboost
                    Sprite.kill()

        # Check each enemy for collision with tanks, or to be destroyed if HP is 0      
        for Sprite in self.enemies:
            if Sprite.HP<=0:
                self.explosions.add(game_items.Explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()
            if pygame.sprite.spritecollide(Sprite, self.player1_group, False, pygame.sprite.collide_mask):
                self.SCORE += 100
                self.PLAYER_1_HP -= Sprite.HP
                self.explosions.add(game_items.Explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()
            if pygame.sprite.spritecollide(Sprite, self.player2_group, False, pygame.sprite.collide_mask):
                self.SCORE += 100
                self.PLAYER_2_HP -= Sprite.HP
                self.explosions.add(game_items.Explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()

            # Also check that this sprite has any bullets that landed
            for bullet in Sprite.bullets:
                if pygame.sprite.spritecollide(bullet, self.player1_group, False, pygame.sprite.collide_mask):
                    self.PLAYER_1_HP -= 25
                    self.explosions.add(game_items.Explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                    bullet.kill()
                if pygame.sprite.spritecollide(bullet, self.player2_group, False, pygame.sprite.collide_mask):
                    self.PLAYER_2_HP -= 25
                    self.explosions.add(game_items.Explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                    bullet.kill()

        # Check if the two tanks' bullets have hit anything 
        if self.player1_group.sprite is not None:
            for bullet in self.player1_group.sprite.bullets:
                for Sprite in self.enemies:
                    if pygame.sprite.collide_mask(bullet, Sprite):
                        self.explosions.add(game_items.Explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                        Sprite.HP -= 10
                        self.SCORE += 100
                        bullet.kill()

        if self.player2_group.sprite is not None:
            for bullet in self.player2_group.sprite.bullets:
                for Sprite in self.enemies:
                    if pygame.sprite.collide_mask(bullet, Sprite):
                        self.explosions.add(game_items.Explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                        Sprite.HP -= 10
                        self.SCORE += 100
                        bullet.kill()

    def draw_changes(self):
        self.player2_group.draw(self.screen)
        self.enemies.draw(self.screen)
        self.player1_group.draw(self.screen)
        self.upgrades.draw(self.screen)
        self.playerTank.bullets.draw(self.screen)
        self.player2Tank.bullets.draw(self.screen)
        for Sprite in self.enemies:
            Sprite.bullets.draw(self.screen)
        self.explosions.draw(self.screen)

    def check_for_game_over(self):
        # Check if each player's HP has hit zero, and kill them if they have, signalling GAME OVER if both are down
        if self.PLAYER_1_HP <= 0:
            for Sprite in self.player1_group:
                self.player1_group.remove(Sprite)
            self.PLAYER_1_HP = 0
        if self.PLAYER_2_HP <= 0:
            for Sprite in self.player2_group:
                self.player2_group.remove(Sprite)
            self.PLAYER_2_HP = 0
        if self.PLAYER_2_HP == self.PLAYER_1_HP == 0:
            self.GAME_OVER = True

    def get_game_mode(self):
        return "coop"