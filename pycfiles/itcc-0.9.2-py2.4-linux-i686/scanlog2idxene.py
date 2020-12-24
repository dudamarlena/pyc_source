# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/scanlog2idxene.py
# Compiled at: 2008-04-20 13:19:45
import sys

def scanlog2idxene(ifile, ofile):
    for line in ifile:
        if 'Potential Surface Map' in line:
            words = line.split()
            ofile.write('%s %s\n' % (words[4], words[5]))


def main():
    import getopt
    (opts, args) = getopt.getopt(sys.argv[1:], 'o:')
    if len(args) != 1:
        import os.path
        sys.stderr.write('Usage: %s [-o ofile] ifile\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ofile = sys.stdout
    for (k, v) in opts:
        if k == '-o':
            ofile = file(v)

    ifile = sys.stdin
    if args[0] != '-':
        ifile = file(args[0])
    scanlog2idxene(ifile, ofile)


if __name__ == '__main__':
    main()