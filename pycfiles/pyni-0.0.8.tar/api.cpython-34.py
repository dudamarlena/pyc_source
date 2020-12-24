# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.4/dist-packages/pynhost/api.py
# Compiled at: 2015-07-09 21:30:20
# Size of source mod 2**32: 604 bytes
from pynhost import keyinput
from pynhost.platforms import platformhandler

def send_string(string_to_send, delay=0, direction='both'):
    tokenized_keys = keyinput.tokenize_keypresses(string_to_send)
    platformhandler.transcribe_line(tokenized_keys, delay, direction)


def mouse_move(x=None, y=None, relative=True):
    platformhandler.mouse_move(x, y, relative)


def mouse_click(button='left', direction='both', number=1):
    platformhandler.mouse_click(button, direction, number)


def activate_window(title):
    """
        title is a string or list of strings
        """
    platformhandler.activate_window(title)