# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\ListBox.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 8350 bytes
from tkinter import Listbox, Frame, Scrollbar, END, BROWSE, EXTENDED
from . import utilities as utils
from .base import TextWidget, ContainerTextWidget, Widget
from .event import EventManager

class ListBox(ContainerTextWidget):

    def __init__(self, master, items=None, selected=None, command=None, grid=None, align=None, visible=True, enabled=None, multiselect=False, scrollbar=False, width=None, height=None):
        """
        Creates a ListBox

        :param Container master:
            The Container (App, Box, etc) the ListBox will belong too.

        :param List items:
            A list of strings to populate the ListBox, defaults to `None`.

        :param string selected:
            The item in the ListBox to select, defaults to `None`.

        :param callback command:
            The callback function to call when the ListBox changes,
            defaults to `None`.

        :param List grid:
            Grid co-ordinates for the widget, required if the master layout
            is 'grid', defaults to `None`.

        :param string align:
            How to align the widget within the grid, defaults to None.

        :param bool visible:
            If the widget should be visible, defaults to `True`.

        :param bool enabled:
            If the widget should be enabled, defaults to `None`. If `None`
            the value is inherited from the master.

        :param bool multiselect:
            If ListBox should allow multiple items to be selected, defaults
            to `False`.

        :param bool scrollbar:
            If ListBox should have a vertical scrollbar, defaults to False.

        :param int width:
            The starting width of the widget. Defaults to `None` and will auto
            size.

        :param int height:
            The starting height of the widget. Defaults to `None` and will auto
            size.
        """
        description = '[ListBox] object'
        tk = Frame(master.tk)
        super(ListBox, self).__init__(master, tk, description, 'auto', grid, align, visible, enabled, width, height)
        self._listbox = ListBoxWidget(self, items, selected, command, None, 'left', visible, enabled, multiselect, None, None)
        self._listbox.resize('fill', 'fill')
        if scrollbar:
            scrollbar_tk_widget = Scrollbar(tk)
            Widget(self, scrollbar_tk_widget, 'scrollbar', None, 'right', True, True, None, 'fill')
            self._listbox.tk.config(yscrollcommand=(scrollbar_tk_widget.set))
            scrollbar_tk_widget.config(command=(self._listbox.tk.yview))
        self._events = EventManager(self, self._listbox.tk)
        self.resize(width, height)

    def resize(self, width, height):
        self._listbox._set_tk_config('width', None if width is None else 0)
        self._set_propagation(width, height)
        super(ListBox, self).resize(width, height)

    @property
    def value(self):
        """
        Sets or returns the items selected in a ListBox

        `None` if 0 items are selected.

        If the ListBox is a not `multiselect`, `value` is the item selected.

        If the ListBox is a `multiselect`, `value` is a list of items
        selected.
        """
        return self._listbox.value

    @value.setter
    def value(self, value):
        self._listbox.value = value

    def insert(self, index, item):
        """
        Insert a new `item` at `index`
        """
        self._listbox.insert(index, item)

    def append(self, item):
        """
        Appends a new `item` to the end of the ListBox.
        """
        self._listbox.append(item)

    def remove(self, item):
        """
        Removes the first `item` from the ListBox.

        Returns `True` if an item was removed.
        """
        return self._listbox.remove(item)

    def clear(self):
        """
        Clears all the items in a ListBox
        """
        self._listbox.clear()

    @property
    def items(self):
        """
        Returns a list of items in the ListBox
        """
        return self._listbox.items

    def update_command(self, command):
        """
        Updates the callback command which is called when the ListBox
        changes.

        Setting to `None` stops the callback.

        :param callback command:
            The callback function to call, it can accept 0 or 1 parameters.

            If it accepts 1 parameter the `value` of the ListBox will be
            passed.
        """
        self._listbox.update_command(command)


class ListBoxWidget(TextWidget):

    def __init__(self, master, items=None, selected=None, command=None, grid=None, align=None, visible=True, enabled=None, multiselect=False, width=None, height=None):
        description = '[ListBox] object'
        self._multiselect = multiselect
        mode = EXTENDED if multiselect else BROWSE
        tk = Listbox((master.tk), selectmode=mode, exportselection=0)
        if items is not None:
            for item in items:
                tk.insert(END, item)

        super(ListBoxWidget, self).__init__(master, tk, description, grid, align, visible, enabled, width, height)
        self.events.set_event('<ListBox.ListboxSelect>', '<<ListboxSelect>>', self._command_callback)
        if selected is not None:
            self.value = selected
        self.update_command(command)

    @property
    def value(self):
        if len(self.tk.curselection()) > 0:
            if self._multiselect:
                return [self.tk.get(selected) for selected in self.tk.curselection()]
            return self.tk.get(self.tk.curselection()[0])
        else:
            return

    @value.setter
    def value(self, value):
        self.tk.selection_clear(0, self.tk.size() - 1)
        for index in range(self.tk.size()):
            if self._multiselect:
                for item in value:
                    if self.tk.get(index) == item:
                        self.tk.select_set(index)

            elif self.tk.get(index) == value:
                self.tk.select_set(index)

    def insert(self, index, item):
        self.tk.insert(index, item)

    def append(self, item):
        self.tk.insert(END, item)

    def remove(self, item):
        for index in range(len(self.items)):
            if item == self.items[index]:
                self.tk.delete(index)
                return True

        return False

    def clear(self):
        self.tk.delete(0, END)

    @property
    def items(self):
        return [self.tk.get(index) for index in range(self.tk.size())]

    def _command_callback(self):
        if self._command:
            args_expected = utils.no_args_expected(self._command)
            if args_expected == 0:
                self._command()
            else:
                if args_expected == 1:
                    self._command(self.value)
                else:
                    utils.error_format('ListBox command function must accept either 0 or 1 arguments.\nThe current command has {} arguments.'.format(args_expected))

    def update_command(self, command):
        if command is None:
            self._command = lambda : None
        else:
            self._command = command