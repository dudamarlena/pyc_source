# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Apps/Whiteboard/Painter.py
# Compiled at: 2008-10-19 12:19:52
import Axon
from Axon.Ipc import producerFinished, shutdownMicroprocess
import pygame

class Painter(Axon.Component.component):
    """    Painter() -> new Painter component.
    """
    Inboxes = {'inbox': 'For receiving PygameDisplay events', 'control': '', 
       'colour': 'select drawing, using colour', 
       'erase': 'select eraser', 
       'load': 'image to load', 
       'save': 'filename to save image to'}
    Outboxes = {'outbox': 'outputs drawing instructions', 'signal': ''}

    def __init__(self):
        super(Painter, self).__init__()
        self.sendbuffer = []

    def finished(self):
        while self.dataReady('control'):
            msg = self.recv('control')
            if isinstance(msg, producerFinished) or isinstance(msg, shutdownMicroprocess):
                self.send(msg, 'signal')
                return True

        return False

    def main(self):
        """Main loop"""
        yield 1
        (r, g, b) = (0, 0, 0)
        dragging = False
        mode = 'LINE'
        while not self.finished():
            while self.dataReady('colour'):
                (r, g, b) = self.recv('colour')
                mode = 'LINE'

            while self.dataReady('erase'):
                self.recv('erase')
                mode = 'ERASE'

            while self.dataReady('load'):
                command = self.recv('load')
                self.sendbuffer.append(command)

            while self.dataReady('save'):
                command = self.recv('save')
                self.sendbuffer.append(command)

            while self.dataReady('inbox'):
                message = self.recv('inbox')
                for data in message:
                    if data.type == pygame.MOUSEBUTTONDOWN:
                        if data.button == 1:
                            oldpos = data.pos
                            dragging = True
                        elif data.button == 3:
                            pygame.display.toggle_fullscreen()
                    elif data.type == pygame.MOUSEMOTION and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                    elif data.type == pygame.MOUSEBUTTONUP and dragging:
                        self.cmd(mode, oldpos, data.pos, r, g, b)
                        oldpos = data.pos
                        dragging = False

            self.flushbuffer()
            self.pause()
            yield 1

    def cmd(self, mode, oldpos, newpos, r, g, b):
        if mode == 'LINE':
            self.sendbuffer.append(['LINE', str(r), str(g), str(b), str(oldpos[0]), str(oldpos[1]), str(newpos[0]), str(newpos[1])])
        elif mode == 'ERASE':
            self.sendbuffer.append(['CIRCLE', '255', '255', '255', str(newpos[0]), str(newpos[1]), '8'])

    def flushbuffer(self):
        if len(self.sendbuffer):
            self.send(self.sendbuffer[:], 'outbox')
            self.sendbuffer = []