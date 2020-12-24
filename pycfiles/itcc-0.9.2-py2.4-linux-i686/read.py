# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/itcc/molecule/read.py
# Compiled at: 2008-04-20 13:19:45
__all__ = [
 'readxyz', 'readgjf', 'FormatError']
__revision__ = '$Rev$'
import re
from itcc.molecule.molecule import Molecule
from itcc.molecule.atom import Atom

class FormatError(Exception):
    __module__ = __name__


def readgjf(ifile_or_ifname):
    if isinstance(ifile_or_ifname, str):
        ifile = file(ifile_or_ifname)
    else:
        ifile = ifile_or_ifname
    blanklines = 0
    mol = Molecule()
    while blanklines < 2:
        line = ifile.readline().strip()
        if line == '':
            blanklines += 1

    ifile.readline()
    for line in ifile:
        line = line.strip()
        if line == '':
            break
        words = line.split()
        x = []
        for word in words:
            x.extend(word.split(','))

        atom = Atom(x[0])
        coord = [ float(coord) for coord in x[-3:] ]
        mol.addatom(atom, coord)

    ifile.close()
    return mol


def readxyz(ifile):
    """readxyz(ifile) => Molecule
    if got errors, raise FormatError
    """
    mol = Molecule()
    connects = []
    line = ifile.readline()
    match = re.compile('^ *(\\d+) *(.*)$').match(line)
    atmnum = int(match.group(1))
    comment = match.group(2).strip()
    if comment:
        mol.comment = comment
    for i in range(atmnum):
        words = ifile.readline().split()
        atom = Atom(words[1], int(words[5]))
        coord = [ float(x) for x in words[2:5] ]
        mol.addatom(atom, coord)
        connects.append(words[6:])

    for (i, connect) in enumerate(connects):
        for j in connect:
            mol.buildconnect(i, int(j) - 1)

    assert atmnum == len(mol)
    return mol