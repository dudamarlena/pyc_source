# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/stress/testReg.py
# Compiled at: 2010-10-11 09:12:05
"""
Benchmark the tsreg module.
"""
import random, sys, time, tsreg

def main(outp=None):
    if outp is None:
        outp = sys.stdout
    DELTAS = (1, 2, 4, 8, 16)
    SIZES = map(int, (1000.0, 10000.0, 50000.0, 100000.0))
    I = 1
    outp.write('Num\tDur\tTime\n')
    for sz in SIZES:
        for delta in DELTAS:
            t, d, v = [], [], []
            for i in xrange(sz):
                t.append(random.uniform(i - I / 2, i + I / 2))
                d.append(random.uniform(delta / 2, delta * 2))
                v.append(random.random())

            n = sz * I
            t0 = time.time()
            _ = tsreg.reg((t, d, v), I, (0, n))
            t1 = time.time()
            outp.write('%d\t%d\t%g\n' % (sz, delta, t1 - t0))

    return 0


if __name__ == '__main__':
    sys.exit(main())