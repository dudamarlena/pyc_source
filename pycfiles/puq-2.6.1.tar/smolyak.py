# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mmh/puq/examples/1dpoly/smolyak.py
# Compiled at: 2015-08-24 12:56:37
from puq import *

def run():
    x = NormalParameter('x', 'x', mean=3, dev=1)
    host = InteractiveHost()
    uq = Smolyak([x], level=1)
    prog = TestProgram('./poly_prog.py', desc='1D Polynomial')
    return Sweep(uq, host, prog)