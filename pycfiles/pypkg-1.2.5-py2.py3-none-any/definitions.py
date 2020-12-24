# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/definitions.py
# Compiled at: 2018-06-29 21:47:06
__doc__ = '\n    Definitions for PDB2PQR\n\n    This file contains classes associated with Amino Acid and Rotamer\n    definitions as used by PDB2PQR.\n\n    ----------------------------\n   \n    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of\n    Poisson-Boltzmann electrostatics calculations\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification, \n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice, \n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice, \n\t\t  this list of conditions and the following disclaimer in the documentation \n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n'
__date__ = '15 May 2008'
__author__ = 'Jens Erik Nielsen, Todd Dolinsky, Yong Huang'
AAPATH = 'dat/AA.xml'
NAPATH = 'dat/NA.xml'
PATCHPATH = 'dat/PATCHES.xml'
import os, copy, re
from xml import sax
from pdb import *
from utilities import *
from structures import *
from routines import *
from errors import PDBInternalError

class DefinitionHandler(sax.ContentHandler):

    def __init__(self):
        self.curelement = ''
        self.curatom = None
        self.curholder = None
        self.curobj = None
        self.map = {}
        self.patches = []
        return

    def startElement(self, name, attributes):
        if name == 'residue':
            obj = DefinitionResidue()
            self.curholder = obj
            self.curobj = obj
        elif name == 'patch':
            obj = Patch()
            self.curholder = obj
            self.curobj = obj
        elif name == 'atom':
            obj = DefinitionAtom()
            self.curatom = obj
            self.curobj = obj
        else:
            self.curelement = name

    def endElement(self, name):
        if name == 'residue':
            residue = self.curholder
            if not isinstance(residue, DefinitionResidue):
                raise PDBInternalError('Internal error parsing XML!')
            resname = residue.name
            if resname == '':
                raise PDBInternalError('Residue name not set in XML!')
            else:
                self.map[resname] = residue
                self.curholder = None
                self.curobj = None
        elif name == 'patch':
            patch = self.curholder
            if not isinstance(patch, Patch):
                raise PDBInternalError('Internal error parsing XML!')
            patchname = patch.name
            if patchname == '':
                raise PDBInternalError('Residue name not set in XML!')
            else:
                self.patches.append(patch)
                self.curholder = None
                self.curobj = None
        elif name == 'atom':
            atom = self.curatom
            if not isinstance(atom, DefinitionAtom):
                raise PDBInternalError('Internal error parsing XML!')
            atomname = atom.name
            if atomname == '':
                raise PDBInternalError('Atom name not set in XML!')
            else:
                self.curholder.map[atomname] = atom
                self.curatom = None
                self.curobj = self.curholder
        else:
            self.curelement = ''
        return self.map

    def characters(self, text):
        if text.isspace():
            return
        try:
            value = float(str(text))
        except ValueError:
            value = str(text)

        if self.curelement == 'bond':
            self.curobj.bonds.append(value)
        elif self.curelement == 'dihedral':
            self.curobj.dihedrals.append(value)
        elif self.curelement == 'altname':
            self.curholder.altnames[value] = self.curatom.name
        elif self.curelement == 'remove':
            self.curobj.remove.append(value)
        else:
            setattr(self.curobj, self.curelement, value)


class Definition:
    """
        Definition class

        The Definition class contains the structured definitions found
        in the files and several mappings for easy access to the information.
    """

    def __init__(self):
        """
            Create a new Definition Object
        """
        self.map = {}
        self.patches = {}
        handler = DefinitionHandler()
        sax.make_parser()
        for path in [AAPATH, NAPATH]:
            defpath = getDatFile(path)
            if defpath == '':
                raise PDBInternalError('%s not found!' % path)
            acidFile = open(defpath)
            sax.parseString(acidFile.read(), handler)
            acidFile.close()
            self.map.update(handler.map)

        defpath = getDatFile(PATCHPATH)
        if defpath == '':
            raise PDBInternalError('%s not found!' % PATCHPATH)
        handler.map = {}
        patchFile = open(defpath)
        sax.parseString(patchFile.read(), handler)
        patchFile.close()
        for patch in handler.patches:
            if patch.newname != '':
                resnames = self.map.keys()
                for name in resnames:
                    regexp = re.compile(patch.applyto).match(name)
                    if not regexp:
                        continue
                    newname = patch.newname.replace('*', name)
                    self.addPatch(patch, name, newname)

            self.addPatch(patch, patch.applyto, patch.name)

    def addPatch(self, patch, refname, newname):
        """
            Add a patch to a definition residue.

            Parameters
                patch:  The patch object to add (Patch)
                refname:  The name of the object to add the patch to (string)
                newname:  The name of the new (patched) object (string)
        """
        try:
            aadef = self.map[refname]
            patchResidue = copy.deepcopy(aadef)
            for atomname in patch.map:
                patchResidue.map[atomname] = patch.map[atomname]
                for bond in patch.map[atomname].bonds:
                    if bond not in patchResidue.map:
                        continue
                    if atomname not in patchResidue.map[bond].bonds:
                        patchResidue.map[bond].bonds.append(atomname)

            for key in patch.altnames:
                patchResidue.altnames[key] = patch.altnames[key]

            for remove in patch.remove:
                if not patchResidue.hasAtom(remove):
                    continue
                removebonds = patchResidue.map[remove].bonds
                del patchResidue.map[remove]
                for bond in removebonds:
                    if remove in patchResidue.map[bond].bonds:
                        patchResidue.map[bond].bonds.remove(remove)

            for dihedral in patch.dihedrals:
                patchResidue.dihedrals.append(dihedral)

            self.map[newname] = patchResidue
            self.patches[newname] = patch
        except KeyError:
            self.patches[newname] = patch


