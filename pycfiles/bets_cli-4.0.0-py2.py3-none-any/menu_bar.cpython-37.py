# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\PROJECT_HOME\bets-cli\src\bets\ui\menu_bar.py
# Compiled at: 2019-03-24 19:11:01
# Size of source mod 2**32: 1040 bytes
from tkinter import Menu
from bets.model.matches import Matches
from bets.ui.table_frame import TableFrame
from bets.utils import log

class MenuBar(Menu):

    def __init__(self, win, matches):
        super().__init__(win)
        win.config(menu=self)
        self.win = win
        self.matches = matches
        self.create_menus()

    def _quit(self):
        self.win.quit()
        self.win.destroy()
        exit()

    def _export_matches(self):
        title = 'Matches'
        columns = self.matches.columns
        rows = [m.values for m in self.matches]
        log.debug(f"title:{title}\ncolumns:{columns}\nrows:{rows}")
        TableFrame(title, columns, rows)

    def create_menus(self):
        matches_menu = Menu(self, tearoff=0)
        matches_menu.add_command(label='Export', command=(self._export_matches))
        matches_menu.add_separator()
        matches_menu.add_command(label='Exit', command=(self._quit))
        self.add_cascade(label='Matches', menu=matches_menu)