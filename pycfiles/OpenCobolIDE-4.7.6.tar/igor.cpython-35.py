# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/styles/igor.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 739 bytes
"""
    pygments.styles.igor
    ~~~~~~~~~~~~~~~~~~~~

    Igor Pro default style.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String

class IgorStyle(Style):
    __doc__ = '\n    Pygments version of the official colors for Igor Pro procedures.\n    '
    default_style = ''
    styles = {Comment: 'italic #FF0000', 
     Keyword: '#0000FF', 
     Name.Function: '#C34E00', 
     Name.Decorator: '#CC00A3', 
     Name.Class: '#007575', 
     String: '#009C00'}