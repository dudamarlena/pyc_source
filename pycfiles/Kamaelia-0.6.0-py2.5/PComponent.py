# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Visualisation/Axon/PComponent.py
# Compiled at: 2008-10-19 12:19:52
import pygame
from Kamaelia.Visualisation.PhysicsGraph import BaseParticle
from pygame.locals import *
_COMPONENT_RADIUS = 32

def abbreviate(string):
    """Abbreviates dot-delimited string to the final (RHS) term"""
    return string.split('.')[(-1)]


def acronym(string):
    """Abbreviates strings to capitals, word starts and numerics and underscores"""
    out = ''
    prev = ''
    for c in string:
        if c.isupper() or c == '_' or c == '.' or c.isalpha() and not prev.isalpha():
            out += c.upper()
        prev = c

    return out


colours = [
 (255, 128, 128),
 (255, 192, 128),
 (224, 224, 128),
 (128, 255, 128),
 (128, 255, 192),
 (128, 224, 224),
 (128, 128, 255)]

class PComponent(BaseParticle):
    """    PComponent(ID,position,name) -> new PComponent object.
    
    Particle representing an Axon/Kamaelia Component for topology visualisation.
    
    Keyword arguments:
    
    - ID        -- a unique ID for this particle
    - position  -- (x,y) tuple of particle coordinates
    - name      -- The full dot-delimited pathname of the component being represented
    """

    def __init__(self, ID, position, name):
        """x.__init__(...) initializes x; see x.__class__.__doc__ for signature"""
        super(PComponent, self).__init__(position=position, ID=ID)
        self.set_label(name)
        self.ptype = 'component'
        self.shortname = abbreviate(name)
        self.left = 0
        self.top = 0
        self.selected = False
        self.radius = _COMPONENT_RADIUS

    def set_label(self, newname):
        self.name = newname
        self.shortname = abbreviate(newname)
        acro = acronym(newname)
        oldhue = []
        for i in xrange(len(acro)):
            factor = acro[:i + 1]
            print factor
            hue = list(colours[(factor.__hash__() % len(colours))])
            if oldhue == []:
                oldhue = hue
            else:
                hue[0] = (hue[0] + oldhue[0]) / 2
                hue[1] = (hue[1] + oldhue[1]) / 2
                hue[2] = (hue[2] + oldhue[2]) / 2

        self.colour = hue
        self.bordercolour = [ x * 0.75 for x in hue ]
        pygame.font.init()
        font = pygame.font.Font(None, 20)
        self.slabel = font.render(self.shortname, True, (0, 0, 0))
        self.slabelxo = -self.slabel.get_width() / 2
        self.slabelyo = -self.slabel.get_height() / 2
        description = 'Component ' + self.shortname + ' : ' + self.name
        self.desclabel = font.render(description, True, (0, 0, 0), (255, 255, 255))
        return

    def render(self, surface):
        """        Multi-pass rendering generator.
        
        Renders this particle in multiple passes to the specified pygame surface - 
        yielding the number of the next pass to be called on between each. Completes
        once it is fully rendered.
        """
        x = int(self.pos[0] - self.left)
        y = int(self.pos[1] - self.top)
        yield 1
        for p in self.bondedTo:
            px = int(p.pos[0] - self.left)
            py = int(p.pos[1] - self.top)
            pygame.draw.line(surface, (192, 192, 192), (x, y), (px, py))

        yield 2
        colour = self.colour
        bordercolour = self.bordercolour
        if self.selected:
            colour = (160, 160, 255)
            bordercolour = (224, 0, 0)
        points = [
         (
          x - self.radius, y),
         (
          x - self.radius / 2, y - int(self.radius * 0.86)),
         (
          x + self.radius / 2, y - int(self.radius * 0.86)),
         (
          x + self.radius, y),
         (
          x + self.radius / 2, y + int(self.radius * 0.86)),
         (
          x - self.radius / 2, y + int(self.radius * 0.86))]
        pygame.draw.polygon(surface, colour, points)
        pygame.draw.polygon(surface, bordercolour, points, 3)
        yield 3
        surface.blit(self.slabel, (x + self.slabelxo, y + self.slabelyo))
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
        """Tell this particle it is selected"""
        self.selected = True

    def deselect(self):
        """Tell this particle it is deselected"""
        self.selected = False