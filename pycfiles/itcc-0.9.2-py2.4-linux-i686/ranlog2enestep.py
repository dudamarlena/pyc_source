# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/ranlog2enestep.py
# Compiled at: 2008-04-20 13:19:45


def ranlog2enestep(ifile, ofile):
    cache = set()
    for (idx, line) in enumerate(ifile):
        enestr = line.split()[(-1)]
        if enestr not in cache:
            cache.add(enestr)
            ofile.write('%s %s\n' % (enestr, idx + 1))


def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s FILE|-\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    ranlog2enestep(ifile, sys.stdout)


if __name__ == '__main__':
    main()