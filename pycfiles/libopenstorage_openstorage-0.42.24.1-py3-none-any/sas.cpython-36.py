# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/styles/sas.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1441 bytes
"""
    pygments.styles.sas
    ~~~~~~~~~~~~~~~~~~~

    Style inspired by SAS' enhanced program editor. Note This is not
    meant to be a complete style. It's merely meant to mimic SAS'
    program editor syntax highlighting.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Other, Whitespace, Generic

class SasStyle(Style):
    __doc__ = "\n    Style inspired by SAS' enhanced program editor. Note This is not\n    meant to be a complete style. It's merely meant to mimic SAS'\n    program editor syntax highlighting.\n    "
    default_style = ''
    styles = {Whitespace: '#bbbbbb', 
     Comment: 'italic #008800', 
     String: '#800080', 
     Number: 'bold #2e8b57', 
     Other: 'bg:#ffffe0', 
     Keyword: '#2c2cff', 
     Keyword.Reserved: 'bold #353580', 
     Keyword.Constant: 'bold', 
     Name.Builtin: '#2c2cff', 
     Name.Function: 'bold italic', 
     Name.Variable: 'bold #2c2cff', 
     Generic: '#2c2cff', 
     Generic.Emph: '#008800', 
     Generic.Error: '#d30202', 
     Error: 'bg:#e3d2d2 #a61717'}