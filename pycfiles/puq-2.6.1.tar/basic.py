# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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