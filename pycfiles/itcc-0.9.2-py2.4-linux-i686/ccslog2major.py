# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/ccslog2major.py
# Compiled at: 2008-04-20 13:19:45
import sys, os.path

def ccslog2enestep(ifile, ofile):
    ok = False
    for line in ifile:
        if line.startswith('Oldidx Newidx Ene(sort by Newidx)'):
            ok = True
            break

    if not ok:
        return
    ene1 = ifile.next().split()[2]
    ene2 = ifile.next().split()[2]
    ofile.write('%s %s %s\n' % (ene1, ene2, float(ene2) - float(ene1)))


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s <FILE>\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    ccslog2enestep(ifile, sys.stdout)


if __name__ == '__main__':
    main()