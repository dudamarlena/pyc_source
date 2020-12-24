# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/sbo/lib/python3.4/site-packages/vai/lexer/token.py
# Compiled at: 2015-05-02 14:07:56
# Size of source mod 2**32: 367 bytes
"""
Module that wraps and augments the pygment tokens, so that we can provide additional
tokens if we recognize them as having additional properties worth of interest.
"""
from pygments.token import *
PythonSelf = Name.Builtin.Pseudo.PythonSelf
PythonPrivate = Name.Function.PythonPrivate
PythonMagic = Name.Function.PythonMagic