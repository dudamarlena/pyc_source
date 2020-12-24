# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-jqog4noo/pygments/pygments/styles/arduino.py
# Compiled at: 2016-12-29 05:31:34
# Size of source mod 2**32: 4492 bytes
"""
    pygments.styles.arduino
    ~~~~~~~~~~~~~~~~~~~~~~~

    Arduino® Syntax highlighting style.

    :copyright: Copyright 2006-2015 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Whitespace

class ArduinoStyle(Style):
    __doc__ = '\n    The Arduino® language style. This style is designed to highlight the\n    Arduino source code, so exepect the best results with it.\n    '
    background_color = '#ffffff'
    default_style = ''
    styles = {Whitespace: '', 
     Error: '#a61717', 
     Comment: '#95a5a6', 
     Comment.Multiline: '', 
     Comment.Preproc: '#434f54', 
     Comment.Single: '', 
     Comment.Special: '', 
     Keyword: '#728E00', 
     Keyword.Constant: '#00979D', 
     Keyword.Declaration: '', 
     Keyword.Namespace: '', 
     Keyword.Pseudo: '#00979D', 
     Keyword.Reserved: '', 
     Keyword.Type: '#00979D', 
     Operator: '#434f54', 
     Operator.Word: '', 
     Name: '#434f54', 
     Name.Attribute: '', 
     Name.Builtin: '', 
     Name.Builtin.Pseudo: '', 
     Name.Class: '', 
     Name.Constant: '', 
     Name.Decorator: '', 
     Name.Entity: '', 
     Name.Exception: '', 
     Name.Function: '#D35400', 
     Name.Property: '', 
     Name.Label: '', 
     Name.Namespace: '', 
     Name.Other: '#728E00', 
     Name.Tag: '', 
     Name.Variable: '', 
     Name.Variable.Class: '', 
     Name.Variable.Global: '', 
     Name.Variable.Instance: '', 
     Number: '#434f54', 
     Number.Float: '', 
     Number.Hex: '', 
     Number.Integer: '', 
     Number.Integer.Long: '', 
     Number.Oct: '', 
     String: '#7F8C8D', 
     String.Backtick: '', 
     String.Char: '', 
     String.Doc: '', 
     String.Double: '', 
     String.Escape: '', 
     String.Heredoc: '', 
     String.Interpol: '', 
     String.Other: '', 
     String.Regex: '', 
     String.Single: '', 
     String.Symbol: '', 
     Generic: '', 
     Generic.Deleted: '', 
     Generic.Emph: '', 
     Generic.Error: '', 
     Generic.Heading: '', 
     Generic.Inserted: '', 
     Generic.Output: '', 
     Generic.Prompt: '', 
     Generic.Strong: '', 
     Generic.Subheading: '', 
     Generic.Traceback: ''}