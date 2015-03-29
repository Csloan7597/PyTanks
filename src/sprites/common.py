__author__ = 'conor'

import pygame, random, sys, os.path

directions = ['n', 'e', 's', 'w', 'nw', 'ne', 'sw', 'se']


def load_image(file):
    """
    Loads a specific image from a file,  given the image's filepath.
    """
    file = os.path.join('../resources/images', file)
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
