# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scythe/convert/scythe_grp_proteinortho.py
# Compiled at: 2014-06-13 07:39:20
import re, sys, getopt

def usage():
    print('\n    ################################\n    #  Scythe_proteinOrtho2grp.py  #\n    ################################\n\n    -f, --file=INFILE        (output of ProteinOrtho, pairs, unambiguous)\n    -l, --loc=LOCFILE        concatenated .loc file or comma separated list of .loc files\n    -o, --output=OUTFILE     output file [default: INFILE.grp]\n    -h, --help               prints this\n\n    ------------\n    .grp format: GroupID\tgeneIDiSp1\tgeneIDjSp2\t...geneIDkSpn\n    ')
    sys.exit(2)


def read_proteinortho2grp(infile, locfile, outfile):
    mod2loc = {}
    locfiles = locfile.split(',')
    for locfile in locfiles:
        locfile = locfile.strip()
        locfile = open(locfile, 'r')
        for ln in locfile:
            ln = ln.rstrip()
            g, gm = ln.split('\t')[0], ln.split('\t')[1:]
            for m in gm:
                mod2loc[m] = g

        locfile.close()

    grp = 0
    outfile = open(outfile, 'w')
    infile = open(infile, 'r')
    for ln in infile:
        if ln.startswith('#'):
            continue
        ln = ln.rstrip()
        ids = ln.split('\t')[3:]
        allid = []
        for i in ids:
            if i == '*':
                continue
            allid.append(mod2loc[i])

        outfile.write(str(grp) + '\t' + '\t'.join(allid) + '\n')
        grp += 1

    infile.close()
    print('# ', str(grp), ' orthogroups formatted.')


def main():
    outfile = None
    infile = None
    locfile = None
    try:
        opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:ho:l:', ['file=', 'help', 'output=', 'loc='])
    except getopt.GetoptError as err:
        print(str(err))
        usage()

    for o, a in opts:
        if o in ('-f', '--file'):
            infile = a
        elif o in ('-h', '--help'):
            usage()
        elif o in ('-o', '--output'):
            outfile = a
        elif o in ('-l', '--loc'):
            locfile = a
            print(a)
        elif not False:
            raise AssertionError('unhandled option')

    if infile is None:
        usage()
    if outfile is None:
        outfile = infile + '.grp'
    if locfile is None:
        usage()
    print('#  Output: ', outfile)
    read_proteinortho2grp(infile, locfile, outfile)
    return


if __name__ == '__main__':
    main()