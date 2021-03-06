# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: src/hydrogens.py
# Compiled at: 2018-10-18 05:37:42
__doc__ = '\n    Hydrogen optimization for PDB2PQR\n\n    This is an module for hydrogen optimization routines.\n\n    ----------------------------\n   \n    PDB2PQR -- An automated pipeline for the setup, execution, and analysis of\n    Poisson-Boltzmann electrostatics calculations\n\n    Copyright (c) 2002-2011, Jens Erik Nielsen, University College Dublin; \n    Nathan A. Baker, Battelle Memorial Institute, Developed at the Pacific \n    Northwest National Laboratory, operated by Battelle Memorial Institute, \n    Pacific Northwest Division for the U.S. Department Energy.; \n    Paul Czodrowski & Gerhard Klebe, University of Marburg.\n\n\tAll rights reserved.\n\n\tRedistribution and use in source and binary forms, with or without modification, \n\tare permitted provided that the following conditions are met:\n\n\t\t* Redistributions of source code must retain the above copyright notice, \n\t\t  this list of conditions and the following disclaimer.\n\t\t* Redistributions in binary form must reproduce the above copyright notice, \n\t\t  this list of conditions and the following disclaimer in the documentation \n\t\t  and/or other materials provided with the distribution.\n        * Neither the names of University College Dublin, Battelle Memorial Institute,\n          Pacific Northwest National Laboratory, US Department of Energy, or University\n          of Marburg nor the names of its contributors may be used to endorse or promote\n          products derived from this software without specific prior written permission.\n\n\tTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND \n\tANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED \n\tWARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. \n\tIN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, \n\tINDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, \n\tBUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, \n\tDATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF \n\tLIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE \n\tOR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED \n\tOF THE POSSIBILITY OF SUCH DAMAGE.\n\n    ----------------------------\n'
import os, string, math
from definitions import *
from utilities import *
from quatfit import *
from routines import *
import topology
__date__ = '22 April 2009'
__author__ = 'Todd Dolinsky, Jens Erik Nielsen, Yong Huang'
HDEBUG = 0
HYDPATH = 'dat/HYDROGENS.xml'
TOPOLOGYPATH = 'dat/TOPOLOGY.xml'
ANGLE_CUTOFF = 20.0
DIST_CUTOFF = 3.3

class HydrogenHandler(sax.ContentHandler):
    """
        Extends the SAX XML Parser to parse the Hydrogens.xml
        class
    """

    def __init__(self):
        """
            Initalize the class.
        """
        self.curelement = ''
        self.curatom = None
        self.curobj = None
        self.curholder = None
        self.map = {}
        return

    def startElement(self, name, attributes):
        """
            Create optimization holder objects or atoms
        """
        if name == 'class':
            obj = OptimizationHolder()
            self.curholder = obj
            self.curobj = obj
        elif name == 'atom':
            obj = DefinitionAtom()
            self.curatom = obj
            self.curobj = obj
        else:
            self.curelement = name

    def endElement(self, name):
        """
            Complete whatever object is currently passed in
            by the name parameter
        """
        if name == 'class':
            obj = self.curholder
            if not isinstance(obj, OptimizationHolder):
                raise PDBInternalError('Internal error parsing XML!')
            self.map[obj.name] = obj
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
        """
            Set a given attribute of the object to the text
        """
        if text.isspace():
            return
        try:
            value = float(str(text))
        except ValueError:
            value = str(text)

        setattr(self.curobj, self.curelement, value)


class PotentialBond():
    """
        A small class containing the hbond structure
    """

    def __init__(self, atom1, atom2, dist):
        """
            Initialize the class

            Parameters
                atom1:  The first atom in the potential bond (Atom)
                atom2:  The second atom in the potential bond (Atom)
                dist:  The distance between the two atoms (float)
        """
        self.atom1 = atom1
        self.atom2 = atom2
        self.dist = dist

    def __str__(self):
        """
            String for debugging
        """
        txt = '%s %s' % (self.atom1.name, self.atom1.residue)
        txt += ' to '
        txt += '%s %s' % (self.atom2.name, self.atom2.residue)
        txt += ' (%.2f A)' % self.dist
        return txt


class hydrogenAmbiguity():
    """
        A class containing information about the ambiguity
    """

    def __init__(self, residue, hdef, routines):
        """
            Initialize the class - if the residue has a rotateable hydrogen,
            remove it.  If it can be flipped, pre-flip the residue by creating
            all additional atoms.

            Parameters
                residue:  The residue in question (residue)
                hdef:     The hydrogen definition matching the residue
                routines: Pointer to the general routines object
        """
        self.residue = residue
        self.hdef = hdef
        self.routines = routines

    def __str__(self):
        """
            Print the ambiguity for debugging purposes
        """
        text = '%s %i %s (%s)' % (self.residue.name, self.residue.resSeq,
         self.residue.chainID, self.hdef.opttype)
        return text


