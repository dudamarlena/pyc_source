# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/multi.py
# Compiled at: 2008-04-20 13:19:45
import sys

def multi(ifile1, ifile2, ofile):
    x2s = ifile2.read().split()
    for x1 in ifile1.read().split():
        for x2 in x2s:
            ofile.write('%s %s\n' % (x1, x2))


def multi1(ifile1, ofile):
    x1s = ifile1.read().split()
    for i in range(len(x1s)):
        for j in range(i):
            ofile.write('%s %s\n' % (x1s[i], x1s[j]))


def main():
    if len(sys.argv) not in (2, 3):
        import os.path
        sys.stderr.write('Usage: %s fname1 fname2\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile1 = sys.stdin
    if sys.argv[1] != '-':
        ifile1 = file(sys.argv[1])
    if len(sys.argv) == 2:
        multi1(ifile1, sys.stdout)
        return
    ifile2 = sys.stdin
    if sys.argv[2] != '-':
        ifile2 = file(sys.argv[2])
    multi(ifile1, ifile2, sys.stdout)


if __name__ == '__main__':
    main()