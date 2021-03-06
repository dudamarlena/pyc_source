# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/ER/PISA.py
# Compiled at: 2008-10-19 12:19:52
from Kamaelia.Visualisation.PhysicsGraph import BaseParticle
import pygame
from pygame.locals import *

def abbreviate(string):
    """Abbreviates strings to capitals, word starts and numerics and underscores"""
    out = ''
    prev = ''
    for c in string:
        if c.isupper() or c.isdigit() or c == '_' or c == '.' or c.isalpha() and not prev.isalpha():
            out += c.upper()
        prev = c

    return string


_COMPONENT_RADIUS = 32

def nearest45DegreeStep((dx, dy)):
    """Returns (in degrees) the nearest 45 degree angle match to the supplied vector.

       Returned values are one of 0, 45, 90, 135, 180, 225, 270, 315.       
       If the supplied vector is (0,0), the returned angle is 0.
    """
    if dx == 0 and dy == 0:
        return 0
    cos = 0.9238795325112867
    sin = 0.3826834323650898
    dx, dy = dx * cos - dy * sin, dy * cos + dx * sin
    index = (
     dy > 0, dx > 0, abs(dy) > abs(dx))
    return angleMappings[index]


angleMappings = {(True, True, False): 0, (True, True, True): 45, 
   (True, False, True): 90, 
   (True, False, False): 135, 
   (False, False, False): 180, 
   (False, False, True): 225, 
   (False, True, True): 270, 
   (False, True, False): 315}

class PISA(BaseParticle):
    labelangles = {0: 2, 45: 3, 90: 0, 135: 1, 180: 2, 225: 3, 270: 0, 315: 1}

    def Isa(ID, position, name):
        """        ISA(ID,position,name) -> new PISA object with boxtype "isa".

        Static method.
        """
        return PISA(ID=ID, position=position, name=name, boxtype='isa')

    Isa = staticmethod(Isa)

    def __init__(self, ID, position, name, boxtype):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PISA, self).__init__(position=position, ID=ID)
        self.name = name
        self.ptype = 'isa'
        self.left = 0
        self.top = 0
        self.radius = 16
        self.buildLabels()
        self.selected = False
        pygame.font.init()

    def buildLabels(self):
        """        Pre-renders text labels to surfaces for different 45 degree
        angles.

        On exit:
        self.label is a list of surfaces containing rendered labels
        self.slabel is the same but coloured for when the particle is selected
        self.labelxo is a list of x-offsets for each label's centre.
        self.labelyo is a list of y-offsets fo reach label's centre.
        self.desclabel is the description label displayed when selected
        """
        from pygame.transform import rotozoom, rotate
        font = pygame.font.Font(None, 14)
        label = font.render(' ' + abbreviate(self.name) + ' ', True, (0, 0, 0))
        self.label = []
        self.labelxo = []
        self.labelyo = []
        self.label.append(rotate(label, 90))
        self.label.append(rotozoom(label, 45, 1.0))
        self.label.append(label)
        self.label.append(rotozoom(label, -45, 1.0))
        slabel = font.render(' ' + abbreviate(self.name) + ' ', True, (96, 96, 255))
        self.slabel = []
        self.slabel.append(rotate(slabel, 90))
        self.slabel.append(rotozoom(slabel, 45, 1.0))
        self.slabel.append(slabel)
        self.slabel.append(rotozoom(slabel, -45, 1.0))
        self.radius = max(self.slabel[0].get_width(), self.slabel[0].get_height()) / 2
        for l in self.label:
            self.labelxo.append(-l.get_width() / 2)
            self.labelyo.append(-l.get_height() / 2)

        font = pygame.font.Font(None, 20)
        self.desclabel = font.render('ISA : ' + self.name, True, (0, 0, 0), (255, 255,
                                                                             255))
        return

    def render(self, surface):
        """        Multi-pass rendering generator.

        Renders this particle in multiple passes to the specified pygame surface -
        yielding the number of the next pass to be called on between each. Completes
        once it is fully rendered.
        """
        direction = (0, 0)
        yield 1
        x = int(self.pos[0] - self.left)
        y = int(self.pos[1] - self.top)
        for p in self.bondedTo:
            endx = int(p.pos[0] - self.left)
            endy = int(p.pos[1] - self.top)
            colour = (192, 192, 192)
            pygame.draw.line(surface, colour, (x, y), (endx, endy))
            midx = (x - endx) / 2 + endx
            midy = (y - endy) / 2 + endy
            mid = (midx, midy)
            direction = (
             endx - x, endy - y)
            length = (direction[0] ** 2 + direction[1] ** 2) ** 0.5
            direction = [ 6 * n / length for n in direction ]
            norm = (
             -direction[1], direction[0])
            leftarrow = (
             mid[0] - direction[0] - norm[0], mid[1] - direction[1] - norm[1])
            rightarrow = (mid[0] - direction[0] + norm[0], mid[1] - direction[1] + norm[1])
            pygame.draw.line(surface, colour, mid, leftarrow, 2)
            pygame.draw.line(surface, colour, mid, rightarrow, 2)

        yield 3
        if direction == (0, 0):
            for p in self.bondedFrom:
                if p.ptype == self.ptype:
                    endx = int(p.pos[0] - self.left)
                    endy = int(p.pos[1] - self.top)
                    direction = (endx - x, endy - y)

        i = PISA.labelangles[nearest45DegreeStep(direction)]
        colour = (255, 255, 255)
        bordercolour = (192, 192, 192)
        if self.selected:
            colour = (160, 160, 255)
            bordercolour = (224, 0, 0)
        R = int(self.radius * 1.3 - self.radius)
        if R < 5:
            R = 5
        x_radius = self.radius + R
        y_radius = x_radius / 2
        if y_radius > 20:
            y_radius = 20
        points = [(x - x_radius, y),
         (
          x, y + y_radius),
         (
          x + x_radius, y),
         (
          x, y - y_radius)]
        points = [
         (
          x - 24, y),
         (
          x, y + 16),
         (
          x + 24, y),
         (
          x, y - 16)]
        pygame.draw.circle(surface, (255, 255, 255), (x, y), self.radius)
        pygame.draw.circle(surface, bordercolour, (x, y), self.radius, 2)
        if self.selected:
            l = self.slabel[i]
        else:
            l = self.label[i]
        surface.blit(l, (x + self.labelxo[i], y + self.labelyo[i]))
        if self.selected:
            yield 10
            surface.blit(self.desclabel, (72, 16))

    def setOffset(self, (x, y)):
        """        Set the offset of the top left corner of the rendering area.

        If this particle is at (px,py) it will be rendered at (px-x,py-y).
        """
        self.left = x
        self.top = y

    def select(self):
        """Tell this particle it is selected."""
        self.selected = True

    def deselect(self):
        """Tell this particle it is deselected."""
        self.selected = False