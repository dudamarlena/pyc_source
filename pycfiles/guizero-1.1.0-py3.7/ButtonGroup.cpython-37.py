# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\ButtonGroup.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 10292 bytes
from tkinter import Frame, StringVar
from . import utilities as utils
from .base import ContainerTextWidget
from .tkmixins import TextMixin
from .RadioButton import RadioButton
from .event import EventManager

class ButtonGroup(ContainerTextWidget):

    def __init__(self, master, options=[], selected=None, horizontal=False, command=None, grid=None, align=None, args=None, visible=True, enabled=None, width=None, height=None):
        """
        Creates a ButtonGroup

        :param Container master:
            The Container (App, Box, etc) the ButtonGroup will belong too.

        :param List option:
            A list of options to append to the ButtonGroup. If a 2D list is
            specified, the first element is the text, the second is the value,
            defaults to an empty list.

        :param string selected:
            The item in the ButtonGroup to select, defaults to `None`.

        :param string horizontal:
            If the ButtonGroup is to be displayed horizontally, defaults to
            `True`.

        :param callback command:
            The callback function to call when the ButtonGroup changes,
            defaults to `None`.

        :param List grid:
            Grid co-ordinates for the widget, required if the master layout
            is 'grid', defaults to `None`.

        :param string align:
            How to align the widget within the grid, defaults to None.

        :param callback args:
            A list of arguments to pass to the widgets `command`, defaults to
            `None`.

        :param bool visible:
            If the widget should be visible, defaults to `True`.

        :param bool enabled:
            If the widget should be enabled, defaults to `None`. If `None`
            the value is inherited from the master.

        :param int width:
            The starting width of the widget. Defaults to `None` and will auto
            size.

        :param int height:
            The starting height of the widget. Defaults to `None` and will auto
            size.
        """
        description = '[ButtonGroup] object with selected option "' + str(selected) + '"'
        self._rbuttons = []
        self._text_size = None
        self._font = None
        self._horizontal = horizontal
        tk = Frame(master.tk)
        self._selected = StringVar(master=(tk.winfo_toplevel()))
        super(ButtonGroup, self).__init__(master, tk, description, 'grid', grid, align, visible, enabled, width, height)
        self._options = []
        for option in options:
            self._options.append(self._parse_option(option))

        self._refresh_options()
        if selected is None and len(self._options) > 0:
            self.value = self._options[0][1]
        else:
            self.value = selected
        self.update_command(command, args)
        option_tks = [option.tk for option in self._rbuttons]
        self._events = EventManager(self, self.tk, *option_tks)
        self.resize(width, height)

    def _parse_option(self, option):
        if not isinstance(option, list):
            return [
             option, option]
        return [option[0], option[1]]

    def _refresh_options(self):
        for button in self._rbuttons:
            button.destroy()

        self._rbuttons = []
        gridx = 0
        gridy = 0
        for button in self._options:
            if self._horizontal:
                gridx += 1
            else:
                gridy += 1
            rbutton = RadioButton(self,
              text=(str(button[0])),
              value=(str(button[1])),
              variable=(self._selected),
              grid=[
             gridx, gridy],
              align='left',
              visible=(self.visible),
              enabled=(self.enabled))
            self._rbuttons.append(rbutton)
            rbutton.tk.config(command=(self._command_callback))

    @property
    def value(self):
        """
        Sets or returns the option selected in a ButtonGroup.
        """
        return self._selected.get()

    @value.setter
    def value(self, value):
        self._selected.set(str(value))

    @property
    def value_text(self):
        """
        Sets or returns the option selected in a ButtonGroup by its text value.
        """
        search = self._selected.get()
        for item in self._rbuttons:
            if item.value == search:
                return item.text

        return ''

    @value_text.setter
    def value_text(self, value):
        for item in self._rbuttons:
            if item.text == value:
                self.value = item.value

    def resize(self, width, height):
        self._width = width
        self._height = height
        for item in self._rbuttons:
            item.width = width

        if len(self._rbuttons) > 0:
            button_height = height
            if isinstance(height, int):
                if height % len(self._rbuttons) != 0:
                    button_height = int(round(height / len(self._rbuttons)))
                    new_height = button_height * len(self._rbuttons)
                    utils.error_format("ButtonGroup height '{}' doesn't divide by the number of buttons '{}' setting height to '{}'.".format(height, len(self._rbuttons), new_height))
                else:
                    button_height = int(height / len(self._rbuttons))
            for item in self._rbuttons:
                item.height = button_height

        super(ButtonGroup, self).resize(width, height)

    @property
    def options(self):
        """
        Returns a list of options in the ButtonGroup
        """
        return self._options

    def append(self, option):
        """
        Appends a new `option` to the end of the ButtonGroup.

        :param string/List option:
            The option to append to the ButtonGroup. If a 2D list is specified,
            the first element is the text, the second is the value.
        """
        self._options.append(self._parse_option(option))
        self._refresh_options()
        self.resize(self._width, self._height)

    def insert(self, index, option):
        """
        Insert a new `option` in the ButtonGroup at `index`.

        :param int option:
            The index of where to insert the option.

        :param string/List option:
            The option to append to the ButtonGroup. If a 2D list is specified,
            the first element is the text, the second is the value.
        """
        self._options.insert(index, self._parse_option(option))
        self._refresh_options()
        self.resize(self._width, self._height)

    def remove(self, option):
        """
        Removes the first `option` from the ButtonGroup.

        Returns `True` if an item was removed.

        :param string option:
            The value of the option to remove from the ButtonGroup.
        """
        for existing_option in self._options:
            if existing_option[1] == option:
                self._options.remove(existing_option)
                self._refresh_options()
                return True

        return False

    def clear(self):
        """
        Clears all the options in a Combo
        """
        self._options = []
        self._refresh_options()
        self.value = ''

    def get_group_as_list(self):
        return [[option.text, option.value] for option in self._rbuttons]

    def update_command(self, command, args=None):
        """
        Updates the callback command which is called when the ButtonGroup
        changes.

        Setting to `None` stops the callback.

        :param callback command:
            The callback function to call.

        :param callback args:
            A list of arguments to pass to the widgets `command`, defaults to
            `None`.
        """
        if command is None:
            self._command = lambda : None
        else:
            if args is None:
                self._command = command
            else:
                self._command = (utils.with_args)(command, *args)

    def _command_callback(self):
        self._command()