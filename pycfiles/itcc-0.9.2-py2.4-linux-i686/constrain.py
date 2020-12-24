# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tinker/constrain.py
# Compiled at: 2008-04-20 13:19:45
from itcc.tinker import tinker
__revision__ = '$Rev$'

def main():
    import sys
    if 2 <= len(sys.argv) <= 3:
        lines = tinker.constrain(*sys.argv[1:])
        for x in lines:
            print x,

    else:
        import os.path
        print >> sys.stderr, 'Usage: %s xyzfname [param]' % os.path.basename(sys.argv[0])
        sys.exit(1)


if __name__ == '__main__':
    main()