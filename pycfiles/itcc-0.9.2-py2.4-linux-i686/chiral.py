# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/molecule/chiral.py
# Compiled at: 2008-04-20 13:19:45
__all__ = [
 'chiral_type']
import sys
from itcc.molecule import mtxyz

def chiral_type(mol, idx):
    if mol.connect is None:
        return
    connects = [ i for i in range(len(mol)) if mol.connect[(idx, i)] ]
    if len(connects) != 4:
        return
    tor = mol.calctor(*connects)
    if tor > 0.0:
        return True
    if tor < 0.0:
        return False
    return


def chiral_types(mol, idxs):
    return type(idxs)([ chiral_type(mol, idx) for idx in idxs ])


def usage(ofile):
    import os.path
    prog = os.path.basename(sys.argv[0])
    ofile.write('Usage: %s [-v] -i|--idx IDX FILENAME...\n       %s [-v] -I|--idx-file IDX-FILE FILENAME...\n       %s -h|--help\n' % (prog, prog, prog))


def main():
    import sys, getopt
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'hvi:I:', [
         'help', 'verbose', 'idx=', 'idx-file='])
    except getopt.GetoptError:
        usage(sys.stderr)
        sys.exit(2)

    idx = None
    verbose = False
    for (k, v) in opts:
        if k in ('-h', '--help'):
            usage(sys.stdout)
            sys.exit(0)
        elif k in ('-v', '--verbose'):
            verbose = True
        elif k in ('-i', '--idx'):
            idx = v
        elif k in ('-I', '--idx-file'):
            ifile = sys.stdin
            if v != '-':
                ifile = file(v)
            idx = ifile.read()

    if idx is None:
        usage(sys.stderr)
        sys.exit(1)
    idx = [ int(x) - 1 for x in idx.split() ]
    for fname in args:
        for mol in mtxyz.Mtxyz(file(fname)):
            if verbose:
                sys.stdout.write('%s ' % fname)
            for x in idx:
                t = chiral_type(mol, x)
                if t is True:
                    sys.stdout.write('A')
                elif t is False:
                    sys.stdout.write('B')
                else:
                    sys.stdout.write('C')

            sys.stdout.write('\n')
            sys.stdout.flush()

    return


if __name__ == '__main__':
    main()