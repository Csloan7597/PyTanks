__author__ = 'conor'

import pygame
import random
import game_items


class Enemy(pygame.sprite.Sprite):
    """
    Class representing an enemy sprite, currently the only enemy, a UFO. This sprite will be generated in a random position, and move at a random
    speed in a random direction. It's all very random.
    """

    def __init__(self, screen, HP):
        """
        Constructor of the enemy sprite; Loads images, calculates position, and direction, and sets initial variables such as HP.
        """
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../resources/images/ufo.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = random.randint(0, screen.get_width())
        self.rect.centery = random.randint(0, screen.get_height())
        self.x, self.y = random.randint(1, 5), random.randint(1, 5)
        self.bullets = pygame.sprite.Group()
        self.shootcounter = random.randint(50, 100)
        self.directions = ('n', 'e', 's', 'w', 'nw', 'ne', 'sw', 'se')
        self.HP = HP
        self.mask = pygame.mask.from_surface(self.image)
        self.font = pygame.font.Font('../resources/fonts/trebucbd.ttf', 15)
        self.message = self.font.render("HP: 100", True, (0, 0, 0))
        self.mrect = self.message.get_rect()

    def boundaries(self):
        """
        Ensures that when this sprite hits the edge of the screen, it bounces off again and stays in the game.
        """
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= (self.screen.get_width() - self.rect.width):
            self.rect.x = self.screen.get_width() - self.rect.width
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= (self.screen.get_height() - self.rect.height):
            self.rect.y = self.screen.get_height() - self.rect.height

    def move(self):
        """
        Moves the sprite on its generated path & direction.
        """
        self.message = self.font.render("HP:"+str(self.HP), True, (0, 0, 0))
        self.rect.y += self.y
        self.rect.x += self.x
        self.mrect.center = (self.rect.x+10, self.rect.y-10)

        if self.rect.x <= 0:
            self.rect.x = 0
            self.x = -self.x
        elif self.rect.x >= (self.screen.get_width() - self.rect.width):
            self.rect.x = self.screen.get_width() - self.rect.width
            self.x = -self.x
        elif self.rect.y <= 0:
            self.rect.y = 0
            self.y = -self.y
        elif self.rect.y >= (self.screen.get_height() - self.rect.height):
            self.rect.y = self.screen.get_height() - self.rect.height
            self.y = -self.y
        self.screen.blit(self.message, self.mrect)

    def shoot(self, direction):
        """
        Shoots a bullet in a random direction.
        """
        die = direction
        bullet = game_items.Bullet(self.screen, die, self.rect.centerx, self.rect.centery, "ufo", False)
        self.bullets.add(bullet)

    def update(self):
        """
        Allows a game to update this sprite.
        """
        self.boundaries()
        self.move()
        self.shootcounter -= 1
        if self.shootcounter == 0:
            self.shoot(self.directions[random.randint(0, 7)])
            self.shootcounter = random.randint(50, 100)