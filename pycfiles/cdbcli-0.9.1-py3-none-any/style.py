# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kevin/src/cdbcli/build/lib/cdbcli/style.py
# Compiled at: 2016-07-12 20:29:29
from prompt_toolkit.styles import style_from_dict
from prompt_toolkit.token import Token
style = style_from_dict({Token.Command: '#33aa33 bold', 
   Token.Operand: '#aa3333 bold'})