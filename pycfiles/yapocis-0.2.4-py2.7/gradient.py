# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/gradient.py
# Compiled at: 2011-08-30 23:33:15
"""
Created on Jul 22, 2011

@author: seant
"""
import numpy as np
from rpc import kernels, interfaces
program = kernels.loadProgram(interfaces.gradient, engine=kernels.GPU_ENGINE)
gradientcl = program.gradient

def gradient(image, reach=1):
    grad, angle = gradientcl(image, reach)
    return (grad, angle)


def test_gradient():
    import time
    a = np.random.sample((1000, 1000)).astype(np.float32)
    t = time.time()
    b = np.gradient(a)
    print 'Numpy seconds', time.time() - t
    for engine in (kernels.GPU_ENGINE, kernels.CPU_ENGINE):
        program = kernels.loadProgram(interfaces.gradient, engine=engine)
        t = time.time()
        c = program.gradient(a, 1)
        print 'Engine %s seconds %s' % (engine, time.time() - t)


if __name__ == '__main__':
    test_gradient()