class Optimize():
    """
        The holder class for the hydrogen optimization
        routines. Individual optimization types inherit off of this
        class.  Any functions used by multiple types appear here.
    """

    def __init__(self):
        """
            Initialize the class
        """
        pass

    def __str__(self):
        """
            String output for debugging
        """
        txt = '%s (%s)' % (self.residue, self.optinstance.opttype)
        return txt

    def debug(self, txt):
        """
            Easy way to turn on/off debugging
        """
        if HDEBUG:
            print txt

    @staticmethod
    def getHbondangle(atom1, atom2, atom3):
        """
            Get the angle between three atoms

            Parameters
                atom1:  The first atom (atom)
                atom2:  The second (vertex) atom (atom)
                atom3:  The third atom (atom)
            Returns
                angle:  The angle between the atoms (float)
        """
        atom2Coords = atom2.getCoords()
        coords1 = subtract(atom3.getCoords(), atom2Coords)
        coords2 = subtract(atom1.getCoords(), atom2Coords)
        norm1 = normalize(coords1)
        norm2 = normalize(coords2)
        dotted = dot(norm1, norm2)
        if dotted > 1.0:
            dotted = 1.0
        elif dotted < -1.0:
            dotted = -1.0
        rad = abs(math.acos(dotted))
        angle = rad * 180.0 / math.pi
        if angle > 180.0:
            angle = 360.0 - angle
        return angle

    def isHbond(self, donor, acc):
        """
            Determine whether this donor acceptor pair is a
            hydrogen bond
        """
        for donorhatom in donor.bonds:
            if not donorhatom.isHydrogen():
                continue
            dist = distance(donorhatom.getCoords(), acc.getCoords())
            if dist > DIST_CUTOFF:
                continue
            flag = 1
            for acchatom in acc.bonds:
                if not acchatom.isHydrogen():
                    continue
                flag = 0
                hdist = distance(donorhatom.getCoords(), acchatom.getCoords())
                if hdist < 1.5:
                    continue
                angle = self.getHbondangle(donorhatom, acchatom, acc)
                if angle < 110.0:
                    flag = 1

            if flag == 0:
                continue
            angle = self.getHbondangle(acc, donor, donorhatom)
            if angle <= ANGLE_CUTOFF:
                self.debug('Found HBOND! %.4f %.4f' % (dist, angle))
                return 1

        return 0

    @staticmethod
    def getPairEnergy(donor, acceptor):
        """
            Get the energy between two atoms

            Parameters
                donor:    The first atom in the pair (Atom)
                acceptor: The second atom in the pair (Atom)
            Returns
                energy:   The energy of the pair (float)
        """
        bump_energy = 10.0
        bump_distance = 1.5
        max_hbond_energy = -10.0
        max_ele_energy = -1.0
        ADH_angle_cutoff = ANGLE_CUTOFF
        DhAhA_angle_cutoff = 110.0
        max_dha_dist = DIST_CUTOFF
        max_ele_dist = 5.0
        energy = 0.0
        if not (donor.hdonor and acceptor.hacceptor):
            return energy
        donorhs = (bond for bond in donor.bonds if bond.isHydrogen())
        acceptorhs = [ bond for bond in acceptor.bonds if bond.isHydrogen() ]
        for donorhatom in donorhs:
            dist = distance(donorhatom.getCoords(), acceptor.getCoords())
            if dist > max_dha_dist and dist < max_ele_dist:
                energy += max_ele_energy / (dist * dist)
                continue
            for acceptorhatom in acceptorhs:
                hdist = distance(donorhatom.getCoords(), acceptorhatom.getCoords())
                if hdist < bump_distance:
                    energy += bump_energy
                    continue
                angle1 = Optimize.getHbondangle(acceptor, donor, donorhatom)
                if angle1 <= ADH_angle_cutoff:
                    angle2 = Optimize.getHbondangle(donorhatom, acceptorhatom, acceptor)
                    if angle2 < DhAhA_angle_cutoff:
                        angle2 = 1.0
                    else:
                        angle2 = (DhAhA_angle_cutoff - angle2) / DhAhA_angle_cutoff
                    angleterm = (ADH_angle_cutoff - angle1) / ADH_angle_cutoff
                    energy += max_hbond_energy / pow(dist, 3) * angleterm * angle2

            if len(acceptorhs) == 0:
                angle1 = Optimize.getHbondangle(acceptor, donor, donorhatom)
                if angle1 <= ADH_angle_cutoff:
                    angleterm = (ADH_angle_cutoff - angle1) / ADH_angle_cutoff
                    energy += max_hbond_energy / pow(dist, 2) * angleterm

        return energy

    def makeAtomWithNoBonds(self, atom, closeatom, addname):
        """
            Called for water oxygen atoms with no current bonds.
            Uses the closeatom to place the new atom directly
            colinear with the atom and the closeatom.

            Parameters
                atom:      The oxygen atom of the water
                closeatom: The nearby atom (donor/acceptor)
                addname:   The name of the atom to add
        """
        newcoords = []
        residue = atom.residue
        vec = subtract(closeatom.getCoords(), atom.getCoords())
        dist = distance(atom.getCoords(), closeatom.getCoords())
        for i in range(3):
            newcoords.append(vec[i] / dist + atom.getCoords()[i])

        residue.createAtom(addname, newcoords)
        newatom = residue.getAtom(addname)
        self.routines.cells.addCell(newatom)
        if newatom not in atom.bonds:
            atom.bonds.append(newatom)
        if atom not in newatom.bonds:
            newatom.bonds.append(atom)

    def makeWaterWithOneBond(self, atom, addname):
        """
            Add an atom to a water residue that already has
            one bond.  Uses the water reference structure to
            align the new atom.
        """
        residue = atom.residue
        nextatom = atom.bonds[0]
        coords = [atom.getCoords(), nextatom.getCoords()]
        refcoords = [residue.reference.map[atom.name].getCoords(),
         residue.reference.map['H1'].getCoords()]
        refatomcoords = residue.reference.map['H2'].getCoords()
        newcoords = findCoordinates(2, coords, refcoords, refatomcoords)
        residue.createAtom(addname, newcoords)
        newatom = residue.getAtom(addname)
        if newatom not in atom.bonds:
            atom.bonds.append(newatom)
        if atom not in newatom.bonds:
            newatom.bonds.append(atom)

    def makeAtomWithOneBondH(self, atom, addname):
        """
            Add a hydrogen to an alcoholic donor with one
            existing bond.
        """
        residue = atom.residue
        nextatom = atom.bonds[0]
        coords = [atom.getCoords(), nextatom.getCoords()]
        refcoords = [residue.reference.map[atom.name].getCoords(),
         residue.reference.map[nextatom.name].getCoords()]
        refatomcoords = residue.reference.map[addname].getCoords()
        newcoords = findCoordinates(2, coords, refcoords, refatomcoords)
        residue.createAtom(addname, newcoords)

    def makeAtomWithOneBondLP(self, atom, addname):
        """
            Add a lone pair to an alcoholic donor with one
            existing bond.
        """
        residue = atom.residue
        for refname in atom.reference.bonds:
            if refname.startswith('H'):
                break

        nextatom = atom.bonds[0]
        coords = [atom.getCoords(), nextatom.getCoords()]
        refcoords = [residue.reference.map[atom.name].getCoords(),
         residue.reference.map[nextatom.name].getCoords()]
        refatomcoords = residue.reference.map[refname].getCoords()
        newcoords = findCoordinates(2, coords, refcoords, refatomcoords)
        residue.createAtom(addname, newcoords)
        newatom = residue.getAtom(addname)
        if newatom not in atom.bonds:
            atom.bonds.append(newatom)
        if atom not in newatom.bonds:
            newatom.bonds.append(atom)

    def trySingleAlcoholicH(self, donor, acc, newatom):
        """
            After a new bond has been added using
            makeAtomWithOneBond*, try to find the best orientation
            by rotating to form a hydrogen bond.  If a bond
            cannot be formed, remove the newatom (thereby
            returning to a single bond).
        """
        besten = 999.99
        bestcoords = []
        residue = donor.residue
        pivot = donor.bonds[0]
        for i in range(72):
            residue.rotateTetrahedral(pivot, donor, 5.0)
            if self.isHbond(donor, acc):
                energy = self.getPairEnergy(donor, acc)
                if energy < besten:
                    bestcoords = newatom.getCoords()
                    besten = energy

        if bestcoords != []:
            newatom.x = bestcoords[0]
            newatom.y = bestcoords[1]
            newatom.z = bestcoords[2]
            self.routines.cells.addCell(newatom)
            return 1
        else:
            residue.removeAtom(newatom.name)
            return 0

    def trySingleAlcoholicLP(self, acc, donor, newatom):
        """
            After a new bond has been added using
            makeAtomWithOneBond*, ensure that a
            hydrogen bond has been made.  If so, try to
            minimze the H(D)-A-LP angle.  If that cannot
            be minimized, ignore the bond and remove the
            atom.
        """
        residue = acc.residue
        pivot = acc.bonds[0]
        bestangle = 180.0
        bestcoords = []
        if not self.isHbond(donor, acc):
            residue.removeAtom(newatom.name)
            return 0
        for donorhatom in donor.bonds:
            if donorhatom.isHydrogen() and self.getHbondangle(acc, donor, donorhatom) < ANGLE_CUTOFF:
                break

        for i in range(72):
            residue.rotateTetrahedral(pivot, acc, 5.0)
            angle = abs(self.getHbondangle(donorhatom, acc, newatom))
            if angle < bestangle:
                bestangle = angle
                bestcoords = newatom.getCoords()

        if bestangle > ANGLE_CUTOFF * 2.0:
            self.debug('Removing due to geometry %.2f > %.2f' % (bestangle, ANGLE_CUTOFF * 2.0))
            residue.removeAtom(newatom.name)
            return 0
        newatom.x = bestcoords[0]
        newatom.y = bestcoords[1]
        newatom.z = bestcoords[2]
        self.routines.cells.addCell(newatom)
        return 1

    def getPositionsWithTwoBonds(self, atom):
        """
            Given a tetrahedral geometry with two
            existing bonds, return the two potential
            sets of coordinates that are possible for
            a new bond.
        """
        residue = atom.residue
        fixed = atom.bonds[0]
        rotate = atom.bonds[1]
        residue.rotateTetrahedral(fixed, atom, 120)
        loc1 = rotate.getCoords()
        residue.rotateTetrahedral(fixed, atom, 120)
        loc2 = rotate.getCoords()
        residue.rotateTetrahedral(fixed, atom, 120)
        return (
         loc1, loc2)

    def tryPositionsWithTwoBondsH(self, donor, acc, newname, loc1, loc2):
        """
            Try adding a new hydrogen two the two potential
            locations.  If both form hydrogen bonds, place at
            whatever returns the best bond as determined by
            getPairEnergy.
        """
        besten = 999.99
        bestcoords = []
        residue = donor.residue
        residue.createAtom(newname, loc1)
        if self.isHbond(donor, acc):
            besten = self.getPairEnergy(donor, acc)
            bestcoords = loc1
        newatom = residue.getAtom(newname)
        newatom.x = loc2[0]
        newatom.y = loc2[1]
        newatom.z = loc2[2]
        if self.isHbond(donor, acc):
            energy = self.getPairEnergy(donor, acc)
            if energy < besten:
                bestcoords = loc2
        if bestcoords != []:
            newatom.x = bestcoords[0]
            newatom.y = bestcoords[1]
            newatom.z = bestcoords[2]
            self.routines.cells.addCell(newatom)
            return 1
        else:
            residue.removeAtom(newname)
            return 0

    def tryPositionsWithTwoBondsLP(self, acc, donor, newname, loc1, loc2):
        """
            Try placing an LP on a tetrahedral geometry with
            two existing bonds.  If this isn't a hydrogen bond
            it can return - otherwise ensure that the H(D)-A-LP
            angle is minimized.
        """
        bestangle = 180.0
        bestcoords = []
        residue = acc.residue
        if not self.isHbond(donor, acc):
            return 0
        for donorhatom in donor.bonds:
            if donorhatom.isHydrogen() and self.getHbondangle(acc, donor, donorhatom) < ANGLE_CUTOFF:
                break

        residue.createAtom(newname, loc1)
        newatom = residue.getAtom(newname)
        angle = abs(self.getHbondangle(donorhatom, acc, newatom))
        if angle < bestangle:
            bestangle = angle
            bestcoords = loc1
        newatom.x = loc2[0]
        newatom.y = loc2[1]
        newatom.z = loc2[2]
        angle = self.getHbondangle(donorhatom, acc, newatom)
        if angle < bestangle:
            bestcoords = loc2
        if bestangle > ANGLE_CUTOFF * 2.0:
            residue.removeAtom(newname)
            return 0
        newatom.x = bestcoords[0]
        newatom.y = bestcoords[1]
        newatom.z = bestcoords[2]
        self.routines.cells.addCell(newatom)
        if newatom not in acc.bonds:
            acc.bonds.append(newatom)
        if acc not in newatom.bonds:
            newatom.bonds.append(acc)
        return 1

    def getPositionWithThreeBonds(self, atom):
        """
           If there's three bonds in a tetrahedral geometry,
           there's only one available position.  Find that
           position.
        """
        residue = atom.residue
        pivot = atom.bonds[0]
        rot1 = atom.bonds[1]
        rot2 = atom.bonds[2]
        residue.rotateTetrahedral(pivot, atom, 120)
        newcoords1 = rot1.getCoords()
        residue.rotateTetrahedral(pivot, atom, 120)
        newcoords2 = rot1.getCoords()
        residue.rotateTetrahedral(pivot, atom, 120)
        if distance(rot2.getCoords(), newcoords1) > 0.1:
            return newcoords1
        else:
            return newcoords2

    def tryPositionsWithThreeBondsH(self, donor, acc, newname, loc):
        """
            Try making a hydrogen bond with the lone available
            position.
        """
        residue = donor.residue
        residue.createAtom(newname, loc)
        if self.isHbond(donor, acc):
            newatom = residue.getAtom(newname)
            self.routines.cells.addCell(newatom)
            return 1
        else:
            residue.removeAtom(newname)
            return 0

    def tryPositionsWithThreeBondsLP(self, acc, donor, newname, loc):
        """
            Try making a hydrogen bond using the lone
            available hydrogen position.
        """
        residue = acc.residue
        if not self.isHbond(donor, acc):
            return 0
        for donorhatom in donor.bonds:
            if donorhatom.isHydrogen() and self.getHbondangle(acc, donor, donorhatom) < ANGLE_CUTOFF:
                break

        residue.createAtom(newname, loc)
        newatom = residue.getAtom(newname)
        angle = abs(self.getHbondangle(donorhatom, acc, newatom))
        if angle > ANGLE_CUTOFF * 2.0:
            residue.removeAtom(newname)
            return 0
        newatom = residue.getAtom(newname)
        self.routines.cells.addCell(newatom)
        if newatom not in acc.bonds:
            acc.bonds.append(newatom)
        if acc not in newatom.bonds:
            newatom.bonds.append(acc)
        return 1


