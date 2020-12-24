# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/styles/monokai_light.py
# Compiled at: 2016-10-16 12:56:54
from pygments.style import Style
from pygments.token import Keyword, Name, Comment, String, Error, Text, Number, Operator, Generic, Whitespace, Punctuation, Other, Literal

class MonokaiLightStyle(Style):
    """
    This style mimics the Monokai color scheme.
    """
    default_style = ''
    background_color = '#fafafa'
    highlight_color = '#e6e3c3'
    styles = {Text: '#272822', 
       Whitespace: '', 
       Error: '#960050 bg:#1e0010', 
       Other: '', 
       Comment: '#75715e', 
       Comment.Multiline: '', 
       Comment.Preproc: '', 
       Comment.Single: '', 
       Comment.Special: '', 
       Keyword: '#00a8c8', 
       Keyword.Constant: '', 
       Keyword.Declaration: '', 
       Keyword.Namespace: '#f92672', 
       Keyword.Pseudo: '', 
       Keyword.Reserved: '', 
       Keyword.Type: '', 
       Operator: '#f92672', 
       Operator.Word: '', 
       Punctuation: '#111111', 
       Name: '#111111', 
       Name.Attribute: '#75af00', 
       Name.Builtin: '', 
       Name.Builtin.Pseudo: '', 
       Name.Class: '#75af00', 
       Name.Constant: '#00a8c8', 
       Name.Decorator: '#75af00', 
       Name.Entity: '', 
       Name.Exception: '#75af00', 
       Name.Function: '#75af00', 
       Name.Property: '', 
       Name.Label: '', 
       Name.Namespace: '', 
       Name.Other: '#75af00', 
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
       Literal.Date: '#d88200', 
       String: '#d88200', 
       String.Backtick: '', 
       String.Char: '', 
       String.Doc: '', 
       String.Double: '', 
       String.Escape: '#8045FF', 
       String.Heredoc: '', 
       String.Interpol: '', 
       String.Other: '', 
       String.Regex: '', 
       String.Single: '', 
       String.Symbol: '', 
       Generic: '', 
       Generic.Deleted: '', 
       Generic.Emph: 'italic', 
       Generic.Error: '', 
       Generic.Heading: '', 
       Generic.Inserted: '', 
       Generic.Output: '', 
       Generic.Prompt: '', 
       Generic.Strong: 'bold', 
       Generic.Subheading: '', 
       Generic.Traceback: ''}