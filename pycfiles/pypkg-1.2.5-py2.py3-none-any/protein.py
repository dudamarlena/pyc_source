# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/protein.py
# Compiled at: 2019-06-28 06:50:35
__doc__ = '\n    Routines for PDB2PQR\n\n    This module contains the protein object used in PDB2PQR and associated\n    methods\n    \n    ----------------------------\n   \n    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of\n    Poisson-Boltzmann electrostatics calculations\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification, \n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice, \n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice, \n\t\t  this list of conditions and the following disclaimer in the documentation \n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n    ----------------------------\n\n'
__date__ = '13 May 2008'
__author__ = 'Todd Dolinsky, Yong Huang'
from pdb import *
from structures import *
from aa import *
from na import *

class Protein:
    """
        Protein class

        The protein class represents the parsed PDB, and provides a
        hierarchy of information - each Protein contains a list of Chain
        objects as provided in the PDB file.  Each Chain then contains its
        associated list of Residue objects, and each Residue contains a list
        of Atom objects, completing the hierarchy.
    """

    def __init__(self, pdblist, definition):
        """
            Initialize using parsed PDB file

            Parameters
                pdblist: List of Classes of PDB lines as created
        """
        self.chainmap = {}
        self.chains = []
        self.residues = []
        self.referencemap = definition.map
        self.patchmap = definition.patches
        chainDict = {}
        previousAtom = None
        residue = []
        numModels = 0
        numChains = 1
        count = 0
        for record in pdblist:
            if isinstance(record, TER):
                numChains += 1

        for record in pdblist:
            if isinstance(record, ATOM) or isinstance(record, HETATM):
                if record.chainID == '' and numChains > 1 and record.resName not in ('WAT',
                                                                                     'HOH'):
                    record.chainID = string.ascii_uppercase[count]
                chainID = record.chainID
                resSeq = record.resSeq
                resName = record.resName
                iCode = record.iCode
                if previousAtom == None:
                    previousAtom = record
                if chainID not in chainDict:
                    myChain = Chain(chainID)
                    chainDict[chainID] = myChain
                if resSeq != previousAtom.resSeq or iCode != previousAtom.iCode or chainID != previousAtom.chainID:
                    myResidue = self.createResidue(residue, previousAtom.resName)
                    chainDict[previousAtom.chainID].addResidue(myResidue)
                    residue = []
                residue.append(record)
                previousAtom = record
            elif isinstance(record, END):
                myResidue = self.createResidue(residue, previousAtom.resName)
                chainDict[previousAtom.chainID].addResidue(myResidue)
                residue = []
            elif isinstance(record, MODEL):
                numModels += 1
                if residue == []:
                    continue
                if numModels > 1:
                    myResidue = self.createResidue(residue, previousAtom.resName)
                    chainDict[previousAtom.chainID].addResidue(myResidue)
                    break
            elif isinstance(record, TER):
                count += 1

        if residue != [] and numModels <= 1:
            myResidue = self.createResidue(residue, previousAtom.resName)
            chainDict[previousAtom.chainID].addResidue(myResidue)
        self.chainmap = chainDict.copy()
        if chainDict.has_key(''):
            chainDict['ZZ'] = chainDict['']
            del chainDict['']
        keys = chainDict.keys()
        keys.sort()
        for key in keys:
            self.chains.append(chainDict[key])

        for chain in self.chains:
            for residue in chain.getResidues():
                self.residues.append(residue)

        return

    def createResidue(self, residue, resname):
        """
            Create a residue object.  If the resname is a known residue
            type, try to make that specific object, otherwise just make
            a standard residue object.

            Parameters
                residue:  A list of atoms (list)
                resname:  The name of the residue (string)

            Returns:
                residue:  The residue object (Residue)
        """
        try:
            refobj = self.referencemap[resname]
            if refobj.name != resname:
                fullobj = self.referencemap[refobj.name]
                obj = '%s(residue, refobj)' % fullobj.name
                residue = eval(obj)
                residue.reference = fullobj
            else:
                obj = '%s(residue, refobj)' % resname
                residue = eval(obj)
        except (KeyError, NameError):
            residue = Residue(residue)

        return residue

    def printAtoms(self, atomlist, chainflag=False, pdbfile=False):
        """
            Get the text for the entire protein
            Parameters
                atomlist:  The list of atoms to include (list)
                chainflag: Flag whether to print chainid or not -
                              Defaults to False
            Returns
                text:      The list of (stringed) atoms (list)
        """
        self.reSerialize()
        text = []
        currentchainID = None
        for atom in atomlist:
            if currentchainID == None:
                currentchainID = atom.chainID
            elif atom.chainID != currentchainID:
                currentchainID = atom.chainID
                text.append('TER\n')
            if pdbfile == True:
                text.append('%s\n' % atom.getPDBString())
            else:
                text.append('%s\n' % atom.getPQRString(chainflag=chainflag))

        text.append('TER\nEND')
        return text

    def createHTMLTypeMap(self, definition, outfilename):
        """
            Create an HTML typemap file at the desired location. If a
            type cannot be found for an atom a blank is listed.
            
            Parameters
                definition: The definition objects.
                outfilename:  The name of the file to write (string)
        """
        from forcefield import Forcefield
        from aconf import STYLESHEET
        numcache = {}
        for atom in self.getAtoms():
            numcache[atom] = atom.serial

        self.reSerialize()
        amberff = Forcefield('amber', definition, None)
        charmmff = Forcefield('charmm', definition, None)
        file = open(outfilename, 'w')
        file.write('<HTML>\n')
        file.write('<HEAD>\n')
        file.write('<TITLE>PQR Typemap (beta)</TITLE>\n')
        file.write('<link rel="stylesheet" href="%s" type="text/css">\n' % STYLESHEET)
        file.write('</HEAD>\n')
        file.write('<BODY>\n')
        file.write('<H3>This is a developmental page including the atom type for the atoms in the PQR file.</H3><P>\n')
        file.write('<TABLE CELLSPACING=2 CELLPADDING=2 BORDER=1>\n')
        file.write('<tr><th>Atom Number</th><th>Atom Name</th><th>Residue Name</th><th>Chain ID</th><th>AMBER Atom Type</th><th>CHARMM Atom Type</th></tr>\n')
        for atom in self.getAtoms():
            if isinstance(atom.residue, (Amino, WAT, Nucleic)):
                resname = atom.residue.ffname
            else:
                resname = atom.residue.name
            ambergroup = amberff.getGroup(resname, atom.name)
            charmmgroup = charmmff.getGroup(resname, atom.name)
            file.write('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>\n' % (atom.serial, atom.name, resname, atom.chainID, ambergroup, charmmgroup))

        file.write('</table>\n')
        file.write('</BODY></HTML>\n')
        file.close()
        for atom in self.getAtoms():
            atom.serial = numcache[atom]

        del numcache
        del amberff
        del charmmff
        return

    def reSerialize(self):
        """
            Generate new serial numbers for atoms in the protein
        """
        count = 1
        for atom in self.getAtoms():
            atom.set('serial', count)
            count += 1

    def getResidues(self):
        """
            Return the list of residues in the entire protein
        """
        return self.residues

    def numResidues(self):
        """
            Get the number of residues for the entire protein (including
            multiple chains)

            Returns
                count:  Number of residues in the protein (int)
        """
        return len(self.getResidues())

    def numAtoms(self):
        """
            Get the number of atoms for the entire protein(including
            multiple chains)
        """
        return len(self.getAtoms())

    def getAtoms(self):
        """
            Return all Atom objects in list format

            Returns
                atomlist:  List of Atom objects in the protein (list)
        """
        atomlist = []
        for chain in self.chains:
            for atom in chain.getAtoms():
                atomlist.append(atom)

        return atomlist

    def getCharge(self):
        """
            Get the total charge on the protein
            NOTE:  Since the misslist is used to identify incorrect
                   charge assignments, this routine does not list the
                   3 and 5 termini of nucleic acid chains as having
                   non-integer charge even though they are (correctly)
                   non-integer.
            Returns:
                misslist: List of residues with non-integer
                          charges (list)
                charge:   The total charge on the protein (float)
        """
        charge = 0.0
        misslist = []
        for chain in self.chains:
            for residue in chain.get('residues'):
                rescharge = residue.getCharge()
                charge += rescharge
                if isinstance(residue, Nucleic):
                    if residue.is3term or residue.is5term:
                        continue
                if float('%i' % rescharge) != rescharge:
                    misslist.append(residue)

        return (
         misslist, charge)

    def getChains(self):
        """
            Get the chains object

            Returns
                chains: The list of chains in the protein (chain)
        """
        return self.chains

    def getSummary(self):
        output = []
        for chain in self.chains:
            output.append(chain.getSummary())

        return (' ').join(output)