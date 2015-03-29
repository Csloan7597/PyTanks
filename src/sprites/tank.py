__author__ = 'conor'

import pygame
import game_items
import common


class PlayerTank(object):
    """
    Player Tank base, setting up most behaviour, except for specifics (images, key controls)
    """

    def __init__(self, screen):
        """
        Constructor of the tank class; Sets a number of variables such as
        speed, starting ammo, health and sprite images.
        """

        # Tank state
        self.hasshot = False
        self.canshoot = True
        self.speed = 5
        self.screen = screen
        self.rapidFire = False
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.centerx = 23
        self.rect.centery = 45
        self.bullets = pygame.sprite.Group()
        self.facing = "n"
        self.ammo = 1000
        self.bulletCounter = 0
        self.canshoot = True
        self.blitLife = 0
        self.font = pygame.font.Font('../resources/fonts/trebucbd.ttf', 15)
        self.cantoggle = True
        self.toggleCounter = 0

    def update(self):
        """
        This method is called by a game using this sprite. It handles rendering messages (e.g. notification of toggled fire mode)
        and handles the interval between which gunshots can be fired, using simple integer counters.
        """
        if not self.cantoggle:
            self.toggleCounter += 1
        if self.toggleCounter == 3:
            self.cantoggle = True
            self.toggleCounter = 0
        if self.blitLife > 0:
            if self.rapidFire:
                self.message = self.font.render("rapid fire!", True, (255, 0, 0))
            elif not self.rapidFire:
                self.message = self.font.render("Normal Fire", True, (0, 0, 0))
            self.mrect = self.message.get_rect()
            self.mrect.midbottom = (self.rect.centerx, self.rect.centery-30)
            self.screen.blit(self.message, self.mrect)
            self.blitLife -= 1
        if not self.canshoot and not self.rapidFire:
            self.bulletCounter += 1
        if self.bulletCounter == 3 and not self.rapidFire:
            self.canshoot = True
            self.bulletCounter = 0

        self.boundaries()

    def boundaries(self):
        """
        Checks the sprite has not gone off screen, and if it tries, ensures it will be blocked.
        """
        if self.rect.x <= 0:
            self.rect.x = 0
        if self.rect.x >= (self.screen.get_width() - self.rect.width):
            self.rect.x = self.screen.get_width() - self.rect.width
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= (self.screen.get_height() - self.rect.height):
            self.rect.y = self.screen.get_height() - self.rect.height

    def shoot(self, direction):
        """
        Fires a bullet from the tank, in a given direction.
        """
        die = direction
        bullet = game_items.Bullet(self.screen, die, self.rect.centerx, self.rect.centery, "tank", self.rapidFire)
        self.bullets.add(bullet)
        self.ammo -= 1

    def move_back(self, othergroup):
        """
        Moves the tank back to where it was before the last action (used in cases of collision to easily recover)
        """
        if self.facing == "n":
            self.rect.centery += self.speed
        elif self.facing == "s":
            self.rect.centery -= self.speed
        elif self.facing == "e":
            self.rect.centerx -= self.speed
        elif self.facing == "w":
            self.rect.centerx += self.speed
        elif self.facing == "nw":
            self.rect.centery += self.speed
            self.rect.centerx += self.speed
        elif self.facing == "ne":
            self.rect.centery += self.speed
            self.rect.centerx -= self.speed
        elif self.facing == "sw":
            self.rect.centery -= self.speed
            self.rect.centerx += self.speed
        elif self.facing == "se":
            self.rect.centery -= self.speed
            self.rect.centerx -= self.speed
        if pygame.sprite.spritecollide(self, othergroup, False, pygame.sprite.collide_mask):
            self.move_back(othergroup)

    def control_tank(self):
        raise Exception('Abstract method, please override in the subclass')


