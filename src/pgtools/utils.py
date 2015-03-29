# Copyright (c) 2007-2010 Nick Efford <nde@comp.leeds.ac.uk>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.


"""Various utilities to simplify the use of Pygame."""

__author__  = 'Nick Efford'
__version__ = '1.2 (2010-11-08)'


import pygame


def create_surface(size, colour=(255,255,255)):
    """Returns a surface with the specified size (width and height,
       as a 2-tuple) and, optionally, colour (a 3-tuple)."""

    surface = pygame.Surface(size)
    surface = surface.convert()
    surface.fill(colour)

    return surface


def create_tiled_surface(size, filename):
    """Returns a surface with the specified size (width and height,
       as a 2-tuple), tiled using the image with the given filename."""

    surface = pygame.Surface(size).convert()
    tile = pygame.image.load(filename).convert()
    width, height = size
    tile_width, tile_height = tile.get_size()

    y = 0
    while y < height:
        x = 0
        while x < width:
            surface.blit(tile, (x, y))
            x += tile_width
        y += tile_height

    return surface


def running():
    """Checks for a Quit event or the Esc key and returns True or False
       to indicate whether Pygame should continue running."""

    check = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            check = False
        elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
            check = False

    return check


class Window(object):
    """A basic window that displays a Pygame surface as a background.

       The background is painted once only, before the window enters its
       display loop.  If you want a dynamic background, or if you want
       to do animation on top of the background, you will need to create
       a subclass of Window and override its update method.  Depending
       on what you are trying to achieve, you may need to repaint the
       background within your overridden method, with this code:

         self.screen.blit(self.background, (0, 0))"""

    def __init__(self, size, title='Pygame Window'):
        """Creates a window with the given size (width and height,
           as a 2-tuple) and, optionally, the given title."""

        self.size = size
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(title)

    def display(self, background, frame_rate=30):
        """Sets the background of the window to the given surface and
           displays it.  The frame rate for display updates can be
           provided as a second argument, if desired."""

        self.background = background
        self.screen.blit(self.background, (0, 0))
        clock = pygame.time.Clock()
        while running():
            clock.tick(frame_rate)
            self.update()
            pygame.display.flip()

    def update(self):
        """A stub that can be overridden by subclasses to update the
           display on a frame-by-frame basis, e.g. with moving sprites."""

        pass
