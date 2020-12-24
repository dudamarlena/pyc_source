# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/rotate_to.py
# Compiled at: 2008-04-20 13:19:45
import numpy
from itcc.molecule import read, write, _rmsd

def rotate_to(idx_ifile, mol_ifile, ofile):
    mol = read.readxyz(mol_ifile)
    idxs = []
    coords = []
    for line in idx_ifile:
        if not line.strip() or line.strip()[0] == '#':
            continue
        words = line.split()
        assert len(words) == 4
        idx = int(words[0]) - 1
        assert 0 <= idx < len(mol)
        idxs.append(idx)
        coords.append([ float(x) for x in words[1:] ])

    coords = numpy.array(coords)
    res = _rmsd.rmsd2(coords, mol.coords.take(idxs, axis=0))
    mat = numpy.array(res[1])
    mol.coords = numpy.dot(mat[:3, :3], mol.coords.transpose()).transpose() + mat[:3, 3]
    write.writexyz(mol, ofile)


def main():
    import sys
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s idx-coord xyz\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    idx_ifile = sys.stdin
    if sys.argv[1] != '-':
        idx_ifile = file(sys.argv[1])
    mol_ifile = sys.stdin
    if sys.argv[2] != '-':
        mol_ifile = file(sys.argv[2])
    rotate_to(idx_ifile, mol_ifile, sys.stdout)


if __name__ == '__main__':
    main()