class Player1Tank(PlayerTank, pygame.sprite.Sprite):
    """
    The player1 sprite, subclass of tank, which implements the abstract method "controltank". This is the concrete class
    used by a game mode.
    """

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.counter = 0
        self.imgs = common.load_images('TN3.png', 'TE3.png',
                                       'TS3.png', 'TW3.png',
                                       'TNW3.png', 'TSW3.png',
                                       'TSE3.png', 'TNE3.png')
        self.masks = {}
        for item in self.imgs:
            self.masks[self.counter] = pygame.mask.from_surface(self.imgs[self.counter])
            self.counter += 1
        self.image = pygame.image.load('../resources/images/TN3.png').convert_alpha()
        PlayerTank.__init__(self, screen)

    def update(self):
        """Allows a game to update this sprite, using the update() method in its superclass"""
        PlayerTank.update(self)
        self.control_tank()

    def control_tank(self):
        """
        Moves this sprite based on key input.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.image = self.imgs[0]
            self.mask = self.masks[0]
            self.rect.centery -= self.speed
            self.facing = "n"
        if keys[pygame.K_s]:
            self.image = self.imgs[2]
            self.mask = self.masks[2]
            self.rect.centery += self.speed
            self.facing = "s"
        if keys[pygame.K_a]:
            self.image = self.imgs[3]
            self.mask = self.masks[3]
            self.rect.centerx -= self.speed
            self.facing = "w"
        if keys[pygame.K_d]:
            self.image = self.imgs[1]
            self.mask = self.masks[1]
            self.rect.centerx += self.speed
            self.facing = "e"
        if keys[pygame.K_w] and keys[pygame.K_a]:
            self.image = self.imgs[4]
            self.mask = self.masks[4]
            self.facing = "nw"
        if keys[pygame.K_s] and keys[pygame.K_a]:
            self.image = self.imgs[5]
            self.mask = self.masks[5]
            self.facing = "sw"
        if keys[pygame.K_w] and keys[pygame.K_d]:
            self.image = self.imgs[7]
            self.mask = self.masks[7]
            self.facing = "ne"
        if keys[pygame.K_s] and keys[pygame.K_d]:
            self.image = self.imgs[6]
            self.mask = self.masks[6]
            self.facing = "se"
        if keys[pygame.K_SPACE] and self.ammo > 0 and (self.canshoot or self.rapidFire):
            self.shoot(self.facing)
            self.canshoot = False
        if keys[pygame.K_f] and self.cantoggle:
            if self.rapidFire:
                self.rapidFire = False
                self.blitLife = 10
                self.cantoggle = False
            elif not self.rapidFire:
                self.rapidFire = True
                self.blitLife = 10
            self.cantoggle = False


class Player2Tank(PlayerTank, pygame.sprite.Sprite):
    """
    The player1 sprite, subclass of tank, which implements the abstract method "controltank". This is the concrete class
    used by a game mode.
    """

    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.counter = 0
        self.imgs = common.load_images('TN2.png', 'TE2.png',
                                       'TS2.png', 'TW2.png',
                                       'TNW2.png', 'TSW2.png',
                                       'TSE2.png', 'TNE2.png')
        self.masks = {}
        for item in self.imgs:
            self.masks[self.counter] = pygame.mask.from_surface(self.imgs[self.counter])
            self.counter += 1
        self.image = pygame.image.load('../resources/images/TN2.png').convert_alpha()
        PlayerTank.__init__(self, screen)

    def update(self):
        """Allows a game to update this sprite, using the update() method in its superclass"""
        PlayerTank.update(self)
        self.control_tank()

    def control_tank(self):
        """
        Moves this sprite based on key input.
        """
        keys = pygame.key.get_pressed()
        if keys[pygame.K_u]:
            self.image = self.imgs[0]
            self.mask = self.masks[0]
            self.rect.centery -= self.speed
            self.facing = "n"
        if keys[pygame.K_j]:
            self.image = self.imgs[2]
            self.mask = self.masks[2]
            self.rect.centery += self.speed
            self.facing = "s"
        if keys[pygame.K_h]:
            self.image = self.imgs[3]
            self.mask = self.masks[3]
            self.rect.centerx -= self.speed
            self.facing = "w"
        if keys[pygame.K_k]:
            self.image = self.imgs[1]
            self.mask = self.masks[1]
            self.rect.centerx += self.speed
            self.facing = "e"
        if keys[pygame.K_u] and keys[pygame.K_h]:
            self.image = self.imgs[4]
            self.mask = self.masks[4]
            self.facing = "nw"
        if keys[pygame.K_j] and keys[pygame.K_h]:
            self.image = self.imgs[5]
            self.mask = self.masks[5]
            self.facing = "sw"
        if keys[pygame.K_u] and keys[pygame.K_k]:
            self.image = self.imgs[7]
            self.mask = self.masks[7]
            self.facing = "ne"
        if keys[pygame.K_j] and keys[pygame.K_k]:
            self.image = self.imgs[6]
            self.mask = self.masks[6]
            self.facing = "se"
        if keys[pygame.K_KP_ENTER] and self.ammo > 0 and (self.canshoot or self.rapidFire):
            self.shoot(self.facing)
            self.canshoot = False
        if keys[pygame.K_KP_PLUS] and self.cantoggle:
            if self.rapidFire:
                self.rapidFire = False
                self.blitLife = 10
                self.cantoggle = False
            elif not self.rapidFire:
                self.rapidFire = True
                self.blitLife = 10
            self.cantoggle = False