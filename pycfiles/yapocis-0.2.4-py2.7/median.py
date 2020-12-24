# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/yapocis/median.py
# Compiled at: 2011-08-30 23:33:15
"""
Provides 2d median filter for 2d arrays
Created on Jul 22, 2011
"""
import numpy as np
from rpc import kernels, interfaces
program = kernels.loadProgram(interfaces.median3x3, width=9, steps=[9])
median3x3cl = program.median3x3

def median3x3(image, iterations=1):
    while iterations > 0:
        image = median3x3cl(image)
        iterations -= 1

    return image


def median3x3fast(image, iterations=1):
    if iterations == 1:
        return median3x3(image)
    input = image
    output = np.zeros_like(input)
    if iterations == 2:
        program.first(input, output)
        input, output = output, input
        program.last(input, output)
        return output
    program.first(input, output)
    input, output = output, input
    iterations -= 2
    while iterations > 1:
        program.step(input, output)
        input, output = output, input
        iterations -= 1

    input, output = output, input
    program.last(input, output)
    return output


def test_median3():
    a1 = np.random.sample((999, 1001)).astype(np.float32)
    a2 = a1.copy()
    from utils import stage
    stage('slow')
    b1 = median3x3(a1, 1000)
    stage()
    stage('fast')
    b2 = median3x3fast(a2, 1000)
    stage()
    print 'Error:', np.sum(np.abs(b1.flatten() - b2.flatten()))


if __name__ == '__main__':
    test_median3()