# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/highlight/styles.py
# Compiled at: 2006-12-26 17:18:07
"""
    pocoo.pkg.highlight.styles
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    Builtin highlighting styles.

    :copyright: 2006 by Georg Brandl.
    :license: GNU GPL, see LICENSE for more details.
"""
from pocoo.pkg.highlight.base import HighlightingStyle, Keyword, Name, Comment, String, Error

class SimpleHighlightingStyle(HighlightingStyle):
    __module__ = __name__
    name = 'simple'

    def get_style_for(self, ttype):
        if ttype == Comment:
            return 'color: #008800'
        elif ttype == Keyword:
            return 'color: #AA22FF; font-weight: bold'
        elif ttype == Name.Builtin:
            return 'color: #AA22FF'
        elif ttype == String:
            return 'color: #bb4444'
        elif ttype == Error:
            return 'border: 1px solid red'
        return