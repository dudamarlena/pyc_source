# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/ene2agr.py
# Compiled at: 2008-04-20 13:19:45


def ene2agr(ifiles, ofile):
    i1 = 0
    for (idx, ifile) in enumerate(ifiles):
        data = [ float(x) for x in ifile ]
        data_min = min(data)
        for x in data:
            ofile.write('@    s%i line color %i\n' % (i1, idx + 1))
            ofile.write('@target G0.S%i\n' % i1)
            ofile.write('@type xy\n')
            ofile.write('%i %s\n' % (idx * 2 + 1, x - data_min))
            ofile.write('%i %s\n' % (idx * 2 + 2, x - data_min))
            ofile.write('&\n')
            i1 += 1


def main():
    import sys
    if len(sys.argv) < 2:
        import os.path
        sys.stderr.write('Usage: %s FILE|- ...\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    ifiles = []
    for x in sys.argv[1:]:
        if x == '-':
            ifiles.append(sys.stdin)
        else:
            ifiles.append(file(x))

    ene2agr(ifiles, sys.stdout)


if __name__ == '__main__':
    main()