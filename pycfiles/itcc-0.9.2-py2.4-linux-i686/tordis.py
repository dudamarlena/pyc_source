# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/tordis.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'
import math

def normtor(tor, lower=-180.0, upper=180.0):
    return (tor - lower) % (upper - lower) + lower


def tordis(ifname):
    ifile = file(ifname)
    headline = ifile.readline()
    basetors = [ float(x) for x in headline.split() ]
    colnum = len(basetors)
    print 0.0
    for line in ifile:
        tors = [ float(x) for x in line.split() ]
        assert len(tors) == colnum
        difftors = [ normtor(tor1 - tor2) for (tor1, tor2) in zip(tors, basetors) ]
        tordiff = math.sqrt(sum([ tor * tor for tor in difftors ]))
        print tordiff

    ifile.close()


def main():
    import sys
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s torfname\n' % sys.argv[0])
        sys.exit(1)
    tordis(sys.argv[1])


if __name__ == '__main__':
    main()