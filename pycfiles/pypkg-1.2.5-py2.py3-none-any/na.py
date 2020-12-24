# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/na.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    Nucleic Acid Structures for PDB2PQR\n\n    This module contains the base nucleic acid structures for\n    pdb2pqr.\n\n    ----------------------------\n   \n    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of\n    Poisson-Boltzmann electrostatics calculations\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification, \n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice, \n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice, \n\t\t  this list of conditions and the following disclaimer in the documentation \n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n    ----------------------------\n\n'
__date__ = '28 February 2006'
__author__ = 'Todd Dolinsky'
import string
from structures import *

class Nucleic(Residue):
    """
        Nucleic class

        This class provides standard features of the nucleic acids listed
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
        self.is3term = 0
        self.is5term = 0
        self.isCterm = 0
        self.isNterm = 0
        self.missing = []
        self.reference = ref
        for a in atoms:
            if a.name in ref.altnames:
                a.name = ref.altnames[a.name]
            if a.name not in self.map:
                atom = Atom(a, 'ATOM', self)
                self.addAtom(atom)

    def createAtom(self, atomname, newcoords):
        """
            Create an atom.  Overrides the generic residue's createAtom().

            Parameters
                atomname:  The name of the atom to add (string)
                newcoords: The coordinates of the atom (list)
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
           Adds the termini for all inherited objects
        """
        if self.is5term:
            self.ffname = self.ffname + '5'
        if self.is3term:
            self.ffname = self.ffname + '3'


class ADE(Nucleic):
    """
        Adenosine class

        This class gives data about the Adenosine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Nucleic.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'A'

    def setState(self):
        """
            Set the state to distinguish RNA from DNA.
        """
        if self.hasAtom("O2'"):
            self.ffname = 'RA'
        else:
            self.ffname = 'DA'
        Nucleic.setState(self)


class CYT(Nucleic):
    """
        Cytidine class

        This class gives data about the Cytidine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Nucleic.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'C'

    def setState(self):
        """
            Set the state to distinguish RNA from DNA.
        """
        if self.hasAtom("O2'"):
            self.ffname = 'RC'
        else:
            self.ffname = 'DC'
        Nucleic.setState(self)


class GUA(Nucleic):
    """
        Guanosine class

        This class gives data about the Guanosine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Nucleic.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'G'

    def setState(self):
        """
            Set the state to distinguish RNA from DNA.
        """
        if self.hasAtom("O2'"):
            self.ffname = 'RG'
        else:
            self.ffname = 'DG'
        Nucleic.setState(self)


class THY(Nucleic):
    """
        Thymine class

        This class gives data about the Thymine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Nucleic.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'T'

    def setState(self):
        """
            Set the state to distinguish RNA from DNA.  In this case it is
            always DNA.
        """
        self.ffname = 'DT'
        Nucleic.setState(self)


class URA(Nucleic):
    """
        Uridine class

        This class gives data about the Uridine object, and inherits
        off the base residue class.
    """

    def __init__(self, atoms, ref):
        """
            Initialize the class

            Parameters
                atoms:      A list of Atom objects to be stored in this class
                            (list)
        """
        Nucleic.__init__(self, atoms, ref)
        self.reference = ref

    def letterCode(self):
        return 'U'

    def setState(self):
        """
            Set the state to distinguish RNA from DNA.  In this case it is
            always RNA.
        """
        self.ffname = 'RU'
        Nucleic.setState(self)


class RA(ADE):
    pass


class RC(CYT):
    pass


class RG(GUA):
    pass


class DT(THY):
    pass


class RU(URA):
    pass