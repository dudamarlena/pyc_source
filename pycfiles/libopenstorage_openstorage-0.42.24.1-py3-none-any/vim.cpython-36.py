# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/styles/vim.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 1976 bytes
"""
    pygments.styles.vim
    ~~~~~~~~~~~~~~~~~~~

    A highlighting style for Pygments, inspired by vim.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Number, Operator, Generic, Whitespace, Token

class VimStyle(Style):
    __doc__ = '\n    Styles somewhat like vim 7.0\n    '
    background_color = '#000000'
    highlight_color = '#222222'
    default_style = '#cccccc'
    styles = {Token: '#cccccc', 
     Whitespace: '', 
     Comment: '#000080', 
     Comment.Preproc: '', 
     Comment.Special: 'bold #cd0000', 
     Keyword: '#cdcd00', 
     Keyword.Declaration: '#00cd00', 
     Keyword.Namespace: '#cd00cd', 
     Keyword.Pseudo: '', 
     Keyword.Type: '#00cd00', 
     Operator: '#3399cc', 
     Operator.Word: '#cdcd00', 
     Name: '', 
     Name.Class: '#00cdcd', 
     Name.Builtin: '#cd00cd', 
     Name.Exception: 'bold #666699', 
     Name.Variable: '#00cdcd', 
     String: '#cd0000', 
     Number: '#cd00cd', 
     Generic.Heading: 'bold #000080', 
     Generic.Subheading: 'bold #800080', 
     Generic.Deleted: '#cd0000', 
     Generic.Inserted: '#00cd00', 
     Generic.Error: '#FF0000', 
     Generic.Emph: 'italic', 
     Generic.Strong: 'bold', 
     Generic.Prompt: 'bold #000080', 
     Generic.Output: '#888', 
     Generic.Traceback: '#04D', 
     Error: 'border:#FF0000'}