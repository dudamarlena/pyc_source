# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\guizero\App.py
# Compiled at: 2019-10-24 09:39:32
# Size of source mod 2**32: 2536 bytes
from tkinter import Tk, Toplevel
from .base import BaseWindow
from . import utilities as utils, system_config

class App(BaseWindow):
    _main_app = None

    def __init__(self, title='guizero', width=500, height=500, layout='auto', bgcolor=None, bg=None, visible=True):
        """
        Creates an App

        :param string title:
            The text in the title bar of the window, defaults to `guizero`.

        :param int width:
            The width of the App window, defaults to 500.

        :param int height:
            The height of the App window, defaults to 500.

        :param string layout:
            The layout manager style for this window, defaults to `auto`.

        :param string bgcolor:
            DEPRECATED: The background colour for this window, defaults to None. Use bg instead.

        :param color bg:
            The background colour for this window, defaults to None. See https://lawsie.github.io/guizero/colors/

        :param bool visible:
            If the widget should be visible, defaults to `True`.

        """
        description = '[App] object'
        if App._main_app is None:
            tk = Tk()
            App._main_app = self
            for option_key in system_config.tk_options:
                tk.option_add(option_key, system_config.tk_options[option_key])

        else:
            tk = Toplevel(App._main_app.tk)
            utils.error_format('There should only be 1 guizero App, use Window to create multiple windows.')
        super(App, self).__init__(None, tk, description, title, width, height, layout, bg, visible)

    def display(self):
        """
        Display the window.

        :return:
            None.
        """
        self.tk.mainloop()

    def destroy(self):
        """
        Destroy and close the App.

        :return:
            None.

         :note:
            Once destroyed an App can no longer be used.
        """
        if self == App._main_app:
            App._main_app = None
        self.tk.destroy()