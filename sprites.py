import pygame, random, sys, os.path

directions = ['n', 'e', 's', 'w', 'nw', 'ne', 'sw', 'se']


def load_image(file):
   """
   Loads a specific image from a file,  given the image's filepath.
   """
    file = os.path.join('images', file)
    try:
        surface = pygame.image.load(file)
    except pygame.error:
        sys.exit("Failed to load image: "+file)
    return surface.convert_alpha()


def load_images(*files):
  """
  Loads a number of image files given an arbitrary number of filepaths,
  returning them as a list. 
  """
    imgs = []
    counter = 0
    for file in files:
      imgs.append(load_image(file))
    return imgs



class tank(pygame.sprite.Sprite):
"""
This class represents the Sprite controlled by a player; a tank. 
It has the ability to move and shoot bullets. 
"""
  def __init__(self, screen):
    """
    Constructor of the tank class; Sets a number of variables such as 
    speed, starting ammo, health and sprite images. 
    """
    hasshot = False
    canshoot = True
    self.speed = 5
    super().__init__()
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
    self.font = pygame.font.Font('trebucbd.ttf', 15)
    self.cantoggle = True
    self.toggleCounter = 0


  def update(self):
    """
    This method is called by a game using this sprite. It handles rendering messages (e.g. notification of toggled fire mode)
    and handles the interval between which gunshots can be fired, using simple integer counters. 
    """
    if(self.cantoggle == False):
      self.toggleCounter +=1
    if(self.toggleCounter == 3):
      self.cantoggle = True
      self.toggleCounter = 0  
    if(self.blitLife > 0):
      if(self.rapidFire == True):
        self.message = self.font.render("rapid fire!", True, (255, 0, 0))
      elif(self.rapidFire == False):
        self.message = self.font.render("Normal Fire", True, (0, 0, 0))
      self.mrect = self.message.get_rect()
      self.mrect.midbottom = (self.rect.centerx, self.rect.centery-30)
      self.screen.blit(self.message, self.mrect)
      self.blitLife -= 1  
    if(self.canshoot == False and self.rapidFire == False):
      self.bulletCounter += 1  
    if(self.bulletCounter == 3 and self.rapidFire == False): 
      self.canshoot = True
      self.bulletCounter = 0
    
    self.boundaries()
    
     
  def boundaries(self):
    """
    Checks the sprite has not gone off screen, and if it tries, ensures it will be blocked. 
    """
    if(self.rect.x <= 0):
      self.rect.x = 0
    if(self.rect.x >= (self.screen.get_width() - self.rect.width)):
      self.rect.x = self.screen.get_width() - self.rect.width
    if(self.rect.y <= 0):
      self.rect.y = 0
    if(self.rect.y >= (self.screen.get_height() - self.rect.height)):
      self.rect.y = self.screen.get_height() - self.rect.height
  

  def shoot(self, direction):
    """
    Fires a bullet from the tank, in a given direction. 
    """
    die = direction 
    self.bullet = bullet(self.screen, die, self.rect.centerx, self.rect.centery, "tank", self.rapidFire)
    self.bullets.add(self.bullet)
    self.ammo = self.ammo-1


  def moveBack(self, othergroup):
    """
    Moves the tank back to where it was before the last action (used in cases of collision to easily recover) 
    """
     if(self.facing == "n"):
        self.rect.centery += self.speed
     elif(self.facing == "s"):
        self.rect.centery -= self.speed
     elif(self.facing == "e"):
       self.rect.centerx -= self.speed
     elif(self.facing == "w"):
       self.rect.centerx += self.speed
     elif(self.facing == "nw"):
       self.rect.centery += self.speed
       self.rect.centerx += self.speed
     elif(self.facing == "ne"):
       self.rect.centery += self.speed
       self.rect.centerx -= self.speed
     elif(self.facing == "sw"):
       self.rect.centery -= self.speed
       self.rect.centerx += self.speed
     elif(self.facing == "se"):
       self.rect.centery -= self.speed
       self.rect.centerx -= self.speed
     if(pygame.sprite.spritecollide(self, othergroup, False, pygame.sprite.collide_mask)):
       self.moveBack(othergroup)

  def controlTank(self):    
    raise Exception('Abstract method, please override in the subclass')
    
  
  
