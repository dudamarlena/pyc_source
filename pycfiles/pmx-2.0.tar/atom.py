# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: pmx/atom.py
# Compiled at: 2019-03-20 07:51:02
"""
This module contains the Atom class. It basically stores Atom
properties but also has some methods for fast calculations.
Basic Usage:
      >>> model = Model().read(args['-f']) # read structure file
      >>> atom = model.atoms[0]     # the first atom
      >>> a = Atom(name='DUM',x = [1,2,3], bfac = 20.) # create atom

      Some methods:
      - distance calculation:
      >>> d = atom1 - atom2    # fast distance calculation
      - angle calculation
      >>> a = atom1.angle(atom2,atom3) # angle calculation
      - dihedral calculation
      >>> dih = atom1.dihedral(atom2,atom3,atom4)

      - output
      >>> print atom   # prints atom in pdb format
      

"""
import _pmx as _p
from numpy import *
import copy, library
from library import pdb_format, pdb_format2

class Atom:
    """ class for storage of atom properties and methods"""

    def __init__(self, line=None, mol2line=None, **kwargs):
        self.race = 'ATOM  '
        self.id = 0
        self.orig_id = 0
        self.code = 0
        self.name = ''
        self.altloc = ''
        self.resname = ''
        self.chain_id = ' '
        self.x = [0, 0, 0]
        self.occ = 1.0
        self.bfac = 0.0
        self.vdw = 0.0
        self.vdw14 = 0.0
        self.atype = ''
        self.hyb = ''
        self.symbol = ''
        self.bonds = []
        self.b13 = []
        self.b14 = []
        self.connected = []
        self.neighbors = []
        self.order = 0
        self.boxid = 0
        self.molecule = None
        self.chain = None
        self.model = None
        self.cgnr = 0.0
        self.v = [0, 0, 0]
        self.f = []
        self.m = 0.0
        self.q = 0.0
        self.mB = 0.0
        self.qB = 0.0
        self.type = ''
        self.typeB = ''
        self.resnr = 0
        self.grpnr = ' '
        self.atomtype = ''
        self.atomtypeB = ''
        self.ptype = ''
        self.long_name = ''
        self.unity = 'A'
        for key, val in kwargs.items():
            setattr(self, key, val)

        if line is not None:
            self.readPDBString(line)
        if mol2line is not None:
            self.read_mol2_line(mol2line)
        return

    def readPDBString(self, line, origID=0):
        """PDB String to Atom"""
        self.race = line[0:6]
        self.id = int(line[7:11])
        self.orig_id = origID
        self.name = line[12:16].strip()
        self.altloc = line[16]
        self.resname = line[17:21].strip()
        self.chain_id = line[21]
        try:
            self.resnr = int(line[22:27])
        except:
            self.resnr = line[22:27]

        self.x = [
         float(line[30:38]),
         float(line[39:46]), float(line[47:54])]
        try:
            self.occ = float(line[55:60])
        except:
            self.occ = 1.0

        try:
            self.bfac = float(line[61:66])
        except:
            self.bfac = 0.0

        try:
            self.symbol = line[70:73].strip()
        except:
            self.symbol = None

        self.unity = 'A'
        if not self.symbol:
            self.get_symbol()
        return self

    def dist(self, other):
        """ returns the distance between two atoms
        Usage: dist=atom1.dist(atom2)
        This function is also called by typing
        d=atom1-atom2"""
        return _p.dist(self.x, other.x)

    def dist2(self, other):
        """ returns the squared distance between two atoms
        Usage: dist=atom1.dist2(atom2)"""
        return _p.dist2(self.x, other.x)

    def __sub__(self, other):
        """ Overloading of the '-' operator for using
        atom1-atom2 instead of atom1.dist(atom2)"""
        return self.dist(other)

    def translate(self, v):
        self.x[0] += v[0]
        self.x[1] += v[1]
        self.x[2] += v[2]

    def nm2a(self):
        if self.unity == 'nm':
            self.x[0] *= 10
            self.x[1] *= 10
            self.x[2] *= 10
            self.unity = 'A'

    def a2nm(self):
        if self.unity == 'A':
            self.x[0] *= 0.1
            self.x[1] *= 0.1
            self.x[2] *= 0.1
            self.unity = 'nm'

    def angle(self, other1, other2, degree=None):
        """ Calcluates the angle between 3 atoms
        Usage: atom1.angle(atom2,atom3)
        The degree flag causes the function to return the angle
        in degrees.
        (Note: atom1 must be between 2 and 3)"""
        angle = _p.angle(other1.x, self.x, other2.x)
        if degree:
            return angle * 180.0 / pi
        else:
            return angle

    def dihedral(self, other1, other2, other3, degree=None):
        """ Calculates the dihedral between four atoms.
        Usage: atom1.dihedral(atom2,atom3,atom4)
        The degree flag causes the function to return the dihedral
        in degrees."""
        ang = _p.dihedral(self.x, other1.x, other2.x, other3.x)
        if degree:
            return ang * 180.0 / pi
        else:
            return ang

    def __str__(self):
        """ prints the atom in PDB format """
        if self.unity == 'nm':
            coords = map(lambda x: x * 10, self.x)
        else:
            coords = self.x
        if len(self.resname) < 4:
            resname = self.resname + ' '
        else:
            resname = self.resname
        if len(self.name) == 1:
            name = ' ' + self.name + '  '
        else:
            if len(self.name) == 2:
                if self.name[0].isdigit():
                    name = self.name + '  '
                else:
                    name = ' ' + self.name + ' '
            else:
                if len(self.name) == 3:
                    if self.name[0].isdigit():
                        name = self.name + ' '
                    else:
                        name = ' ' + self.name
                else:
                    name = self.name
                idx = self.id % 100000
                try:
                    resid = self.resnr % 10000
                except:
                    resid = str(self.resnr)

            try:
                s = pdb_format % (self.race, idx, name, self.altloc,
                 resname, self.chain_id, resid,
                 coords[0], coords[1],
                 coords[2], self.occ, self.bfac, self.symbol)
            except:
                s = pdb_format2 % (self.race, idx, name, self.altloc,
                 resname, self.chain_id, resid,
                 coords[0], coords[1],
                 coords[2], self.occ, self.bfac)

        return s

    def set_resname(self, resname):
        self.resname = resname

    def set_chain_id(self, chain_id):
        """ change chain identifier"""
        self.chain_id = chain_id

    def make_long_name(self):
        """ make extended name to determine element
        and order"""
        ali = library._aliases
        if ali.has_key(self.resname) and ali[self.resname].has_key(self.name):
            name = ali[self.resname][self.name]
        else:
            name = self.name.strip()
        if len(name) == 4:
            if not name[0].isdigit():
                tmp = name[3]
                name = tmp + name[:-1]
        elif len(name) == 3:
            if name[0].isdigit():
                name += ' '
            else:
                name = ' ' + name
        elif len(name) == 2:
            if name[1].isdigit() and name[0] == 'H' and self.resname in library._aacids:
                name = name[1] + name[0] + '  '
            else:
                name = ' ' + name + ' '
        elif len(name) == 1:
            name = ' ' + name + '  '
        self.long_name = name

    def copy(self):
        """ copy atom"""
        return copy.deepcopy(self)

    def get_symbol(self):
        """ get element"""
        if self.long_name == '':
            self.make_long_name()
        if self.resname in library._protein_residues or self.resname in library._nucleic_acids:
            self.symbol = self.long_name[1]
        elif self.resname in library._ions:
            self.symbol = self.resname.upper()
            if len(self.symbol) > 2:
                self.symbol = self.symbol[:2]
        elif self.resname in library._water:
            self.symbol = self.name[0]
        else:
            c1 = self.long_name[1]
            c2 = self.long_name[2]
            if c1 == 'C':
                self.symbol = 'C'
                if c2.upper() == 'L':
                    self.symbol = 'CL'
            elif c1 == 'O':
                self.symbol = 'O'
            elif c1 == 'N':
                self.symbol = 'N'
            elif c1 == 'H':
                self.symbol = 'H'
            elif c1 == 'S':
                self.symbol = 'S'
            elif c1 == 'P':
                self.symbol = 'P'
            elif c1 == 'B':
                if c2.upper() == 'R':
                    self.symbol = 'BR'
            elif c1 == 'F':
                if c2.upper() == 'E':
                    self.symbol = 'FE'
                else:
                    self.symbol = 'F'
            elif c1 == 'I':
                self.symbol = 'I'
            elif c1 == 'D':
                self.symbol = 'D'
            elif c1 == 'M':
                self.symbol = 'D'
            else:
                self.symbol = 'UN'

    def get_order(self):
        """ get the order (number of bonds to mainchain)"""
        if self.long_name == '':
            self.make_long_name()
        if self.symbol == '':
            self.get_symbol()
        if self.resname not in library._protein_residues:
            print 'Sorry, implemented for proteins only'
            return
        el = self.symbol
        x = self.long_name[2]
        if self.name in ('C', 'CA', 'N'):
            self.order = 0
        elif self.name in ('H', 'H1', 'H2', 'H3', '1H', '2H', '3H', 'O', 'O1', 'O2',
                           'OC1', 'OC2', 'OXT', 'OT1', 'OT2'):
            self.order = 1
        elif el != 'H':
            if x == 'B':
                self.order = 1
            elif x == 'G':
                self.order = 2
            elif x == 'D':
                self.order = 3
            elif x == 'E':
                self.order = 4
            elif x == 'Z':
                self.order = 5
            elif x == 'H':
                self.order = 6
        elif el == 'H':
            if x == 'A':
                self.order = 1
            elif x == 'B':
                self.order = 2
            elif x == 'G':
                self.order = 3
            elif x == 'D':
                self.order = 4
            elif x == 'E':
                self.order = 5
            elif x == 'Z':
                self.order = 6
            elif x == 'H':
                self.order = 7

    def read_mol2_line(self, line):
        entr = line.split()
        if len(entr) == 9:
            self.id = int(entr[0])
            self.name = entr[1]
            self.x[0] = float(entr[2])
            self.x[1] = float(entr[3])
            self.x[2] = float(entr[4])
            self.atype = entr[5]
            self.resnr = int(entr[6])
            self.resname = entr[7]
            self.q = float(entr[8])
            self.unity = 'A'
            self.symbol = self.atype.split('.')[0]
        elif len(entr) == 10:
            self.id = int(entr[0])
            self.name = entr[1]
            self.x[0] = float(entr[3])
            self.x[1] = float(entr[4])
            self.x[2] = float(entr[5])
            self.atype = entr[6]
            self.resnr = int(entr[7])
            self.resname = entr[8]
            self.q = float(entr[9])
            self.unity = 'A'
            self.symbol = self.atype.split('.')[0]
        else:
            print 'Error: Cannot convert line to atom'
            print line
            sys.exit(1)
        return self