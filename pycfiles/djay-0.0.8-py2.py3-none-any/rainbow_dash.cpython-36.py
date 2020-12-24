# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/styles/rainbow_dash.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 2480 bytes
"""
    pygments.styles.rainbow_dash
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    A bright and colorful syntax highlighting `theme`.

    .. _theme: http://sanssecours.github.io/Rainbow-Dash.tmbundle

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Comment, Error, Generic, Name, Number, Operator, String, Text, Whitespace, Keyword
BLUE_LIGHT = '#0080ff'
BLUE = '#2c5dcd'
GREEN = '#00cc66'
GREEN_LIGHT = '#ccffcc'
GREEN_NEON = '#00cc00'
GREY = '#aaaaaa'
GREY_LIGHT = '#cbcbcb'
GREY_DARK = '#4d4d4d'
PURPLE = '#5918bb'
RED = '#cc0000'
RED_DARK = '#c5060b'
RED_LIGHT = '#ffcccc'
RED_BRIGHT = '#ff0000'
WHITE = '#ffffff'
TURQUOISE = '#318495'
ORANGE = '#ff8000'

class RainbowDashStyle(Style):
    __doc__ = '\n    A bright and colorful syntax highlighting theme.\n    '
    background_color = WHITE
    styles = {Comment: 'italic {}'.format(BLUE_LIGHT), 
     Comment.Preproc: 'noitalic', 
     Comment.Special: 'bold', 
     Error: 'bg:{} {}'.format(RED, WHITE), 
     Generic.Deleted: 'border:{} bg:{}'.format(RED_DARK, RED_LIGHT), 
     Generic.Emph: 'italic', 
     Generic.Error: RED_BRIGHT, 
     Generic.Heading: 'bold {}'.format(BLUE), 
     Generic.Inserted: 'border:{} bg:{}'.format(GREEN_NEON, GREEN_LIGHT), 
     Generic.Output: GREY, 
     Generic.Prompt: 'bold {}'.format(BLUE), 
     Generic.Strong: 'bold', 
     Generic.Subheading: 'bold {}'.format(BLUE), 
     Generic.Traceback: RED_DARK, 
     Keyword: 'bold {}'.format(BLUE), 
     Keyword.Pseudo: 'nobold', 
     Keyword.Type: PURPLE, 
     Name.Attribute: 'italic {}'.format(BLUE), 
     Name.Builtin: 'bold {}'.format(PURPLE), 
     Name.Class: 'underline', 
     Name.Constant: TURQUOISE, 
     Name.Decorator: 'bold {}'.format(ORANGE), 
     Name.Entity: 'bold {}'.format(PURPLE), 
     Name.Exception: 'bold {}'.format(PURPLE), 
     Name.Function: 'bold {}'.format(ORANGE), 
     Name.Tag: 'bold {}'.format(BLUE), 
     Number: 'bold {}'.format(PURPLE), 
     Operator: BLUE, 
     Operator.Word: 'bold', 
     String: GREEN, 
     String.Doc: 'italic', 
     String.Escape: 'bold {}'.format(RED_DARK), 
     String.Other: TURQUOISE, 
     String.Symbol: 'bold {}'.format(RED_DARK), 
     Text: GREY_DARK, 
     Whitespace: GREY_LIGHT}