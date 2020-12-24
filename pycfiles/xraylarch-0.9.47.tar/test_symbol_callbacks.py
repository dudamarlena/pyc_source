# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Newville/Codes/xraylarch/tests/test_symbol_callbacks.py
# Compiled at: 2017-04-05 21:43:24
from larch import Interpreter
linp = Interpreter()

def onVarChange(group=None, symbolname=None, value=None, **kws):
    print ('var changed ', group, symbolname, value, kws)


linp('x = 100.0')
linp.symtable.add_callback('x', onVarChange)
linp.symtable.set_symbol('x', 30)
linp.symtable.set_symbol('x', 'a string')
linp('x = arange(7)')