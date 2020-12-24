# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/mtxyz2txyz.py
# Compiled at: 2008-04-20 13:19:45
from itcc.molecule import read, write

def mtxyz2txyz(ifile, ofilenamepattern):
    i = 1
    while 1:
        try:
            ofname = ofilenamepattern % i
            mol = read.readxyz(ifile)
            write.writexyz(mol, file(ofname, 'w'))
        except:
            break

        i += 1


def main():
    import sys
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s <ifile|-> ofilenamepattern\n' % os.path.basename(sys.argv[0]))
        sys.stderr.write('Example: %s foo.mtxyz foo-%%03i.xyz\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    mtxyz2txyz(ifile, sys.argv[2])


if __name__ == '__main__':
    main()