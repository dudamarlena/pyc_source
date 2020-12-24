# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/styles/borland.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 1562 bytes
"""
    pygments.styles.borland
    ~~~~~~~~~~~~~~~~~~~~~~~

    Style similar to the style used in the Borland IDEs.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Whitespace

class BorlandStyle(Style):
    __doc__ = '\n    Style similar to the style used in the borland IDEs.\n    '
    default_style = ''
    styles = {Whitespace: '#bbbbbb', 
     Comment: 'italic #008800', 
     Comment.Preproc: 'noitalic #008080', 
     Comment.Special: 'noitalic bold', 
     String: '#0000FF', 
     String.Char: '#800080', 
     Number: '#0000FF', 
     Keyword: 'bold #000080', 
     Operator.Word: 'bold', 
     Name.Tag: 'bold #000080', 
     Name.Attribute: '#FF0000', 
     Generic.Heading: '#999999', 
     Generic.Subheading: '#aaaaaa', 
     Generic.Deleted: 'bg:#ffdddd #000000', 
     Generic.Inserted: 'bg:#ddffdd #000000', 
     Generic.Error: '#aa0000', 
     Generic.Emph: 'italic', 
     Generic.Strong: 'bold', 
     Generic.Prompt: '#555555', 
     Generic.Output: '#888888', 
     Generic.Traceback: '#aa0000', 
     Error: 'bg:#e3d2d2 #a61717'}