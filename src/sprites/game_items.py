__author__ = 'conor'

import pygame
import random


class Bullet(pygame.sprite.Sprite):
    """
    Class representing the bullet sprite. Created when the tank fires, and moves at a set speed
    in the direction the tank is pointing when fired.
    """

    def __init__(self, screen, direction, xpos, ypos, side, rapidFire):
        """
        Constructor of the bullet, loads images based on firing mode and sets initial position and direction.
        """
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        if side == "ufo":
            self.image = pygame.image.load('../resources/images/bullet2.png').convert_alpha()
        elif side == "tank" and rapidFire is True:
            self.image = pygame.image.load('../resources/images/bullet3.png').convert_alpha()
        elif side == "tank" and not rapidFire:
            self.image = pygame.image.load('../resources/images/bullet.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.centery = ypos
        self.x = 0
        self.y = 0
        self.die = direction
        self.flight_path()
        self.set_position()

    def set_position(self):
        """
        Sets the position of the bullet relative to the tank sprite which fired it.
        """
        if self.die == "n":
            self.rect.centerx += -1
            self.rect.centery += -25
        elif self.die == "e":
            self.rect.centerx += 35
            self.rect.centery += -14
        elif self.die == "s":
            self.rect.centerx += -2
            self.rect.centery += 25
        elif self.die == "w":
            self.rect.centerx += -9
            self.rect.centery += -15
        elif self.die == "nw":
            self.rect.centerx += -6
            self.rect.centery += -20
        elif self.die == "ne":
            self.rect.centerx += 26
            self.rect.centery += -22
        elif self.die == "sw":
            self.rect.centerx += -8
            self.rect.centery += 14
        elif self.die == "se":
            self.rect.centerx += 29
            self.rect.centery += 14

    def flight_path(self):
        """
        Maps the direction of the bullet to the changes in position required on update.
        """
        if self.die == "n":
            self.x = 0
            self.y = -10
        if self.die == "s":
            self.x = 0
            self.y = 10
        if self.die == "w":
            self.x = -10
            self.y = 0
        if self.die == "e":
            self.x = 10
            self.y = 0
        if self.die == "nw":
            self.x = -10
            self.y = -10
        if self.die == "ne":
            self.x = 10
            self.y = -10
        if self.die == "sw":
            self.x = -10
            self.y = 10
        if self.die == "se":
            self.x = 10
            self.y = 10

    def boundaries(self):
        """
        Ensures that when this bullet hits a screen boundary, it is immediately destroyed.
        """
        if(self.rect.x <= 0 or self.rect.x >= (self.screen.get_width()-self.rect.width) or self.rect.y <= 0
           or self.rect.y >= (self.screen.get_height()-self.rect.height)):
            self.kill()

    def update(self):
        """
        Allows a game to update this sprite.
        """
        self.boundaries()
        self.rect.centery += self.y
        self.rect.centerx += self.x


class HealthBox(pygame.sprite.Sprite):
    """
    Class representing a health box. Generated at random, this sprite gives a random health boost on collision.
    """

    def __init__(self, screen):
        """
        Constructor of the healthbox. Generates random position, health boost, and lifetime, and loads the sprite image.
        """
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../resources/images/health.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen.get_width())
        self.rect.y = random.randint(0, screen.get_height())
        self.healthboost = random.randint(50, 350)
        self.tolive = 400

    def update(self):
        """
        Allows the game to update this sprite.
        """
        self.tolive -= 1
        if self.tolive == 0:
            self.collided()

    def collided(self):
        """
        Ensures that if this sprite hits something, it will be destroyed.
        """
        self.kill()

    def get_name(self):
        """Returns the name of this object"""
        return "health"


class AmmoBox(pygame.sprite.Sprite):
    """
    Class representing an ammo box, another upgrade generated at random, which gives a boost to player ammo.
    """

    def __init__(self, screen):
        """
        Constructor for ammo box, loads image and generates random position, ammo boost and lifetime for this sprite.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('../resources/images/ammo.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen.get_width())
        self.rect.y = random.randint(0, screen.get_height())
        self.ammoboost = random.randint(100, 200)
        self.mask = pygame.mask.from_surface(self.image)
        self.tolive = 400

    def update(self):
        """
        Allows the game to update this sprite.
        """
        self.tolive -= 1
        if self.tolive == 0:
            self.collided()

    def collided(self):
        """
        Ensures that if this sprite has collided, it will be destroyed.
        """
        self.kill()

    def get_name(self):
        """
        Returns the name of this upgrade.
        """
        return "ammo"


class Explosion(pygame.sprite.Sprite):
    """
    Class representing an explosion sprite, created when something blows up!
    """

    def __init__(self, screen, xpos, ypos, size):
        """
        Constructor of the explosion sprite, given position and size, loads the image of the sprite and
        gives it lifetime.
        """
        self.screen = screen
        pygame.sprite.Sprite.__init__(self)
        if size == "small":
            self.image = pygame.image.load('../resources/images/explosion.png').convert_alpha()
        else:
            self.image = pygame.image.load('../resources/images/bigexp.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = xpos
        self.rect.centery = ypos
        self.lifemax = 10
        self.lifecounter = 0

    def update(self):
        """
        Allows the game to update this sprite.
        """
        self.lifecounter += 1
        if self.lifecounter == self.lifemax:
            self.kill()