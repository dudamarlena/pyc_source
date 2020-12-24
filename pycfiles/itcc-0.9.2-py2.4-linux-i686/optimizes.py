# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tinker/optimizes.py
# Compiled at: 2008-04-20 13:19:45
import getopt, sys
from itcc.tinker import tinker
__revision__ = '$Rev$'

def usage():
    print >> sys.stderr, 'Usage: %s [-c converge] xyzfname ...' % sys.argv[0]


def main():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hc:', ['help'])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    converge = 0.01
    for (o, a) in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in '-c':
            converge = float(a)

    enes = tinker.batchoptimize(args, converge=converge)
    for (fname, ene) in zip(args, enes):
        print '%s,%.3f' % (fname, ene)


if __name__ == '__main__':
    main()