class Patch:
    """
        Patch the definitionResidue class
    """

    def __init__(self):
        """
            Initialize the Patch object.
        """
        self.name = ''
        self.applyto = ''
        self.map = {}
        self.remove = []
        self.altnames = {}
        self.dihedrals = []
        self.newname = ''

    def __str__(self):
        """
            A basic string representation for debugging
        """
        text = '%s\n' % self.name
        text += 'Apply to: %s\n' % self.applyto
        text += 'Atoms to add: \n'
        for atom in self.map:
            text += '\t%s\n' % str(self.map[atom])

        text += 'Atoms to remove: \n'
        for remove in self.remove:
            text += '\t%s\n' % remove

        text += 'Alternate naming map: \n'
        text += '\t%s\n' % self.altnames
        return text


class DefinitionResidue(Residue):
    """
        DefinitionResidue class

        The DefinitionResidue class extends the Residue class to allow for a
        trimmed down initializing function.
    """

    def __init__(self):
        """
            Initialize the class using a few parameters

            Parameters:
                name: The abbreviated amino acid name of the DefinitionResidue
        """
        self.name = ''
        self.dihedrals = []
        self.map = {}
        self.altnames = {}

    def __str__(self):
        """
            A basic string representation for debugging
        """
        text = '%s\n' % self.name
        text += 'Atoms: \n'
        for atom in self.map:
            text += '\t%s\n' % str(self.map[atom])

        text += 'Dihedrals: \n'
        for dihedral in self.dihedrals:
            text += '\t%s\n' % dihedral

        text += 'Alternate naming map: \n'
        text += '\t%s\n' % self.altnames
        return text

    def addDihedral(self, atom):
        """
            Add the atom to the list of dihedral bonds

            Parameters:
                atom: The atom to be added
        """
        self.dihedralatoms.append(atom)

    def getNearestBonds(self, atomname):
        """
            Parameters
                number:   The number of bonds to get
            Returns
                bonds:    A list of atomnames that are within three bonds of
                          the atom and present in residue (list)
        """
        bonds = []
        lev2bonds = []
        atom = self.map[atomname]
        for bondedatom in atom.bonds:
            if bondedatom not in bonds:
                bonds.append(bondedatom)

        for bondedatom in atom.bonds:
            for bond2 in self.map[bondedatom].bonds:
                if bond2 not in bonds and bond2 != atomname:
                    bonds.append(bond2)
                    lev2bonds.append(bond2)

        for lev2atom in lev2bonds:
            for bond3 in self.map[lev2atom].bonds:
                if bond3 not in bonds:
                    bonds.append(bond3)

        return bonds


class DefinitionAtom(Atom):
    """
        A trimmed down version of the Atom class
    """

    def __init__(self, name=None, x=None, y=None, z=None):
        """
            Initialize the class
        """
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        if name == None:
            self.name = ''
        if x == None:
            self.x = 0.0
        if y == None:
            self.y = 0.0
        if z == None:
            self.z = 0.0
        self.bonds = []
        return

    def __str__(self):
        """
            A basic string representation for debugging
        """
        text = '%s: %.3f %.3f %.3f' % (self.name, self.x, self.y, self.z)
        for bond in self.bonds:
            text += ' %s' % bond

        return text

    def isBackbone(self):
        """
            Return true if atom name is in backbone, otherwise false

            Returns
                state: 1 if true, 0 if false
        """
        if self.name in BACKBONE:
            return 1
        else:
            return 0