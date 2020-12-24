# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/styles/abap.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 751 bytes
"""
    pygments.styles.abap
    ~~~~~~~~~~~~~~~~~~~~

    ABAP workbench like style.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator

class AbapStyle(Style):
    default_style = ''
    styles = {Comment: 'italic #888', 
     Comment.Special: '#888', 
     Keyword: '#00f', 
     Operator.Word: '#00f', 
     Name: '#000', 
     Number: '#3af', 
     String: '#5a2', 
     Error: '#F00'}