# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/styles/xcode.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1501 bytes
"""
    pygments.styles.xcode
    ~~~~~~~~~~~~~~~~~~~~~

    Style similar to the `Xcode` default theme.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Literal

class XcodeStyle(Style):
    __doc__ = '\n    Style similar to the Xcode default colouring theme.\n    '
    default_style = ''
    styles = {Comment: '#177500', 
     Comment.Preproc: '#633820', 
     String: '#C41A16', 
     String.Char: '#2300CE', 
     Operator: '#000000', 
     Keyword: '#A90D91', 
     Name: '#000000', 
     Name.Attribute: '#836C28', 
     Name.Class: '#3F6E75', 
     Name.Function: '#000000', 
     Name.Builtin: '#A90D91', 
     Name.Builtin.Pseudo: '#5B269A', 
     Name.Variable: '#000000', 
     Name.Tag: '#000000', 
     Name.Decorator: '#000000', 
     Name.Label: '#000000', 
     Literal: '#1C01CE', 
     Number: '#1C01CE', 
     Error: '#000000'}