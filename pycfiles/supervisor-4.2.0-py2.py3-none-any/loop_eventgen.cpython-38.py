# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/supervisor/scripts/loop_eventgen.py
# Compiled at: 2018-02-15 12:36:50
# Size of source mod 2**32: 779 bytes
import sys, time
from supervisor import childutils

def main(max):
    start = time.time()
    report = open('/tmp/report', 'w')
    i = 0
    while True:
        childutils.pcomm.stdout('the_data')
        sys.stdin.readline()
        report.write(str(i) + ' @ %s\n' % childutils.get_asctime())
        report.flush()
        i += 1
        if max and i >= max:
            end = time.time()
            report.write('%s per second\n' % (i / (end - start)))
            sys.exit(0)


if __name__ == '__main__':
    max = 0
    if len(sys.argv) > 1:
        max = int(sys.argv[1])
    main(max)