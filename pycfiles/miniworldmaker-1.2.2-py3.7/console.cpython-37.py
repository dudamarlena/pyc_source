# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\containers\console.py
# Compiled at: 2019-08-09 04:03:43
# Size of source mod 2**32: 1932 bytes
import os, pygame
from miniworldmaker.containers import container

class Console(container.Container):
    __doc__ = '\n    A console.\n\n    You can write text into the console\n    '

    def __init__(self, lines=5):
        super().__init__()
        self._lines = lines
        self._height = self._lines * 20
        self._text_queue = []
        self.margin_first = 10
        self.margin_last = 5
        self.row_height = 25
        self.row_margin = 10
        self.margin_left = 10
        self.margin_right = 10
        self._dirty = 1

    def repaint(self):
        self.surface = pygame.Surface((self._container_width, self._container_height))
        if self.dirty:
            self.surface.fill((255, 255, 255))
            package_directory = os.path.dirname(os.path.abspath(__file__))
            myfont = pygame.font.SysFont('monospace', 15)
            for i, text in enumerate(self._text_queue):
                row = pygame.Surface((self.width - (self.margin_left + self.margin_right), self.row_height))
                row.fill((200, 200, 200))
                label = myfont.render(text, 1, (0, 0, 0))
                row.blit(label, (10, 5))
                self.surface.blit(row, (self.margin_left, self.margin_first + i * self.row_height + i * self.row_margin))

        self.window.repaint_areas.append(self.rect)
        self.dirty = 0

    def max_height(self):
        width = self.margin_first
        for widget in self.widgets:
            width += widget.width + 5

        return width - 5

    @property
    def lines(self):
        self._lines = int(self.height - self.margin_first - self.margin_last) / (self.row_height + self.row_margin)
        return self._lines

    def newline(self, text):
        self._text_queue.append(text)
        if len(self._text_queue) > self.lines:
            self._text_queue.pop(0)
        self.dirty = 1