class Flip(Optimize):
    """
        The holder for optimization of flippable residues.
    """

    def __init__(self, residue, optinstance, routines):
        """
            Initialize a potential flip.  Rather than flipping
            the given residue back and forth, take each atom
            that would be flipped and pre-flip it, making a
            new *FLIP atom in its place.

            Parameters
                residue:      The residue to flip (residue)
                optinstance:  The optimization instance containing
                              information about what to optimize
                
        """
        self.optinstance = optinstance
        self.residue = residue
        self.routines = routines
        self.atomlist = []
        self.hbonds = []
        map = {}
        dihedral = optinstance.optangle
        pivot = dihedral.split()[2]
        moveablenames = self.routines.getMoveableNames(residue, pivot)
        if residue.isCterm:
            newmoveablenames = []
            for i in range(len(moveablenames)):
                if moveablenames[i] == 'HO':
                    pass
                else:
                    newmoveablenames.append(moveablenames[i])

            moveablenames = newmoveablenames
        for name in moveablenames:
            atom = residue.getAtom(name)
            map[name] = atom.getCoords()

        anglenum = residue.reference.dihedrals.index(dihedral)
        if anglenum == -1:
            raise PDBInternalError('Unable to find Flip dihedral angle!')
        newangle = 180.0 + residue.dihedrals[anglenum]
        self.routines.setDihedralAngle(residue, anglenum, newangle)
        for name in map:
            newname = '%sFLIP' % name
            residue.createAtom(newname, map[name])
            newatom = residue.getAtom(newname)
            self.routines.cells.addCell(newatom)
            newatom.reference = residue.reference.map[name]
            for bond in newatom.reference.bonds:
                newbond = '%sFLIP' % bond
                if residue.hasAtom(newbond):
                    bondatom = residue.map[newbond]
                    if bondatom not in newatom.bonds:
                        newatom.bonds.append(bondatom)
                    if newatom not in bondatom.bonds:
                        bondatom.bonds.append(newatom)
                newbond = bond
                if residue.hasAtom(newbond):
                    bondatom = residue.map[newbond]
                    if bondatom not in newatom.bonds:
                        newatom.bonds.append(bondatom)
                    if newatom not in bondatom.bonds:
                        bondatom.bonds.append(newatom)

        residue.setDonorsAndAcceptors()
        for name in moveablenames:
            atom = residue.getAtom(name)
            if not atom.isHydrogen() and (atom.hdonor or atom.hacceptor):
                self.atomlist.append(atom)
            atom = residue.getAtom('%sFLIP' % name)
            if not atom.isHydrogen() and (atom.hdonor or atom.hacceptor):
                self.atomlist.append(atom)

        if isinstance(residue, HIS) and 'HIS' == residue.name:
            if len(residue.patches) == 1:
                for atom in self.atomlist:
                    if atom.name.startswith('N'):
                        atom.hacceptor = 1

    def tryBoth(self, donor, acc, accobj):
        """
           Called when both the donor and acceptor are optimizeable;
           If one is fixed, we only need to try one side.  Otherwise
           first try to satisfy the donor - if that's succesful,
           try to satisfy the acceptor.  An undo may be necessary
           if the donor is satisfied and the acceptor isn't.
        """
        if donor.residue.fixed:
            if accobj.tryAcceptor(acc, donor):
                return 1
            else:
                return 0

        if acc.residue.fixed:
            if self.tryDonor(donor, acc):
                return 1
            else:
                return 0

        self.debug('Working on %s %s (donor) to %s %s (acceptor)' % (
         donor.residue, donor.name, acc.residue, acc.name))
        if self.isHbond(donor, acc):
            if accobj.tryAcceptor(acc, donor):
                self.fixFlip(donor)
                donor.hacceptor = 0
                self.debug('NET BOND SUCCESSFUL!')
                return 1
            else:
                return 0

    def tryDonor(self, donor, acc):
        """
           The main driver for adding a hydrogen to an
           optimizeable residue.
        """
        residue = self.residue
        if not acc.hacceptor:
            return 0
        else:
            self.debug('Working on %s %s (donor) to %s %s (acceptor)' % (
             donor.residue, donor.name, acc.residue, acc.name))
            if self.isHbond(donor, acc):
                residue.fixed = donor.name
                self.fixFlip(donor)
                donor.hacceptor = 0
                return 1
            return 0

    def tryAcceptor(self, acc, donor):
        """
           The main driver for adding an LP to an optimizeable
           residue.
        """
        residue = acc.residue
        if not donor.hdonor:
            return 0
        else:
            self.debug('Working on %s %s (acceptor) to %s %s (donor)' % (
             acc.residue, acc.name, donor.residue, donor.name))
            if self.isHbond(donor, acc):
                residue.fixed = acc.name
                self.fixFlip(acc)
                acc.hdonor = 0
                return 1
            return 0

    def fixFlip(self, bondatom):
        """
           Called if a hydrogen bond has been found using
           the bondatom.  If bondatom is *FLIP, remove all *
           atoms, otherwise remove all *FLIP atoms. 
        """
        atomlist = []
        residue = bondatom.residue
        for atom in residue.getAtoms():
            atomlist.append(atom)

        flag = 0
        if bondatom.name.endswith('FLIP'):
            flag = 1
        for atom in atomlist:
            atomname = atom.name
            if atomname.endswith('FLIP') and flag:
                if residue.hasAtom(atomname[:-4]):
                    self.routines.cells.removeCell(residue.getAtom(atomname[:-4]))
                    residue.removeAtom(atomname[:-4])
            elif atomname.endswith('FLIP'):
                self.routines.cells.removeCell(atom)
                residue.removeAtom(atomname)
            else:
                continue

        residue.fixed = 1

    def finalize(self):
        """
            Finalizes a flippable back to its original state -
            since the original atoms are now *FLIP, it deletes
            the * atoms and renames the *FLIP atoms back to *.
        """
        residue = self.residue
        if residue.fixed:
            return
        atomlist = []
        for atom in residue.getAtoms():
            atomlist.append(atom)

        for atom in atomlist:
            if atom.name.endswith('FLIP'):
                self.routines.cells.removeCell(atom)
                residue.removeAtom(atom.name[:-4])
                residue.renameAtom(atom.name, atom.name[:-4])

        residue.fixed = 1

    def complete(self):
        """
            Complete the flippable residue optimization.  Call the finalize
            function, and then rename all FLIP atoms back to their standard
            names.
        """
        residue = self.residue
        self.finalize()
        for atom in residue.getAtoms():
            atomname = atom.name
            if atomname.endswith('FLIP'):
                residue.renameAtom(atomname, atomname[:-4])


class Alcoholic(Optimize):
    """
        The class for alcoholic residues
    """

    def __init__(self, residue, optinstance, routines):
        """
           Initialize the alcoholic class by removing
           the alcoholic hydrogen if it exists.
        """
        self.optinstance = optinstance
        self.residue = residue
        self.routines = routines
        self.atomlist = []
        self.hbonds = []
        name = optinstance.map.keys()[0]
        self.hname = name
        bondname = residue.reference.getAtom(name).bonds[0]
        self.atomlist.append(residue.getAtom(bondname))
        if residue.hasAtom(name):
            atom = residue.getAtom(name)
            self.routines.cells.removeCell(atom)
            residue.removeAtom(name)

    def tryBoth(self, donor, acc, accobj):
        """
           Called when both the donor and acceptor are optimizeable;
           If one is fixed, we only need to try one side.  Otherwise
           first try to satisfy the donor - if that's succesful,
           try to satisfy the acceptor.  An undo may be necessary
           if the donor is satisfied and the acceptor isn't.
        """
        residue = donor.residue
        if donor.residue.fixed:
            if accobj.tryAcceptor(acc, donor):
                return 1
            else:
                return 0

        if acc.residue.fixed:
            if self.tryDonor(donor, acc):
                return 1
            else:
                return 0

        if self.tryDonor(donor, acc):
            if accobj.tryAcceptor(acc, donor):
                self.debug('NET BOND SUCCESSFUL!')
                return 1
            else:
                residue.removeAtom(self.hname)
                self.debug('REMOVED NET HBOND')
                return 0

        else:
            return 0

    def tryDonor(self, donor, acc):
        """
           The main driver for adding a hydrogen to an
           optimizeable residue.
        """
        residue = self.residue
        if not acc.hacceptor:
            return 0
        newname = self.hname
        if residue.hasAtom(newname):
            return 0
        self.debug('Working on %s %s (donor) to %s %s (acceptor)' % (
         donor.residue, donor.name, acc.residue, acc.name))
        if len(donor.bonds) == 1:
            self.makeAtomWithOneBondH(donor, newname)
            newatom = donor.residue.getAtom(newname)
            return self.trySingleAlcoholicH(donor, acc, newatom)
        if len(donor.bonds) == 2:
            loc1, loc2 = self.getPositionsWithTwoBonds(donor)
            return self.tryPositionsWithTwoBondsH(donor, acc, newname, loc1, loc2)
        if len(donor.bonds) == 3:
            loc = self.getPositionWithThreeBonds(donor)
            return self.tryPositionsWithThreeBondsH(donor, acc, newname, loc)

    def tryAcceptor(self, acc, donor):
        """
           The main driver for adding an LP to an optimizeable
           residue.
        """
        residue = acc.residue
        if not donor.hdonor:
            return 0
        if residue.hasAtom('LP2'):
            return 0
        if residue.hasAtom('LP1'):
            newname = 'LP2'
        else:
            newname = 'LP1'
        self.debug('Working on %s %s (acceptor) to %s %s (donor)' % (
         acc.residue, acc.name, donor.residue, donor.name))
        if len(acc.bonds) == 1:
            self.makeAtomWithOneBondLP(acc, newname)
            newatom = acc.residue.getAtom(newname)
            return self.trySingleAlcoholicLP(acc, donor, newatom)
        if len(acc.bonds) == 2:
            loc1, loc2 = self.getPositionsWithTwoBonds(acc)
            return self.tryPositionsWithTwoBondsLP(acc, donor, newname, loc1, loc2)
        if len(acc.bonds) == 3:
            loc = self.getPositionWithThreeBonds(acc)
            return self.tryPositionsWithThreeBondsLP(acc, donor, newname, loc)

    def finalize(self):
        """
            Finalize an alcoholic residue.  Try to minimize
            conflict with nearby atoms by building away
            from them.  Called when LPs are still present
            so as to account for their bonds.
        """
        residue = self.residue
        atom = self.atomlist[0]
        addname = self.hname
        if residue.fixed:
            return
        if residue.hasAtom(addname):
            return
        if len(atom.bonds) == 1:
            pivot = atom.bonds[0]
            bestcoords = []
            bestenergy = 999.99
            self.makeAtomWithOneBondH(atom, addname)
            newatom = residue.getAtom(addname)
            self.routines.cells.addCell(newatom)
            for _ in range(18):
                residue.rotateTetrahedral(pivot, atom, 20.0)
                closeatoms = self.routines.cells.getNearCells(atom)
                energy = 0.0
                for catom in closeatoms:
                    energy += self.getPairEnergy(atom, catom) + self.getPairEnergy(catom, atom)

                if energy < bestenergy:
                    bestenergy = energy
                    bestcoords = newatom.getCoords()

            if bestcoords != []:
                newatom.x = bestcoords[0]
                newatom.y = bestcoords[1]
                newatom.z = bestcoords[2]
        elif len(atom.bonds) == 2:
            loc1, loc2 = self.getPositionsWithTwoBonds(atom)
            residue.createAtom(addname, loc1)
            newatom = residue.getAtom(addname)
            self.routines.cells.addCell(newatom)
            closeatoms = self.routines.cells.getNearCells(atom)
            energy1 = 0.0
            for catom in closeatoms:
                energy1 += self.getPairEnergy(atom, catom) + self.getPairEnergy(catom, atom)

            self.routines.cells.removeCell(newatom)
            newatom.x = loc2[0]
            newatom.y = loc2[1]
            newatom.z = loc2[2]
            self.routines.cells.addCell(newatom)
            energy2 = 0.0
            for catom in closeatoms:
                energy2 += self.getPairEnergy(atom, catom) + self.getPairEnergy(catom, atom)

            if energy2 > energy1:
                self.routines.cells.removeCell(newatom)
                newatom.x = loc1[0]
                newatom.y = loc1[1]
                newatom.z = loc1[2]
                self.routines.cells.addCell(newatom)
        elif len(atom.bonds) == 3:
            loc = self.getPositionWithThreeBonds(atom)
            residue.createAtom(addname, loc)
            self.routines.cells.addCell(residue.getAtom(addname))

    def complete(self):
        """
            Complete an alcoholic optimization.  Call finalize(), and then
            remove all extra LP atoms.
        """
        residue = self.residue
        self.finalize()
        residue.fixed = 1
        atomlist = []
        for atom in residue.getAtoms():
            atomlist.append(atom)

        for atom in atomlist:
            if atom.name.startswith('LP'):
                residue.removeAtom(atom.name)


