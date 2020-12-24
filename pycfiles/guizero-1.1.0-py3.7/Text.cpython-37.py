# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\Text.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 1928 bytes
from tkinter import Label, StringVar
from . import utilities as utils
from .base import TextWidget

class Text(TextWidget):

    def __init__(self, master, text='', size=None, color=None, bg=None, font=None, grid=None, align=None, visible=True, enabled=None, width=None, height=None):
        description = '[Text] object with text "' + str(text) + '"'
        self._text = str(text)
        tk = Label((master.tk), text=text)
        super(Text, self).__init__(master, tk, description, grid, align, visible, enabled, width, height)
        if bg:
            self.bg = bg
        if size is not None:
            self.text_size = size
        if font is not None:
            self.font = font
        if color is not None:
            self.text_color = color

    @property
    def value(self):
        return self._text

    @value.setter
    def value(self, value):
        self.tk.config(text=value)
        self._text = str(value)
        self.description = '[Text] object with text "' + str(value) + '"'

    @property
    def size(self):
        return self.text_size

    @size.setter
    def size(self, size):
        self.text_size = size

    def clear(self):
        self._text = ''
        self.tk.config(text='')

    def append(self, text):
        new_text = self._text + str(text)
        self._text = new_text
        self.tk.config(text=new_text)
        self.description = '[Text] object with text "' + new_text + '"'