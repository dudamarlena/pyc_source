# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/styles/fruity.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1298 bytes
"""
    pygments.styles.fruity
    ~~~~~~~~~~~~~~~~~~~~~~

    pygments version of my "fruity" vim theme.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Token, Comment, Name, Keyword, Generic, Number, String, Whitespace

class FruityStyle(Style):
    __doc__ = '\n    Pygments version of the "native" vim theme.\n    '
    background_color = '#111111'
    highlight_color = '#333333'
    styles = {Whitespace: '#888888', 
     Token: '#ffffff', 
     Generic.Output: '#444444 bg:#222222', 
     Keyword: '#fb660a bold', 
     Keyword.Pseudo: 'nobold', 
     Number: '#0086f7 bold', 
     Name.Tag: '#fb660a bold', 
     Name.Variable: '#fb660a', 
     Comment: '#008800 bg:#0f140f italic', 
     Name.Attribute: '#ff0086 bold', 
     String: '#0086d2', 
     Name.Function: '#ff0086 bold', 
     Generic.Heading: '#ffffff bold', 
     Keyword.Type: '#cdcaa9 bold', 
     Generic.Subheading: '#ffffff bold', 
     Name.Constant: '#0086d2', 
     Comment.Preproc: '#ff0007 bold'}