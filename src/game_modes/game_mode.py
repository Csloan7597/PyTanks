__author__ = 'conor'

__author__ = 'conor'

import random
from pgtools.utils import *
from sprites import tank, game_items, enemy


class GameMode(object):
    """Class representing one player game mode"""

    def __init__(self, screen):
        pygame.init()
        self.screen = screen

        # Load background and resources, adding them to the correct sprite groups
        self.background = create_tiled_surface(screen.get_size(), '../resources/images/grass.jpg')
        self.screen.blit(self.background, (0, 0))
        self.font = pygame.font.Font('../resources/fonts/trebucbd.ttf', 28)

        # Set up initial game state
        self.GAME_OVER = False

    def game_is_over(self):
        return self.GAME_OVER

    def get_score(self):
        raise Exception('Abstract method, please override in the subclass')

    def display_game_message(self):
        raise Exception('Abstract method, please override in the subclass')

    def update_sprites(self):
        raise Exception('Abstract method, please override in the subclass')

    def generate_game_items(self):
        raise Exception('Abstract method, please override in the subclass')

    def handle_collisions(self):
        raise Exception('Abstract method, please override in the subclass')

    def draw_changes(self):
        raise Exception('Abstract method, please override in the subclass')

    def check_for_game_over(self):
        raise Exception('Abstract method, please override in the subclass')

    def get_game_mode(self):
        raise Exception('Abstract method, please override in the subclass')

    def get_game_difficulty(self):
        return self.difficulty

    def update(self):
        """
        Allows the game runner to update this game by one iteration.
        :return:
        """
        self.screen.blit(self.background, (0, 0))
        self.generate_game_items()
        self.handle_collisions()

        # Update all of the game sprites, allowing them to move, respond to events, etc.
        self.update_sprites()

        # Draw changes to screen
        self.draw_changes()

        self.display_game_message()
        self.check_for_game_over()

        pygame.display.flip()