# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/anaconda3/lib/python3.7/site-packages/reademptionlib/wiggle.py
# Compiled at: 2019-07-15 11:56:07
# Size of source mod 2**32: 937 bytes


class WiggleWriter(object):

    def __init__(self, track_str, fh):
        self._fh = fh
        self._fh.write('track type=wiggle_0 name="%s"\n' % track_str)

    def write_replicons_coverages(self, replicon_str, coverages, discard_zeros=True, factor=1.0):
        self._fh.write('variableStep chrom=%s span=1\n' % replicon_str)
        self._fh.write('\n'.join(['%s %s' % (pos + 1, coverage * factor) for pos, coverage in filter(lambda pos_and_cov: pos_and_cov[1] != 0.0, enumerate(coverages))]) + '\n')

    def close_file(self):
        self._fh.close()