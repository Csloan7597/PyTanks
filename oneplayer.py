import pygame, random
import sprites
from pgtools.utils import *
from pygame.locals import *

class oneplayer:
    """
    Class representing the one player game mode of tanks. 
    This game involves 1 player tank sprite, and a bunch of enemies.
    The aim of the game is to destroy as many enemies as possible! 
    """

    def __init__(self, screen, difficulty):
        """
        Constructor of the one player game. Sets initial values and loads sprites, ready for the game to begin.
        """
        # Initialise pygame and display
        pygame.init()
        self.screen = screen

        # Load background and sprites, adding them to the correct sprite groups
        self.background = create_tiled_surface(screen.get_size(), 'images/grass.jpg')
        self.screen.blit(self.background, (0, 0)) 
        self.playerTank = sprites.player1(self.screen)
        self.explosions = pygame.sprite.Group()
        self.player_group = pygame.sprite.GroupSingle(self.playerTank)
        self.enemies = pygame.sprite.Group()
        self.upgrades = pygame.sprite.Group()

        # Set initial values for game session constants
        self.HEALTH_INTERVAL = random.randint(800, 1200)
        self.AMMO_INTERVAL = random.randint(800, 1200)
        self.PLAYER_1_HP = 1000
        self.P1_SCORE = 0
        self.font = pygame.font.Font('trebucbd.ttf', 28)
        self.GAMEOVER = False
        self.enemyHP = 100

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
        # Blit the background
        self.screen.blit(self.background, (0, 0))      

        # Logic for anything spawned or activated by a timed interval, acheived using counters (++ per call to update)
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
            self.ENEMY_INTERVAL = random.randint(self.enemyMin, self.enemyMax)
            self.enemyMax -= 1

        # Update all of the game sprites, allowing them to move, respond to events, etc.          
        self.player_group.update()     
        self.enemies.update()                                  
        self.upgrades.update()                                 
        self.playerTank.bullets.update()                      
        self.upgrades.update()
        self.explosions.update()
        for Sprite in self.enemies:
            Sprite.bullets.update()

        # Check if the tank has hit an upgrade, and make changes necessary
        for Sprite in self.upgrades:
            if (pygame.sprite.spritecollide(Sprite, self.player_group, False, pygame.sprite.collide_mask)):
                if(Sprite.getName() == "health"):
                    self.PLAYER_1_HP += Sprite.healthboost
                    Sprite.kill()                                               
                elif(Sprite.getName() == "ammo"):                              
                    self.playerTank.ammo += Sprite.ammoboost                    
                    Sprite.kill()

        # Check each enemy for collision with tank, or to be destroyed if HP is 0  
        for Sprite in self.enemies:
            if(Sprite.HP<=0):
                self.explosions.add(sprites.explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()
            if(pygame.sprite.spritecollide(Sprite, self.player_group, False, pygame.sprite.collide_mask)):
                self.P1_SCORE += 100 
                self.PLAYER_1_HP -= Sprite.HP
                self.explosions.add(sprites.explosion(self.screen, Sprite.rect.centerx, Sprite.rect.centery, "big"))
                Sprite.kill()     

        # Also check if this sprite's bullets have hit the tank                                                                                      
        for bullet in Sprite.bullets:                                   
            if(pygame.sprite.spritecollide(bullet, self.player_group, False, pygame.sprite.collide_mask)):
                self.PLAYER_1_HP -= 25 
                self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                bullet.kill()                                               

        # Check if the tank's bullets have hit anything
        for bullet in self.player_group.sprite.bullets:                          
            for Sprite in self.enemies:                                         
                if(pygame.sprite.collide_mask(bullet, Sprite)):               
                    self.explosions.add(sprites.explosion(self.screen, bullet.rect.centerx, bullet.rect.centery, "small"))
                    Sprite.HP -= 10
                    self.P1_SCORE += 100
                    bullet.kill()

        # Draw changes to screen
        self.enemies.draw(self.screen) 
        self.player_group.draw(self.screen)
        self.upgrades.draw(self.screen)                                  
        self.playerTank.bullets.draw(self.screen)
        for Sprite in self.enemies:
            Sprite.bullets.draw(self.screen)
        self.explosions.draw(self.screen)

        # Check the player has died, and if so, signal game over
        if(self.PLAYER_1_HP <= 0):
            self.playerTank.kill()                                            
            self.GAMEOVER = True                                               
            self.PLAYER_1_HP = 0                                              

        # Update game message for points, HP, etc, and flip the display
        self.message = self.font.render('Player 1: Score: '+str(self.P1_SCORE)+" Health: "+str(self.PLAYER_1_HP)+" Ammo: "+str(self.playerTank.ammo), True, (0, 0, 0))
        self.rectm = self.message.get_rect()      
        self.rectm.bottomleft = (20, 50)                                     
        self.screen.blit(self.message, self.rectm)
        pygame.display.flip()                                              