class player1(tank):
  """
  The player1 sprite, subclass of tank, which implements the abstract method "controltank". This is the concrete class
  used by a game mode. 
  """

  def __init__(self, screen):
    """
    Constructor for player1 sprite, loads images for the sprite. 
    """
    self.counter = 0
    self.imgs = load_images('TN3.png', 'TE3.png', 'TS3.png', 'TW3.png', 'TNW3.png', 'TSW3.png', 'TSE3.png', 'TNE3.png')
    self.masks = {}
    for item in self.imgs:  
      self.masks[self.counter] = pygame.mask.from_surface(self.imgs[self.counter])
      self.counter += 1
    self.image = pygame.image.load('images/TN3.png').convert_alpha()
    super().__init__(screen)


  def update(self):
    """Allows a game to update this sprite, using the update() method in its superclass"""
    super().update()
    self.controlTank()


  def controlTank(self):
    """
    Moves this sprite based on key input. 
    """
    self.keys = pygame.key.get_pressed()
    if self.keys[pygame.K_w]:
      self.image = self.imgs[0]
      self.mask = self.masks[0]
      self.rect.centery -= self.speed
      self.facing = "n"
    if self.keys[pygame.K_s]:
      self.image = self.imgs[2]
      self.mask = self.masks[2]
      self.rect.centery += self.speed
      self.facing = "s"      
    if self.keys[pygame.K_a]:
      self.image = self.imgs[3]
      self.mask = self.masks[3]
      self.rect.centerx -= self.speed
      self.facing = "w"
    if self.keys[pygame.K_d]:
      self.image = self.imgs[1]
      self.mask = self.masks[1]
      self.rect.centerx += self.speed
      self.facing = "e"
    if self.keys[pygame.K_w] and self.keys[pygame.K_a]:
      self.image = self.imgs[4]
      self.mask = self.masks[4]
      self.facing = "nw" 
    if self.keys[pygame.K_s] and self.keys[pygame.K_a]:
      self.image = self.imgs[5]
      self.mask = self.masks[5] 
      self.facing = "sw"
    if self.keys[pygame.K_w] and self.keys[pygame.K_d]:
      self.image = self.imgs[7]
      self.mask = self.masks[7]
      self.facing = "ne"
    if self.keys[pygame.K_s] and self.keys[pygame.K_d]:
      self.image = self.imgs[6]
      self.mask = self.masks[6] 
      self.facing = "se"
    if self.keys[pygame.K_SPACE] and self.ammo > 0 and (self.canshoot==True or self.rapidFire == True):
      self.shoot(self.facing)
      self.canshoot = False
    if self.keys[pygame.K_f] and self.cantoggle == True:
      if(self.rapidFire == True):
        self.rapidFire = False
        self.blitLife = 10
        self.cantoggle = False
      elif(self.rapidFire == False):
        self.rapidFire = True
        self.blitLife = 10
      self.cantoggle = False



class player2(tank):
  """
  The player1 sprite, subclass of tank, which implements the abstract method "controltank". This is the concrete class
  used by a game mode. 
  """

  def __init__(self, screen):
    """
    Constructor for player1 sprite, loads images for the sprite. 
    """
    self.counter = 0
    self.imgs = load_images('TN2.png', 'TE2.png', 'TS2.png', 'TW2.png', 'TNW2.png', 'TSW2.png', 'TSE2.png', 'TNE2.png')
    self.masks = {}
    for item in self.imgs:  
      self.masks[self.counter] = pygame.mask.from_surface(self.imgs[self.counter])
      self.counter += 1
    self.image = pygame.image.load('images/TN2.png').convert_alpha()  
    super().__init__(screen)


  def update(self):
    """
    Allows a game to update this sprite, using the update() method in its superclass.
    """
    super().update()
    self.controlTank()

  
  def controlTank(self):
    """
    Moves this sprite based on key input,
    """
    self.keys = pygame.key.get_pressed()
    if self.keys[pygame.K_u]:
      self.image = self.imgs[0]
      self.mask = self.masks[0]
      self.rect.centery -= self.speed
      self.facing = "n"
    if self.keys[pygame.K_j]:
      self.image = self.imgs[2]
      self.mask = self.masks[2]
      self.rect.centery += self.speed
      self.facing = "s"
    if self.keys[pygame.K_h]:
      self.image = self.imgs[3]
      self.mask = self.masks[3]
      self.rect.centerx -= self.speed
      self.facing = "w"
    if self.keys[pygame.K_k]:
      self.image = self.imgs[1]
      self.mask = self.masks[1]
      self.rect.centerx += self.speed
      self.facing = "e"
    if self.keys[pygame.K_u] and self.keys[pygame.K_h]:
      self.image = self.imgs[4]
      self.mask = self.masks[4]
      self.facing = "nw" 
    if self.keys[pygame.K_j] and self.keys[pygame.K_h]:
      self.image = self.imgs[5]
      self.mask = self.masks[5]
      self.facing = "sw"
    if self.keys[pygame.K_u] and self.keys[pygame.K_k]:
      self.image = self.imgs[7]
      self.mask = self.masks[7]
      self.facing = "ne"
    if self.keys[pygame.K_j] and self.keys[pygame.K_k]:
      self.image = self.imgs[6]
      self.mask = self.masks[6] 
      self.facing = "se"
    if self.keys[pygame.K_KP_ENTER] and self.ammo > 0 and (self.canshoot == True or self.rapidFire == True):
      self.shoot(self.facing)
      self.canshoot = False
    if self.keys[pygame.K_KP_PLUS] and self.cantoggle == True:
      if(self.rapidFire == True):
        self.rapidFire = False
        self.blitLife = 10
        self.cantoggle = False
      elif(self.rapidFire == False):
        self.rapidFire = True
        self.blitLife = 10
      self.cantoggle = False


        
