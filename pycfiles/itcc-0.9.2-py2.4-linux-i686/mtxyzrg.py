# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/tools/mtxyzrg.py
# Compiled at: 2008-04-20 13:19:45
__revision__ = '$Rev$'
from itcc.molecule import mtxyz, molecule
from itcc.core import tools

def rg(mol):
    center = molecule.CoordType()
    mass = 0.0
    for i in range(len(mol)):
        thismass = mol.atoms[i].mass
        mass += thismass
        center += mol.coords[i] * thismass

    center /= mass
    result = 0.0
    for i in range(len(mol)):
        result += tools.length(mol.coords[i] - center) ** 2 * mol.atoms[i].mass

    result /= mass
    return result


def mtxyzrg(ifname):
    ifile = file(ifname)
    for mol in mtxyz.Mtxyz(ifile):
        print rg(mol)


def main():
    import sys
    if len(sys.argv) != 2:
        import os.path
        print 'Usage: %s ifname' % os.path.basename(sys.argv[0])
        sys.exit(1)
    mtxyzrg(sys.argv[1])


if __name__ == '__main__':
    main()