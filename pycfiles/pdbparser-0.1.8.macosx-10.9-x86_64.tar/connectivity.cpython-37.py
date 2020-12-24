# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Utilities/Connectivity.py
# Compiled at: 2019-02-16 11:53:22
# Size of source mod 2**32: 19110 bytes
"""
This module contains the connectivity classes used to calculate the atoms connectivity such as
bonds, angles, dihedrals, etc.

.. inheritance-diagram:: pdbparser.Utilities.Connectivity
    :parts: 2

"""
from __future__ import print_function
import numpy as np, copy
from pdbparser.log import Logger
from pdbparser import pdbparser
from pdbparser.Utilities.Information import get_coordinates, get_records_database_property_values, get_records_attribute_values
from pdbparser.Utilities.Collection import is_integer

class Connectivity(object):
    __doc__ = '\n    It takes any pdbparser object and calculates the atoms connectivity (bonds, angles, dihedrals).\n    '

    def __init__(self, pdb):
        self.set_pdb(pdb)

    def set_pdb(self, pdb):
        assert isinstance(pdb, pdbparser), Logger.error('pdb must be a pdbparser instance')
        self._Connectivity__pdb = pdb
        self.initialize_variables()

    def initialize_variables(self):
        self._bonds = []
        self._numberOfBonds = 0
        self._angles = []
        self._dihedrals = []
        self._molecules = []

    @property
    def bonds(self):
        return self._bonds

    @property
    def angles(self):
        return self._angles

    @property
    def dihedrals(self):
        return self._dihedrals

    @property
    def numberOfBonds(self):
        return np.sum([len(b) for b in self._bonds])

    @property
    def numberOfAngles(self):
        return len(self._angles)

    @property
    def numberOfDihedrals(self):
        return len(self._dihedrals)

    @property
    def molecules(self):
        return self._molecules

    def calculate_bonds(self, regressive=False, bondingRadii=None, tolerance=0.25, maxNumberOfBonds=4):
        """
        calculate the bonds list of all the atoms.

        :Parameters:
            #. regressive (boolean): If regressive all bonds are counted even those of earlier atoms.
            #. bondingRadii (numpy.array): The distances defining a bond. Must have the same length as indexes.
            #. tolerance (float): The tolerance is defined as the bond maximum stretching
            #. maxNumberOfBonds (integer): Maximum number of bonds allowed per atom
        """
        if not isinstance(regressive, bool):
            raise AssertionError(Logger.error('regressive must be boolean'))
        else:
            if not is_integer(maxNumberOfBonds):
                raise AssertionError(Logger.error('maxNumberOfBonds must be integer'))
            else:
                maxNumberOfBonds = int(float(maxNumberOfBonds))
                assert maxNumberOfBonds > 0, Logger.error('maxNumberOfBonds must be bugger than 0')
                indexes = self._Connectivity__pdb.indexes
                if bondingRadii is None:
                    bondingRadii = np.array(get_records_database_property_values(indexes, self._Connectivity__pdb, 'covalentRadius'))
                coordinates = get_coordinates(indexes, self._Connectivity__pdb)
                self._bonds = []
                if regressive:
                    indexes = range(coordinates.shape[0])
                else:
                    indexes = range(coordinates.shape[0] - 1)
            bc = self._Connectivity__pdb.boundaryConditions
            for idx in indexes:
                if regressive:
                    cRadii = 0.5 * (bondingRadii + bondingRadii[idx]) + tolerance
                    distances = bc.real_distance(coordinates[idx], coordinates)
                    connected = list(np.where(distances <= cRadii)[0])
                    connected.remove(idx)
                else:
                    cRadii = 0.5 * (bondingRadii[idx + 1:] + bondingRadii[idx]) + tolerance
                    distances = bc.real_distance(coordinates[idx], coordinates[idx + 1:])
                    connected = list(np.where(distances <= cRadii)[0] + idx + 1)
                assert len(connected) <= maxNumberOfBonds, Logger.error("record '%s' is found having more than %i bonds with %s " % (str(idx), maxNumberOfBonds, str(connected)))
                self._bonds.append(connected)
                self._numberOfBonds += len(connected)

            regressive or self._bonds.append([])

    def calculate_molecules(self):
        """
        calculate the angles list of all the atoms.

        """

        def build_chain(chains, key):
            chain = [idx for idx in chains[key]]
            chains[key] = []
            for c in chain:
                chain.extend(build_chain(chains, c))

            return chain

        if not self._bonds:
            self.calculate_bonds()
        chains = {}
        for idx in self._Connectivity__pdb.indexes:
            chains[idx] = self._bonds[idx]

        for idx in self._Connectivity__pdb.indexes:
            chains[idx] = build_chain(chains, idx)

        self._molecules = []
        for idx, c in chains.items():
            if len(c):
                mol = [
                 idx]
                mol.extend(c)
                self._molecules.append(sorted(set(mol)))

    def calculate_angles(self):
        """
        calculate the angles list of all the atoms.

        """
        if not self._bonds:
            self.calculate_bonds()
        for atomIdx in self._Connectivity__pdb.indexes:
            firstBonds = copy.copy(self._bonds[atomIdx])
            while firstBonds:
                firstBond = firstBonds.pop(0)
                for secondBond in firstBonds:
                    self._angles.append([firstBond, atomIdx, secondBond])

                secondBonds = copy.copy(self._bonds[firstBond])
                while secondBonds:
                    secondBond = secondBonds.pop(0)
                    self._angles.append([atomIdx, firstBond, secondBond])

        self._numberOfAngles = len(self._angles)

    def calculate_dihedrals(self):
        """
        calculate the dihedrals list of all the atoms.

        """
        if not self._angles:
            self.calculate_angles()
        sortedDihedrals = []
        for angle in self._angles:
            for idx in self._bonds[angle[0]]:
                dihedral = list(set([idx, angle[0], angle[1], angle[2]]))
                if len(dihedral) == 4 and dihedral not in sortedDihedrals:
                    sortedDihedrals.append(dihedral)
                    self._dihedrals.append([idx, angle[0], angle[1], angle[2]])

            for idx in self._bonds[angle[2]]:
                dihedral = list(set([angle[0], angle[1], angle[2], idx]))
                if len(dihedral) == 4 and dihedral not in sortedDihedrals:
                    sortedDihedrals.append(dihedral)
                    self._dihedrals.append([angle[0], angle[1], angle[2], idx])

    def get_bonds(self, key=None):
        """
        get bonds lists using key attribute to match with the pdb attributes.

        :Parameters:
            #. key (str): any pdbparser.records attribute.

        :Returns:
            #. connectRecord (list): The first records in the bonds.
            #. connectedTo (list): List of lists where every item list is the atoms bonded to the connectRecords item of the same index in list.
        """
        if not self._bonds:
            self.calculate_bonds()
        elif key is None:
            connectRecord = self._Connectivity__pdb.indexes
            connectedTo = self._bonds
        else:
            connectRecord = get_records_attribute_values(self._Connectivity__pdb.indexes, self._Connectivity__pdb, key)
            connectedTo = [get_records_attribute_values(item, self._Connectivity__pdb, key) for item in self._bonds]
        return (
         connectRecord, connectedTo)

    def get_angles(self, key=None):
        """
        get angles list using key attribute to match with the pdb attributes.

        :Parameters:
            #. key (str): any pdbparser.records attribute.

        :Returns:
            #. angles (list): The list of bonds.
        """
        if not self._bonds:
            self.calculate_angles()
        elif key is None:
            angles = self._angles
        else:
            angles = [get_records_attribute_values(item, self._Connectivity__pdb, key) for item in self._angles]
        return angles

    def get_dihedrals(self, key=None):
        """
        get dihedrals list using key attribute to match with the pdb attributes.

        :Parameters:
            #. key (str): any pdbparser.records attribute.

        :Returns:
            #. dihedrals (list): The list of dihedrals.
        """
        if not self._dihedrals:
            self.calculate_dihedrals()
        elif key is None:
            dihedrals = self._dihedrals
        else:
            dihedrals = [get_records_attribute_values(item, self._Connectivity__pdb, key) for item in self._dihedrals]
        return dihedrals

    def export_atoms(self, filePath, indexesOffset=1, format='NAMD_PSF', closeFile=True):
        """
        Exports atoms to ascii file.

        :Parameters:
            #. filePath (path): the file path.
            #. indexesOffset (int): atoms indexing starts from zero. this adds an offset
            #. format (str): The format of exportation. Exisiting formats are: NAMD_PSF,
        """
        try:
            fd = open(filePath, 'w')
        except:
            raise Logger.error('cannot open file %r for writing' % filePath)

        if format is 'NAMD_PSF':
            self.__NAMD_PSF_export_atoms__(fd, indexesOffset=indexesOffset)
        else:
            fd.close()
            raise Logger.error('format %r is not defined' % format)
        if closeFile:
            fd.close()

    def export_bonds(self, filePath, key='atom_name', indexesOffset=1, format='NAMD_PSF', closeFile=True):
        """
        Exports bonds to ascii file.

        :Parameters:
            #. filePath (path): the file path.
            #. indexesOffset (int): atoms indexing starts from zero. this adds an offset. applies only to NAMD_PSF
            #. key (str): any pdbparser.records attribute. applies only to NAMD_TOP
            #. format (str): The format of exportation. Exisiting formats are: NAMD_PSF, NAMD_TOP
        """
        try:
            fd = open(filePath, 'w')
        except:
            raise Logger.error('cannot open file %r for writing' % filePath)

        if format is 'NAMD_PSF':
            self.__NAMD_PSF_export_bonds__(fd, indexesOffset=indexesOffset)
        else:
            if format is 'NAMD_TOP':
                self.__NAMD_TOP_export_bonds__(fd, key=key)
            else:
                fd.close()
                raise Logger.error('format %r is not defined' % format)
        if closeFile:
            fd.close()

    def export_angles(self, filePath, indexesOffset=1, key='atom_name', format='NAMD_PSF', closeFile=True):
        """
        Exports angles to ascii file.

        :Parameters:
            #. filePath (path): the file path.
            #. indexesOffset (int): atoms indexing starts from zero. this adds an offset. applies only to NAMD_PSF
            #. key (str): any pdbparser.records attribute. applies only to NAMD_TOP
            #. format (str): The format of exportation. Exisiting formats are: NAMD_PSF, NAMD_TOP
        """
        try:
            fd = open(filePath, 'w')
        except:
            raise Logger.error('cannot open file %r for writing' % filePath)

        if format is 'NAMD_PSF':
            self.__NAMD_PSF_export_angles__(fd, indexesOffset=indexesOffset)
        else:
            if format is 'NAMD_TOP':
                self.__NAMD_TOP_export_angles__(fd, key=key)
            else:
                fd.close()
                raise Logger.error('format %r is not defined' % format)
        if closeFile:
            fd.close()

    def export_dihedrals(self, filePath, indexesOffset=1, key='atom_name', format='NAMD_PSF', closeFile=True):
        """
        Exports dihedrals to ascii file.

        :Parameters:
            #. filePath (path): the file path.
            #. indexesOffset (int): atoms indexing starts from zero. this adds an offset. applies only to NAMD_PSF
            #. key (str): any pdbparser.records attribute. applies only to NAMD_TOP
            #. format (str): The format of exportation. Exisiting formats are: NAMD_PSF, NAMD_TOP
        """
        try:
            fd = open(filePath, 'w')
        except:
            raise Logger.error('cannot open file %r for writing' % filePath)

        if format is 'NAMD_PSF':
            self.__NAMD_PSF_export_dihedrals__(fd, indexesOffset=indexesOffset)
        else:
            if format is 'NAMD_TOP':
                self.__NAMD_TOP_export_dihedrals__(fd, key=key)
            else:
                fd.close()
                raise Logger.error('format %r is not defined' % format)
        if closeFile:
            fd.close()

    def __NAMD_PSF_export_atoms__(self, fd, indexesOffset=1):
        fd.write('\n%8d !NATOM\n' % len(self._Connectivity__pdb))
        indexes = self._Connectivity__pdb.indexes
        atomsWeights = np.array(get_records_database_property_values(indexes, self._Connectivity__pdb, 'atomicWeight'))
        for idx in indexes:
            at = self._Connectivity__pdb[idx]
            atomLine = str('%i' % (idx + indexesOffset)).rjust(8, ' ')
            atomLine += str(' ')
            atomLine += str('%s' % at['segment_identifier']).ljust(4, ' ')
            atomLine += str(' ')
            atomLine += str('%i' % at['sequence_number']).ljust(5, ' ')
            atomLine += str('%s' % at['residue_name']).ljust(5, ' ')
            atomLine += str('%s' % at['atom_name']).ljust(5, ' ')
            atomLine += str('%s' % at['atom_name']).ljust(5, ' ')
            atomLine += str('  0.000000')
            atomLine += str('      ')
            atomLine += str('%8.4f' % atomsWeights[idx])
            atomLine += str('           0')
            atomLine += str('\n')
            fd.write(atomLine)

    def __NAMD_PSF_export_bonds__(self, fd, indexesOffset=1):
        bonds = self.get_bonds()
        fd.write('\n%8d !NBOND: bonds\n' % self._numberOfBonds)
        numberOfBonds = 1
        for atomIdx in bonds[0]:
            for bondedIdx in bonds[1][atomIdx]:
                bondsStr = str('%8d' % (atomIdx + indexesOffset) + '%8d' % (bondedIdx + indexesOffset) + (not numberOfBonds % 4) * '\n')
                fd.write(bondsStr)
                numberOfBonds += 1

    def __NAMD_TOP_export_bonds__(self, fd, key='atom_name'):
        connectRecord, connectedTo = self.get_bonds(key=key)
        bonds = ''
        for idx in range(len(connectRecord)):
            for to in connectedTo[idx]:
                bonds += str('%s' % connectRecord[idx]).ljust(5) + ' ' + str('%s' % to).ljust(5) + '    '

            if bonds:
                fd.write('BOND %s\n' % bonds)
                bonds = ''

    def __NAMD_PSF_export_angles__(self, fd, indexesOffset=1):
        angles = self.get_angles()
        fd.write('\n%8d !NTHETA: angles\n' % self._numberOfAngles)
        numberOfAngles = 1
        for angle in angles:
            anglesStr = str('%8d' % (angle[0] + indexesOffset) + '%8d' % (angle[1] + indexesOffset) + '%8d' % (angle[2] + indexesOffset) + (not numberOfAngles % 3) * '\n')
            fd.write(anglesStr)
            numberOfAngles += 1

    def __NAMD_TOP_export_angles__(self, fd, key='atom_name'):
        angles = self.get_angles(key=key)
        count = 3
        angleLine = ''
        while angles:
            if count:
                angle = angles.pop(0)
                count -= 1
                angleLine += str('%s' % angle[0]).ljust(5) + ' ' + str('%s' % angle[1]).ljust(5) + ' ' + str('%s' % angle[2]).ljust(5) + '    '
            else:
                fd.write('ANGLE %s\n' % angleLine)
                angleLine = ''
                count = 3

        if angleLine:
            fd.write('ANGLE %s\n' % angleLine)

    def __NAMD_PSF_export_dihedrals__(self, fd, indexesOffset=1):
        dihedrals = self.get_dihedrals()
        fd.write('\n%8d !NPHI: dihedrals\n' % self.numberOfDihedrals)
        numberOfDihedrals = 1
        for dihedral in dihedrals:
            dihedralsStr = str('%8d' % (dihedral[0] + indexesOffset) + '%8d' % (dihedral[1] + indexesOffset) + '%8d' % (dihedral[2] + indexesOffset) + '%8d' % (dihedral[3] + indexesOffset) + (not numberOfDihedrals % 2) * '\n')
            fd.write(dihedralsStr)
            numberOfDihedrals += 1

    def __NAMD_TOP_export_dihedrals__(self, fd, key='atom_name'):
        dihedrals = self.get_dihedrals(key=key)
        count = 2
        dihedralLine = ''
        while dihedrals:
            if count:
                dihedral = dihedrals.pop(0)
                count -= 1
                dihedralLine += str('%s' % dihedral[0]).ljust(5) + ' ' + str('%s' % dihedral[1]).ljust(5) + ' ' + str('%s' % dihedral[2]).ljust(5) + ' ' + str('%s' % dihedral[3]).ljust(5) + '    '
            else:
                fd.write('DIHE %s\n' % dihedralLine)
                dihedralLine = ''
                count = 2

        if dihedralLine:
            fd.write('ANGLE %s\n' % dihedralLine)