# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/s_tui/help_menu.py
# Compiled at: 2019-12-27 09:31:39
# Size of source mod 2**32: 2811 bytes
"""A class display the help message menu
"""
from __future__ import print_function
from __future__ import absolute_import
import urwid
from s_tui.sturwid.ui_elements import ViListBox
HELP_MESSAGE = "\nTUI interface:\n\nThe side bar houses the controls for the displayed graphs.\nAt the bottom, all sensors reading are presented in text form.\n\n* Use the arrow keys or 'hjkl' to navigate the side bar\n* Toggle between stressed and regular operation using the radio buttons in 'Modes'.\n* If you wish to alternate stress defaults, you can do it in <Stress options>\n* Select graphs to display in the <Graphs> menu \n* Select summaries to display in the <Summaries> menu \n* Change time between updates using the 'Refresh' field\n* Use the <Reset> button to reset graphs and statistics\n* If your system supports it, you can use the UTF-8 button to get a smoother graph\n* Save your current configuration with the <Save Settings> button\n* Press 'q' or the <Quit> button to quit\n\n* Run `s-tui --help` to get this message and additional cli options\n\n"
MESSAGE_LEN = 30

class HelpMenu:
    __doc__ = ' HelpMenu is a widget containing instructions on usage of s-tui'
    MAX_TITLE_LEN = 90

    def __init__(self, return_fn):
        self.return_fn = return_fn
        self.help_message = HELP_MESSAGE
        self.time_out_ctrl = urwid.Text(self.help_message)
        cancel_button = urwid.Button('Exit', on_press=(self.on_cancel))
        cancel_button._label.align = 'center'
        if_buttons = urwid.Columns([cancel_button])
        title = urwid.Text(('bold text', '  Help Menu  \n'), 'center')
        self.titles = [
         title,
         self.time_out_ctrl,
         if_buttons]
        self.main_window = urwid.LineBox(ViListBox(self.titles))

    def get_size(self):
        """ returns size of HelpMenu"""
        return (
         MESSAGE_LEN + 3, self.MAX_TITLE_LEN)

    def on_cancel(self, w):
        """ Returns to original widget"""
        self.return_fn()