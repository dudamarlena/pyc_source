# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Utilities/Convert.py
# Compiled at: 2019-02-16 12:09:48
# Size of source mod 2**32: 32666 bytes
"""
This module contains all the classes to convert from and to pdbparser format.

.. inheritance-diagram:: pdbparser.Utilities.Convert
    :parts: 2
"""
from __future__ import print_function
import os, copy, itertools
from collections import OrderedDict
import numpy as np
from pdbparser.log import Logger
from pdbparser import pdbparser
from .Geometry import *
from .Information import *
from .Database import is_element, __ATOM__, __atoms_database__
from .Connectivity import Connectivity
from pdbparser.Utilities.BoundaryConditions import InfiniteBoundaries, PeriodicBoundaries
from pdbparser.Utilities.Information import get_records_attribute_values, get_records_indexes_by_attribute_value

class Convert(object):
    __doc__ = '\n    The mother class of all convert classes from format to pdbparser.\n    '
    __defaults__ = {}
    __defaults__['pdb'] = None
    __defaults__['filePath'] = None

    def __init__(self, *args, **kwargs):
        for kwarg, value in kwargs.items():
            self.__setattr__(kwarg, value)

        self.initialize_default_attributes()

    def __setattr__(self, name, value):
        if name == 'pdb':
            Logger.error('attribute %r is protected' % name)
            raise
        else:
            object.__setattr__(self, name, value)

    def set_pdb(self, pdb):
        assert isinstance(pdb, pdbparser.pdbparser), Logger.error('pdb must a pdbparser instance')
        object.__setattr__(self, 'pdb', pdb)

    def initialize_default_attributes(self):
        if not hasattr(self, 'pdb'):
            object.__setattr__(self, 'pdb', pdbparser())
        else:
            if not isinstance(self.pdb, pdbparser):
                raise AssertionError(Logger.error('pdb must a pdbparser instance'))
            elif not hasattr(self, 'filePath'):
                object.__setattr__(self, 'filePath', self.__defaults__['filePath'])
            else:
                if self.filePath is not None:
                    try:
                        fd = open(self.filePath, 'r')
                    except:
                        Logger.error('Cannot open %r for reading.' % self.filePath)
                        raise
                    else:
                        fd.close()
            self.info = {}

    def get_lines(self):
        fd = open(self.filePath, 'r')
        lines = fd.readlines()
        fd.close()
        return lines

    def get_pdb(self):
        return self.pdb

    def convert(self):
        """
        This method should be over wrote in every convert child class
        """
        pass

    def convert_pdb(self):
        """
        This method should be over wrote in every convert child class
        """
        pass