class Water(Optimize):
    """
        The class for water residues
    """

    def __init__(self, residue, optinstance, routines):
        """
             Initialize the water optimization class
        """
        self.optinstance = optinstance
        self.residue = residue
        self.routines = routines
        self.hbonds = []
        oxatom = residue.getAtom('O')
        if oxatom == None:
            raise PDBInternalError('Unable to find oxygen atom in %s!' % residue)
        oxatom.hdonor = 1
        oxatom.hacceptor = 1
        self.atomlist = [
         oxatom]
        return

    def tryBoth(self, donor, acc, accobj):
        """
           Called when both the donor and acceptor are optimizeable;
           If one is fixed, we only need to try one side.  Otherwise
           first try to satisfy the donor - if that's succesful,
           try to satisfy the acceptor.  An undo may be necessary
           if the donor is satisfied and the acceptor isn't.
        """
        residue = donor.residue
        if donor.residue.fixed:
            if accobj.tryAcceptor(acc, donor):
                return 1
            else:
                return 0

        if acc.residue.fixed:
            if self.tryDonor(donor, acc):
                return 1
            else:
                return 0

        if self.tryDonor(donor, acc):
            if accobj.tryAcceptor(acc, donor):
                self.debug('NET BOND SUCCESSFUL!')
                return 1
            else:
                self.debug('REMOVED NET HBOND')
                if residue.hasAtom('H2'):
                    residue.removeAtom('H2')
                elif residue.hasAtom('H1'):
                    residue.removeAtom('H1')
                return 0

        else:
            return 0

    def tryAcceptor(self, acc, donor):
        """
           The main driver for adding an LP to an optimizeable
           residue.
        """
        residue = acc.residue
        if not donor.hdonor:
            return 0
        if residue.hasAtom('LP2'):
            return 0
        if residue.hasAtom('LP1'):
            newname = 'LP2'
        else:
            newname = 'LP1'
        self.debug('Working on %s %s (acceptor) to %s %s (donor)' % (
         acc.residue, acc.name, donor.residue, donor.name))
        if len(acc.bonds) == 0:
            if self.isHbond(donor, acc):
                bestdist = distance(acc.getCoords(), donor.getCoords())
                for donorh in donor.bonds:
                    dist = distance(acc.getCoords(), donorh.getCoords())
                    if dist < bestdist:
                        bestdist = dist

                self.makeAtomWithNoBonds(acc, donorh, newname)
                self.debug('Added %s to %s' % (newname, acc.residue))
                return 1
            else:
                return 0

        else:
            if len(acc.bonds) == 1:
                self.debug('Trying to add %s to %s with one bond' % (newname, acc.residue))
                self.makeWaterWithOneBond(acc, newname)
                newatom = acc.residue.getAtom(newname)
                return self.trySingleAlcoholicLP(acc, donor, newatom)
            if len(acc.bonds) == 2:
                self.debug('Trying to add %s to %s with two bonds' % (newname, acc.residue))
                loc1, loc2 = self.getPositionsWithTwoBonds(acc)
                return self.tryPositionsWithTwoBondsLP(acc, donor, newname, loc1, loc2)
            if len(acc.bonds) == 3:
                self.debug('Trying to add %s to %s with three bonds' % (newname, acc.residue))
                loc = self.getPositionWithThreeBonds(acc)
                return self.tryPositionsWithThreeBondsLP(acc, donor, newname, loc)

    def tryDonor(self, donor, acc):
        """
           The main driver for adding a hydrogen to an
           optimizeable residue.
        """
        residue = self.residue
        if not acc.hacceptor:
            return 0
        if residue.hasAtom('H2'):
            return 0
        if residue.hasAtom('H1'):
            newname = 'H2'
        else:
            newname = 'H1'
        self.debug('Working on %s %s (donor) to %s %s (acceptor)' % (
         donor.residue, donor.name, acc.residue, acc.name))
        if len(donor.bonds) == 0:
            self.makeAtomWithNoBonds(donor, acc, newname)
            if self.isHbond(donor, acc):
                return 1
            self.routines.cells.removeCell(residue.getAtom(newname))
            residue.removeAtom(newname)
            return 0
        if len(donor.bonds) == 1:
            self.makeWaterWithOneBond(donor, newname)
            newatom = donor.residue.getAtom(newname)
            return self.trySingleAlcoholicH(donor, acc, newatom)
        if len(donor.bonds) == 2:
            loc1, loc2 = self.getPositionsWithTwoBonds(donor)
            return self.tryPositionsWithTwoBondsH(donor, acc, newname, loc1, loc2)
        if len(donor.bonds) == 3:
            loc = self.getPositionWithThreeBonds(donor)
            return self.tryPositionsWithThreeBondsH(donor, acc, newname, loc)

    def finalize(self):
        """
            Finalize a water residue.  Try to minimize
            conflict with nearby atoms by building away
            from them.  Called when LPs are still present
            so as to account for their bonds.
        """
        residue = self.residue
        if residue.fixed:
            self.debug('Residue %s already fixed' % residue)
            return
        else:
            if residue.hasAtom('H2'):
                self.debug('Residue %s already has H2' % residue)
                return
            atom = residue.getAtom('O')
            if not residue.hasAtom('H1'):
                addname = 'H1'
            else:
                addname = 'H2'
            self.debug('Finalizing %s by adding %s (%i current O bonds)' % (residue, addname, len(atom.bonds)))
            if len(atom.bonds) == 0:
                newcoords = []
                closeatom = self.routines.getClosestAtom(atom)
                if closeatom != None:
                    vec = subtract(atom.getCoords(), closeatom.getCoords())
                    dist = distance(atom.getCoords(), closeatom.getCoords())
                    for i in range(3):
                        newcoords.append(vec[i] / dist + atom.getCoords()[i])

                else:
                    newcoords = add(atom.getCoords(), [1.0, 0.0, 0.0])
                residue.createAtom(addname, newcoords)
                self.routines.cells.addCell(residue.getAtom(addname))
                self.finalize()
            elif len(atom.bonds) == 1:
                pivot = atom.bonds[0]
                bestdist = 0.0
                bestcoords = []
                self.makeWaterWithOneBond(atom, addname)
                newatom = residue.getAtom(addname)
                self.routines.cells.addCell(newatom)
                for i in range(18):
                    residue.rotateTetrahedral(pivot, atom, 20.0)
                    nearatom = self.routines.getClosestAtom(newatom)
                    if nearatom == None:
                        continue
                    dist = distance(nearatom.getCoords(), newatom.getCoords())
                    if dist > bestdist:
                        bestdist = dist
                        bestcoords = newatom.getCoords()

                if bestcoords != []:
                    newatom.x = bestcoords[0]
                    newatom.y = bestcoords[1]
                    newatom.z = bestcoords[2]
                if addname == 'H1':
                    self.finalize()
                residue.fixed = 1
            elif len(atom.bonds) == 2:
                loc1, loc2 = self.getPositionsWithTwoBonds(atom)
                residue.createAtom(addname, loc1)
                newatom = residue.getAtom(addname)
                self.routines.cells.addCell(newatom)
                nearatom = self.routines.getClosestAtom(newatom)
                if nearatom != None:
                    dist1 = distance(newatom.getCoords(), nearatom.getCoords())
                    self.routines.cells.removeCell(atom)
                    newatom.x = loc2[0]
                    newatom.y = loc2[1]
                    newatom.z = loc2[2]
                    self.routines.cells.addCell(atom)
                    nearatom = self.routines.getClosestAtom(newatom)
                    if nearatom != None:
                        if distance(newatom.getCoords(), nearatom.getCoords()) < dist1:
                            self.routines.cells.removeCell(atom)
                            newatom.x = loc1[0]
                            newatom.y = loc1[1]
                            newatom.z = loc1[2]
                            self.routines.cells.addCell(atom)
                if addname == 'H1':
                    self.finalize()
            elif len(atom.bonds) == 3:
                loc = self.getPositionWithThreeBonds(atom)
                residue.createAtom(addname, loc)
                self.routines.cells.addCell(residue.getAtom(addname))
            return

    def complete(self):
        """
            Complete the water optimization class
        """
        self.finalize()
        residue = self.residue
        atomlist = []
        for atom in residue.getAtoms():
            atomlist.append(atom)

        for atom in atomlist:
            if atom.name.startswith('LP'):
                residue.removeAtom(atom.name)


