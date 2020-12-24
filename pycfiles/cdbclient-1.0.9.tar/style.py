# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/kevin/src/cdbcli/build/lib/cdbcli/style.py
# Compiled at: 2016-07-12 20:29:29
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
style = style_from_dict({Token.Command: '#33aa33 bold', 
   Token.Operand: '#aa3333 bold'})