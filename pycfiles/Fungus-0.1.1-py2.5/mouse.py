# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyglet/window/mouse.py
# Compiled at: 2009-02-07 06:48:50
"""Mouse constants and utilities for pyglet.window.
"""
__docformat__ = 'restructuredtext'
__version__ = '$Id: mouse.py 1579 2008-01-15 14:47:19Z Alex.Holkner $'

def buttons_string(buttons):
    """Return a string describing a set of active mouse buttons.

    Example::

        >>> buttons_string(LEFT | RIGHT)
        'LEFT|RIGHT'

    :Parameters:
        `buttons` : int
            Bitwise combination of mouse button constants.

    :rtype: str
    """
    button_names = []
    if buttons & LEFT:
        button_names.append('LEFT')
    if buttons & MIDDLE:
        button_names.append('MIDDLE')
    if buttons & RIGHT:
        button_names.append('RIGHT')
    return ('|').join(button_names)


LEFT = 1
MIDDLE = 2
RIGHT = 4