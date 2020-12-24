# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\miniworldmaker\containers\color_toolbar.py
# Compiled at: 2019-08-09 04:03:11
# Size of source mod 2**32: 1031 bytes
from miniworldmaker.containers import toolbar
from miniworldmaker.containers.toolbar_widgets import *

class ColorToolbar(toolbar.Toolbar):
    __doc__ = '\n    A toolbar to get the background color at a specific pixel\n    '

    def __init__(self, board):
        super().__init__()
        self.registered_events.add('all')
        self.registered_events.add('debug')
        self.board = board
        self.default_size = 220
        self.color_label = ColorLabel('Color')
        self.add_widget(self.color_label)

    def get_event(self, event, data):
        if 'mouse_left' in event:
            if self.board.is_in_container(data[0], data[1]):
                self.color_label.set_text(str(self.board.background.color_at(data)))
                self.color_label.set_color(self.board.background.color_at(data))


class ColorLabel(ToolbarLabel):

    def __init__(self, text):
        super().__init__(text)

    def set_color(self, color):
        self.background_color = color
        self.dirty = 1