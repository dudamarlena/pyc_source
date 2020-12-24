# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/itcc_main.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'
import sys, os.path, itcc

def help():
    basename = os.path.basename(sys.argv[0])
    print 'Version:', itcc.__version__
    print
    print 'report bugs to <lidaobing@gmail.com>'


def main():
    help()
    if len(sys.argv) == 2 and sys.argv[1] == '-v':
        print 'itcc path:', sys.modules['itcc'].__file__
        import numpy
        print 'numpy version:', numpy.__version__
    if len(sys.argv) != 1:
        sys.exit(1)


if __name__ == '__main__':
    main()