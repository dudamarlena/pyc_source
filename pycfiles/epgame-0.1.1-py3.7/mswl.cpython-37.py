# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\epgame\mswl.py
# Compiled at: 2019-08-13 00:59:58
# Size of source mod 2**32: 11818 bytes
from pygame.locals import *
import pygame, sys, time, random, math, datetime
pygame.init()
deepPink = (255, 20, 147)
violet = (238, 130, 238)
purple = (128, 0, 128)
skyBlue = (135, 206, 235)
yellow = (255, 255, 0)
gold = (255, 215, 0)
orange = (255, 165, 0)
tomato = (255, 99, 71)
snow = (255, 250, 250)
silver = (192, 192, 192)
brown = (165, 42, 42)
white = (255, 255, 255)
pink = (255, 192, 203)
black = (0, 0, 0)
blue = (0, 0, 255)
grey = (128, 128, 128)
red = (255, 0, 0)
green = (0, 128, 0)
darkGreen = (0, 100, 0)
userEvent = pygame.USEREVENT

def get_now_second():
    return datetime.datetime.now().second


def key_down(a):
    return a.type == KEYDOWN


def key_up(a):
    return a.type == KEYUP


def mouse_down(a):
    return a.type == MOUSEBUTTONDOWN


def mouse_up(a):
    return a.type == MOUSEBUTTONUP


def mouse_move(a):
    return a.type == MOUSEMOTION


def setInterval(a, b):
    return pygame.time.set_timer(a, b)


def event_type(a, b):
    return a.type == b


def window_close(a):
    if a.type == QUIT:
        pygame.quit()
        sys.exit()


def get_event():
    return pygame.event.get()


def update_screen():
    return pygame.display.update()


def set_screen(a, b):
    return pygame.display.set_mode((a, b), 0, 32)


def collide_img(a, b):
    return pygame.sprite.collide_rect(a, b)


def collide_shape(a, b):
    x1 = a.x
    y1 = a.y
    w1 = a.width
    h1 = a.height
    x2 = b.x
    y2 = b.y
    w2 = b.width
    h2 = b.height
    lx = max(x1 + w1 - x2, x2 + w2 - x1)
    ly = max(y1 + h1 - y2, y2 + h2 - y1)
    if lx < w1 + w2:
        if ly < h1 + h2:
            if w1 + w2 - lx < h1 + h2 - ly:
                return True
            return True


def c_collide_r(a, b):
    DeltaX = a.x - max(b.x, min(a.x, b.x + b.width))
    DeltaY = a.y - max(b.y, min(a.y, b.y + b.height))
    return DeltaX * DeltaX + DeltaY * DeltaY <= a.r * a.r


def clear(a):
    a.fill(black)


def drawXY():
    pygame.display.set_caption('x,y:' + str(pygame.mouse.get_pos()))


def drawGrid(a, w, h, size, co=darkGreen):
    for x in range(0, w + size, size):
        x_line = Line(x, 0, x, h, co)
        x_line.draw(a)

    for y in range(0, h + size, size):
        y_line = Line(0, y, w, y, co)
        y_line.draw(a)


def playSound(a):
    pygame.mixer.init()
    pygame.mixer.music.load(a)
    pygame.mixer.music.play()


