# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sy85\sywave.py
# Compiled at: 2010-04-11 18:31:39
import os, sys, struct
from converters.smf import *
SYWAVE_HEADER = (
 ('10s', 'file_id'),
 ('6x', ),
 ('B', '_highkey_a'),
 ('B', '_highkey_b'),
 ('B', 'orig_key'),
 ('x', ),
 ('B', '_pitch_a'),
 ('B', '_pitch_b'),
 ('2x', ),
 ('B', 'loop_type'),
 ('B', '_sy_loop_start_hi'),
 ('B', '_sy_loop_start_mid'),
 ('B', '_sy_loop_start_lo'),
 ('B', '_sy_loop_end_mid'),
 ('B', '_sy_loop_end_lo'),
 ('B', '_sy_loop_end_hi'),
 ('B', '_sample_no_hi'),
 ('B', '_sample_no_mid'),
 ('B', '_sample_no_lo')('B', 'volume'),
 ('9x', ),
 ('B', 'sample_format'),
 ('B', '_sample_period_lo'),
 ('B', '_sample_period_mid'),
 ('B', '_sample_period_hi'),
 ('B', '_sample_len_lo'),
 ('B', '_sample_len_mid'),
 ('B', '_sample_len_hi'),
 ('B', '_loop_start_lo'),
 ('B', '_loop_start_mid'),
 ('B', '_loop_start_hi'),
 ('B', '_loop_end_lo'),
 ('B', '_loop_end_mid'),
 ('B', '_loop_end_hi'),
 ('x', ),
 ('B', '_small_blocks_a'),
 ('B', '_small_blocks_b'),
 ('B', '_big_blocks_a'),
 ('B', '_big_blocks_b'),
 ('2x', ),
 ('B', '_low_key_a'),
 ('B', '_low_key_b'),
 ('958x', ))

def parse_struct(structdef, data):
    fmt = ('').join(x[0] for x in structdef)
    fields = (x[1] for x in structdef if len(x) >= 2 if x[1])
    return dict(zip(fields, struct.unpack(fmt, data[:struct.calcsize(fmt)])))


class SYWave(object):

    def __init__(self, fn):
        sywave = open(fn)
        header = parse_struct(SYWAVE_HEADER, sywave.read(1024))
        sywave.close()
        self.__dict__.update(header)

    @property
    def loop_end(self):
        return self._loop_end_hi << 16 | self._loop_end_mid << 8 | self._loop_end_lo

    @property
    def loop_start(self):
        return self._loop_start_hi << 16 | self._loop_start_mid << 8 | self._loop_start_lo


def main(args):
    from pprint import pprint
    sywave = SYWave(args[0])
    pprint(sywave.__dict__)
    print 'Loop start:', sywave.loop_start
    print 'Loop end:', sywave.loop_end
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))