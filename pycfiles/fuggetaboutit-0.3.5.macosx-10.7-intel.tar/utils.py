# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/fuggetaboutit/utils.py
# Compiled at: 2013-10-30 17:15:16
import contextlib, time, os

@contextlib.contextmanager
def TimingBlock(name, N=None):
    start = time.time()
    yield
    dt = time.time() - start
    if N:
        print '[%0.1f][timing] %s: %fs (%f / s with %d trials)' % (start, name, dt, N / dt, N)
    else:
        print '[%0.1f][timing] %s: %fs' % (start, name, dt)


@contextlib.contextmanager
def TestFile(filename, mode='r'):
    fd = open(filename, mode)
    yield fd
    fd.close()
    os.unlink(filename)