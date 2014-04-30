import pygame, random
import sprites
from pgtools.utils import *
from pygame.locals import *

class twoplayer:
    """
    Class representing the two player game mode of tanks. 
    This game involves 2 player tank sprites, and a bunch of enemies.
    The aim of the game is to destroy the other tank! 
    """

    def __init__(self, screen, difficulty):
        """
        Constructor of the co-op game. Sets initial values and loads sprites, ready for the game to begin.
        """
        # Initialise pygame and display
        pygame.init()
        self.running = True
        self.screen = screen

        # Load background and sprites, adding them to the correct sprite groups
        self.background = create_tiled_surface(screen.get_size(), 'images/grass.jpg')
        self.playerTank = sprites.player1(self.screen)
        self.player2Tank = sprites.player2(self.screen)
        self.explosions = pygame.sprite.Group()
        self.player1_group = pygame.sprite.GroupSingle(self.playerTank)
        self.player2_group = pygame.sprite.GroupSingle(self.player2Tank)
        self.enemies = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()

        # Set initial values for game session constants
        self.HEALTH_INTERVAL = random.randint(8, 12)
        self.AMMO_INTERVAL = random.randint(800, 1200)
        self.PLAYER_1_HP = 1000
        self.PLAYER_2_HP = 1000
        self.P1_SCORE = 0
        self.P2_SCORE = 0
        self.font = pygame.font.Font('trebucbd.ttf', 28)
        self.GAMEOVER = False

        # Based on difficulty input, set values for enemy sprites to use for generation and general aggression
        if(difficulty == 'easy'):
            self.enemyMin, self.enemyMax = 50, 300
            self.spriteHP = 100
        elif(difficulty == 'medium'):
            self.enemyMin, self.enemyMax = 40, 250
            self.spriteHP = 150
        elif(difficulty == 'hard'): 
            self.enemyMin, self.enemyMax = 20, 150
            self.spriteHP = 200
        self.ENEMY_INTERVAL = random.randint(self.enemyMin, self.enemyMax)


    def update(self):
        """
        Allows the game runner to update this game by one iteration. 
        """ 
        # Interval logic here, for anything which is based on an interval timer  
        self.HEALTH_INTERVAL -= 1
        self.AMMO_INTERVAL -= 1
        if(self.HEALTH_INTERVAL == 0):
            self.upgrades.add(sprites.healthBox(self.screen))
            self.HEALTH_INTERVAL = random.randint(800, 1200)
        if(self.AMMO_INTERVAL == 0):
            self.upgrades.add(sprites.ammoBox(self.screen))  
            self.AMMO_INTERVAL = random.randint(800, 1200)
        self.ENEMY_INTERVAL -= 1
        if(self.ENEMY_INTERVAL == 0):
            self.enemies.add(sprites.enemy(self.screen, self.spriteHP))        
            self.ENEMY_INTERVAL = random.randint(self.enemyMin, self.enemyMax )

        # Blit changes to the screen
        self.screen.blit(self.background, (0, 0))
        self.player1_group.clear(self.screen, self.background)
        self.player2_group.clear(self.screen, self.background)

        # Update sprites, and check for collisions between the two tanks
        self.player1_group.update()  
        if(pygame.sprite.spritecollide(self.playerTank, self.player2_group, False, pygame.sprite.collide_mask)):
            self.playerTank.moveBack(self.player2_group)   
        self.player2_group.update()
        if(pygame.sprite.spritecollide(self.player2Tank, self.player1_group, False, pygame.sprite.collide_mask)):
            self.player2Tank.moveBack(self.player1_group)   

        # Update all of the game sprites
        self.enemies.update() 
        self.upgrades.update()
        self.upgrades.update()
        self.playerTank.bullets.update()
        self.player2Tank.bullets.update()
        self.explosions.update()
        for Sprite in self.enemies:
            Sprite.bullets.update()

        # Check if a tank has hit an upgrade, and make changes necessary
        for Sprite in self.upgrades:
            if (pygame.sprite.spritecollide(Sprite, self.player1_group, False, pygame.sprite.collide_mask)):
                if(Sprite.getName() == "health"):
                    self.PLAYER_1_HP += Sprite.healthboost
                    Sprite.kill()
                elif(Sprite.getName() == "ammo"): 
                    self.playerTank.ammo += Sprite.ammoboost
                    Sprite.kill()
            elif (pygame.sprite.spritecollide(Sprite, self.player2_group, False, pygame.sprite.collide_mask)):
                if(Sprite.getName() == "health"):
                    self.PLAYER_2_HP += Sprite.healthboost
                    Sprite.kill()
                elif(Sprite.getName() == "ammo"):
                    self.player2Tank.ammo += Sprite.ammoboost
                    Sprite.kill()

        # Check each enemy for collision with tanks, or to be destroyed if HP is 0  
        for Sprite in self.enemies:
            if(Sprite.HP<=0):
                self.explosions.add(sprites.explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()
            if(pygame.sprite.spritecollide(Sprite, self.player1_group, False, pygame.sprite.collide_mask)):
                self.P1_SCORE += 100 
                self.PLAYER_1_HP -= Sprite.HP
                self.explosions.add(sprites.explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()
            if(pygame.sprite.spritecollide(Sprite, self.player2_group, False, pygame.sprite.collide_mask)):
                self.P2_SCORE += 100 
                self.PLAYER_2_HP -= Sprite.HP
                self.explosions.add(sprites.explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()

        # Also check that this sprite has any bullets that landed
        for bullet in Sprite.bullets:
            if(pygame.sprite.spritecollide(bullet, self.player1_group, False, pygame.sprite.collide_mask)):
                self.PLAYER_1_HP -= 25 
                self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                bullet.kill()
            if(pygame.sprite.spritecollide(bullet, self.player2_group, False, pygame.sprite.collide_mask)):
                self.PLAYER_2_HP -= 25
                self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                bullet.kill()

        # Check if the two tanks' bullets have hit anything
        for bullet in self.player1_group.sprite.bullets:
            if(pygame.sprite.spritecollide(bullet, self.player2_group, False, pygame.sprite.collide_mask)):
                self.PLAYER_2_HP -= 5
                self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                bullet.kill()
            if(pygame.sprite.spritecollide(bullet, self.player2_group.sprite.bullets, True, pygame.sprite.collide_mask)):
                self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                bullet.kill()
            for Sprite in self.enemies:
                if(pygame.sprite.collide_mask(bullet, Sprite)):
                    self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                    Sprite.HP -= 10
                    self.P1_SCORE += 100
                    bullet.kill()
        for bullet in self.player2_group.sprite.bullets:
            if(pygame.sprite.spritecollide(bullet, self.player1_group, False, pygame.sprite.collide_mask)):
                self.PLAYER_1_HP -= 5
                self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                bullet.kill()
            if(pygame.sprite.spritecollide(bullet, self.player1_group.sprite.bullets, True, pygame.sprite.collide_mask)):
                self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                bullet.kill()
            for Sprite in self.enemies:
                if(pygame.sprite.collide_mask(bullet, Sprite)):
                    self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                    Sprite.HP -= 10
                    self.P2_SCORE += 100
                    bullet.kill()

        # Draw all of these changes on screen
        self.player2_group.draw(self.screen)
        self.enemies.draw(self.screen) 
        self.player1_group.draw(self.screen)
        self.upgrades.draw(self.screen)
        self.playerTank.bullets.draw(self.screen)
        self.player2Tank.bullets.draw(self.screen) 
        for Sprite in self.enemies:
            Sprite.bullets.draw(self.screen)
        self.explosions.draw(self.screen)

        # Check if eithre of the players have died
        if(self.PLAYER_1_HP <= 0):
            self.playerTank.kill()
            self.PLAYER_1_HP = 0
            self.GAMEOVER = True
            self.winner = "Player 2" 
        if(self.PLAYER_2_HP <= 0):
            self.player2Tank.kill()
            self.PLAYER_2_HP = 0
            self.GAMEOVER = True
            self.winner = "Player 1"  

        # Update and redraw text messages on the game screen, and flip the display
        self.message = self.font.render('Player 1: Score: '+str(self.P1_SCORE)+" Health: "+str(self.PLAYER_1_HP)+" Ammo: "+str(self.playerTank.ammo), True, (0, 0, 0))
        self.message2 = self.font.render('Player 2: Score: '+str(self.P2_SCORE)+" Health: "+str(self.PLAYER_2_HP)+" Ammo: "+str(self.player2Tank.ammo), True, (0, 0, 0))
        self.rectm = self.message.get_rect()
        self.rectm2 = self.message2.get_rect()
        self.rectm.bottomleft = (25, 40)
        self.rectm2.bottomleft = (25, 80)
        self.screen.blit(self.message, self.rectm)
        self.screen.blit(self.message2, self.rectm2)
        pygame.display.flip()