class Carboxylic(Optimize):
    """
        The class for carboxylic residues
    """

    def __init__(self, residue, optinstance, routines):
        """
            Initialize a case where the lone hydrogen atom
            can have four different orientations.  Works similar
            to initializeFlip by preadding the necessary atoms.

            This also takes into account that the carboxyl group
            has different bond lengths for the two C-O bonds -
            this is probably due to one bond being assigned
            as a C=O.  As a result hydrogens are only added to
            the C-O (longer) bond.
            
            Parameters
                residue:  The residue to flip (residue)
                dihedral: The angle to flip about
                hname:    The name of one of the hydrogens to add
            Returns
                optlist:  A list of optimizeable donors and
                          acceptors in the residue (list)
        """
        self.optinstance = optinstance
        self.residue = residue
        self.routines = routines
        self.atomlist = []
        self.hbonds = []
        self.hlist = []
        hname2 = ''
        hname1 = ''
        for name in optinstance.map.keys():
            if name.endswith('2'):
                hname2 = name
            else:
                hname1 = name

        bondatom1 = residue.getAtom(optinstance.map[hname1].bond)
        bondatom2 = residue.getAtom(optinstance.map[hname2].bond)
        longflag = 0
        for pivotatom in bondatom1.bonds:
            if not pivotatom.isHydrogen():
                break

        d1 = distance(pivotatom.getCoords(), bondatom1.getCoords())
        d2 = distance(pivotatom.getCoords(), bondatom2.getCoords())
        order = [
         hname1, hname2]
        if d2 > d1 and abs(d1 - d2) > 0.05:
            longflag = 1
            order = [hname2, hname1]
        else:
            if d1 > d2 and abs(d1 - d2) > 0.05:
                longflag = 1
                order = [hname1, hname2]
            for hname in order:
                bondatom = residue.getAtom(optinstance.map[hname].bond)
                for di in residue.reference.dihedrals:
                    if di.endswith(hname):
                        break

                anglenum = residue.reference.dihedrals.index(di)
                if anglenum == -1:
                    raise PDBInternalError('Unable to find Carboxylic dihedral angle!')
                if residue.dihedrals[anglenum] == None:
                    self.atomlist.append(bondatom)
                    continue
                newangle = 180.0 + residue.dihedrals[anglenum]
                self.routines.setDihedralAngle(residue, anglenum, newangle)
                hatom = residue.getAtom(hname)
                newcoords = hatom.getCoords()
                newangle = 180.0 + residue.dihedrals[anglenum]
                self.routines.setDihedralAngle(residue, anglenum, newangle)
                residue.renameAtom(hname, '%s1' % hname)
                newname = '%s2' % hname
                residue.createAtom(newname, newcoords)
                newatom = residue.getAtom(newname)
                self.routines.cells.addCell(newatom)
                newatom.refdistance = hatom.refdistance
                if bondatom not in newatom.bonds:
                    newatom.bonds.append(bondatom)
                if newatom not in bondatom.bonds:
                    bondatom.bonds.append(newatom)
                self.atomlist.append(bondatom)
                self.hlist.append(residue.getAtom('%s1' % hname))
                self.hlist.append(residue.getAtom('%s2' % hname))
                if longflag:
                    break

        residue.setDonorsAndAcceptors()
        return

    def tryBoth(self, donor, acc, accobj):
        """
           Called when both the donor and acceptor are optimizeable;
           If one is fixed, we only need to try one side.  Otherwise
           first try to satisfy the donor - if that's succesful,
           try to satisfy the acceptor.  An undo may be necessary
           if the donor is satisfied and the acceptor isn't.
        """
        if donor.residue.fixed:
            if accobj.tryAcceptor(acc, donor):
                return 1
            else:
                return 0

        if acc.residue.fixed:
            if self.tryDonor(donor, acc):
                return 1
            else:
                return 0

        self.debug('Working on %s %s (donor) to %s %s (acceptor)' % (
         donor.residue, donor.name, acc.residue, acc.name))
        if self.isHbond(donor, acc):
            if accobj.tryAcceptor(acc, donor):
                self.fix(donor, acc)
                self.debug('NET BOND SUCCESSFUL!')
                return 1
            else:
                return 0

    def isCarboxylicHbond(self, donor, acc):
        """
            Determine whether this donor acceptor pair is a
            hydrogen bond
        """
        for donorhatom in donor.bonds:
            if not donorhatom.isHydrogen():
                continue
            dist = distance(donorhatom.getCoords(), acc.getCoords())
            if dist > DIST_CUTOFF:
                continue
            angle = self.getHbondangle(acc, donor, donorhatom)
            if angle <= ANGLE_CUTOFF:
                self.debug('Found HBOND! %.4f %.4f' % (dist, angle))
                return 1

        return 0

    def tryAcceptor(self, acc, donor):
        """
           The main driver for adding an LP to an optimizeable
           residue.
        """
        residue = acc.residue
        if not donor.hdonor:
            return 0
        else:
            self.debug('Working on %s %s (acceptor) to %s %s (donor)' % (
             acc.residue, acc.name, donor.residue, donor.name))
            if self.isCarboxylicHbond(donor, acc):
                hyds = []
                dist = None
                donorhatom = None
                for hatom in self.hlist:
                    if hatom.isHydrogen():
                        hyds.append(hatom)

                if len(hyds) < 2:
                    return 1
                dist = distance(hyds[0].getCoords(), donor.getCoords())
                dist2 = distance(hyds[1].getCoords(), donor.getCoords())
                if dist < dist2:
                    self.hlist.remove(hyds[0])
                    self.routines.cells.removeCell(hyds[0])
                    residue.removeAtom(hyds[0].name)
                    donorhatom = residue.getAtom(hyds[1].name)
                elif hyds[1] in self.hlist:
                    self.hlist.remove(hyds[1])
                    self.routines.cells.removeCell(hyds[1])
                    residue.removeAtom(hyds[1].name)
                    if residue.hasAtom(hyds[0].name):
                        donorhatom = residue.getAtom(hyds[0].name)
                    elif len(self.hlist) != 0 and residue.hasAtom(self.hlist[0].name):
                        donorhatom = residue.getAtom(self.hlist[0].name)
                if len(self.hlist) == 1:
                    if donorhatom != None:
                        self.rename(donorhatom)
                    residue.fixed = 1
                return 1
            return 0
            return

    def tryDonor(self, donor, acc):
        """
           The main driver for adding a hydrogen to an
           optimizeable residue.
        """
        if not acc.hacceptor:
            return 0
        else:
            if self.isHbond(donor, acc):
                self.fix(donor, acc)
                return 1
            return 0

    def fix(self, donor, acc):
        """
            Fix the carboxylic residue.
        """
        self.debug('Fixing residue %s due to %s' % (donor.residue, donor.name))
        residue = donor.residue
        for donorhatom in donor.bonds:
            if donorhatom.isHydrogen() and self.getHbondangle(acc, donor, donorhatom) <= ANGLE_CUTOFF:
                break

        hydrogens = self.hlist[:]
        for atom in hydrogens:
            if atom != donorhatom:
                self.routines.cells.removeCell(atom)
                self.hlist.remove(atom)
                residue.removeAtom(atom.name)

        self.rename(donorhatom)
        residue.fixed = 1

    def finalize(self):
        """
            Finalize a protontated residue.  Try to minimize
            conflict with nearby atoms.
        """
        hydrogens = []
        bestatom = None
        residue = self.residue
        if residue.fixed:
            return
        else:
            bestenergy = 999.99
            for hydatom in self.hlist:
                energy = 0
                bondedatom = hydatom.bonds[0]
                closeatoms = self.routines.cells.getNearCells(bondedatom)
                for catom in closeatoms:
                    energy += self.getPairEnergy(bondedatom, catom) + self.getPairEnergy(catom, bondedatom)

                if energy < bestenergy:
                    bestenergy = energy
                    bestatom = hydatom

            for hydatom in self.hlist:
                hydrogens.append(hydatom)

            for hydatom in hydrogens:
                if bestatom != hydatom:
                    self.hlist.remove(hydatom)
                    residue.removeAtom(hydatom.name)

            if bestatom != None and len(bestatom.name) == 4:
                self.rename(bestatom)
            residue.fixed = 1
            return

    def rename(self, hydatom):
        """
             Rename the optimized atoms appropriately.  This is done
             since the forcefields tend to require that the hydrogen is
             linked to a specific oxygen, and this atom may have different
             parameter values.

             Parameters
                 hydatom:  The hydrogen atom that was added. (atom)
        """
        residue = self.residue
        optinstance = self.optinstance
        if hydatom.name not in residue.map.keys():
            return
        if len(hydatom.name) == 4:
            hname = hydatom.name[:-1]
            residue.renameAtom(hydatom.name, hname)
        if len(self.atomlist) == 2:
            if hydatom.name.endswith('1'):
                residue.renameAtom(hydatom.name, '%s2' % hydatom.name[:-1])
                bondname0 = self.atomlist[0].name
                bondname1 = self.atomlist[1].name
                tempname = 'FLIP'
                residue.renameAtom(self.atomlist[0].name, tempname)
                residue.renameAtom(self.atomlist[1].name, bondname0)
                residue.renameAtom(tempname, bondname1)
            elif hydatom.name.endswith('OXT'):
                residue.renameAtom(hydatom.name, 'HO')
                bondname0 = self.atomlist[0].name
                bondname1 = self.atomlist[1].name
                tempname = 'FLIP'
                residue.renameAtom(self.atomlist[0].name, tempname)
                residue.renameAtom(self.atomlist[1].name, bondname0)
                residue.renameAtom(tempname, bondname1)
        elif len(self.atomlist) == 1:
            hnames = [
             hname[:-1] + '1', hname[:-1] + '2']
            for hn in hnames:
                bondatom = residue.getAtom(optinstance.map[hn].bond)
                if bondatom.name != self.atomlist[0].name:
                    self.atomlist.append(bondatom)

            if hydatom.name.endswith('1'):
                if hydatom.name[:-1] + '2' in residue.map.keys():
                    residue.removeAtom('%s2' % hydatom.name[:-1])
                residue.renameAtom(hydatom.name, '%s2' % hydatom.name[:-1])
                bondname0 = self.atomlist[0].name
                bondname1 = self.atomlist[1].name
                tempname = 'FLIP'
                residue.renameAtom(self.atomlist[0].name, tempname)
                residue.renameAtom(self.atomlist[1].name, bondname0)
                residue.renameAtom(tempname, bondname1)
            elif hydatom.name.endswith('OXT'):
                residue.renameAtom(hydatom.name, 'HO')
                bondname0 = self.atomlist[0].name
                bondname1 = self.atomlist[1].name
                tempname = 'FLIP'
                residue.renameAtom(self.atomlist[0].name, tempname)
                residue.renameAtom(self.atomlist[1].name, bondname0)
                residue.renameAtom(tempname, bondname1)

    def complete(self):
        """
            If not already fixed, finalize
        """
        if len(self.hlist) == 2 and self.residue.fixed == 1:
            self.residue.fixed = 0
        if not self.residue.fixed:
            self.finalize()


