# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\MenuBar.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 2664 bytes
from tkinter import Menu
from .tkmixins import ScheduleMixin, DestroyMixin, FocusMixin
from . import utilities as utils
from .base import Component
from .App import App
from .Window import Window

class MenuBar(Component):

    def __init__(self, master, toplevel, options):
        if not isinstance(master, (App, Window)):
            utils.error_format('The [MenuBar] must have an [App] or [Window] object as its master')
        description = '[MenuBar] object '
        tk = Menu(master.tk)
        super(MenuBar, self).__init__(master, tk, description, False)
        self._sub_menus = []
        for i in range(len(toplevel)):
            new_menu = Menu((self.tk), tearoff=0)
            for menu_item in options[i]:
                new_menu.add_command(label=(menu_item[0]), command=(menu_item[1]))

            self._sub_menus.append(new_menu)
            self.tk.add_cascade(label=(toplevel[i]), menu=(self._sub_menus[i]))

        master.tk.config(menu=(self.tk))

    @property
    def bg(self):
        return super(MenuBar, self.__class__).bg.fget(self)

    @bg.setter
    def bg(self, color):
        super(MenuBar, self.__class__).bg.fset(self, color)
        for sub_menu in self._sub_menus:
            sub_menu['bg'] = utils.convert_color(color)