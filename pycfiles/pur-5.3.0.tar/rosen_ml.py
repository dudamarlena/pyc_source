# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/mmh/puq/examples/rosen/rosen_ml.py
# Compiled at: 2015-04-06 17:56:33
from puq import *

def run(lev=4):
    p1 = UniformParameter('x', 'x', min=-2, max=2)
    p2 = UniformParameter('y', 'y', min=-2, max=2)
    host = InteractiveHost()
    uq = Smolyak([p1, p2], level=lev)
    prog = TestProgram(exe="octave -q --eval 'rosen($x, $y)'", desc='Rosenbrock Function (octave)')
    return Sweep(uq, host, prog)