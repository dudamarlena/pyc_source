# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/tests/stress/rpython_perf.py
# Compiled at: 2010-10-02 15:55:08
"""
Performance test for rpython routines
"""
import math, time
from netlogger.analysis.datamining import rpython

def time_mdf(nrow, ncol):
    _ncol, ncol_f, ncol_s = ncol, 0, 0
    ncol_i = int(math.ceil(ncol / 3))
    _ncol -= ncol_i
    if _ncol > 0:
        ncol_f = int(math.ceil(_ncol / 3))
        _ncol -= ncol_f
        if _ncol > 0:
            ncol_s = _ncol
    data = []
    for i in xrange(nrow):
        row = []
        for j in xrange(ncol_i):
            row.append(1)

        for j in xrange(ncol_f):
            row.append(3.14)

        for j in xrange(ncol_s):
            row.append('hello')

        data.append(row)

    colnames = [ 'col%d' % i for i in xrange(ncol) ]
    coltypes = [rpython.COLTYPE.INT] * ncol_i + [rpython.COLTYPE.FLOAT] * ncol_f + [
     rpython.COLTYPE.STR] * ncol_s
    t0 = time.time()
    df = rpython.make_data_frame(data, colnames, coltypes)
    t1 = time.time()
    return t1 - t0


def main():
    (min_row, max_row, row_mult) = (1000, 1000000, 10)
    (min_col, max_col, col_step) = (5, 15, 10)
    rnum = min_row
    while rnum <= max_row:
        print '%d rows' % rnum
        for cnum in xrange(min_col, max_col + 1, col_step):
            print '  %d cols =' % cnum,
            t = time_mdf(rnum, cnum)
            usec_row = 1000000.0 * (t / rnum)
            usec_datum = 1000000.0 * (t / rnum / cnum)
            print '%.3f sec, %.3f us/row, %.3f us/datum' % (t, usec_row,
             usec_datum)

        rnum *= row_mult


if __name__ == '__main__':
    main()