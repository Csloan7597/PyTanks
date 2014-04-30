import pygame
import twoplayer, oneplayer, coop
from pgtools.utils import *                                 #importing modules for game modes, pygame, pgtools, and the two xml apis i used for high scores.
from pygame.locals import *
import xml.etree.ElementTree as xo
from xml.dom.minidom import parse



def displayDifficulty():
  font = pygame.font.Font('Purisa.ttf', 20) 
  if(difficulty == 'easy'):
    message = font.render("Easy", True, (0, 0, 100))
  elif(difficulty == 'medium'):
    message = font.render("Medium", True, (20, 20, 20)) 
  elif(difficulty == 'hard'):
    message = font.render("Hard", True, (255, 0, 0))
  

  rect = message.get_rect()
  rect.bottomleft = (screen.get_width()-80, 40)
  screen.blit(message, rect)

def changeDifficulty(difficulty):
  if(difficulty == 'easy'):
    difficulty = 'medium'   
  elif(difficulty == 'medium'):
    difficulty = 'hard' 
  elif(difficulty == 'hard'):
    difficulty = 'easy'
  return difficulty

def recordScore(name, score, scoresheet, difficulty):
  #this function parses the high scores file, modifies it to add the new player name and score, then rewrites it to the 'scores.xml' file

  dom = parse(scoresheet)
  theName = str(name)
  theScore = str(score)
  theDiff = str(difficulty)
  x = dom.createElement("Player")       
  name = dom.createElement("Name")
  score = dom.createElement("Score")
  diff = dom.createElement("Difficulty")
  x.appendChild(name)
  x.appendChild(score)
  x.appendChild(diff)
  nametxt = dom.createTextNode(theName) 
  scoretxt = dom.createTextNode(theScore)
  difftext = dom.createTextNode(theDiff)
  name.appendChild(nametxt)
  score.appendChild(scoretxt)
  diff.appendChild(difftext)
  dom.childNodes[0].appendChild(x) 
  xt = dom.toxml()
  fh = open(scoresheet, 'w')
  fh.write(xt)
  

def getHighScores(scoresheet, difficulty):
  #Given a sheet name and difficulty, this function will read in the high scores in simple text format, adding them to a dictionary, with score as the key, and name as the value. 

  dicto = dict()
  instance = xo.parse(scoresheet)
  playerlist = instance.findall('Player')
  for item in range (0, len(playerlist)):
    name = playerlist[item].findall('Name')
    score = playerlist[item].findall('Score')
    diff = playerlist[item].findall('Difficulty')
    if(diff[0].text == difficulty):
      dicto.__setitem__(int(score[0].text), name[0].text )
    
  return dicto



def displayScores(scoresheet, difficulty): 
  #given a dictionary of names and scores (see 'getHighScores()' this function displays the sorted (highest to lowest score)
  #list of the best 10 scores with their respective names. Reading from the specified file.
  
  maxi = 10
  font2 = pygame.font.Font('Purisa.ttf', 25)
  highScores = getHighScores(scoresheet, difficulty)
  keys = highScores.keys()
  xposn = 850
  xposs = 1100
  ypos = 180
  if(scoresheet == 'scores.xml'):
    typem = font2.render("Normal Scores", True, (250, 100, 100))
  else:
    typem = font2.render("Co-op Scores", True, (250, 100, 100))
  rectm = typem.get_rect()
  rectm.midbottom = ((xposn+xposs)/2, ypos-85) 
  screen.blit(typem, rectm)
  for key in reversed(sorted(highScores)):
    message = font2.render("{0: ^}".format(highScores[key]), True, (100, 100, 100))
    message2 = font2.render("{0: ^}".format(key), True, (100, 100, 100))
    rect2 = message2.get_rect()
    rect = message.get_rect()
    rect.midbottom = xposn, ypos
    rect2.midbottom = xposs, ypos
    if(maxi>0):
      screen.blit(message2, rect2)
      screen.blit(message, rect)
      ypos += 30
      maxi -= 1



#Here the main program starts. The program is structured into nested while loops, one outer and one inner loop. The outer loop, 'ingame' controls the open pygame
#window, and will display the main menu, while listening for instructions. When a game mode is chosen, the inner loop, 'running' will be entered, controlling the 
#game itself. When the game is finished, the same iteration of the outer loop will continue. One play of a single/multiplayer mode = one iteration of 'ingame'


pygame.init()
running = False
screen = pygame.display.set_mode((1200,800))
clock = pygame.time.Clock()
clock2 = pygame.time.Clock()                                           #The main constants and objects for use, such as fonts, are declared. Booleans onesplayer,
gamewinner = ""                                                        #twosplayer, paused, running, and ingame control the choice of mode and startup of the actual
font = pygame.font.Font('Purisa.ttf', 35)                              #game mode. 
lastscore = -1
onesplayer = False
twosplayer = False
ingame = True
Paused = False
pausedmessage = font.render("Paused", True, (255, 0, 0))
prect = pausedmessage.get_rect()
prect.center = (600, 400)
coopgame = False
whichScores = False
difficulty = 'easy'


