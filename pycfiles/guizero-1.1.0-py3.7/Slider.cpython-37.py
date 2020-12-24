# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\Slider.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 2608 bytes
from tkinter import Scale, HORIZONTAL, VERTICAL
from . import utilities as utils
from .base import TextWidget

class Slider(TextWidget):

    def __init__(self, master, start=0, end=100, horizontal=True, command=None, grid=None, align=None, visible=True, enabled=None, width=None, height=None):
        description = '[Slider] object from ' + str(start) + ' to ' + str(end)
        self._horizontal = horizontal
        orient = HORIZONTAL if horizontal else VERTICAL
        tk = Scale((master.tk), from_=start, to=end, orient=orient, command=(self._command_callback))
        super(Slider, self).__init__(master, tk, description, grid, align, visible, enabled, width, height)
        self.update_command(command)

    @property
    def value(self):
        return self.tk.get()

    @value.setter
    def value(self, value):
        self.tk.set(value)

    def resize(self, width, height):
        self._set_width(width)
        self._set_height(height)
        if width == 'fill' or height == 'fill':
            self.master.display_widgets()

    def _set_width(self, width):
        self._width = width
        if width != 'fill':
            if self._horizontal:
                self._set_tk_config('length', width)
            else:
                self._set_tk_config('width', width)

    def _set_height(self, height):
        self._height = height
        if height != 'fill':
            if self._horizontal:
                self._set_tk_config('width', height)
            else:
                self._set_tk_config('length', height)

    def _command_callback(self, value):
        if self._command:
            args_expected = utils.no_args_expected(self._command)
            if args_expected == 0:
                self._command()
            else:
                if args_expected == 1:
                    self._command(value)
                else:
                    utils.error_format('Slider command function must accept either 0 or 1 arguments.\nThe current command has {} arguments.'.format(args_expected))

    def update_command(self, command):
        if command is None:
            self._command = lambda : None
        else:
            self._command = command