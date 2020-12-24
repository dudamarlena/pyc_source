# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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