class VASPFractionalCoordinates(Convert):
    __doc__ = '\n    Converts VASP Fractional Coordinates format to pdbparser.\n\n    :Example:\n    ::\n\n        Li2MnO4\n           1.00000000000000\n             8.6545396172990436    4.9967007752759676    0.0000000000000000\n             0.0000000000000000    9.9934015505519351    0.0000000000000000\n             1.4424232695498407    0.8327834632249816    4.8153858430651875\n           Li   Mn   O\n            2    1    4\n        Direct\n          0.9157449887734188  0.1685090824163638  0.5000002836784176\n          0.0801471319727156  0.3326620394419919  0.5042883184992419\n          0.9114744514958772  0.6683354316415233  0.5049720216553411\n          0.4171328149824021  0.1657344623682278  0.5000002273738957\n          0.2484635160767397  0.5030735275277323  0.4999994413126529\n          0.0847322081135644  0.8305354318744094  0.5000000522719219\n          0.5871908407369446  0.3326623821732326  0.4957118172424586\n\n          0.00000000E+00  0.00000000E+00  0.00000000E+00\n          0.00000000E+00  0.00000000E+00  0.00000000E+00\n          0.00000000E+00  0.00000000E+00  0.00000000E+00\n          0.00000000E+00  0.00000000E+00  0.00000000E+00\n          0.00000000E+00  0.00000000E+00  0.00000000E+00\n          0.00000000E+00  0.00000000E+00  0.00000000E+00\n          0.00000000E+00  0.00000000E+00  0.00000000E+00\n\n    :Parameters:\n        #. filePath (str): the VASP fractional coordinates file path.\n    '

    def __init__(self, filePath, *args, **kwargs):
        self.filePath = filePath
        (super(VASPFractionalCoordinates, self).__init__)(*args, **kwargs)

    def __get_formula__(self, lines):
        return str(lines.pop(0).split('\n')[0].strip())

    def __get_scale_factor__(self, lines):
        return float(lines.pop(0).split('\n')[0])

    def __get_axes_vectors__(self, lines):
        xAxis = np.array([float(item) for item in lines.pop(0).split('\n')[0].split()])
        yAxis = np.array([float(item) for item in lines.pop(0).split('\n')[0].split()])
        zAxis = np.array([float(item) for item in lines.pop(0).split('\n')[0].split()])
        return (xAxis, yAxis, zAxis)

    def __get_elements_order__(self, lines):
        elements = [[str(item)] for item in lines.pop(0).split('\n')[0].split()]
        numbers = [int(item) for item in lines.pop(0).split('\n')[0].split()]
        assert len(numbers) == len(elements)
        return sum(list(itertools.imap(list.__mul__, elements, numbers)), [])

    def __get_fractional_coordinates__(self, lines, number):
        lines.pop(0)
        fracCoord = np.empty((number, 3)).astype(np.float)
        for idx in xrange(number):
            fracCoord[idx, :] = [float(item) for item in lines.pop(0).split('\n')[0].split()]

        return fracCoord

    def __calculate_real_coordinates__(self, fracCoord, xAxis, yAxis, zAxis):
        realCoord = np.empty(fracCoord.shape).astype(np.float)
        for idx in xrange(fracCoord.shape[0]):
            realCoord[idx, :] = xAxis * fracCoord[(idx, 0)] + yAxis * fracCoord[(idx, 1)] + zAxis * fracCoord[(idx, 2)]

        return realCoord

    def __create_pdb__(self, elements, realCoord, name=None):
        if name is not None:
            self.pdb.set_name(name)
        records = []
        for idx in xrange(realCoord.shape[0]):
            at = copy.deepcopy(__ATOM__)
            at['coordinates_x'] = realCoord[(idx, 0)]
            at['coordinates_y'] = realCoord[(idx, 1)]
            at['coordinates_z'] = realCoord[(idx, 2)]
            at['residue_name'] = 'CRY'
            at['element_symbol'] = elements[idx]
            at['atom_name'] = elements[idx]
            records.append(at)

        self.pdb.records = records

    def convert(self):
        """
        Converts to pdbparser
        """
        lines = self.get_lines()
        self.info['formula'] = self.__get_formula__(lines)
        self.info['scaleFactor'] = self.__get_scale_factor__(lines)
        self.info['xAxis'], self.info['yAxis'], self.info['zAxis'] = self.__get_axes_vectors__(lines)
        self.info['elements'] = self.__get_elements_order__(lines)
        fracCoord = self.__get_fractional_coordinates__(lines, len(self.info['elements']))
        BC = PeriodicBoundaries(np.array([self.info['xAxis'], self.info['yAxis'], self.info['zAxis']]))
        realCoord = self.info['scaleFactor'] * BC.box_to_real_array(fracCoord)
        self.__create_pdb__((self.info['elements']), realCoord, name=(self.info['formula']))
        BC = PeriodicBoundaries(np.array([self.info['xAxis'], self.info['yAxis'], self.info['zAxis']]))
        self.pdb.set_boundary_conditions(BC)
        return self