class Generic(Optimize):
    """
        Generic optimization class
    """

    def __init__(self, residue, optinstance, routines):
        """
             Initialize the generic optimization class
        """
        self.optinstance = optinstance
        self.residue = residue
        self.routines = routines
        self.hbonds = []
        self.atomlist = []

    def finalize(self):
        pass

    def complete(self):
        """
            If not already fixed, finalize
        """
        if not self.residue.fixed:
            self.finalize()


class hydrogenRoutines():
    """
        The main routines for hydrogen optimization.  This could
        potentially be extended from the routines object...
    """

    def __init__(self, routines):
        """
            Parse the XML hydrogenFile and store the data in a map
        """
        self.routines = routines
        self.protein = routines.protein
        self.optlist = []
        self.atomlist = []
        self.resmap = {}
        self.hydrodefs = []
        handler = HydrogenHandler()
        sax.make_parser()
        defpath = getDatFile(HYDPATH)
        if defpath == '':
            raise PDBInternalError('Could not find %s!' % HYDPATH)
        hydrogenFile = open(defpath)
        sax.parseString(hydrogenFile.read(), handler)
        hydrogenFile.close()
        self.map = handler.map

    def debug(self, text):
        """
            Print text to stdout for debugging purposes.

            Parameters
                text:  The text to output (string)
        """
        if HDEBUG:
            print text

    def switchstate(self, states, amb, stateID):
        """
            Switch a residue to a new state by first removing all
            hydrogens.

            Parameters
                states: The list of states (list)
                amb   : The amibiguity to switch (tuple)
                stateID    : The state id to switch to (int)
        """
        if states == 'pKa':
            return self.pKa_switchstate(amb, stateID)
        else:
            if stateID > len(states):
                raise PDBInternalError('Invalid State ID!')
            residue = getattr(amb, 'residue')
            hdef = getattr(amb, 'hdef')
            for conf in hdef.conformations:
                hname = conf.hname
                boundname = conf.boundatom
                if residue.getAtom(hname) != None:
                    print 'Removing', residue.name, residue.resSeq, hname
                    residue.removeAtom(hname)
                residue.getAtom(boundname).hacceptor = 1
                residue.getAtom(boundname).hdonor = 0

            name = residue.get('name')
            defresidue = self.routines.aadef.getResidue(name)
            residue.updateIntraBonds(defresidue)
            state = states[stateID]
            for conf in state:
                refcoords = []
                defcoords = []
                defatomcoords = []
                if conf == ():
                    continue
                hname = conf.hname
                for atom in conf.atoms:
                    atomname = atom.get('name')
                    resatom = residue.getAtom(atomname)
                    if atomname == hname:
                        defatomcoords = atom.getCoords()
                    elif resatom != None:
                        refcoords.append(resatom.getCoords())
                        defcoords.append(atom.getCoords())
                    else:
                        raise PDBInternalError('Could not find necessary atom!')

                newcoords = findCoordinates(3, refcoords, defcoords, defatomcoords)
                boundname = conf.boundatom
                residue.createAtom(hname, newcoords, 'ATOM')
                residue.addDebumpAtom(residue.getAtom(hname))
                residue.getAtom(boundname).addIntraBond(hname)
                residue.getAtom(boundname).hacceptor = 0
                residue.getAtom(boundname).hdonor = 1
                residue.getAtom(hname).sybylType = 'H'
                residue.getAtom(hname).formalcharge = 0.0
                residue.getAtom(hname).titratableH = True
                residue.getAtom(hname).addIntraBond(boundname)

            return

    def pKa_switchstate(self, amb, stateID):
        """
            Switch a residue to a new state by first removing all
            hydrogens. this routine is used in pKa calculations only!

            Parameters
                amb   : The amibiguity to switch (tuple)
                stateID    : The state id to switch to (list)

        """
        titrationdict = {'ASH1c': '1', 'ASH1t': '2', 'ASH2c': '3', 'ASH2t': '4', 'ASP': '0', 'GLH1c': '1', 
           'GLH1t': '2', 'GLH2c': '3', 'GLH2t': '4', 'GLU': '0', 'ARG0': '1+2+3+4', 
           'ARG': '1+2+3+4+5', 'LYS': '1', 
           'LYS0': '0', 'TYR': '1', 
           'TYR-': '0', 'HSD': '1', 
           'HSE': '2', 'HSP': '1+2', 'H3': '1', 
           'H2': '2', 'H3+H2': '1+2', 'CTR01c': '1', 
           'CTR01t': '2', 'CTR02c': '3', 'CTR02t': '4', 'CTR-': '0'}
        stateID = titrationdict[stateID]
        stateID = stateID.split('+')
        new_stateID = []
        for i in stateID:
            new_stateID.append(int(i))

        residue = getattr(amb, 'residue')
        hdef = getattr(amb, 'hdef')
        for conf in hdef.conformations:
            hname = conf.hname
            boundname = conf.boundatom
            if residue.getAtom(hname) != None:
                residue.removeAtom(hname)
            residue.getAtom(boundname).hacceptor = 1
            residue.getAtom(boundname).hdonor = 0

        for stateID in new_stateID:
            if stateID == 0:
                continue
            conf = hdef.conformations[(stateID - 1)]
            refcoords = []
            defcoords = []
            defatomcoords = []
            if conf == ():
                continue
            hname = conf.hname
            for atom in conf.atoms:
                if residue.isNterm and residue.name == 'PRO':
                    if atom.name == 'H':
                        atom.name = 'CD'
                        atom.x = 1.874
                        atom.y = 0.862
                        atom.z = 1.306

            if not Routines.rebuildTetrahedral(residue, hname):
                for atom in conf.atoms:
                    atomname = atom.get('name')
                    resatom = residue.getAtom(atomname)
                    if atomname == hname:
                        defatomcoords = atom.getCoords()
                    elif resatom != None:
                        refcoords.append(resatom.getCoords())
                        defcoords.append(atom.getCoords())
                    else:
                        raise PDBInternalError('Could not find necessary atom!')

                newcoords = findCoordinates(3, refcoords, defcoords, defatomcoords)
                residue.createAtom(hname, newcoords)
            boundname = conf.boundatom
            residue.getAtom(boundname).hacceptor = 0
            residue.getAtom(boundname).hdonor = 1
            residue.getAtom(hname).sybylType = 'H'
            residue.getAtom(hname).formalcharge = 0.0
            residue.getAtom(hname).titratableH = True

        if residue.isNterm and residue.name == 'PRO':
            for atom in residue.getAtoms():
                if atom.name == 'H':
                    residue.removeAtom('H')

        residue.update_terminus_status()
        return

    def cleanup(self):
        """
            If there are any extra carboxlyic *1 atoms, delete them.

            This may occur when no optimization is chosen
        """
        for residue in self.routines.protein.getResidues():
            if not isinstance(residue, Amino):
                continue
            if residue.name == 'GLH' or 'GLH' in residue.patches:
                if residue.hasAtom('HE1') and residue.hasAtom('HE2'):
                    residue.removeAtom('HE1')
            elif residue.name == 'ASH' or 'ASH' in residue.patches:
                if residue.hasAtom('HD1') and residue.hasAtom('HD2'):
                    residue.removeAtom('HD1')

    def isOptimizeable(self, residue):
        """
            Check to see if the given residue is optimizeable
            There are three ways to identify a residue:

            1.  By name (i.e. HIS)
            2.  By reference name - a PDB file HSP has
                a HIS reference name
            3.  By patch - applied by PropKa, terminal selection

            Parameters
                residue:  The residue in question (Residue)
            Returns
                optinstance: None if not optimizeable, otherwise
                             the OptimizationHolder instance that
                             corresponds to the residue.
        """
        optinstance = None
        if not (isinstance(residue, Amino) or isinstance(residue, WAT)):
            return optinstance
        else:
            if residue.name in self.map:
                optinstance = self.map[residue.name]
            elif residue.reference.name in self.map:
                optinstance = self.map[residue.reference.name]
            else:
                for patch in residue.patches:
                    if patch in self.map:
                        optinstance = self.map[patch]
                        break

            if optinstance != None:
                if optinstance.opttype == 'Alcoholic':
                    atomname = optinstance.map.keys()[0]
                    if not residue.reference.hasAtom(atomname):
                        optinstance = None
            return optinstance

    def setOptimizeableHydrogens(self):
        """
            Set any hydrogen listed in HYDROGENS.xml that
            is optimizeable.  Used BEFORE hydrogen optimization
            to label atoms so that they won't be debumped - i.e.
            if SER HG is too close to another atom, don't debump
            but wait for optimization.  This function should not
            be used if full optimization is not taking place.
        """
        for residue in self.protein.getResidues():
            optinstance = self.isOptimizeable(residue)
            if optinstance == None:
                continue
            for atom in residue.getAtoms():
                if atom.name in optinstance.map:
                    atom.optimizeable = 1

        return

    def initializeFullOptimization(self):
        """
            Initialize the full optimization.  Detects all
            optimizeable donors and acceptors and sets the internal
            optlist.
        """
        self.routines.write('Initializing full optimization...\n')
        self.routines.cells = Cells(5)
        self.routines.cells.assignCells(self.protein)
        self.routines.calculateDihedralAngles()
        self.routines.setDonorsAndAcceptors()
        self.routines.updateInternalBonds()
        self.routines.setReferenceDistance()
        self.optlist = []
        self.atomlist = []
        for residue in self.protein.getResidues():
            optinstance = self.isOptimizeable(residue)
            if isinstance(residue, Amino):
                if False in residue.stateboolean.values():
                    residue.fixed = 1
                else:
                    residue.fixed = 0
            if optinstance == None:
                continue
            type = optinstance.opttype
            command = '%s(residue, optinstance, self.routines)' % type
            if residue.fixed == 1:
                pass
            else:
                myobj = eval(command)
                self.atomlist += myobj.atomlist
                self.optlist.append(myobj)
                self.resmap[residue] = myobj

        self.routines.write('Done.\n')
        return

    def initializeWaterOptimization(self):
        """
            Initialize optimization for waters only.  Detects all
            optimizeable donors and acceptors and sets the internal
            optlist.
        """
        self.routines.write('Initializing water bonding optimization...\n')
        self.routines.cells = Cells(5)
        self.routines.cells.assignCells(self.protein)
        self.routines.calculateDihedralAngles()
        self.routines.setDonorsAndAcceptors()
        self.routines.updateInternalBonds()
        self.routines.setReferenceDistance()
        self.optlist = []
        for residue in self.protein.getResidues():
            optinstance = self.isOptimizeable(residue)
            if optinstance == None:
                continue
            type = optinstance.opttype
            if type == 'Water':
                command = '%s(residue, optinstance, self.routines)' % type
                myobj = eval(command)
                self.atomlist += myobj.atomlist
                self.optlist.append(myobj)
                self.resmap[residue] = myobj

        self.routines.write('Done.\n')
        return

    def optimizeHydrogens(self):
        """
            The main driver for the optimization.  Should be
            called only after the optlist has been initialized.
        """
        self.routines.write('Optimization progress:\n')
        optlist = self.optlist
        resmap = {}
        connectivity = {}
        if len(optlist) == 0:
            return
        self.routines.write('  Detecting potential hydrogen bonds:\n')
        self.routines.write('0% |                    | 100%\n', 1)
        self.routines.write('    ', 1)
        progress = 0.0
        increment = 1.0 / len(optlist)
        for obj in optlist:
            connectivity[obj] = []
            for atom in obj.atomlist:
                closeatoms = self.routines.cells.getNearCells(atom)
                for closeatom in closeatoms:
                    if atom.residue == closeatom.residue:
                        continue
                    if not (closeatom.hacceptor or closeatom.hdonor):
                        continue
                    if atom.hdonor and not atom.hacceptor and not closeatom.hacceptor:
                        continue
                    if atom.hacceptor and not atom.hdonor and not closeatom.hdonor:
                        continue
                    dist = distance(atom.getCoords(), closeatom.getCoords())
                    if dist < 4.3:
                        residue = atom.residue
                        hbond = PotentialBond(atom, closeatom, dist)
                        obj.hbonds.append(hbond)
                        if closeatom in self.atomlist:
                            closeobj = self.resmap[closeatom.residue]
                            if closeobj not in connectivity[obj]:
                                connectivity[obj].append(closeobj)

            progress += increment
            while progress >= 0.0499:
                self.routines.write('*')
                progress -= 0.05

        if len(optlist) > 0:
            self.routines.write('\n')
        for obj in optlist:
            if len(obj.hbonds) == 0:
                if obj.residue.fixed:
                    continue
                self.debug('%s has no nearby partners - fixing.' % obj.residue)
                obj.finalize()

        networks = []
        seen = []
        for obj in optlist:
            if obj.residue.fixed:
                continue
            if obj in seen:
                continue
            network = analyzeConnectivity(connectivity, obj)
            for obj in network:
                if obj not in seen:
                    seen.append(obj)

            networks.append(network)

        if len(networks) > 0:
            self.routines.write('  Optimizing hydrogen bonds:\n')
            self.routines.write('0% |                    | 100%\n', 1)
            self.routines.write('    ', 1)
            progress = 0.0
            increment = 1.0 / len(networks)
        for network in networks:
            txt = ''
            for obj in network:
                txt += '%s, ' % obj

            self.debug('\nStarting network %s' % txt[:-2])
            self.debug('* Optimizeable to backbone *')
            hbondmap = {}
            for obj in network:
                for hbond in obj.hbonds:
                    if hbond.atom2 not in self.atomlist:
                        hbondmap[hbond] = hbond.dist

            hbondlist = sortDictByValue(hbondmap)
            hbondlist.reverse()
            for hbond in hbondlist:
                atom = hbond.atom1
                atom2 = hbond.atom2
                obj = self.resmap[atom.residue]
                if atom.residue.fixed:
                    continue
                if atom.hdonor:
                    obj.tryDonor(atom, atom2)
                if atom.hacceptor:
                    obj.tryAcceptor(atom, atom2)

            self.debug('\n* Optimizeable to optimizeable *')
            hbondmap = {}
            seenlist = []
            for obj in network:
                for hbond in obj.hbonds:
                    if hbond.atom2 in self.atomlist and not (isinstance(hbond.atom1.residue, WAT) and isinstance(hbond.atom2.residue, WAT)):
                        if (
                         hbond.atom2, hbond.atom1) not in seenlist:
                            hbondmap[hbond] = hbond.dist
                            seenlist.append((hbond.atom1, hbond.atom2))

            hbondlist = sortDictByValue(hbondmap)
            hbondlist.reverse()
            for hbond in hbondlist:
                atom = hbond.atom1
                atom2 = hbond.atom2
                obj1 = self.resmap[atom.residue]
                obj2 = self.resmap[atom2.residue]
                if not atom.residue.hasAtom(atom.name):
                    continue
                if not atom2.residue.hasAtom(atom2.name):
                    continue
                res = 0
                if atom.hdonor and atom2.hacceptor:
                    res = obj1.tryBoth(atom, atom2, obj2)
                if atom.hacceptor and atom2.hdonor and res == 0:
                    obj2.tryBoth(atom2, atom, obj1)

            self.debug('\n* Water to Water *')
            hbondmap = {}
            seenlist = []
            for obj in network:
                for hbond in obj.hbonds:
                    residue = hbond.atom1.residue
                    if isinstance(residue, WAT) and isinstance(hbond.atom2.residue, WAT):
                        if (
                         hbond.atom2, hbond.atom1) not in seenlist:
                            hbondmap[hbond] = hbond.dist
                            seenlist.append((hbond.atom1, hbond.atom2))

            hbondlist = sortDictByValue(hbondmap)
            hbondlist.reverse()
            for hbond in hbondlist:
                atom = hbond.atom1
                atom2 = hbond.atom2
                obj1 = self.resmap[atom.residue]
                obj2 = self.resmap[atom2.residue]
                res = 0
                if atom.hdonor and atom2.hacceptor:
                    res = obj1.tryBoth(atom, atom2, obj2)
                if atom.hacceptor and atom2.hdonor and res == 0:
                    obj2.tryBoth(atom2, atom, obj1)

            for obj in network:
                obj.complete()

            progress += 100.0 * increment
            while progress >= 5.0:
                self.routines.write('*')
                progress -= 5.0

        if len(networks) > 0:
            self.routines.write('\n')

    def parseHydrogen(self, res):
        """
            Parse a list of lines in order to make a hydrogen
            definition

            Parameters
                lines:  The lines to parse (list)
            Returns
                mydef:  The hydrogen definition object (HydrogenDefinition)

        This is the current definition:  Name Ttyp  A R # Stdconf   HT Chi OPTm
        """
        toppath = getDatFile(TOPOLOGYPATH)
        if toppath == '':
            raise PDBInternalError('Could not find %s!' % TOPOLOGYPATH)
        topfile = open(toppath)
        top = topology.Topology(topfile)
        topfile.close()
        name = self.map[res].name
        opttype = self.map[res].opttype
        optangle = self.map[res].optangle
        map = self.map[res].map
        mydef = HydrogenDefinition(name, opttype, optangle, map)
        conf = []
        patchmap = []
        refmap = {}
        titrationstatemap = {}
        tautomermap = {}
        conformermap = {}
        atommap = {}
        for res in top.residues:
            refmap[res.name] = res.reference
            for atom in refmap[res.name].atoms:
                atommap[(res.name, atom.name)] = atom

            for titrationstate in res.titrationStates:
                titrationstatemap[titrationstate.name] = titrationstate
                for tautomer in titrationstate.tautomers:
                    tautomermap[tautomer.name] = tautomer
                    for conformer in tautomer.conformers:
                        conformermap[conformer.name] = conformer

        if name == 'CYS':
            reference = refmap['CYS']
            atoms = ['HG']
            refatoms = ['SG', 'CB']
        else:
            if name == 'HIS':
                reference = refmap['HIS']
                atoms = ['HD1', 'HE2']
                for atom in atoms:
                    refatoms = [
                     'ND1', 'CG', 'CE1']

            elif name == 'LYS':
                reference = self.routines.protein.referencemap[name]
                patchmap = self.routines.protein.patchmap['LYN']
                atoms = patchmap.remove
                refatoms = ['HZ1', 'HZ2', 'NZ']
            elif name == 'TYR':
                reference = self.routines.protein.referencemap[name]
                patchmap = self.routines.protein.patchmap['TYM']
                atoms = patchmap.remove
                refatoms = ['OH', 'CZ', 'CE2']
            elif name == 'WAT':
                reference = self.routines.protein.referencemap[name]
                patchmap = self.routines.protein.patchmap['HOH']
                atoms = ['H1', 'H2']
                refatoms = None
            elif name == 'NTR':
                ntrmap = {}
                for tautomer in titrationstatemap['NTER'].tautomers:
                    for conformer in tautomermap[tautomer.name].conformers:
                        for conformeradds in conformermap[conformer.name].conformerAdds:
                            for atom in conformeradds.atoms:
                                ntrmap[atom.name] = atom

                atoms = [
                 'H3', 'H2']
                refatoms = ['CA', 'H', 'N']
            elif name == 'CTR':
                hmap = {}
                nonhmap = {}
                conformernames = []
                for tautomer in titrationstatemap['CTER'].tautomers:
                    for conformer in tautomermap[tautomer.name].conformers:
                        for conformeradds in conformermap[conformer.name].conformerAdds:
                            for atom in conformeradds.atoms:
                                nonhmap[atom.name] = atom

                for tautomer in titrationstatemap['CTER0'].tautomers:
                    for conformer in tautomermap[tautomer.name].conformers:
                        conformernames.append(conformer.name)
                        for conformeradds in conformermap[conformer.name].conformerAdds:
                            for atom in conformeradds.atoms:
                                hmap[(conformer.name, atom.name)] = atom

                atoms = [
                 'HO']
                refatoms = ['O', 'C', 'OXT']
            elif name in ('SER', 'GLN', 'THR', 'ARG', 'ASN'):
                reference = refmap[name]
                if name == 'SER':
                    atoms = [
                     'HG']
                    refatoms = ['OG', 'CB']
                elif name == 'GLN':
                    atoms = [
                     'HE21']
                    refatoms = ['NE2']
                elif name == 'THR':
                    atoms = [
                     'HG1']
                    refatoms = ['OG1', 'CB']
                elif name == 'ARG':
                    atoms = [
                     'HH11', 'HH12', 'HH21', 'HH22', 'HE']
                    for atom in atoms:
                        refatoms = [
                         'NH1', 'NH2', 'CZ']

                elif name == 'ASN':
                    atoms = [
                     'HD21']
                    refatoms = ['ND2']
            elif name == 'ASH':
                hmap = {}
                nonhmap = {}
                conformernames = []
                reference = refmap['ASP']
                for tautomer in titrationstatemap['ASH'].tautomers:
                    for conformer in tautomermap[tautomer.name].conformers:
                        for conformeradds in conformermap[conformer.name].conformerAdds:
                            for atom in conformeradds.atoms:
                                hmap[(conformer.name, atom.name)] = atom
                                conformernames.append(conformer.name)

                atoms = [
                 'HD1', 'HD2']
                refatoms = ['OD1', 'CG', 'OD2']
            elif name == 'GLH':
                hmap = {}
                nonhmap = {}
                conformernames = []
                reference = refmap['GLU']
                for tautomer in titrationstatemap['GLH'].tautomers:
                    for conformer in tautomermap[tautomer.name].conformers:
                        for conformeradds in conformermap[conformer.name].conformerAdds:
                            for atom in conformeradds.atoms:
                                hmap[(conformer.name, atom.name)] = atom
                                conformernames.append(conformer.name)

                atoms = [
                 'HE1', 'HE2']
                refatoms = ['OE1', 'CD', 'OE2']
            else:
                patchmap = self.routines.protein.patchmap[name]
                atoms = patchmap.map.keys()
                atoms.sort()
            if name in ('NTR', ):
                for atom in atoms:
                    hname = atom
                    x = ntrmap[hname].x
                    y = ntrmap[hname].y
                    z = ntrmap[hname].z
                    bondatom = ntrmap[hname].bonds[0]
                    bondlength = 1.0
                    myconf = HydrogenConformation(hname, bondatom, bondlength)
                    atom = DefinitionAtom(hname, x, y, z)
                    myconf.addAtom(atom)
                    for atom in refatoms:
                        if atom == 'N':
                            natom = DefinitionAtom(atom, 1.201, 0.847, 0.0)
                            myconf.addAtom(natom)
                        elif atom == 'CA':
                            caatom = DefinitionAtom(atom, 0.0, 0.0, 0.0)
                            myconf.addAtom(caatom)
                        elif atom == 'H':
                            caatom = DefinitionAtom(atom, 1.201, 1.847, 0.0)
                            myconf.addAtom(caatom)

                    mydef.addConf(myconf)

                conf = []
            elif name in ('CTR', ):
                for conformer in conformernames:
                    for atom in atoms:
                        hname = atom
                        x = hmap[(conformer, hname)].x
                        y = hmap[(conformer, hname)].y
                        z = hmap[(conformer, hname)].z
                        bondatom = hmap[(conformer, hname)].bonds[0]
                        bondlength = 1.0
                        myconf = HydrogenConformation(hname, bondatom, bondlength)
                        atom = DefinitionAtom(hname, x, y, z)
                        myconf.addAtom(atom)
                        for atom in refatoms:
                            if atom == 'C':
                                catom = DefinitionAtom(atom, -1.25, 0.881, 0.0)
                                myconf.addAtom(catom)
                            else:
                                atomname = atom
                                x = nonhmap[atom].x
                                y = nonhmap[atom].y
                                z = nonhmap[atom].z
                                atom = DefinitionAtom(atomname, x, y, z)
                                myconf.addAtom(atom)

                        mydef.addConf(myconf)

                conf = []
            elif name in ('ASH', 'GLH'):
                for conformer in conformernames:
                    for atom in atoms:
                        hname = atom
                        if '1' in conformer and '1' in atom or '2' in conformer and '2' in atom:
                            x = hmap[(conformer, hname)].x
                            y = hmap[(conformer, hname)].y
                            z = hmap[(conformer, hname)].z
                            bondatom = hmap[(conformer, hname)].bonds[0]
                            bondlength = 1.0
                            myconf = HydrogenConformation(hname, bondatom, bondlength)
                            atom = DefinitionAtom(hname, x, y, z)
                            myconf.addAtom(atom)
                            for atom in refatoms:
                                atomname = atom
                                if name == 'ASH':
                                    refresname = 'ASP'
                                elif name == 'GLH':
                                    refresname = 'GLU'
                                x = atommap[(refresname, atom)].x
                                y = atommap[(refresname, atom)].y
                                z = atommap[(refresname, atom)].z
                                atom = DefinitionAtom(atomname, x, y, z)
                                myconf.addAtom(atom)

                            mydef.addConf(myconf)

                conf = []
            else:
                if name in ('WAT', ):
                    pass
                else:
                    for atom in atoms:
                        hname = atom
                        x = atommap[(name, hname)].x
                        y = atommap[(name, hname)].y
                        z = atommap[(name, hname)].z
                        bondatom = atommap[(name, hname)].bonds[0]
                        bondlength = 1.0
                        myconf = HydrogenConformation(hname, bondatom, bondlength)
                        atom = DefinitionAtom(hname, x, y, z)
                        myconf.addAtom(atom)
                        if refatoms != None:
                            if name == 'HIS' and atom.name == 'HE2':
                                refatoms = [
                                 'NE2', 'CE1', 'CD2']
                            if name == 'ARG' and atom.name == 'HE':
                                refatoms = [
                                 'NE', 'CZ', 'NH1']
                            for atom in refatoms:
                                atomname = atom
                                x = atommap[(name, atomname)].x
                                y = atommap[(name, atomname)].y
                                z = atommap[(name, atomname)].z
                                atom = DefinitionAtom(atomname, x, y, z)
                                myconf.addAtom(atom)

                            mydef.addConf(myconf)

                conf = []
        return mydef

    def readHydrogenDefinition(self):
        """
            Read the Hydrogen Definition file

            Returns
                hydrodef:  The hydrogen definition ()
        """
        self.hydrodefs = []
        for m in self.map:
            res = m
            mydef = self.parseHydrogen(res)
            self.hydrodefs.append(mydef)
            res = ''


