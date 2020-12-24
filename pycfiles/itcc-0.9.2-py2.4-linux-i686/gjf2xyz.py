# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/molecule/gjf2xyz.py
# Compiled at: 2008-04-20 13:19:45
import sys
from itcc.molecule import read, write
__revision__ = '$Rev$'

def gjf2xyz(gjffname, ofile):
    if gjffname == '-':
        ifile = sys.stdin
    else:
        ifile = file(gjffname)
    write.writexyz(read.readgjf(ifile), ofile)
    ofile.close()


def main():
    if len(sys.argv) not in (2, 3):
        import os.path
        print >> sys.stderr, 'Usage: %s gjffname|- [xyzfname|-]' % os.path.basename(sys.argv[0])
        sys.exit(1)
    if len(sys.argv) == 2 or sys.argv[2] == '-':
        ofile = sys.stdout
    else:
        ofile = file(sys.argv[2], 'w')
    gjf2xyz(sys.argv[1], ofile)


if __name__ == '__main__':
    main()