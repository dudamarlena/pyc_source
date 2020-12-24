# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/aa.py
# Compiled at: 2018-10-09 09:50:08
__doc__ = '\n    Amino Acid Structures for PDB2PQR\n\n    This module contains the base amino acid structures for\n    pdb2pqr.\n\n    ----------------------------\n\n    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of\n    Poisson-Boltzmann electrostatics calculations\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin;\n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific\n    Northwest National Laboratory, operated by Battelle Memorial Institute,\n    Pacific Northwest Division for the U.S. Department Energy.;\n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification,\n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice,\n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice,\n\t\t  this list of conditions and the following disclaimer in the documentation\n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND\n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED\n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.\n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT,\n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,\n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,\n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF\n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE\n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED\n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n    ----------------------------\n\n'
__date__ = '28 December 2006'
__author__ = 'Todd Dolinsky'
import string
from structures import *
from src.errors import PDBInputError

class Amino(Residue):
    """
        Amino class

        This class provides standard features of the amino acids listed
        below

        Parameters
            atoms:  A list of Atom objects to be stored in this class
                     (list)
            ref:    The reference object for the amino acid.  Used to
                    convert from the alternate naming scheme to the
                    main naming scheme.
    """

    def __init__(self, atoms, ref):
        sampleAtom = atoms[(-1)]
        self.atoms = []
        self.name = sampleAtom.resName
        self.chainID = sampleAtom.chainID
        self.resSeq = sampleAtom.resSeq
        self.iCode = sampleAtom.iCode
        self.ffname = self.name
        self.map = {}
        self.dihedrals = []
        self.patches = []
        self.peptideC = None
        self.peptideN = None
        self.isNterm = 0
        self.isCterm = 0
        self.is5term = 0
        self.is3term = 0
        self.missing = []
        self.reference = ref
        self.fixed = 0
        self.stateboolean = {}
        for a in atoms:
            if a.name in ref.altnames:
                a.name = ref.altnames[a.name]
            if a.name not in self.map:
                atom = Atom(a, 'ATOM', self)
                self.addAtom(atom)

        return

    def createAtom(self, atomname, newcoords):
        """
            Create an atom.  Override the generic residue's version of
            createAtom().

            Parameters
                atomname:  The name of the atom (string)
                newcoords: The coordinates of the atom (list).
        """
        oldatom = self.atoms[0]
        newatom = Atom(oldatom, 'ATOM', self)
        newatom.set('x', newcoords[0])
        newatom.set('y', newcoords[1])
        newatom.set('z', newcoords[2])
        newatom.set('name', atomname)
        newatom.set('occupancy', 1.0)
        newatom.set('tempFactor', 0.0)
        newatom.added = 1
        self.addAtom(newatom)

    def addAtom(self, atom):
        """
            Override the existing addAtom - include the link to the
            reference object
        """
        self.atoms.append(atom)
        atomname = atom.get('name')
        self.map[atomname] = atom
        try:
            atom.reference = self.reference.map[atomname]
            for bond in atom.reference.bonds:
                if self.hasAtom(bond):
                    bondatom = self.map[bond]
                    if bondatom not in atom.bonds:
                        atom.bonds.append(bondatom)
                    if atom not in bondatom.bonds:
                        bondatom.bonds.append(atom)

        except KeyError:
            atom.reference = None

        return

    def addDihedralAngle(self, value):
        """
            Add the value to the list of chiangles

            Parameters
                value: The value to be added (float)
        """
        self.dihedrals.append(value)

    def setState(self):
        """
           Set the name to use for the forcefield based on the current
           state.  Uses N* and C* for termini.
        """
        if self.isNterm:
            if 'NEUTRAL-NTERM' in self.patches:
                self.ffname = 'NEUTRAL-N%s' % self.ffname
            else:
                self.ffname = 'N%s' % self.ffname
        elif self.isCterm:
            if 'NEUTRAL-CTERM' in self.patches:
                self.ffname = 'NEUTRAL-C%s' % self.ffname
            else:
                self.ffname = 'C%s' % self.ffname


