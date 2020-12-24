# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/stats.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'
from numpy import *

def stat_helper(ifile):
    for line in ifile:
        for word in line.split():
            yield float(word)


def stat(ifile):
    data = array(tuple(stat_helper(ifile)))
    print 'n', len(data)
    print 'sum', data.sum()
    if len(data) == 0:
        return
    print 'min', data.min()
    print 'max', data.max()
    print 'median', median(data)
    print 'mean', data.mean()
    print 'stdev', data.std()


def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s datafile|-\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    if sys.argv[1] == '-':
        stat(sys.stdin)
    else:
        stat(file(sys.argv[1]))


if __name__ == '__main__':
    main()