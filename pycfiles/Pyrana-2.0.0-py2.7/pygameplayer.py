# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/players/pygameplayer.py
# Compiled at: 2011-07-09 22:56:18
import pygame.event, pygame.mixer, pygame.display, threading, time
from feather import Plugin
ENDEVENT = 42

class PyGamePlayer(Plugin):
    listeners = set(['songloaded', 'pause', 'skipsong', 'skipalbum'])
    messengers = set(['songstart', 'songpause', 'songend', 'songresume'])
    name = 'PyGamePlayer'

    def pre_run(self):
        pygame.display.init()
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(ENDEVENT)
        t = threading.Thread(target=self._songend_bubble, args=(self,))
        t.daemon = True
        t.start()

    def _songend_bubble(s, self):
        while self.runnable:
            event = pygame.event.get(ENDEVENT)
            if event:
                self.send('songend')
            else:
                time.sleep(0.1)

    def songloaded(self, payload):
        try:
            pygame.mixer.music.load(payload)
        except:
            pass

        pygame.mixer.music.play()
        self.playing = True
        self.send('songstart', payload)

    def pause(self, payload=None):
        if self.playing:
            pygame.mixer.music.pause()
            self.playing = False
            self.send('songpause')
        else:
            pygame.mixer.music.unpause()
            self.playing = True
            self.send('songresume')

    def skipsong(self, payload=None):
        pygame.mixer.music.stop()

    def skipalbum(self, payload=None):
        pygame.mixer.music.stop()