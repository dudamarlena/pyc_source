# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Python32\lib\site-packages\Ferra\sprite.py
# Compiled at: 2012-10-03 11:42:35
from pyglet.sprite import Sprite
from pyglet.image import load

def wrap_slide(value, width):
    if value > width:
        value -= width
    elif value < 0:
        value += width
    return value


def wrap_stop(value, width):
    if value > width:
        value = width
    elif value < 0:
        value = 0
    return value


class Sprite(Sprite):
    """ A clone of pyglet.sprite.Sprite with rotate function,
        please do not create an instance of this directly use create_sprite instead
    """

    def rotate(self, degree):
        self.rotation += degree


def center_image(image):
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2


def create_sprite(imagename, x, y, rotation=0):
    r""" Create a sprite at the position x, y, with rotation 'rotation',
        imagename is the file name of the image with the directory,
        if it is in the current directory just put ./ or .\ at the beginning
    """
    image = load(imagename)
    center_image(image)
    sprite = Sprite(img=image, x=x, y=y)
    sprite.rotation = rotation
    return sprite


class StaticSprite(object):
    """ A sprite that just stands there """

    def __init__(self, imagename, x, y):
        self.image = load(imagename)
        center_image(self.image)
        self.x, self.y = x, y

    def draw(self):
        try:
            self.image.blit(self.x, self.y)
        except AttributeError:
            pass

    def delete(self):
        self.image = None
        return

    def set_image(self, imagename):
        self.image = load(imagename)


class RotatingSprite(Sprite):
    """ A sprite that rotates,
        img must have been loaded"""

    def __init__(self, img, x, y, rotate_speed, batch=None):
        center_image(img)
        super(RotatingSprite, self).__init__(img=img, x=x, y=y, batch=batch)
        self.rotate_speed = rotate_speed

    def update(self, dt):
        rotation = self.rotation + self.rotate_speed * dt
        self.rotation = wrap_slide(rotation, 360.0)