while(ingame):                                                           #The outer loop. Here the clock begins to tick, listening for events such as quit or 
                                                                         #key instructions, and displaying the main menu, as well as high scores. 
  clock.tick(30)
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      ingame = False

  
  background = create_tiled_surface(screen.get_size(), 'images/background.png')
  screen.blit(background, (0, 0))
  if(whichScores == True):
    displayScores('coopscores.xml', difficulty)
  else:
    displayScores('scores.xml', difficulty)

  displayDifficulty()                                                      #Here is where the functions displayScores and displayDifficulty are called
  if(gamewinner != ""):
    message = font.render("The winner was: "+gamewinner, True, (0, 0, 255))
    mrect = message.get_rect()
    mrect.center = (550, 50)                                               #If statements that check if either a 'gamewinner' exists (only when a 2p game has just 
    screen.blit(message, mrect)                                            #ended, or a 'lastscore' exists (only when 1p game has just ended). It then displays a
                                                                           #message on the background telling the user their score or winning player. 
  elif(lastscore != -1):
    message = font.render("You got: "+str(lastscore), True, (0, 0, 255))
    mrect = message.get_rect()
    mrect.center = (550, 50)
    screen.blit(message, mrect)
  
  pygame.display.flip()                                                     # Flip Display.



  keys = pygame.key.get_pressed()
  if keys[pygame.K_2]:                                                      #The event stack. Listens for any instruction as to which game to play. If '1' or '2' is 
    gamewinner = ""                                                         #selected, an instance of the twoplayer class is created and running is set to True, as 
    twos = twoplayer.twoplayer(screen, difficulty)                          #well as the correct mode boolean (ones/twos)player. These ensure the program will enter 
    twosplayer = True                                                       #the inner while loop and perform the correct operations respectively.
    running = True
  elif keys[pygame.K_1]:
    lastscore = 0
    ones = oneplayer.oneplayer(screen, difficulty)
    onesplayer = True
    running = True
  elif keys[pygame.K_c]:
    lastscore = 0
    coops = coop.coop(screen, difficulty)  
    coopgame = True
    running = True
  elif keys[pygame.K_h]:
    if(whichScores == False):
      whichScores = True 
    elif(whichScores == True):
      whichScores = False
  elif keys[pygame.K_d]:
    difficulty = changeDifficulty(difficulty)
  
  while(running):                                                           #The inner while loop. Ticks the second clock, and listens for events relating to the  
                                                                            #state of the game window, such as escape to quit, or p to pause, controlled by a boolean.
    
    clock2.tick(30)                                                         
    for event in pygame.event.get():
      if event.type == pygame.QUIT:
        running = False
        ingame = False
      if event.type == pygame.KEYDOWN:
        key = pygame.key.get_pressed()
        if(key[pygame.K_p] and Paused == False):
          Paused = True
          screen.blit(pausedmessage, prect)
          pygame.display.flip()
        elif(key[pygame.K_p] and Paused == True):
          Paused = False
        elif(key[pygame.K_ESCAPE]):                                          #when escaped, the inner loop will not be iterated through again as running is false, 
          running = False                                                    #and for the current iteration nothing will happen, as neither ones or twosplayer are 
          twosplayer = False                                                 #true. 
          onesplayer = False
          coopgame = False
          Paused = False
        elif(key[pygame.K_RETURN] and coopgame == True):
          if(coops.PLAYER_1_HP == 0 and coops.PLAYER_2_HP > 150):
            coops.PLAYER_1_HP += 100
            coops.PLAYER_2_HP -= 150
            coops.group.add(coops.playerTank)
          elif(coops.PLAYER_2_HP == 0 and coops.PLAYER_1_HP > 150):
            coops.PLAYER_2_HP += 100
            coops.PLAYER_1_HP -= 150
            coops.groups.add(coops.player2Tank)
            
            
            
    if(twosplayer == True):
      if(twos.GAMEOVER == True): 
        gamewinner = twos.winner
        running = False
        twosplayer = False
      elif(twos.GAMEOVER == False and Paused == False):
        twos.update()                                                        #This part of the code controls the main function of the game mode. Firstly, it checks
                                                                             #which mode it is in. It then checks if the game is over, and if it is, exits the while
                                                                             #loop, and writes scores/records winner accordingly. If the game is not over, it checks
    elif(onesplayer == True):                                                #that the game is not paused. If all criteria is met, the instance of one or two player's
      if(ones.GAMEOVER == True):                                             #update() method is called, so the game continues as normal. 
        lastscore = ones.P1_SCORE
        x = input("What is your name, player")
        recordScore(str(x), str(lastscore), 'scores.xml', difficulty)
        running = False
        onesplayer = False
      elif(ones.GAMEOVER == False and Paused == False):
        ones.update()
  
    
    elif(coopgame == True):
      if(coops.GAMEOVER == True):
        lastscore = coops.SCORE
        x = input("Pick a coop name: ")
        recordScore(str(x), str(lastscore), 'coopscores.xml', difficulty)
        running = False
        coopgame = False
      elif(coops.GAMEOVER == False and Paused == False):
        coops.update()

