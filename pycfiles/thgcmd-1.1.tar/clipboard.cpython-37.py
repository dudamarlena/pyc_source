# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tools/tmp/cmd2/thgcmd/clipboard.py
# Compiled at: 2019-07-17 15:07:37
# Size of source mod 2**32: 821 bytes
"""
This module provides basic ability to copy from and paste to the clipboard/pastebuffer.
"""
import pyperclip
from pyperclip import PyperclipException
try:
    _ = pyperclip.paste()
except PyperclipException:
    can_clip = False
else:
    can_clip = True

def get_paste_buffer() -> str:
    """Get the contents of the clipboard / paste buffer.

    :return: contents of the clipboard
    """
    pb_str = pyperclip.paste()
    return pb_str


def write_to_paste_buffer(txt: str) -> None:
    """Copy text to the clipboard / paste buffer.

    :param txt: text to copy to the clipboard
    """
    pyperclip.copy(txt)