# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/styles/monokai.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 5086 bytes
"""
    pygments.styles.monokai
    ~~~~~~~~~~~~~~~~~~~~~~~

    Mimic the Monokai color scheme. Based on tango.py.

    http://www.monokai.nl/blog/2006/07/15/textmate-color-theme/

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Text, Number, Operator, Generic, Whitespace, Punctuation, Other, Literal

class MonokaiStyle(Style):
    __doc__ = '\n    This style mimics the Monokai color scheme.\n    '
    background_color = '#272822'
    highlight_color = '#49483e'
    styles = {Text: '#f8f8f2', 
     Whitespace: '', 
     Error: '#960050 bg:#1e0010', 
     Other: '', 
     Comment: '#75715e', 
     Comment.Multiline: '', 
     Comment.Preproc: '', 
     Comment.Single: '', 
     Comment.Special: '', 
     Keyword: '#66d9ef', 
     Keyword.Constant: '', 
     Keyword.Declaration: '', 
     Keyword.Namespace: '#f92672', 
     Keyword.Pseudo: '', 
     Keyword.Reserved: '', 
     Keyword.Type: '', 
     Operator: '#f92672', 
     Operator.Word: '', 
     Punctuation: '#f8f8f2', 
     Name: '#f8f8f2', 
     Name.Attribute: '#a6e22e', 
     Name.Builtin: '', 
     Name.Builtin.Pseudo: '', 
     Name.Class: '#a6e22e', 
     Name.Constant: '#66d9ef', 
     Name.Decorator: '#a6e22e', 
     Name.Entity: '', 
     Name.Exception: '#a6e22e', 
     Name.Function: '#a6e22e', 
     Name.Property: '', 
     Name.Label: '', 
     Name.Namespace: '', 
     Name.Other: '#a6e22e', 
     Name.Tag: '#f92672', 
     Name.Variable: '', 
     Name.Variable.Class: '', 
     Name.Variable.Global: '', 
     Name.Variable.Instance: '', 
     Number: '#ae81ff', 
     Number.Float: '', 
     Number.Hex: '', 
     Number.Integer: '', 
     Number.Integer.Long: '', 
     Number.Oct: '', 
     Literal: '#ae81ff', 
     Literal.Date: '#e6db74', 
     String: '#e6db74', 
     String.Backtick: '', 
     String.Char: '', 
     String.Doc: '', 
     String.Double: '', 
     String.Escape: '#ae81ff', 
     String.Heredoc: '', 
     String.Interpol: '', 
     String.Other: '', 
     String.Regex: '', 
     String.Single: '', 
     String.Symbol: '', 
     Generic: '', 
     Generic.Deleted: '#f92672', 
     Generic.Emph: 'italic', 
     Generic.Error: '', 
     Generic.Heading: '', 
     Generic.Inserted: '#a6e22e', 
     Generic.Output: '#66d9ef', 
     Generic.Prompt: 'bold #f92672', 
     Generic.Strong: 'bold', 
     Generic.Subheading: '#75715e', 
     Generic.Traceback: ''}