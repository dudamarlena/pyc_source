# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/moleculetype/atom.py
# Compiled at: 2020-02-28 01:46:19
# Size of source mod 2**32: 2636 bytes
import numpy as np

class Atom:
    __doc__ = 'Represents an atom in a molecule\n\n    Attributes are:\n        - index: atom index (int)\n        - atomtype: atom type name (str)\n        - resi: residue index (int)\n        - resn: residue name (str)\n        - name: atom name (str)\n        - cgnr: charge group index (int)\n        - charge: partial charge (electronic charge unit, float)\n        - mass: atomic mass (amu, float)\n    '
    index: int
    atomtype: str
    resi: int
    resn: str
    name: str
    cgnr: int
    charge: float
    mass: float

    def __init__(self, index: int, atomtype: str, resi: int, resn: str, name: str, cgnr: int, charge: float, mass: float):
        """Create a new Atom instance

        :param index: integer atom index
        :type index: int
        :param atomtype: atom type name
        :type atomtype: str
        :param resi: residue index
        :type resi: int
        :param resn: residue name
        :type resn: str
        :param name: atom name
        :type name: str
        :param cgnr: charge group index
        :type cgnr: int
        :param charge: partial charge (elementary charge unit)
        :type charge: float
        :param mass: atomic mass (amu)
        :type mass: float
        """
        self.index = index
        self.atomtype = atomtype
        self.resi = resi
        self.resn = resn
        self.name = name
        self.cgnr = cgnr
        self.charge = charge
        self.mass = mass

    @classmethod
    def fromITPLine(cls, line: str) -> 'Atom':
        """Create a new atom from a line in an ITP file.

        :param line: line read from an itp file, in the [ atoms ] section
        :type line: str
        :return: the new Atom instance
        :rtype: Atom
        """
        linesplit = line.split(';', 1)[0].split()
        if len(linesplit) == 8:
            index, atomtype, resi, resn, name, cgnr, charge, mass = linesplit
        else:
            if len(linesplit) == 7:
                index, atomtype, resi, resn, name, cgnr, charge = linesplit
                mass = np.nan
            else:
                raise ValueError('Invalid ITP atom line: {}'.format(line))
        return cls(index=(int(index)), atomtype=atomtype,
          resi=(int(resi)),
          resn=resn,
          name=name,
          cgnr=(int(cgnr)),
          charge=(float(charge)),
          mass=(float(mass)))

    def __deepcopy__(self, memodict={}) -> 'Atom':
        """Deep copy operation"""
        return Atom(self.index, self.atomtype, self.resi, self.resn, self.name, self.cgnr, self.charge, self.mass)