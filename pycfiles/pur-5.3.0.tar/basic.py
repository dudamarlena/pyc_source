# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mmh/puq/examples/basic/basic.py
# Compiled at: 2015-04-06 17:56:33
from puq import *

def run():
    x = UniformParameter('x', 'x', min=0, max=10)
    y = NormalParameter('y', 'y', mean=10, dev=2)
    host = InteractiveHost()
    uq = Smolyak([x, y], level=1)
    prog = TestProgram('./basic_prog.py', desc='Basic identity function')
    return Sweep(uq, host, prog)