class ALA(Amino):
    """
        Alanine class

        This class gives data about the Alanine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'A'


class ARG(Amino):
    """
        Arginine class

        This class gives data about the Arginine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'R'

    def setState(self):
        """
           Set the name to use for the forcefield based on the current
           state.
        """
        if 'AR0' in self.patches or self.name == 'AR0':
            self.ffname = 'AR0'
        Amino.setState(self)


class ASN(Amino):
    """
        Asparagine class

        This class gives data about the Asparagine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'N'


class ASP(Amino):
    """
        Aspartic Acid class

        This class gives data about the Aspartic Acid object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'D'

    def setState(self):
        """
           Set the name to use for the forcefield based on the current
           state.
        """
        if 'ASH' in self.patches or self.name == 'ASH':
            self.ffname = 'ASH'
        Amino.setState(self)


class CYS(Amino):
    """
        Cysteine class

        This class gives data about the Cysteine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref
        self.SSbonded = 0
        self.SSbondedpartner = None
        return

    def letterCode(self):
        return 'C'

    def setState(self):
        """
            Set the state of the CYS object.  If SS-bonded, use CYX.  If
            negatively charged, use CYM.  If HG is not present, use CYX.
        """
        if 'CYX' in self.patches or self.name == 'CYX':
            self.ffname = 'CYX'
        elif self.SSbonded:
            self.ffname = 'CYX'
        elif 'CYM' in self.patches or self.name == 'CYM':
            self.ffname = 'CYM'
        elif not self.hasAtom('HG'):
            self.ffname = 'CYX'
        Amino.setState(self)


class GLN(Amino):
    """
        Glutamine class

        This class gives data about the Glutamine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'Q'


class GLU(Amino):
    """
        Glutamic Acid class

        This class gives data about the Glutamic Acid object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'E'

    def setState(self):
        """
           Set the name to use for the forcefield based on the current
           state.
        """
        if 'GLH' in self.patches or self.name == 'GLH':
            self.ffname = 'GLH'
        Amino.setState(self)


class GLY(Amino):
    """
        Glycine class

        This class gives data about the Glycine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'G'


class HIS(Amino):
    """
        Histidine class

        This class gives data about the Histidine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'H'

    def setState(self):
        """
            Histidines are a special case due to the presence of
            several different forms.  This function sets all non-
            positive incarnations of HIS to neutral HIS by
            checking to see if optimization removed hacceptor or
            hdonor flags.  Otherwise HID is used as the default.
        """
        self.ffname = 'HIP'
        Amino.setState(self)


class ILE(Amino):
    """
        Isoleucine class

        This class gives data about the Isoleucine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'I'


class LEU(Amino):
    """
        Leucine class

        This class gives data about the Leucine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'L'


class LYS(Amino):
    """
        Lysine class

        This class gives data about the Lysine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'K'

    def setState(self):
        """
            Determine if this is LYN or not
        """
        if 'LYN' in self.patches or self.name == 'LYN':
            self.ffname = 'LYN'
        Amino.setState(self)


class MET(Amino):
    """
        Methionine class

        This class gives data about the Methionine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'M'


class PHE(Amino):
    """
        Phenylalanine class

        This class gives data about the Phenylalanine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'F'


class PRO(Amino):
    """
        Proline class

        This class gives data about the Proline object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'P'

    def setState(self):
        """
           Set the name to use for the forcefield based on the current
           state.  Uses N* and C* for termini.
        """
        if self.isNterm:
            self.ffname = 'N%s' % self.ffname
        elif self.isCterm:
            if 'NEUTRAL-CTERM' in self.patches:
                self.ffname = 'NEUTRAL-C%s' % self.ffname
            else:
                self.ffname = 'C%s' % self.ffname


class SER(Amino):
    """
        Serine class

        This class gives data about the Serine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'S'


class THR(Amino):
    """
        Threonine class

        This class gives data about the Threonine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'T'


class TRP(Amino):
    """
        Tryptophan class

        This class gives data about the Tryptophan object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'W'


class TYR(Amino):
    """
        Tyrosine class

        This class gives data about the Tyrosine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'Y'

    def setState(self):
        """
            See if the TYR is negative or not
        """
        if 'TYM' in self.patches or self.name == 'TYM':
            self.ffname = 'TYM'
        Amino.setState(self)


class VAL(Amino):
    """
        Valine class

        This class gives data about the Valine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Amino.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'V'


