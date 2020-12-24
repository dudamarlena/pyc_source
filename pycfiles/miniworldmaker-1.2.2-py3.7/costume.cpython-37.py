# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\tokens\costume.py
# Compiled at: 2019-09-20 05:25:17
# Size of source mod 2**32: 2252 bytes
import asyncio, math, pygame
import miniworldmaker.tools as appear

class Costume(appear.Appearance):
    __doc__ = ' A costume contains one or multiple images\n\n    Every token has a costume which defines the "look" of the token.\n    You can switch the images in a costume to animate the token.\n\n    A costume is created if you add an image to an actor with token.add_image(path_to_image)\n    '

    def __init__(self, token):
        super().__init__()
        self.parent = token
        self._is_upscaled = True
        self._info_overlay = False
        self._is_rotatable = True
        self.image_actions_pipeline.append(('info_overlay', self.image_action_info_overlay, 'info_overlay'))

    @property
    def info_overlay(self):
        return self._info_overlay

    @info_overlay.setter
    def info_overlay(self, value):
        """
        Shows info overlay (Rectangle around the token and Direction marker)
        Args:
            color: Color of info_overlay
        """
        self._info_overlay = value
        self.dirty = 1
        self.call_action('info_overlay')

    def set_costume(self, index):
        self._image_index = index

    def image_action_info_overlay(self, image: pygame.Surface, parent) -> pygame.Surface:
        pygame.draw.rect(image, (255, 0, 0, 100), image.get_rect(), 4)
        rect = parent.rect
        center = (rect.centerx - parent.x, rect.centery - parent.y)
        x = center[0] + math.sin(math.radians(parent.direction)) * rect.width / 2
        y = center[1] - math.cos(math.radians(parent.direction)) * rect.width / 2
        start_pos, end_pos = (center[0], center[1]), (x, y)
        pygame.draw.line(image, (255, 0, 0, 100), start_pos, end_pos, 3)
        return image

    async def update(self):
        if self.parent.board:
            if self.is_animated:
                if self.parent.board.frame % self.animation_speed == 0:
                    self.next_image()
                    self.reload_image()
            else:
                self.reload_image()
        else:
            self.reload_image()