class Image(pygame.sprite.Sprite):

    def __init__(self, img, x, y, w, h, index=0, down=False, up=False):
        pygame.sprite.Sprite.__init__(self)
        self.src = img
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.flip_x = False
        self.flip_y = False
        self.degree = 0
        self.speedx = 0
        self.speedy = 0
        self.isFeed = 0
        self.isExited = False
        self.isRotated = True
        self.image = pygame.image.load(self.src).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.state = 0
        self.index = index
        self.down = down
        self.up = up

    def isClicked(self, a, b=0, c=0, d=0, e=0):
        if a.type == MOUSEBUTTONDOWN:
            x, y = a.pos
            pressed_array = pygame.mouse.get_pressed()
            if self.rect.left + b <= x <= self.rect.right + c:
                if self.rect.top + d <= y <= self.rect.bottom + e:
                    if pressed_array[0]:
                        return True

    def flip(self, a=False, b=False):
        self.image = pygame.transform.flip(self.image, a, b)

    def rotate(self, a):
        self.image = pygame.image.load(self.src).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.image = pygame.transform.rotate(self.image, a)

    def scale(self, a, b):
        self.image = pygame.image.load(self.src).convert_alpha()
        self.image = pygame.transform.scale(self.image, (int(self.width * a), int(self.height * b)))

    def draw(self, a):
        a.blit(self.image, self.rect)

    def drawRotate(self, a):
        w = self.image.get_rect().width
        h = self.image.get_rect().height
        a.blit(self.image, (self.rect.x - w // 2, self.rect.y - h // 2))


class Text(object):

    def __init__(self, text, x, y, size, co=(255, 255, 255), style=None):
        self.x = x
        self.y = y
        self.color = co
        self.src = text
        self.style = style
        self.size = size
        self.font = None
        self.text = None
        self.rect = None

    def draw(self, a):
        self.font = pygame.font.Font(self.style, self.size)
        self.text = self.font.render(self.src, True, self.color)
        self.rect = self.text.get_rect(topleft=(self.x, self.y))
        a.blit(self.text, self.rect)

    def isClicked(self, a):
        if a.type == MOUSEBUTTONDOWN:
            x, y = a.pos
            pressed_array = pygame.mouse.get_pressed()
            if self.x <= x <= self.x + self.size / 2 * len(self.src):
                if self.y <= y <= self.y + self.size / 2:
                    if pressed_array[0]:
                        return True


class Rectangle(object):

    def __init__(self, x=100, y=100, w=50, h=50, co=blue, a=0):
        self.fillStyle = co
        self.x = x
        self.y = y
        self.width = w
        self.height = h
        self.lineWidth = a
        self.index = 0
        self.state = 0

    def draw(self, a):
        pygame.draw.rect(a, self.fillStyle, Rect((self.x, self.y), (self.width, self.height)), self.lineWidth)

    def isClicked(self, a):
        if a.type == MOUSEBUTTONDOWN:
            x, y = a.pos
            pressed_array = pygame.mouse.get_pressed()
            if self.x <= x <= self.x + self.width:
                if self.y <= y <= self.y + self.height:
                    if pressed_array[0]:
                        return True


class Circle(object):

    def __init__(self, x, y, r, co=blue):
        self.x = x
        self.y = y
        self.r = r
        self.fillStyle = co

    def draw(self, a):
        pygame.draw.circle(a, self.fillStyle, (self.x, self.y), self.r)

    def isClicked(self, a):
        if a.type == MOUSEBUTTONDOWN:
            x, y = a.pos
            pressed_array = pygame.mouse.get_pressed()
            if self.x - self.r <= x <= self.x + self.r:
                if self.y - self.r <= y <= self.y + self.r:
                    if pressed_array[0]:
                        return True

    def dropOn(self, b):
        if c_collide_r(self, b):
            if self.y < b.y:
                self.state = b.index
                boxMoveX = 0
                self.fillStyle = b.fillStyle


class Triangle(object):

    def __init__(self, x1, y1, x2, y2, x3, y3, co=blue, a=0):
        self.fillStyle = co
        self.lineWidth = a
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x3 = x3
        self.y3 = y3
        self.pointList = ((x1, y1), (x2, y2), (x3, y3))

    def draw(self, a):
        pygame.draw.polygon(a, self.fillStyle, self.pointList, self.lineWidth)


class Polygon(object):

    def __init__(self, pl, co=blue, a=0):
        self.fillStyle = co
        self.lineWidth = a
        self.pointList = pl

    def draw(self, a):
        pygame.draw.polygon(a, self.fillStyle, self.pointList, self.lineWidth)


class Line(object):

    def __init__(self, x1, y1, x2, y2, co=blue, a=1):
        self.color = co
        self.lineWidth = a
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

    def draw(self, a):
        pygame.draw.line(a, self.color, (self.x1, self.y1), (self.x2, self.y2), self.lineWidth)


class Ellipse(object):

    def __init__(self, x, y, w, h, co=blue, a=0):
        self.fillStyle = co
        self.lineWidth = a
        self.x = x
        self.y = y
        self.width = w
        self.height = h

    def draw(self, a):
        pygame.draw.ellipse(a, self.fillStyle, (self.x, self.y, self.width, self.height), self.lineWidth)

    def isClicked(self, a):
        if a.type == MOUSEBUTTONDOWN:
            x, y = a.pos
            pressed_array = pygame.mouse.get_pressed()
            if self.x <= x <= self.x + self.width:
                if self.y <= y <= self.y + self.height:
                    if pressed_array[0]:
                        return True


def set_interval(a, b):
    return pygame.time.set_timer(a, b)