class WAT(Residue):
    """
        Water class

        This class gives data about the Water object, and inherits
        off the base residue class.
    """
    water_residue_names = [
     'HOH', 'WAT']

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        sampleAtom = atoms[(-1)]
        self.atoms = []
        self.name = sampleAtom.resName
        self.chainID = sampleAtom.chainID
        self.resSeq = sampleAtom.resSeq
        self.iCode = sampleAtom.iCode
        self.fixed = 0
        self.ffname = 'WAT'
        self.map = {}
        self.reference = ref
        for a in atoms:
            if a.name in ref.altnames:
                a.name = ref.altnames[a.name]
            atom = Atom(a, 'HETATM', self)
            atomname = atom.get('name')
            if atomname not in self.map:
                self.addAtom(atom)
            else:
                oldatom = self.getAtom(atomname)
                oldatom.set('altLoc', '')

    def createAtom(self, atomname, newcoords):
        """
            Create a water atom.  Note the HETATM field.

            Parameters
                atomname: The name of the atom (string)
                newcoords:  The new coordinates of the atom (list)
        """
        oldatom = self.atoms[0]
        newatom = Atom(oldatom, 'HETATM', self)
        newatom.set('x', newcoords[0])
        newatom.set('y', newcoords[1])
        newatom.set('z', newcoords[2])
        newatom.set('name', atomname)
        newatom.set('occupancy', 1.0)
        newatom.set('tempFactor', 0.0)
        newatom.added = 1
        self.addAtom(newatom)

    def addAtom(self, atom):
        """
            Override the existing addAtom - include the link to the
            reference object
        """
        self.atoms.append(atom)
        atomname = atom.get('name')
        self.map[atomname] = atom
        try:
            atom.reference = self.reference.map[atomname]
            for bond in atom.reference.bonds:
                if self.hasAtom(bond):
                    bondatom = self.map[bond]
                    if bondatom not in atom.bonds:
                        atom.bonds.append(bondatom)
                    if atom not in bondatom.bonds:
                        bondatom.bonds.append(atom)

        except KeyError:
            atom.reference = None

        return


class LIG(Residue):
    """
        Generic ligand class

        This class gives data about the generic ligand object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        sampleAtom = atoms[(-1)]
        self.atoms = []
        self.name = sampleAtom.resName
        self.chainID = sampleAtom.chainID
        self.resSeq = sampleAtom.resSeq
        self.iCode = sampleAtom.iCode
        self.fixed = 0
        self.ffname = 'WAT'
        self.map = {}
        self.reference = ref
        self.isNterm = 0
        self.isCterm = 0
        for a in atoms:
            if a.name in ref.altnames:
                a.name = ref.altnames[a.name]
            atom = Atom(a, 'HETATM', self)
            atomname = atom.get('name')
            if atomname not in self.map:
                self.addAtom(atom)
            else:
                oldatom = self.getAtom(atomname)
                oldatom.set('altLoc', '')

    def createAtom(self, atomname, newcoords):
        """
            Create a water atom.  Note the HETATM field.

            Parameters
                atomname: The name of the atom (string)
                newcoords:  The new coordinates of the atom (list)
        """
        oldatom = self.atoms[0]
        newatom = Atom(oldatom, 'HETATM', self)
        newatom.set('x', newcoords[0])
        newatom.set('y', newcoords[1])
        newatom.set('z', newcoords[2])
        newatom.set('name', atomname)
        newatom.set('occupancy', 1.0)
        newatom.set('tempFactor', 0.0)
        newatom.added = 1
        self.addAtom(newatom)

    def addAtom(self, atom):
        """
            Override the existing addAtom - include the link to the
            reference object
        """
        self.atoms.append(atom)
        atomname = atom.get('name')
        self.map[atomname] = atom
        try:
            atom.reference = self.reference.map[atomname]
            for bond in atom.reference.bonds:
                if self.hasAtom(bond):
                    bondatom = self.map[bond]
                    if bondatom not in atom.bonds:
                        atom.bonds.append(bondatom)
                    if atom not in bondatom.bonds:
                        bondatom.bonds.append(atom)

        except KeyError:
            atom.reference = None

        return