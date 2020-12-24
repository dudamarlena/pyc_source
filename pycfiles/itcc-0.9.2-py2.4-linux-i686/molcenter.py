# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/molcenter.py
# Compiled at: 2008-04-20 13:19:45
import sys
from numpy import array
from itcc.molecule import read

def molcenter(mol):
    total_coord = array((0.0, 0.0, 0.0))
    total_mass = 0.0
    for i in range(len(mol)):
        mass = mol.atoms[i].getmass()
        assert mass > 0, mol.atoms[i]
        total_mass += mass
        total_coord += mol.coords[i] * mass

    return total_coord / total_mass


def main():
    if len(sys.argv) != 2:
        import os.path
        sys.stderr.write('Usage: %s molfname\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol = read.readxyz(file(sys.argv[1]))
    res = molcenter(mol)
    for i in range(3):
        print res[i],

    print


if __name__ == '__main__':
    main()