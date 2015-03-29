__author__ = 'conor'


import xml.etree.ElementTree as xo
from xml.dom.minidom import parse
import pygame


class HighScores:

    def __init__(self, scoresheets):
        """
        Construct high scores xml abstraction.
        :param scoresheets: Map of game mode to score sheet XML files
        """
        self.scoresheets = scoresheets

    def get_high_scores(self, game_mode, difficulty):
        """Given a sheet name and difficulty, this function will read in the high scores in simple text format,
        adding them to a dictionary, with score as the key, and name as the value.
        :param game_mode: game mode
        :param difficulty: game difficulty
        """
        results = dict()
        instance = xo.parse(self.scoresheets[game_mode])
        player_list = instance.findall('Player')
        for item in range (0, len(player_list)):
            name = player_list[item].findall('Name')
            score = player_list[item].findall('Score')
            diff = player_list[item].findall('Difficulty')
            if diff[0].text == difficulty:
                results[int(score[0].text)] = name[0].text
        return results

    def record_score(self, name, score, game_mode, difficulty):
        """
        Record a score in the correct xml file based on game mode & difficulty.
        :param name: team or player name
        :param score: team or player score
        :param game_mode:  game mode
        :param difficulty: difficulty
        """
        scoresheet = self.scoresheets[game_mode]
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

    def display_scores(self, game_mode, difficulty, screen):
        """
        given a dictionary of names and scores (see 'getHighScores()' this function displays the sorted (highest to lowest score)
        list of the best 10 scores with their respective names. Reading from the specified file.
        """

        maxi = 10
        font2 = pygame.font.Font('../resources/fonts/Purisa.ttf', 25)
        hiscores = self.get_high_scores(game_mode, difficulty)
        keys = hiscores.keys()
        xposn = 850
        xposs = 1100
        ypos = 180
        if game_mode == '1player':
            typem = font2.render("One Player Scores", True, (250, 100, 100))
        elif game_mode == '2player':
            typem = font2.render("Two Player Scores", True, (250, 100, 100))
        else:
            typem = font2.render("Co-op Scores", True, (250, 100, 100))
        rectm = typem.get_rect()
        rectm.midbottom = ((xposn+xposs)/2, ypos-85)
        screen.blit(typem, rectm)
        for key in reversed(sorted(hiscores)):
            message = font2.render("{0: ^}".format(hiscores[key]), True, (100, 100, 100))
            message2 = font2.render("{0: ^}".format(key), True, (100, 100, 100))
            rect2 = message2.get_rect()
            rect = message.get_rect()
            rect.midbottom = xposn, ypos
            rect2.midbottom = xposs, ypos
            if maxi > 0:
                screen.blit(message2, rect2)
                screen.blit(message, rect)
                ypos += 30
                maxi -= 1
