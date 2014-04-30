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


"""Various specialisations of standard Pygame sprites, adapted from
   code in "Game Programming" by Andy Harris (Wiley 2007)."""

__author__  = 'Nick Efford'
__version__ = '1.2 (2010-11-08)'


import os, pygame


# Standard movement directions

EAST      = 0
NORTHEAST = 1
NORTH     = 2
NORTHWEST = 3
WEST      = 4
SOUTHWEST = 5
SOUTH     = 6
SOUTHEAST = 7


class AnimatedSprite(pygame.sprite.Sprite):
    """Version of the basic Pygame sprite consisting of a sequence
       of animation frames.

       Each frame is represented by a PNG image with a filename like
       'foo01.png', 'foo02.png', etc.  It is assumed that the background
       of this image should be made transparent; the top-left corner
       of each image is sampled to determine the background colour."""

    file_pattern = '{}{:02d}.png'

    def __init__(self, dirpath, prefix, num_images):
        """Creates an AnimatedSprite using images from the specified
           directory, whose filenames have the specified prefix."""

        super().__init__()

        self.images = self._load_images(dirpath, prefix, num_images)
        self.counter = self.anim_delay = 3
        self.frame = 0
        self.image = self.images[self.frame]
        self.rect = self.image.get_rect()

    def _load_images(self, dirpath, prefix, num_images):

        images = []
        for i in range(num_images):
            filename = self.file_pattern.format(prefix, i)
            pathname = os.path.join(dirpath, filename)
            image = pygame.image.load(pathname).convert()
            colour = image.get_at((0, 0))
            image.set_colorkey(colour)
            images.append(image)

        return images

    def update(self):
        """Updates this Sprite."""

        self.animate()
        self.move()
        self.check_bounds()

    def animate(self):
        """Animates this Sprite by changing its image at regular intervals."""

        self.counter -= 1
        if self.counter == 0:
            self.counter = self.anim_delay
            self.frame += 1
            if self.frame == len(self.images):
                self.frame = 0
            self.image = self.images[self.frame]

    def move(self):
        """Moves this Sprite.
           Note: this is a stub that can be overridden in subclasses."""

        pass

    def check_bounds(self):
        """Checks whether this Sprite is within bounds.
           Note: this is a stub that can be overridden in subclasses."""

        pass



class MovingAnimatedSprite(AnimatedSprite):
    """Version of AnimatedSprite in which the sprite is moving continually
       in any one of eight possible directions."""

    directions = ('e', 'ne', 'n', 'nw', 'w', 'sw', 's', 'se')
    delta_x = (1,  .7,  0, -.7, -1, -.7, 0, .7)
    delta_y = (0, -.7, -1, -.7,  0,  .7, 1, .7)
    min_speed = 2
    max_speed = 10

    def __init__(self, dirpath, prefix, num_images):
        """Creates a MovingAnimatedSprite using images from the specified
           dirpathectory, whose filenames have the specified prefix."""

        super(AnimatedSprite, self).__init__()

        self.images = []
        for direction in self.directions:
            full_prefix = prefix + '_' + direction
            sequence = self._load_images(dirpath, full_prefix, num_images)
            self.images.append(sequence)

        self.direction = EAST
        self.frame = 0
        self.image = self.images[self.direction][self.frame]
        self.rect = self.image.get_rect()
        self.counter = self.anim_delay = 3
        self.speed = self.min_speed

    def animate(self):
        """Animates this Sprite by changing its image at regular intervals."""

        self.counter -= 1
        if self.counter == 0:
            self.counter = self.anim_delay
            self.frame += 1
            if self.frame == len(self.images[self.direction]):
                self.frame = 0
            self.image = self.images[self.direction][self.frame]

    def move(self):
        """Moves this Sprite in the current direction at the current speed."""

        self.dx = self.delta_x[self.direction]*self.speed
        self.dy = self.delta_y[self.direction]*self.speed
        self.rect.centerx += self.dx
        self.rect.centery += self.dy

    def turn_left(self):
        """Turns this Sprite left by 45 degrees."""

        self.direction += 1
        if self.direction > SOUTHEAST:
            self.direction = EAST

    def turn_right(self):
        """Turns this Sprite right by 45 degrees."""

        self.direction -= 1
        if self.direction < EAST:
            self.direction = SOUTHEAST

    def speed_up(self):
        """Increases the speed of this Sprite."""

        self.speed = min(self.speed+1, self.max_speed)

    def slow_down(self):
        """Decreases the speed of this Sprite."""

        self.speed = max(self.speed-1, self.min_speed)
