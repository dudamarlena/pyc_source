# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/lreg_fill.py
# Compiled at: 2007-08-13 06:22:59
import g_pipe, Num
LREG = '/home/gpk/misctts/lreg_fit2'

def fill(f, wt, s):
    assert len(f) == len(wt)
    pi, po = g_pipe.popen2(LREG, ['lreg_fit2', '-smooth', '%g' % s])
    for tfw in zip(f, wt):
        pi.write('%g %g\n' % tfw)

    pi.close()
    o = map(float, po.readlines())
    po.close()
    assert len(o) == len(f)
    tmp = Num.asarray(o, Num.Float)
    return tmp