# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/Pygments/pygments/styles/bw.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1355 bytes
"""
    pygments.styles.bw
    ~~~~~~~~~~~~~~~~~~

    Simple black/white only style.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Operator, Generic

class BlackWhiteStyle(Style):
    background_color = '#ffffff'
    default_style = ''
    styles = {Comment: 'italic', 
     Comment.Preproc: 'noitalic', 
     Keyword: 'bold', 
     Keyword.Pseudo: 'nobold', 
     Keyword.Type: 'nobold', 
     Operator.Word: 'bold', 
     Name.Class: 'bold', 
     Name.Namespace: 'bold', 
     Name.Exception: 'bold', 
     Name.Entity: 'bold', 
     Name.Tag: 'bold', 
     String: 'italic', 
     String.Interpol: 'bold', 
     String.Escape: 'bold', 
     Generic.Heading: 'bold', 
     Generic.Subheading: 'bold', 
     Generic.Emph: 'italic', 
     Generic.Strong: 'bold', 
     Generic.Prompt: 'bold', 
     Error: 'border:#FF0000'}