class OptimizationHolder():
    """
        A holder class for the XML parser.
    """

    def __init__(self):
        """
            Initialize the class.
        """
        self.name = ''
        self.map = {}
        self.opttype = ''
        self.optangle = ''

    def __str__(self):
        """
            A basic string representation for debugging
        """
        text = '%s\n' % self.name
        text += 'Type: %s\n' % self.opttype
        if self.optangle != '':
            text += 'Optimization Angle: %s\n' % self.optangle
        text += 'Atoms: \n'
        for atomname in self.map:
            text += '\t%s\n' % str(self.map[atomname])

        return text


class HydrogenDefinition():
    """
        HydrogenDefinition class

        The HydrogenDefinition class provides information on possible
        ambiguities in amino acid hydrogens.  It is essentially the hydrogen
        definition file in object form.
    """

    def __init__(self, name, opttype, optangle, map):
        """
            Initialize the object with information from the definition file

            Parameters:
                name:          The name of the grouping (string)
                opttype:       The optimization type of the grouping (string)
                optangle:      The optimization angle of the grouping (string)
                map:           The map of Hydrogens.  

                See HYDROGENS.XML for more information
        """
        self.name = name
        self.opttype = opttype
        self.optangle = optangle
        self.map = map
        self.conformations = []

    def __str__(self):
        """
            Used for debugging purposes

            Returns
                output:  The information about this definition (string)
        """
        output = 'Name:                  %s\n' % self.name
        output += 'Opttype:               %s\n' % self.opttype
        output += 'Optangle:              %s\n' % self.optangle
        output += 'map:                   %s\n' % self.map
        output += 'Conformations:\n'
        for conf in self.conformations:
            output += '\n%s' % conf

        output += '*****************************************\n'
        return output

    def addConf(self, conf):
        """
            Add a HydrogenConformation to the list of conformations

            Parameters
                conf:  The conformation to be added (HydrogenConformation)
        """
        self.conformations.append(conf)


class HydrogenConformation():
    """
        HydrogenConformation class

        The HydrogenConformation class contains data about possible
        hydrogen conformations as specified in the hydrogen data file.
    """

    def __init__(self, hname, boundatom, bondlength):
        """
           Initialize the object

           Parameters
               hname      : The hydrogen name (string)
               boundatom  : The atom the hydrogen is bound to (string)
               bondlength : The bond length (float)
        """
        self.hname = hname
        self.boundatom = boundatom
        self.bondlength = bondlength
        self.atoms = []

    def __str__(self):
        """
            Used for debugging purposes

            Returns
                output:  Information about this conformation (string)
        """
        output = 'Hydrogen Name: %s\n' % self.hname
        output += 'Bound Atom:    %s\n' % self.boundatom
        output += 'Bond Length:   %.2f\n' % self.bondlength
        for atom in self.atoms:
            output += '\t%s\n' % atom

        return output

    def addAtom(self, atom):
        """
            Add an atom to the list of atoms

            Parameters
                atom: The atom to be added (DefinitionAtom)
        """
        self.atoms.append(atom)