# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/console.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1721 bytes
"""
    pygments.console
    ~~~~~~~~~~~~~~~~

    Format colored console output.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
esc = '\x1b['
codes = {}
codes[''] = ''
codes['reset'] = esc + '39;49;00m'
codes['bold'] = esc + '01m'
codes['faint'] = esc + '02m'
codes['standout'] = esc + '03m'
codes['underline'] = esc + '04m'
codes['blink'] = esc + '05m'
codes['overline'] = esc + '06m'
dark_colors = [
 'black', 'red', 'green', 'yellow', 'blue',
 'magenta', 'cyan', 'gray']
light_colors = ['brightblack', 'brightred', 'brightgreen', 'brightyellow', 'brightblue',
 'brightmagenta', 'brightcyan', 'white']
x = 30
for d, l in zip(dark_colors, light_colors):
    codes[d] = esc + '%im' % x
    codes[l] = esc + '%im' % (60 + x)
    x += 1

del d
del l
del x
codes['white'] = codes['bold']

def reset_color():
    return codes['reset']


def colorize(color_key, text):
    return codes[color_key] + text + codes['reset']


def ansiformat(attr, text):
    """
    Format ``text`` with a color and/or some attributes::

        color       normal color
        *color*     bold color
        _color_     underlined color
        +color+     blinking color
    """
    result = []
    if attr[:1] == attr[-1:] == '+':
        result.append(codes['blink'])
        attr = attr[1:-1]
    if attr[:1] == attr[-1:] == '*':
        result.append(codes['bold'])
        attr = attr[1:-1]
    if attr[:1] == attr[-1:] == '_':
        result.append(codes['underline'])
        attr = attr[1:-1]
    result.append(codes[attr])
    result.append(text)
    result.append(codes['reset'])
    return ''.join(result)