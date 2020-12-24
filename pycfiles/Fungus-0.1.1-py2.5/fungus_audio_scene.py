# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fungus_audio_scene.py
# Compiled at: 2009-02-26 08:30:19
"""An example for a fungus scene definition. """
from os import path
from pyglet.window import key
from fungus_scene import BaseScene
from fungus_core import __copyright__
from time import time
from random import random, choice
from os import listdir
from os.path import isfile, join, dirname
sword_file = 'sword.wav'
AUDIO_BASE_PATH = join(dirname(__file__), 'audio')

class Scene(BaseScene):
    """A dummy scene - mostly just the Scene API."""

    def __init__(self, core, *args, **kwds):
        """Initialize the scene with a core object for basic functions."""
        super(Scene, self).__init__(core, *args, **kwds)
        self.players = []
        self.bg = self.core.load_player(sword_file, loop=True)
        self.state = {'scene': None}
        self.start_time = time()
        return

    def update(self):
        """Update the stats of all scene objects. 

Don't blit them, though. That's done by the Game itself.

To show something, add it to the self.visible list. 
To add a collider, add it to the self.colliding list. 
To add an overlay sprite, add it to the self.overlay list. 
"""
        self.bg.dispatch_events()
        for player in self.players[:]:
            player.dispatch_events()
            if not player.playing:
                self.players.remove(player)

        if self.state['scene'] is None:
            self.start_menu()
        if self.state['scene'] == 'menu' and time() - self.start_time >= 5:
            if self.bg.volume > 0.0:
                self.bg.volume -= 0.001
            else:
                self.start_intro()
        if time() - self.start_time > 10:
            self.core.win.has_exit = True
        return

    def start_menu(self):
        """Start the menu"""
        print 'start menu'
        self.state['scene'] = 'menu'
        self.bg.play()

    def start_intro(self):
        """Start the intro playback."""
        print 'start intro'
        self.state['scene'] = 'intro'
        self.intro_player = self.core.load_player(sword_file)
        self.bg.pause()
        self.intro_player.play()
        self.players.append(self.intro_player)

    def on_key_press(self, symbol, modifiers):
        """Forwarded keyboard input."""
        if symbol == key.ESCAPE:
            self.core.win.has_exit = True