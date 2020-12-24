# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/scanlog2enestep.py
# Compiled at: 2008-04-20 13:19:45


def scanlog2enestep(ifile, ofile):
    step = 0
    for line in ifile:
        if 'Step' in line:
            step += 1
        elif 'Potential Surface Map' in line:
            ofile.write('%s %i\n' % (line.split()[(-1)], step))


def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s [-i] <ifname|->\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifile = sys.stdin
    if sys.argv[1] != '-':
        ifile = file(sys.argv[1])
    scanlog2enestep(ifile, sys.stdout)


if __name__ == '__main__':
    main()