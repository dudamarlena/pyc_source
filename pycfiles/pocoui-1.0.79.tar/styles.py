# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pocoo/pkg/highlight/styles.py
# Compiled at: 2006-12-26 17:18:07
__doc__ = '\n    pocoo.pkg.highlight.styles\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    Builtin highlighting styles.\n\n    :copyright: 2006 by Georg Brandl.\n    :license: GNU GPL, see LICENSE for more details.\n'
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