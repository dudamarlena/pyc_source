# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mmh/puq/examples/1dpoly/smolyak.py
# Compiled at: 2015-08-24 12:56:37
from puq import *

def run():
    x = NormalParameter('x', 'x', mean=3, dev=1)
    host = InteractiveHost()
    uq = Smolyak([x], level=1)
    prog = TestProgram('./poly_prog.py', desc='1D Polynomial')
    return Sweep(uq, host, prog)