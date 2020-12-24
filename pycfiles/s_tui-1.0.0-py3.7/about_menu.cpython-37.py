# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/about_menu.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 2285 bytes
"""Displays the About message menu """
from __future__ import print_function
from __future__ import absolute_import
import urwid
from s_tui.sturwid.ui_elements import ViListBox
from s_tui.helper_functions import __version__
ABOUT_MESSAGE = "\ns-tui is a monitoring tool for your CPU's temperature, frequency, utilization and power.\n\nCode for s-tui is available on github\nhttps://github.com/amanusk/s-tui\n\nHelp, issues and pull requests are appreciated.\n\nCreated by:\n    - Alex Manuskin\n    - Gil Tsuker\n    - Maor Veitsman\n    And others\n\nApril 2017\n\n"
ABOUT_MESSAGE += 's-tui ' + __version__ + ' Released under GNU GPLv2 '
MESSAGE_LEN = 20

class AboutMenu:
    __doc__ = 'Displays the About message menu '
    MAX_TITLE_LEN = 50

    def __init__(self, return_fn):
        self.return_fn = return_fn
        self.about_message = ABOUT_MESSAGE
        self.time_out_ctrl = urwid.Text(self.about_message)
        cancel_button = urwid.Button('Exit', on_press=(self.on_cancel))
        cancel_button._label.align = 'center'
        if_buttons = urwid.Columns([cancel_button])
        title = urwid.Text(('bold text', '  About Menu  \n'), 'center')
        self.titles = [
         title,
         self.time_out_ctrl,
         if_buttons]
        self.main_window = urwid.LineBox(ViListBox(self.titles))

    def get_size(self):
        return (
         MESSAGE_LEN + 3, self.MAX_TITLE_LEN)

    def on_cancel(self, w):
        self.return_fn()