class bullet(pygame.sprite.Sprite):
"""
Class representing the bullet sprite. Created when the tank fires, and moves at a set speed 
in the direction the tank is pointing when fired. 
"""


  def __init__(self, screen, direction, xpos, ypos, side, rapidFire):
    """
    Constructor of the bullet, loads images based on firing mode and sets initial position and direction. 
    """
    self.screen = screen
    super().__init__()
    if(side == "ufo"):
      self.image = pygame.image.load('images/bullet2.png').convert_alpha()
    elif(side == "tank" and rapidFire == True):
      self.image = pygame.image.load('images/bullet3.png').convert_alpha() 
    elif(side == "tank" and rapidFire == False):
      self.image = pygame.image.load('images/bullet.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.centerx = xpos
    self.rect.centery = ypos
    self.x = 0
    self.y = 0
    self.die = direction
    self.flightPath()
    self.setPosition()
    #print("just created the bullet"+str(self.die))


  def setPosition(self):
    """
    Sets the position of the bullet relative to the tank sprite which fired it. 
    """
    if(self.die == "n"):
      self.rect.centerx += -1
      self.rect.centery += -25
    elif(self.die == "e"):
      self.rect.centerx += 35
      self.rect.centery += -14
    elif(self.die == "s"):
      self.rect.centerx += -2
      self.rect.centery += 25
    elif(self.die == "w"):
      self.rect.centerx += -9
      self.rect.centery += -15
    elif(self.die == "nw"):
      self.rect.centerx += -6
      self.rect.centery += -20
    elif(self.die == "ne"):
      self.rect.centerx += 26
      self.rect.centery += -22
    elif(self.die == "sw"):
      self.rect.centerx += -8
      self.rect.centery += 14
    elif(self.die == "se"):
      self.rect.centerx += 29
      self.rect.centery += 14


  def flightPath(self):
    """
    Maps the direction of the bullet to the changes in position required on update. 
    """
    if(self.die == "n"):
      self.x = 0
      self.y = -10 
    if(self.die == "s"):
      self.x = 0
      self.y = 10
    if(self.die == "w"):
      self.x = -10
      self.y = 0
    if(self.die == "e"):
      self.x = 10
      self.y = 0
    if(self.die == "nw"):
      self.x = -10
      self.y = -10
    if(self.die == "ne"):
      self.x = 10
      self.y = -10
    if(self.die == "sw"):
      self.x = -10
      self.y = 10
    if(self.die == "se"):
      self.x = 10
      self.y = 10


  def boundaries(self):
      """
      Ensures that when this bullet hits a screen boundary, it is immediately destroyed.
      """
      if(self.rect.x<=0 or self.rect.x>=(self.screen.get_width()-self.rect.width) or self.rect.y<=0 or self.rect.y>=(self.screen.get_height()-self.rect.height)):
        self.kill()
  
           
  def update(self):
    """
    Allows a game to update this sprite.
    """
    self.boundaries()
    self.rect.centery += self.y
    self.rect.centerx += self.x
#~~~~~~~~~~~~~~~~~~~~~~~~~~



class enemy(pygame.sprite.Sprite):
"""
Class representing an enemy sprite, currently the only enemy, a UFO. This sprite will be generated in a random position, and move at a random
speed in a random direction. It's all very random. 
"""

  def __init__(self, screen, HP):
    """
    Constructor of the enemy sprite; Loads images, calculates position, and direction, and sets initial variables such as HP.  
    """
    self.screen = screen
    super().__init__()
    self.image = pygame.image.load('images/ufo.png').convert_alpha()
    self.rect = self.image.get_rect()
    self.rect.centerx = random.randint(0, screen.get_width())
    self.rect.centery = random.randint(0, screen.get_height())
    self.x, self.y = random.randint(1, 5), random.randint(1, 5)
    self.bullets = pygame.sprite.Group()
    self.shootcounter = random.randint(50, 100)
    self.directions = ('n', 'e', 's', 'w', 'nw', 'ne', 'sw', 'se')
    self.HP = HP
    self.mask = pygame.mask.from_surface(self.image)
    self.font = pygame.font.Font('trebucbd.ttf', 15)
    self.message = self.font.render("HP: 100", True, (0, 0, 0))
    self.mrect = self.message.get_rect()


  def boundaries(self):
    """
    Ensures that when this sprite hits the edge of the screen, it bounces off again and stays in the game. 
    """
    if(self.rect.x <= 0):
      self.rect.x = 0
    if(self.rect.x >= (self.screen.get_width() - self.rect.width)):
      self.rect.x = self.screen.get_width() - self.rect.width
    if(self.rect.y <= 0):
      self.rect.y = 0
    if(self.rect.y >= (self.screen.get_height() - self.rect.height)):
      self.rect.y = self.screen.get_height() - self.rect.height
  

  def move(self):
    """
    Moves the sprite on its generated path & direction. 
    """
    self.message = self.font.render("HP:"+str(self.HP), True, (0, 0, 0))
    self.rect.y += self.y
    self.rect.x += self.x
    self.mrect.center = (self.rect.x+10, self.rect.y-10)

    if(self.rect.x <= 0):
      self.rect.x = 0
      self.x = -(self.x)
    elif(self.rect.x >= (self.screen.get_width() - self.rect.width)):
      self.rect.x = self.screen.get_width() - self.rect.width
      self.x = -(self.x)
    elif(self.rect.y <= 0):
      self.rect.y = 0
      self.y = -(self.y)
    elif(self.rect.y >= (self.screen.get_height() - self.rect.height)):
      self.rect.y = self.screen.get_height() - self.rect.height
      self.y = -(self.y)
    self.screen.blit(self.message, self.mrect)


  def shoot(self, direction):
    """
    Shoots a bullet in a random direction. 
    """
    die = direction 
    self.bullet2 = bullet(self.screen, die, self.rect.centerx, self.rect.centery, "ufo", False)
    self.bullets.add(self.bullet2)
  

  def update(self):
    """
    Allows a game to update this sprite.
    """
    self.boundaries()
    self.move()
    self.shootcounter -= 1
    if(self.shootcounter == 0):
      
      self.shoot(self.directions[random.randint(0, 7)])
      self.shootcounter = random.randint(50, 100)
    
#~~~~~~~~~~~~~~~~~~~~~~~~~~~



class healthBox(pygame.sprite.Sprite):
"""
Class representing a health box. Generated at random, this sprite gives a random health boost on collision. 
"""

  def __init__(self, screen):
    """
    Constructor of the healthbox. Generates random position, health boost, and lifetime, and loads the sprite image. 
    """
    self.screen = screen
    super().__init__()
    self.image = pygame.image.load('images/health.png').convert_alpha()
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
    if(self.tolive == 0):
      self.collided()
    

  def collided(self):
    """
    Ensures that if this sprite hits something, it will be destroyed.
    """
    self.kill()    

  def getName(self):
    """Returns the name of this object"""
    return "health"



class ammoBox(pygame.sprite.Sprite):
"""
Class representing an ammo box, another upgrade generated at random, which gives a boost to player ammo. 
"""

  def __init__(self, screen):
    """
    Constructor for ammo box, loads image and generates random position, ammo boost and lifetime for this sprite.
    """
    super().__init__()
    self.image = pygame.image.load('images/ammo.png').convert_alpha()   
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
    if(self.tolive == 0):
      self.collided()


  def collided(self):
    """
    Ensures that if this sprite has collided, it will be destroyed.
    """ 
    self.kill()


  def getName(self):
    """
    Returns the name of this upgrade.
    """
    return "ammo"
 


class explosion(pygame.sprite.Sprite):
"""
Class representing an explosion sprite, created when something blows up! 
"""

  def __init__(self, screen, xpos, ypos, size):
    """
    Constructor of the explosion sprite, given position and size, loads the image of the sprite and 
    gives it lifetime. 
    """
    self.screen = screen
    super().__init__()
    if(size == "small"):
      self.image = pygame.image.load('images/explosion.png').convert_alpha()
    else:
      self.image = pygame.image.load('images/bigexp.png').convert_alpha()
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
    if(self.lifecounter == self.lifemax):
      self.kill()  