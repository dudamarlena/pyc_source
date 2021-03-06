# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/xyz2gro.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'

def xyz2gro(ifname, ofname):
    ifile = file(ifname)
    lines = ifile.readlines()
    ifile.close()
    lines = lines[1:]
    words = [ x.split() for x in lines ]
    ofile = file(ofname, 'w+')
    ofile.write('GROningen MAchine for Chemical Simulation\n')
    ofile.write('%5d\n' % len(words))
    for x in words:
        no = int(x[0])
        symbol = '%s%d' % (x[1], no)
        cx = float(x[2]) / 10.0
        cy = float(x[3]) / 10.0
        cz = float(x[4]) / 10.0
        ofile.write('%5d%5s%5s%5d%8.3f%8.3f%8.3f\n' % (1, 'DIEST', symbol, no, cx, cy, cz))

    ofile.write('%10.5f%10.5f%10.5f\n' % (0, 0, 0))
    ofile.close()


def main():
    import sys
    if len(sys.argv) != 3:
        import os.path
        print >> sys.stderr, 'Usage: %s ifname ofname' % os.path.basename(sys.argv[0])
        sys.exit(1)
    xyz2gro(sys.argv[1], sys.argv[2])


if __name__ == '__main__':
    main()