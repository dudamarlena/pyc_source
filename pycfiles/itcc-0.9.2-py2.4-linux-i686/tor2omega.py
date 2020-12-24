# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/tor2omega.py
# Compiled at: 2008-04-20 13:19:45
import sys, os.path

def tor2omega(ifile, ofile):
    for line in ifile:
        data = [ float(x) for x in line.split() ]
        res = []
        for x in data:
            if abs(x) > 90:
                res.append('T')
            else:
                res.append('C')

        ofile.write(('').join(res) + '\n')


def main():
    if len(sys.argv) != 2:
        sys.stderr.write('Usage: %s FILE\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    tor2omega(ifile, sys.stdout)


if __name__ == '__main__':
    main()