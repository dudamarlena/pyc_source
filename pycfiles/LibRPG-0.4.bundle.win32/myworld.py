# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\pygame\librpg\librpg\test\worldtest\myworld.py
# Compiled at: 2009-09-27 16:01:18
from librpg.world import World
from librpg.util import Position
from librpg.party import Character, Party
from librpg.path import *
from worldtest.mymaps import *

def char_factory(name):
    return Character('Andy', charset_path('naked_man.png'))


class MyWorld(World):

    def __init__(self, save_file=None):
        maps = {1: Map1, 2: Map2, 3: Map3}
        World.__init__(self, maps=maps, character_factory=char_factory)
        if save_file is None:
            self.initial_state(map=1, position=Position(5, 4), chars=['Andy'])
        else:
            self.load_state(state_file=save_file)
        return

    def custom_gameover(self):
        print 'MyWorld.custom_gameover()'