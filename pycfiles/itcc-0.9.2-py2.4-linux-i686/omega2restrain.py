# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/omega2restrain.py
# Compiled at: 2008-04-20 13:19:45


def omega2restrain(ifile, ofile):
    for line in ifile:
        line = line.strip()
        assert len(line.split()) == 4
        ofile.write('RESTRAIN-TORSION %s 1.0 120.0 240.0\n' % line)


def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s OMEGA|-\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    omega2restrain(ifile, sys.stdout)


if __name__ == '__main__':
    main()