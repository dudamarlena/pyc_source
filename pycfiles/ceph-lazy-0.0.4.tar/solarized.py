# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kdreyer/dev/ceph-installer/docs/source/_themes/solarized.py
# Compiled at: 2016-02-25 16:12:02
__doc__ = '\n    pygments.styles.solarized.light\n    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n\n    The Solarized style, inspired by Schoonover.\n\n    :copyright: Copyright 2012 by the Shoji KUMAGAI, see AUTHORS.\n    :license: MIT, see LICENSE for details.\n'
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Text, Number, Operator, Generic, Whitespace, Other, Literal, Punctuation

class LightStyle(Style):
    """
    The Solarized Light style, inspired by Schoonover.
    """
    background_color = '#fdf6e3'
    default_style = ''
    styles = {Text: '#657b83', 
       Whitespace: '#fdf6e3', 
       Error: '#dc322f', 
       Other: '#657b83', 
       Comment: 'italic #93a1a1', 
       Comment.Multiline: 'italic #93a1a1', 
       Comment.Preproc: 'italic #93a1a1', 
       Comment.Single: 'italic #93a1a1', 
       Comment.Special: 'italic #93a1a1', 
       Keyword: '#859900', 
       Keyword.Constant: '#859900', 
       Keyword.Declaration: '#859900', 
       Keyword.Namespace: '#cb4b16', 
       Keyword.Pseudo: '#cb4b16', 
       Keyword.Reserved: '#859900', 
       Keyword.Type: '#859900', 
       Operator: '#657b83', 
       Operator.Word: '#859900', 
       Name: '#586e75', 
       Name.Attribute: '#657b83', 
       Name.Builtin: '#268bd2', 
       Name.Builtin.Pseudo: 'bold #268bd2', 
       Name.Class: '#268bd2', 
       Name.Constant: '#b58900', 
       Name.Decorator: '#cb4b16', 
       Name.Entity: '#cb4b16', 
       Name.Exception: '#cb4b16', 
       Name.Function: '#268bd2', 
       Name.Property: '#268bd2', 
       Name.Label: '#657b83', 
       Name.Namespace: '#b58900', 
       Name.Other: '#657b83', 
       Name.Tag: '#859900', 
       Name.Variable: '#cb4b16', 
       Name.Variable.Class: '#268bd2', 
       Name.Variable.Global: '#268bd2', 
       Name.Variable.Instance: '#268bd2', 
       Number: '#2aa198', 
       Number.Float: '#2aa198', 
       Number.Hex: '#2aa198', 
       Number.Integer: '#2aa198', 
       Number.Integer.Long: '#2aa198', 
       Number.Oct: '#2aa198', 
       Literal: '#657b83', 
       Literal.Date: '#657b83', 
       Punctuation: '#657b83', 
       String: '#2aa198', 
       String.Backtick: '#2aa198', 
       String.Char: '#2aa198', 
       String.Doc: '#2aa198', 
       String.Double: '#2aa198', 
       String.Escape: '#cb4b16', 
       String.Heredoc: '#2aa198', 
       String.Interpol: '#cb4b16', 
       String.Other: '#2aa198', 
       String.Regex: '#2aa198', 
       String.Single: '#2aa198', 
       String.Symbol: '#2aa198', 
       Generic: '#657b83', 
       Generic.Deleted: '#657b83', 
       Generic.Emph: '#657b83', 
       Generic.Error: '#657b83', 
       Generic.Heading: '#657b83', 
       Generic.Inserted: '#657b83', 
       Generic.Output: '#657b83', 
       Generic.Prompt: '#657b83', 
       Generic.Strong: '#657b83', 
       Generic.Subheading: '#657b83', 
       Generic.Traceback: '#657b83'}