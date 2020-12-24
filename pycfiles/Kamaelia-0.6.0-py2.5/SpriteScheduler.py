# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Games4Kids/SpriteScheduler.py
# Compiled at: 2008-10-19 12:19:52
import Axon
from Axon.Component import component
import pygame
from Kamaelia.UI.GraphicDisplay import PygameDisplay

class SpriteScheduler(component):
    Inboxes = [
     'inbox', 'control', 'callback']
    Outboxes = ['outbox', 'signal', 'display_signal']
    displaysize = (924, 658)
    bgcolour = (32, 0, 128)

    def __init__(self, sprites, **argd):
        super(SpriteScheduler, self).__init__(**argd)
        self.allsprites = []
        self.sprites = sprites
        self.background = pygame.Surface(self.displaysize)
        self.background.fill(self.bgcolour)
        self.disprequest = {'DISPLAYREQUEST': True, 'callback': (
                      self, 'callback'), 
           'size': self.displaysize, 
           'position': (50, 50)}

    def pygame_display_flip(self):
        self.send({'REDRAW': True, 'surface': self.display}, 'display_signal')

    def getDisplay(self):
        displayservice = PygameDisplay.getDisplayService()
        self.link((self, 'display_signal'), displayservice)
        self.send(self.disprequest, 'display_signal')
        while not self.dataReady('callback'):
            self.pause()
            yield 1

        self.display = self.recv('callback')

    def main(self):
        yield Axon.Ipc.WaitComplete(self.getDisplay())
        self.allsprites = pygame.sprite.RenderPlain(self.sprites)
        while 1:
            self.allsprites.update()
            self.display.blit(self.background, (0, 0))
            try:
                self.allsprites.draw(self.display)
            except TypeError:
                pass

            self.pygame_display_flip()
            yield 1