# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: simple_ml/common/gradient_check.py
# Compiled at: 2016-09-08 18:07:02
import random, numpy as np

def grad_check(func, x, verbose=False, force_finish=False):
    rndstate = random.getstate()
    random.setstate(rndstate)
    _, grad = func(x)
    it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    max_diff = 0
    h = 0.0001
    while not it.finished:
        ix = it.multi_index
        old_value = x[ix]
        x[ix] = old_value - h
        random.setstate(rndstate)
        f1, _ = func(x)
        x[ix] = old_value + h
        random.setstate(rndstate)
        f2, _ = func(x)
        numgrad = (f2 - f1) / (2 * h)
        x[ix] = old_value
        reldiff = np.max(abs(numgrad - grad[ix]) / max(1, abs(numgrad), abs(grad[ix])))
        if reldiff > 1e-05:
            print 'Gradient check failed.', reldiff
            print 'First gradient error found at index %s' % str(ix)
            print 'Your gradient: %f \t Numerical gradient: %f' % (grad[ix], numgrad)
            if not force_finish:
                return
        elif verbose:
            print reldiff
        max_diff = max(max_diff, reldiff)
        it.iternext()

    print 'Gradient finished!', max_diff