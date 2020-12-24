# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\RadioButton.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 1782 bytes
from tkinter import Radiobutton
from . import utilities as utils
from .base import TextWidget

class RadioButton(TextWidget):

    def __init__(self, master, text, value, variable, command=None, grid=None, align=None, visible=True, enabled=None):
        description = '[RadioButton] object with option="' + str(text) + '" value="' + str(value) + '"'
        self._text = text
        self._value = value
        tk = Radiobutton((master.tk), text=(self._text), value=(self._value), variable=variable)
        super(RadioButton, self).__init__(master, tk, description, grid, align, visible, enabled, None, None)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        self._value = str(value)
        self.tk.config(value=(str(value)))
        self.description = '[RadioButton] object with option="' + self._text + '" value="' + str(value) + '"'

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = str(text)
        self.tk.config(text=(self._text))
        self.description = '[RadioButton] object with option="' + str(text) + '" value="' + self._value + '"'