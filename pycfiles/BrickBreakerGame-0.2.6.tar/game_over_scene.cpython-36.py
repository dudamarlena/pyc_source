# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/uros/Projects/BrickBreaker/BrickBreaker/Scenes/game_over_scene.py
# Compiled at: 2017-12-17 12:40:06
# Size of source mod 2**32: 1355 bytes
import pygame
from BrickBreaker.Scenes.scene import Scene
from BrickBreaker.Shared import *
from BrickBreaker import Highscore

class GameOverScene(Scene):

    def __init__(self, game):
        super().__init__(game)
        self._player_name = ''
        self._high_score_image = pygame.image.load(GameConstants.HIGHSCORE_IMAGE)

    def render(self):
        self.get_game().screen.blit(self._high_score_image, (15, 20))
        self.clear_text()
        self.add_text('Please enter your name: ', 300, 200, size=30)
        self.add_text((self._player_name), 300, 250, size=30)
        super().render()

    def handle_events(self, events):
        super().handle_events(events)
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = self.get_game()
                    Highscore().add(self._player_name, game.get_score())
                    game.reset()
                    self._player_name = ''
                    game.change_scene(GameConstants.HIGHSCORE_SCENE)
                else:
                    if 122 >= event.key >= 65:
                        self._player_name += chr(event.key)
                    elif event.key == pygame.K_BACKSPACE:
                        self._player_name = self._player_name[:-1]