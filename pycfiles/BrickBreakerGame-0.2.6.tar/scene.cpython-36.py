# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uros/Projects/BrickBreaker/BrickBreakerGame/Scenes/scene.py
# Compiled at: 2017-12-10 16:26:23
# Size of source mod 2**32: 691 bytes
import pygame

class Scene:

    def __init__(self, game):
        self._game = game
        self._texts = []

    def render(self):
        for text in self._texts:
            self._game.screen.blit(text[0], text[1])

    def get_game(self):
        return self._game

    def handle_events(self, events):
        pass

    def clear_text(self):
        self._texts = []

    def add_text(self, string, x=0, y=0, color=[255, 255, 255], background=[0, 0, 0], size=17, font_type=None, italic=False, bold=False):
        font = pygame.font.SysFont(font_type, size, bold=bold, italic=italic)
        self._texts.append([font.render(string, True, color, background), (x, y)])