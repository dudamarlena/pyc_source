# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mmh/puq/examples/rosen/rosen_mc.py
# Compiled at: 2015-04-06 17:56:33
from puq import *

def run(num=20):
    p1 = UniformParameter('x', 'x', min=-2, max=2)
    p2 = UniformParameter('y', 'y', min=-2, max=2)
    host = InteractiveHost()
    uq = MonteCarlo([p1, p2], num=num)
    prog = TestProgram(exe='./rosen_prog.py --x=$x --y=$y', desc='Rosenbrock Function')
    return Sweep(uq, host, prog)