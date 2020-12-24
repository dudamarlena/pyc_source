# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scythe/convert/scythe_grp_tsv.py
# Compiled at: 2014-06-13 04:01:08
import sys, getopt
VERB = True

def usage():
    print('\n    ###################################\n    #  Scythe_ensemble2grp.py (v0.1)  #\n    ###################################\n    -s NUM, --species    number of species in infile\n    -f INFILE, --file=INFILE\n                   input format: SP0geneID0    ...    SPkgeneID0\n                   first line is header\n\n    -o OUTFILE, --output=OUTFILE    default: ENSEMBLE input.grp]\n    -h, --help    prints this\n    #----------------------------------#\n    .grp format: GroupID\tgeneIDiSp1\tgeneIDjSp2\t...geneIDkSpn\n    ')
    sys.exit(2)


outfile = None
ensemblMap = None
numSp = None
try:
    opts, args = getopt.gnu_getopt(sys.argv[1:], 'f:ho:s:', ['file=', 'help', 'output=', 'species='])
except getopt.GetoptError as err:
    print(str(err))
    usage()

for o, a in opts:
    if o in ('-f', '--file'):
        ensemblMap = a
    elif o in ('-h', '--help'):
        usage()
    elif o in ('-s', '--species'):
        numSp = a
    elif o in ('-o', '--output'):
        outfile = a
    elif not False:
        raise AssertionError('unhandled option')

if not ensemblMap or not numSp:
    usage()
if not outfile:
    outfile = ensemblMap + '.grp'

def printInfo(numSp, numLoc, outfile=outfile, verb=False):
    if verb:
        print('# Success\n# Formatted ' + str(numSp) + ' species and ' + str(numLoc) + ' geneIDs.')
        print('# Saved to file ' + outfile)


def readEnsemblMap(infile, outfile, numSp):
    seen = []
    many = set()
    one = set()
    seenDct = {}
    result = ''
    id = 0
    inf = open(infile, 'r')
    out = open(outfile, 'w')
    for l in inf:
        if l.startswith('Ensembl '):
            continue
        l = l.rstrip('\n')
        tmp = l.split('\t')
        if len(tmp) < 2 or len(tmp) > int(numSp):
            print('Check your input file', infile)
            usage()
        tmp = [t for t in tmp if t != '']
        if len(tmp) < 2:
            continue
            new = [t for t in tmp if t not in one]
            for n in new:
                one.add(n)

            if len(new) < len(tmp):
                continue
                seen.append('\t'.join(new))

    inf.close()
    for l in seen:
        out.write(str(id) + '\t' + l + '\n')
        id += 1

    out.close()
    printInfo(verb=VERB, numLoc=id + 1, numSp=numSp)


readEnsemblMap(ensemblMap, outfile, numSp)