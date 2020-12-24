# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/styles/stata_light.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1274 bytes
"""
    pygments.styles.stata_light
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Light Style inspired by Stata's do-file editor. Note this is not
    meant to be a complete style, just for Stata's file formats.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Whitespace, Text

class StataLightStyle(Style):
    __doc__ = "\n    Light mode style inspired by Stata's do-file editor. This is not\n    meant to be a complete style, just for use with Stata.\n    "
    default_style = ''
    styles = {Text: '#111111', 
     Whitespace: '#bbbbbb', 
     Error: 'bg:#e3d2d2 #a61717', 
     String: '#7a2424', 
     Number: '#2c2cff', 
     Operator: '', 
     Name.Function: '#2c2cff', 
     Name.Other: '#be646c', 
     Keyword: 'bold #353580', 
     Keyword.Constant: '', 
     Comment: 'italic #008800', 
     Name.Variable: 'bold #35baba', 
     Name.Variable.Global: 'bold #b5565e'}