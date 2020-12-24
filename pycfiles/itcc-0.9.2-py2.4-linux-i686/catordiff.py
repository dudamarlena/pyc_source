# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/ccs2/catordiff.py
# Compiled at: 2008-04-20 13:19:45
"""calculate the torsion diff of two cycloalkane"""
import sys, math
from itcc.tools import periodnumber
from itcc.molecule import read, molecule, tools
from itcc.ccs2 import detectloop, tordiff
__revision__ = '$Rev$'
__all__ = ['catordiff']
debug = False
Angle = periodnumber.genPNclass(-math.pi, math.pi)

def catordiff(mol1, mol2, loop=None):
    assert isinstance(mol1, molecule.Molecule)
    assert isinstance(mol2, molecule.Molecule)
    tors1 = getlooptor(mol1, loop)
    tors2 = getlooptor(mol2, loop)
    return tordiff.torsdiff(tors1, tors2, True, 0, 1)


def getlooptor(mol, loop):
    if loop is None:
        loops = detectloop.loopdetect(mol)
        assert len(loops) == 1
        loop = loops[0]
    return tools.calclooptor(mol, loop)


def main():
    if len(sys.argv) != 3:
        import os.path
        sys.stderr.write('Usage: %s xyzfname1 xyzfname2\nresult unit is degree\n' % os.path.basename(sys.argv[0]))
        sys.exit(1)
    mol1 = read.readxyz(file(sys.argv[1]))
    mol2 = read.readxyz(file(sys.argv[2]))
    print math.degrees(catordiff(mol1, mol2))


if __name__ == '__main__':
    main()