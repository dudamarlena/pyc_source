# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/scalexyz.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'
from itcc.molecule import read, write

def scalexyz(ifname, scaleratio):
    mol = read.readxyz(file(ifname))
    mol.coords = [ coord * scaleratio for coord in mol.coords ]
    write.writexyz(mol)


def main():
    import sys
    if len(sys.argv) != 3:
        import os.path
        print >> sys.stderr, 'Usage: %s xyzfname scaleratio' % os.path.basename(sys.argv[0])
        sys.exit(1)
    scalexyz(sys.argv[1], float(sys.argv[2]))


if __name__ == '__main__':
    main()