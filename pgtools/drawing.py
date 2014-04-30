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


"""Drawing functions for Pygame surfaces."""

__author__  = 'Nick Efford'
__version__ = '1.2 (2010-11-08)'


import os, pygame


font_cache = {}
current_font = None


def set_font(identifier, size):
    """Sets the current font for text drawing to the specified font
       filename/family and size.  Use the value None as an identifier
       to get a system default font."""

    global current_font

    key = '{}:{:d}'.format(identifier, size)
    if key in font_cache:
        current_font = font_cache[key]
    elif identifier and os.path.isfile(identifier):
        current_font = pygame.font.Font(identifier, size)
        font_cache[key] = current_font
    else:
        current_font = pygame.font.SysFont(identifier, size)
        font_cache[key] = current_font


def draw_text(surface, string, colour, position):
    """Draws some text at the given location on the specified surface,
       using the current font and the given colour."""

    text = current_font.render(string, True, colour)
    surface.blit(text, position)


def draw_image(surface, filename, position, alpha=False):
    """Draws an image loaded from the given filename at the given
       location on the specified surface.  A value of True should be
       given for alpha if the image contains transparent pixels."""

    image = pygame.image.load(filename)
    if alpha:
        surface.blit(image.convert_alpha(), position)
    else:
        surface.blit(image.convert(), position)


# Aliases for standard Pygame drawing functions

draw_rect = pygame.draw.rect
draw_polygon = pygame.draw.polygon
draw_circle = pygame.draw.circle
draw_ellipse = pygame.draw.ellipse
draw_arc = pygame.draw.arc
draw_line = pygame.draw.line
draw_lines = pygame.draw.lines