class RMCplusplus(Convert):
    __doc__ = '\n    Converts RMC++ configuration file to pdbparser.\n\n    :Example:\n    ::\n\n        (Version 3 format configuration file) !file created by SimpleCfg::save !\n        CCl4_at\n\n\n              1279896          324543           55745 moves generated, tried, accepted\n              0              configurations saved\n\n          10240 molecules of all types\n              2 types of molecules\n              1 is the largest number of atoms in a molecule\n              0 Euler angles are provided\n\n              F (box is cubic)\n                Defining vectors are:\n                 34.235218   0.000000   0.000000\n                  0.000000  34.235218   0.000000\n                  0.000000   0.000000  34.235218\n\n           2048 molecules of type  1\n              1 atomic sites\n                  0.000000   0.000000   0.000000\n\n           8192 molecules of type  2\n              1 atomic sites\n                  0.000000   0.000000   0.000000\n\n        -0.906638958281220  -0.657018016704405  -0.728731730614787\n        -0.786972436949130  -0.657627328226054  -0.787627155672891\n        -0.777310920528387  -0.784783890438497  -0.593932422372214\n         0.995954003399787  -0.696941212792459  -0.096196347815229\n        -0.900490089683701  -0.833132404483661  0.2288995145083130\n        -0.934597263489565  -0.763072730515099  0.4172921957931380\n        -0.802394301831597  -0.767756191733287  0.6916877096275050\n        .\n        .\n        .\n\n    '

    def __init__(self, filePath=None, *args, **kwargs):
        """
        Initialize the RMC++ converter.

         :Parameters:
            #. filePath (str): the RMC++ input configuration file path.
        """
        self.filePath = filePath
        (super(RMCplusplus, self).__init__)(*args, **kwargs)

    def __get_number_of_records__(self, lines):
        nrecords = False
        while lines:
            line = lines.pop(0)
            if 'molecules of all types' in line:
                nrecords = int(line.split()[0])
                break

        if not nrecords:
            Logger.error("number of 'molecules of all types' not found.")
            raise
        return nrecords

    def __get_number_of_types__(self, lines):
        ntypes = False
        line = lines.pop(0)
        if 'types of molecules' in line:
            ntypes = int(line.split()[0])
        else:
            Logger.error("number of 'types of molecules' not found.")
            raise
        return ntypes

    def __get_box_vectors__(self, lines):
        while lines:
            line = lines.pop(0)
            if 'Defining vectors are:' in line:
                try:
                    ox = [float(it) for it in lines.pop(0).split()]
                except:
                    Logger.error("couldn't parse defining 'OX' vectors")
                else:
                    if not len(ox) == 3:
                        raise AssertionError('OX vector must have three float entries')
                    else:
                        try:
                            oy = [float(it) for it in lines.pop(0).split()]
                        except:
                            Logger.error("couldn't parse defining 'OY' vectors")
                        else:
                            if not len(oy) == 3:
                                raise AssertionError('OY vector must have three float entries')
                            else:
                                try:
                                    oz = [float(it) for it in lines.pop(0).split()]
                                except:
                                    Logger.error("couldn't parse defining 'OZ' vectors")

                            assert len(oz) == 3, 'OZ vector must have three float entries'
                    break

        if not lines:
            Logger.error("simulation box 'Defining vectors' not found.")
            raise
        return np.array([ox, oy, oz])

    def __get_records_per_type__(self, lines, number):
        nrecords = False
        while lines:
            line = lines.pop(0)
            if 'molecules of type' in line:
                split = line.split()
                nrecords = int(split[0])
                assert int(split[(-1)]) == int(number), "molecule order %r in file doesn't match with number %r"(str(split[(-1)]), str(number))
                break

        if not nrecords:
            Logger.error('number of records for type number %r not found.' % number)
            raise
        line = lines.pop(0)
        assert 'atomic sites' in line, "'atomic site' line must proceed 'molecules of type  %i'" % number
        nsites = int(line.split()[0])
        assert nsites > 0, "number of 'atomic sites' must be bigger than 1"
        while nsites > 0:
            nsites -= 1
            lines.pop(0)

        return nrecords

    def __get_coordinates__(self, lines):
        coords = []
        while lines:
            line = lines.pop(0).strip()
            if not line:
                continue
            else:
                line = line.split()
                assert len(line) == 3, 'coordinates line must contain 3 elements, X, Y and Z values'
                coords.append([float(it) for it in line])

        return np.array(coords)

    def __calculate_real_coordinates__(self, fracCoord):
        realCoord = np.empty(fracCoord.shape).astype(np.float)
        xAxis = self.info['vectors'][0, :]
        yAxis = self.info['vectors'][1, :]
        zAxis = self.info['vectors'][2, :]
        for idx in xrange(fracCoord.shape[0]):
            realCoord[idx, :] = xAxis * fracCoord[(idx, 0)] + yAxis * fracCoord[(idx, 1)] + zAxis * fracCoord[(idx, 2)]

        return realCoord

    def __create_pdb__(self, realCoord, name=None):
        if name is not None:
            self.pdb.set_name(name)
        bc = PeriodicBoundaries()
        bc.set_vectors(2 * np.array(self.info['vectors']))
        self.pdb.set_boundary_conditions(bc)
        records = []
        for typeNumber in range(self.info['number_of_types']):
            element = self.info['types'][typeNumber]['element']
            name = self.info['types'][typeNumber]['name']
            for idx in range(len(records), len(records) + self.info['records_per_type'][typeNumber]):
                at = copy.deepcopy(__ATOM__)
                at['serial_number'] = idx + 1
                at['coordinates_x'] = realCoord[(idx, 0)]
                at['coordinates_y'] = realCoord[(idx, 1)]
                at['coordinates_z'] = realCoord[(idx, 2)]
                at['residue_name'] = 'RMC'
                at['element_symbol'] = element
                at['atom_name'] = name
                records.append(at)

        self.pdb.records = records

    def __write_fnc_file__(self, path, name, bondsMap, bondsMapElementsKey, bonds):
        """
        writes .fnc

        :Parameters:
            #. path (str): The RMC++ output configuration file path.
            #. name (str): The tile name to be put in the beginning of the file
            #. bondsMap (dict): Dictionary of bonds elements keys mapping to a bonds indexes. Double dash '--' must seperate keys. e.g. {'H2--O': 1, 'H1--O': 2}
            #. bondsMapElementsKey (list): The list of all atoms keys in pdb used to map atoms to bondsMap. e.g. ["H1","H2", ... , "H1","H2","O","O", ...]
            #. bonds (dict): The dictionary of bonds indexes. e.g. {1:[100,101], 2:[102,103,104], ..., 999:[], 1000:[20,21], ...}
        """
        try:
            fd = open(path, 'w')
        except:
            Logger.error('cannot open file %r for writing' % outputPath)
            raise

        fd.write('     ' + str(name) + '\n\n')
        bondsMapLUT = {}
        for b, v in bondsMap.items():
            bondsMapLUT[v] = b

        fd.write('     No. of possible rmin-rmax pairs:\n')
        fd.write('      ' + str(len(bondsMap)) + '\n')
        fd.write('0.90'.rjust(10) * len(bondsMap) + '\n')
        fd.write('2.10'.rjust(10) * len(bondsMap) + '\n')
        constraints = ''.join([bondsMapLUT[idx].rjust(10) for idx in sorted(bondsMapLUT.keys())])
        fd.write('! %s \n' % constraints[1:])
        fd.write('            ' + str(len(bonds)) + '\n\n')
        for cr in sorted(bonds.keys()):
            ctList = bonds[cr]
            fd.write(str(cr + 1).rjust(12) + str(len(ctList)).rjust(5) + '\n')
            types = '  '
            for ct in ctList:
                fd.write(str(ct + 1).rjust(12))
                setted = list(set([bondsMapElementsKey[cr], bondsMapElementsKey[ct]]))
                types += str(bondsMap[(str(setted[0]) + '--' + str(setted[1]))]).ljust(1) + ' '

            fd.write('\n')
            fd.write(types)
            fd.write('\n')

        fd.close()

    def convert(self, types=None):
        """
        Converts to pdbparser
        """
        lines = self.get_lines()
        self.info['number_of_records'] = self.__get_number_of_records__(lines)
        self.info['number_of_types'] = self.__get_number_of_types__(lines)
        self.info['vectors'] = self.__get_box_vectors__(lines)
        if types is None:
            Logger.info('types are not given. carbon element is considered for all types')
            self.info['types'] = [{'name':'c%s' % idx,  'element':'c'} for idx in range(self.info['number_of_types'])]
        else:
            assert len(types) == self.info['number_of_types'], 'types must be a list of length equal to the number of types'
            for idx in range(self.info['number_of_types']):
                if not isinstance(types[idx], dict):
                    assert is_element(types[idx]), '%s not found database elements' % types[idx]
                    types[idx] = {'name':types[idx],  'element':types[idx]}
                assert 'name' in types[idx], "every type dictionary must have 'name' and 'element' keys"
                assert 'element' in types[idx], "every type dictionary must have 'name' and 'element' keys"
                if types[idx]['element'].lower() not in __atoms_database__.keys():
                    Logger.warr('type %r is not defined in database' % types[idx]['element'])
                else:
                    types[idx]['element'] = types[idx]['element'].lower()

            self.info['types'] = types
        self.info['records_per_type'] = []
        for idx in range(self.info['number_of_types']):
            self.info['records_per_type'].append(self.__get_records_per_type__(lines, idx + 1))

        assert sum(self.info['records_per_type']) == self.info['number_of_records'], "the sum of number of molecules in all types must be equal to number of ' molecules of all types'"
        fracCoord = self.__get_coordinates__(lines)
        assert fracCoord.shape == (self.info['number_of_records'], 3), "stored fractional coordinates must be equal to number of ' molecules of all types'"
        realCoord = self.__calculate_real_coordinates__(fracCoord)
        self.__create_pdb__(realCoord)
        return self

    def convert_pdb(self, outputPath, halfBoxLength=None, name=None):
        """
        Converts and exports pdb to RMC++ configuration file.

        :Parameters:
            #. pdb (pdbparser): the pdb to convert to RMC++ configuration file
            #. outputPath (str): the RMC++ output configuration file path.
            #. halfBoxLength (list, tuple, numpy.ndarray): the simulation half box lengths for X, Y and Z.
        """
        pdb = self.pdb
        elements = pdb.elements
        types = set(elements)
        typesIndexes = {}
        for t in types:
            typesIndexes[t] = get_records_indexes_by_attribute_value(pdb.indexes, pdb, 'element_symbol', t)

        if name is None:
            name = pdb.name
        elif name is None:
            name = '_'.join([str(t) + str(len(typesIndexes[t])) for t in typesIndexes.keys()])
        else:
            name = str(name)
        mX, MX, mY, MY, mZ, MZ = get_min_max(pdb.indexes, pdb)
        coordinates = pdb.coordinates
        center = [
         (MX + mX) / 2.0, (MY + mY) / 2.0, (MZ + mZ) / 2.0]
        coordinates -= np.array(center)
        if halfBoxLength is None:
            halfBoxLength = isinstance(pdb.boundaryConditions, PeriodicBoundaries) or np.max([np.abs(MX - mX) / 2.0, np.abs(MY - mY) / 2.0, np.abs(MZ - mZ) / 2.0])
        else:
            if isinstance(pdb.boundaryConditions, PeriodicBoundaries):
                bc = pdb.boundaryConditions
                halfBoxLength = np.max([bc.get_a() / 2.0, bc.get_b() / 2.0, bc.get_c() / 2.0])
            else:
                halfBoxLength = float(halfBoxLength)
                assert halfBoxLength > 0, Logger.error('negative halfBoxLength is not allowed')
                vectors = np.array([halfBoxLength, halfBoxLength, halfBoxLength])
                coordinates[:, 0] /= vectors[0]
                coordinates[:, 1] /= vectors[1]
                coordinates[:, 2] /= vectors[2]
                try:
                    fd = open(outputPath, 'w')
                except:
                    raise Exception(Logger.error('cannot open file %r for writing' % outputPath))

                formula = '_'.join([str(t) + str(len(typesIndexes[t])) for t in typesIndexes.keys()])
                fd.write(' (Version 3 format configuration file) !file created by pdbparser V1.0; types are %s; formula: %s !\n' % (list(types), formula))
                fd.write('%s\n' % name)
                fd.write('\n\n')
                fd.write('     0         0         0      moves generated, tried, accepted \n')
                fd.write('          0              configurations saved \n')
                fd.write('\n')
                fd.write('%s molecules of all types\n' % str(len(pdb)).rjust(11, ' '))
                fd.write('%s types of molecules\n' % str(len(typesIndexes.keys())).rjust(11, ' '))
                fd.write('          1 is the largest number of atoms in a molecule\n')
                fd.write('          0 Euler angles are provided \n')
                fd.write('\n')
                fd.write('          F (box is cubic)\n')
                fd.write('            Defining vectors are:\n')
                fd.write('            %10.6f   0.000000   0.000000\n' % vectors[0])
                fd.write('              0.000000 %10.6f   0.000000\n' % vectors[1])
                fd.write('              0.000000   0.000000 %10.6f\n' % vectors[2])
                fd.write('\n')
                typeNumber = 0
                for t in types:
                    typeNumber += 1
                    fd.write('%s molecules of type %s\n' % (str(len(typesIndexes[t])).rjust(11, ' '), typeNumber))
                    fd.write('          1 atomic sites\n')
                    fd.write('              0.000000   0.000000   0.000000\n')
                    fd.write('\n')

                for t in types:
                    for idx in typesIndexes[t]:
                        fd.write(' %.15f  %.15f  %.15f\n' % (coordinates[(idx, 0)], coordinates[(idx, 1)], coordinates[(idx, 2)]))

    def generate_fixed_neighbours_constraint(self, outputPath, key='sequence_number', bondMapKey='atom_name', regressive=True):
        """
        generates automatically RMC++ .fnc file from a pdbparser instance.
        RMC++ .cfg file atoms are ordered element wise.
        Therefore .fnc atoms indexes might not be the same as the given pdb records indexes
        but reordered to correspond to the .cfg file exported using convert_pdb method.
        In order to get a pdb file respecting the same order as .cfg file,
        one should convert the original pdb using convert_pdb then convert it back to pdb using convert method.

        :Parameters:
            #. outputPath (str): The RMC++ .fnc output configuration file path.
            #. key (str): Any pdbparser record valid key used to split records into molecules and generate bonds.
            #. bondMapKey (str): Any pdbparser record valid key used to generate bonds types.
            #. regressive (bool): Insures that a bond is calculated for both atoms of the same bond.
                                  If atom X is bonded to Y, normaly Y is in the bonds list of X, regressive insures that also X is in the bonds list of Y
        """
        elements = self.get_pdb().elements
        types = set(elements)
        typesIndexes = []
        for t in types:
            typesIndexes.extend(get_records_indexes_by_attribute_value(self.get_pdb().indexes, self.get_pdb(), 'element_symbol', t))

        pdb = pdbparser.pdbparser()
        pdb.set_name(self.get_pdb().name)
        pdb.records = [self.get_pdb().records[idx] for idx in typesIndexes]
        slicedPdb = pdbparser.pdbparser()
        molecules = set(get_records_attribute_values(pdb.indexes, pdb, key))
        centralRecord = []
        connectedTo = []
        for mol in molecules:
            indexes = get_records_indexes_by_attribute_value(pdb.indexes, pdb, key, mol)
            slicedPdb.records = [pdb.records[idx] for idx in indexes]
            connectivity = Connectivity(slicedPdb)
            connectivity.calculate_bonds(regressive=True)
            cr, ct = connectivity.get_bonds()
            centralRecord.extend([indexes[idx] for idx in cr])
            connectedTo.extend([[indexes[idx] for idx in item] for item in ct])

        bonds = dict(zip(centralRecord, connectedTo))
        bondsMapElementsKey = get_records_attribute_values(pdb.indexes, pdb, bondMapKey)
        bondsMap = []
        for crIdx in range(len(centralRecord)):
            cr = centralRecord[crIdx]
            for ct in connectedTo[crIdx]:
                setted = list(set([bondsMapElementsKey[cr], bondsMapElementsKey[ct]]))
                bondsMap.append(str(setted[0]) + '--' + str(setted[1]))

        bondsMap = OrderedDict(zip(set(bondsMap), range(1, len(bondsMap) + 1)))
        self.__write_fnc_file__(outputPath, pdb.name, bondsMap, bondsMapElementsKey, bonds)

    def create_fixed_neighbours_constraint(self, outputPath, map, regressive=True):
        """
        generates rmc++ .fnc file from a pdbparser instance using a user-defined bonds maping.
        RMC++ .cfg file atoms are ordered element wise.
        Therefore .fnc atoms indexes might not be the same as the given pdb records indexes
        but reordered to correspond to the .cfg file exported using convert_pdb method.
        In order to get a pdb file respecting the same order as .cfg file,
        one should convert the original pdb using convert_pdb then convert it back to pdb using convert method.

        :Parameters:
            #. outputPath (str): The RMC++ .fnc output configuration file path.
            #. map (list): list of dictionary. Every dictionary must contain mapping specific keys.Valid keys are:
               #. 'molecule_mapping' : Any pdbparser record valid key used to split records into molecules.
               #. 'molecule_key' : the molecules in the pdb.
               #. 'atoms_mapping' : Any pdbparser record valid key used to map records bonds.
               #. 'bonds' : dictionary of atom keys and list of atoms bonds value.

               ::

                   e.g. map=[ {"molecules_mapping" : "sequence_number",
                               "atoms_mapping"     : "atom_name",
                               "bonds"             : {"O":["H1","H2"]} },
                              {"molecules_mapping" : "sequence_number",
                               "atoms_mapping"     : "atom_name",
                               "bonds"             : {"C":["H1","H2","H3","H4"],
                                                      "H1":["H2","H3","H4"],
                                                      "H2":["H3","H4"],
                                                      "H3":["H4"]} } ]

            #. regressive (bool): Insures that a bond is calculated for both atoms of the same bond.
                                  If atom X is bonded to Y, normaly Y is in the bonds list of X, regressive insures that also X is in the bonds list of Y
        """
        assert isinstance(regressive, bool), Logger.error('regressive must be a boolean')
        assert isinstance(map, (list, set, tuple)), Logger.error('map should be a list')
        map = list(map)
        for m in map:
            assert isinstance(m, dict), Logger.error('map item must be python dictionary')
            assert 'molecules_mapping' in m, Logger.error("map item must have 'molecules_mapping' key")
            assert 'atoms_mapping' in m, Logger.error("map item must have 'atoms_mapping' key")
            assert 'bonds' in m, Logger.error("map item must have 'bonds' key")
            assert isinstance(m['bonds'], dict), Logger.error("map 'bonds' value must be a dictionary")

        if regressive:
            for m in map:
                for cr, values in m['bonds'].items():
                    for ct in values:
                        if m['bonds'].get(ct, None) is None:
                            m['bonds'][ct] = [
                             cr]
                        else:
                            m['bonds'][ct].append(cr)

                for ct in m['bonds'].keys():
                    m['bonds'][ct] = list(set(m['bonds'][ct]))

        elements = self.get_pdb().elements
        types = set(elements)
        typesIndexes = []
        for t in types:
            typesIndexes.extend(get_records_indexes_by_attribute_value(self.get_pdb().indexes, self.get_pdb(), 'element_symbol', t))

        pdb = pdbparser.pdbparser()
        pdb.set_name(self.get_pdb().name)
        pdb.records = [self.get_pdb().records[idx] for idx in typesIndexes]
        centralRecord = []
        connectedTo = []
        bondsMapElementsKey = [None for idx in pdb.indexes]
        for m in map:
            molecules = set(get_records_attribute_values(pdb.indexes, pdb, m['molecules_mapping']))
            for mol in molecules:
                molAtomsIndexes = get_records_indexes_by_attribute_value(pdb.indexes, pdb, m['molecules_mapping'], mol)
                for cr, values in m['bonds'].items():
                    crIdx = get_records_indexes_by_attribute_value(molAtomsIndexes, pdb, m['atoms_mapping'], cr)
                    assert len(crIdx) == 1, "Only one central atom in molecule map bonds must be found. '%i' where found for central atom '%s'" % (len(crIdx), str(cr))
                    centralRecord.append(crIdx[0])
                    bondsMapElementsKey[crIdx[0]] = pdb.records[crIdx[0]][m['atoms_mapping']]
                    ctList = []
                    for ct in values:
                        ctIdx = get_records_indexes_by_attribute_value(molAtomsIndexes, pdb, m['atoms_mapping'], ct)
                        assert len(ctIdx) == 1, "Only one connected atom in molecule map bonds must be found. '%i' where found for connected atom '%s' in central atom '%s' in map %s" % (len(ctIdx), str(ct), str(cr), str(m['bonds'][cr]))
                        ctList.append(ctIdx[0])
                        bondsMapElementsKey[ctIdx[0]] = pdb.records[ctIdx[0]][m['atoms_mapping']]

                    connectedTo.append(ctList)

        bonds = {}
        for idx in pdb.indexes:
            bonds[idx] = []

        for idx in range(len(centralRecord)):
            bonds[centralRecord[idx]] = connectedTo[idx]

        bondsMap = []
        for crIdx in range(len(bonds)):
            for ctIdx in bonds[crIdx]:
                cr = bondsMapElementsKey[crIdx]
                ct = bondsMapElementsKey[ctIdx]
                if not cr is None:
                    if ct is None:
                        raise AssertionError('mapping error')
                    setted = list(set([cr, ct]))
                    bondsMap.append(str(setted[0]) + '--' + str(setted[1]))

        bondsMap = OrderedDict(zip(set(bondsMap), range(1, len(bondsMap) + 1)))
        self.__write_fnc_file__(outputPath, pdb.name, bondsMap, bondsMapElementsKey, bonds)