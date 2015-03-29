__author__ = 'conor'

from pgtools.utils import *
from game_modes import one_player, two_player, coop
from high_scores import scores
import inputbox

# -------- INITIAL CONFIG -------- #
pygame.init()
screen = pygame.display.set_mode((1200, 800))
clock = pygame.time.Clock()

# Load resources, like paused message
font = pygame.font.Font('../resources/fonts/Purisa.ttf', 35)
paused_message = font.render("Paused", True, (255, 0, 0))
prect = paused_message.get_rect()
prect.center = (600, 400)
high_scores = scores.HighScores({"1player": "./high_scores/1player.xml",
                                 "2player": "./high_scores/2player.xml",
                                 "coop": "./high_scores/coop.xml"})

# Global game state
running = True
game_mode = "1player"
difficulty = 'easy'


def display_difficulty(difficulty, screen):
    if difficulty == 'easy':
        message = font.render("Easy", True, (0, 0, 100))
    elif difficulty == 'medium':
        message = font.render("Medium", True, (20, 20, 20))
    elif difficulty == 'hard':
        message = font.render("Hard", True, (255, 0, 0))
    rect = message.get_rect()
    rect.bottomleft = (screen.get_width()-130, 60)
    screen.blit(message, rect)


def change_difficulty(difficulty):
    if difficulty == 'easy':
        return 'medium'
    elif difficulty == 'medium':
        return 'hard'
    elif difficulty == 'hard':
        return 'easy'


def change_high_score_mode(game_mode):
    if game_mode == '1player':
        return '2player'
    elif game_mode == '2player':
        return 'coop'
    else:
        return '1player'


def run_game(game):
    """Given a certain game mode, run the game, listening for certain events and recording scores"""
    paused = False
    game_running = True
    score = -1

    while game_running:
        clock.tick(30)

        # Listen for pause and escape events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
            elif event.type == pygame.KEYDOWN:
                key = pygame.key.get_pressed()
                if key[pygame.K_p] and not paused:
                    paused = True
                elif key[pygame.K_p] and paused:
                    paused = False
                elif key[pygame.K_ESCAPE]:
                    game_running = False
                    paused = False

        if game.game_is_over():
            game_running = False
            score = game.get_score()

        if paused:
            screen.blit(paused_message, prect)
            pygame.display.flip()

        if not paused:
            game.update()

    # Record Score
    if score is not -1:
        inp = str(inputbox.ask(screen, 'Player / Team name'))
        high_scores.record_score(inp, score, game.get_game_mode(), game.get_game_difficulty())


# -------- RUN PYTANKS --------- #


# While loop representing the entire game session
while running:
    clock.tick(30)

    # Handle quit event
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Display background, difficulty and high scores
    background = create_tiled_surface(screen.get_size(), '../resources/images/background.png')
    screen.blit(background, (0, 0))
    display_difficulty(difficulty, screen)
    high_scores.display_scores(game_mode, difficulty, screen)
    pygame.display.flip()

    # Handle key presses to control menu
    keys = pygame.key.get_pressed()
    if keys[pygame.K_2]:
        run_game(two_player.TwoPlayer(screen, difficulty))
    elif keys[pygame.K_1]:
        run_game(one_player.OnePlayer(screen, difficulty))
    elif keys[pygame.K_c]:
        run_game(coop.Cooperative(screen, difficulty))
    elif keys[pygame.K_d]:
        difficulty = change_difficulty(difficulty)
    elif keys[pygame.K_h]:
        game_mode = change_high_score_mode(game_mode)