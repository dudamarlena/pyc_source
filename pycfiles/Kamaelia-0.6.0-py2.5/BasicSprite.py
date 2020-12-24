# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Games4Kids/BasicSprite.py
# Compiled at: 2008-10-19 12:19:52
import pygame
from Axon.Component import component

class BasicSprite(pygame.sprite.Sprite, component):
    Inboxes = [
     'translation', 'imaging', 'inbox', 'control']
    allsprites = []

    def __init__(self, imagepath, name, pos=None, border=40):
        pygame.sprite.Sprite.__init__(self)
        component.__init__(self)
        self.imagepath = imagepath
        self.image = None
        self.original = None
        self.rect = None
        self.pos = pos
        if self.pos == None:
            self.pos = [
             100, 100]
        self.dir = ''
        self.name = name
        self.update = self.sprite_logic().next
        self.screensize = (924, 658)
        self.border = border
        self.__class__.allsprites.append(self)
        return

    def allSprites(klass):
        return klass.allsprites

    allSprites = classmethod(allSprites)

    def sprite_logic(self):
        while 1:
            yield 1

    def main(self):
        self.image = pygame.image.load(self.imagepath)
        self.original = self.image
        self.image = self.original
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        center = list(self.rect.center)
        current = self.image
        pos = center
        (dx, dy) = (0, 0)
        d = 10
        while 1:
            self.image = current
            if self.dataReady('imaging'):
                self.image = self.recv('imaging')
                current = self.image
            if self.dataReady('translation'):
                pos = self.recv('translation')
            if self.dataReady('inbox'):
                event = self.recv('inbox')
                if event == 'start_up':
                    dy = dy + d
                if event == 'stop_up':
                    dy = dy - d
                if event == 'start_down':
                    dy = dy - d
                if event == 'stop_down':
                    dy = dy + d
                if event == 'start_right':
                    dx = dx + d
                if event == 'stop_right':
                    dx = dx - d
                if event == 'start_left':
                    dx = dx - d
                if event == 'stop_left':
                    dx = dx + d
            if dx != 0 or dy != 0:
                self.pos[0] += dx
                if self.pos[0] > self.screensize[0] - self.border:
                    self.pos[0] = self.screensize[0] - self.border
                if self.pos[1] > self.screensize[1] - self.border:
                    self.pos[1] = self.screensize[1] - self.border
                if self.pos[0] < self.border:
                    self.pos[0] = self.border
                if self.pos[1] < self.border:
                    self.pos[1] = self.border
                self.pos[1] -= dy
                self.rect.center = self.pos
                self.send(self.pos, 'outbox')
            yield 1