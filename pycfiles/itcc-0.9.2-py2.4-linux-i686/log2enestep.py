# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/log2enestep.py
# Compiled at: 2008-04-20 13:19:45


def log2enestep(ifile, ofile):
    step = 0
    for line in ifile:
        if line.startswith('  Step'):
            step = int(line.split()[1])
        elif line.startswith('    Potential'):
            ofile.write('%s %s\n' % (line.split()[(-1)], step))


def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        print 'usage: %s ifile > ofile' % os.path.basename(sys.argv[0])
        sys.exit(1)
    log2enestep(file(sys.argv[1]), sys.stdout)


if __name__ == '__main__':
    main()