# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Analysis/Dynamics/MeanSquareDisplacement.py
# Compiled at: 2019-02-16 11:57:16
# Size of source mod 2**32: 22446 bytes
"""
This module provides all mean square displacement classes.

.. inheritance-diagram:: pdbparser.Analysis.Dynamics.MeanSquareDisplacement
    :parts: 2
"""
from __future__ import print_function
from collections import Counter
import numpy as np
from pdbparser.log import Logger
from pdbparser.Analysis.Core import Analysis, AxisDefinition
from pdbparser.Utilities.Information import get_records_database_property_values
from pdbparser.Utilities.Collection import correlation, get_data_weighted_sum
from pdbparser.Utilities.Database import get_element_property, is_element_property

class MeanSquareDisplacement(Analysis):
    __doc__ = '\n    Computes the mean square displacement for a set of atoms.\n\n    :Parameters:\n        #. trajectory (pdbTrajectory): pdbTrajectory instance.\n        #. configurationsIndexes (list, set, tuple): List of selected indexes of configuration used to perform the analysis.\n        #. targetAtomsIndexes (list, set, tuple): Selected target atoms indexes.\n        #. weighting (database key): a database property to weight the mean square displacement partials.\n    '

    def __init__(self, trajectory, configurationsIndexes, targetAtomsIndexes, weighting='equal', *args, **kwargs):
        (super(MeanSquareDisplacement, self).__init__)(trajectory, *args, **kwargs)
        self.targetAtomsIndexes = self.get_atoms_indexes(targetAtomsIndexes)
        self.numberOfSteps = len(self.targetAtomsIndexes)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        assert is_element_property(weighting), Logger.error("weighting '%s' don't exist in database" % weighting)
        self.weighting = weighting
        self.__initialize_variables__()
        self.__initialize_results__()

    def __initialize_variables__(self):
        self.weights = np.array(get_records_database_property_values(self.targetAtomsIndexes, self.structure, self.weighting))
        elements = self._trajectory.elements
        self.elements = [elements[idx] for idx in self.targetAtomsIndexes]
        elementsSet = set(self.elements)
        self.elementsWeights = dict(zip(elementsSet, [get_element_property(el, self.weighting) for el in elementsSet]))
        self.elementsNumber = dict(Counter(self.elements))

    def __initialize_results__(self):
        self.results['time'] = np.array([self.time[idx] for idx in self.configurationsIndexes], dtype=(np.float))
        for el in set(self.elements):
            self.results['msd_%s' % el] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))

    def step(self, index):
        """
        analysis step of calculation method.

        :Parameters:
            #. atomIndex (int): the atom step index

        :Returns:
            #. stepData (object): object used in combine method
        """
        atomIndex = self.targetAtomsIndexes[index]
        atomTrajectory = self._trajectory.get_atom_trajectory(atomIndex, self.configurationsIndexes)
        dsq = np.add.reduce(atomTrajectory * atomTrajectory, 1)
        sum_dsq1 = np.add.accumulate(dsq)
        sum_dsq2 = np.add.accumulate(dsq[::-1])
        sumsq = 2.0 * sum_dsq1[(-1)]
        Saabb = sumsq - np.concatenate(([0.0], sum_dsq1[:-1])) - np.concatenate(([0.0], sum_dsq2[:-1]))
        Saabb = Saabb / (len(dsq) - np.arange(len(dsq)))
        Sab = 2.0 * correlation(atomTrajectory)
        atomicMSD = Saabb - Sab
        return (index, atomicMSD)

    def combine(self, index, stepData):
        """
        analysis combine method called after each step.

        :Parameters:
            #. atomIndex (int): the atomIndex of the last calculated atom
            #. stepData (object): the returned data from step method
        """
        atomIndex = self.targetAtomsIndexes[index]
        element = self.elements[index]
        if element == 'NA':
            print(index, atomIndex)
        self.results[('msd_%s' % element)] += stepData

    def finalize(self):
        """
        called once all the steps has been run.

        """
        data = {}
        for el in set(self.elements):
            self.results[('msd_%s' % el)] /= len([item for item in self.elements if item == el])
            data[el] = self.results[('msd_%s' % el)]

        self.results['msd_total'] = get_data_weighted_sum(data, numbers=(self.elementsNumber), weights=(self.elementsWeights))


class MeanSquareDisplacementInCylinder(Analysis):
    __doc__ = '\n    Computes the mean square displacement for a set of atoms splitting partials between inside and outside of a cylinder.\n\n    :Parameters:\n        #. trajectory (pdbTrajectory): pdbTrajectory instance.\n        #. configurationsIndexes (list, set, tuple): List of selected indexes of configuration used to perform the analysis.\n        #. cylinderAtomsIndexes (list, set, tuple): Selected atoms indexes supposedly forming a cylinder e.g. nanotube.\n        #. targetAtomsIndexes (list, set, tuple): Selected target atoms indexes.\n        #. weighting (database key): a database property to weight the mean square displacement partials.\n        #. axis (None, vector): The cylinder main axis, If None main principal axis of cylinderAtomsIndexes is calculated automatically.\n    '

    def __init__(self, trajectory, configurationsIndexes, cylinderAtomsIndexes, targetAtomsIndexes, axis=None, weighting='equal', histBin=1, *args, **kwargs):
        (super(MeanSquareDisplacementInCylinder, self).__init__)(trajectory, *args, **kwargs)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        self.targetAtomsIndexes = self.get_atoms_indexes(targetAtomsIndexes)
        self.cylinderAtomsIndexes = self.get_atoms_indexes(cylinderAtomsIndexes)
        self.numberOfSteps = len(self.targetAtomsIndexes)
        assert is_element_property(weighting), Logger.error("weighting '%s' don't exist in database" % weighting)
        self.weighting = weighting
        try:
            self.histBin = float(histBin)
        except:
            raise Logger.error('histBin must be number convertible. %s is given.' % histBin)

        assert self.histBin % 1 == 0, logger.error('histBin must be integer. %s is given.' % histBin)
        assert self.histBin > 0, logger.error('histBin must be positive. %s is given.' % histBin)
        assert self.histBin < len(self.configurationsIndexes), logger.error('histBin must smaller than numberOfConfigurations')
        self.__initialize_variables__(axis)
        self.__initialize_results__()
        Logger.info('%s --> initializing cylinder parameters along all configurations' % self.__class__.__name__)
        self.cylCenters, self.cylMatrices, self.cylRadii, self.cylLengths = self.__get_cylinder_properties__()

    def __initialize_variables__(self, axis):
        self.weights = np.array(get_records_database_property_values(self.targetAtomsIndexes, self.structure, self.weighting))
        elements = self._trajectory.elements
        self.elements = [elements[idx] for idx in self.targetAtomsIndexes]
        elementsSet = set(self.elements)
        self.elementsWeights = dict(zip(elementsSet, [get_element_property(el, self.weighting) for el in elementsSet]))
        self.elementsNumber = dict(Counter(self.elements))
        if len(set.intersection(set(self.cylinderAtomsIndexes), set(self.targetAtomsIndexes))):
            raise AssertionError(Logger.error("cylinderAtomsIndexes and targetAtomsIndexes can't have any index in common"))
        if axis is None:
            axis = {'principal': self.cylinderAtomsIndexes}
        self.axis = AxisDefinition(self._trajectory, axis)

    def __initialize_results__(self):
        self.results['time'] = np.array([self.time[idx] for idx in self.configurationsIndexes], dtype=(np.float))
        self.results['histogram_edges'] = self.histBin * np.array(range(int(len(self.configurationsIndexes) / self.histBin) + 1))
        for el in set(self.elements):
            self.results['residency_time_inside_%s' % el] = [
             0.0, 0]
            self.results['residency_time_outside_%s' % el] = [0.0, 0]
            self.results['msd_inside_%s' % el] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
            self.results['msd_inside_axial_%s' % el] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
            self.results['msd_inside_transversal_%s' % el] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
            self.results['msd_outside_%s' % el] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
            self.results['histogram_inside_%s' % el] = np.zeros((int(len(self.configurationsIndexes) / self.histBin) + 1), dtype=(np.float))
            self.results['histogram_outside_%s' % el] = np.zeros((int(len(self.configurationsIndexes) / self.histBin) + 1), dtype=(np.float))

        self.insideNormalization = {}
        self.outsideNormalization = {}
        for el in set(self.elements):
            self.insideNormalization[el] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
            self.outsideNormalization[el] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))

    def __get_cylinder_properties__(self):
        cylCenters = []
        cylMatrices = []
        cylRadii = []
        cylLengths = []
        for confIdx in self.configurationsIndexes:
            self._trajectory.set_configuration_index(confIdx)
            coordinates = self._trajectory.get_configuration_coordinates(confIdx)
            cylinderAtomsCoordinates = coordinates[self.cylinderAtomsIndexes]
            center, rotationMatrix = self.axis.get_center_rotationMatrix(coordinates)
            cylinderAtomsCoordinates -= center
            cylinderAtomsCoordinates = np.dot(cylinderAtomsCoordinates, rotationMatrix)
            cylRadiusSquared = np.sqrt(np.mean(cylinderAtomsCoordinates[:, 1] ** 2 + cylinderAtomsCoordinates[:, 2] ** 2))
            cylLength = np.abs(np.max(cylinderAtomsCoordinates[:, 0]) - np.min(cylinderAtomsCoordinates[:, 0]))
            cylCenters.append(center)
            cylMatrices.append(rotationMatrix)
            cylRadii.append(cylRadiusSquared)
            cylLengths.append(cylLength)

        return (
         np.array(cylCenters), np.array(cylMatrices), np.array(cylRadii), np.array(cylLengths))

    def __split_trajectory_to_inside_outside__(self, atomTrajectory):
        inside = []
        outside = []
        isIn = False
        isOut = False
        inCylBasisAtomTraj = np.empty(atomTrajectory.shape)
        for idx in range(atomTrajectory.shape[0]):
            center = self._trajectory.boundaryConditions.real_difference((self.cylCenters[idx]), (atomTrajectory[idx]), index=idx)
            inCylCoords = np.dot(center, self.cylMatrices[idx])
            inCylBasisAtomTraj[idx] = inCylCoords + self.cylCenters[idx]
            if np.abs(inCylCoords[0]) > self.cylLengths[idx] / 2.0:
                if isOut:
                    outside[(-1)].append(idx)
                else:
                    outside.append([idx])
                isIn = False
                isOut = True
                continue
            radius = np.sqrt(inCylCoords[1] ** 2 + inCylCoords[2] ** 2)
            if radius < self.cylRadii[idx]:
                if isIn:
                    inside[(-1)].append(idx)
                else:
                    inside.append([idx])
                isIn = True
                isOut = False
            else:
                if isOut:
                    outside[(-1)].append(idx)
                else:
                    outside.append([idx])
                isIn = False
                isOut = True

        return (
         inside, outside, inCylBasisAtomTraj)

    def __get_sub_trajectory_msd__(self, atomSubTrajectory):
        dsq = np.add.reduce(atomSubTrajectory * atomSubTrajectory, 1)
        sum_dsq1 = np.add.accumulate(dsq)
        sum_dsq2 = np.add.accumulate(dsq[::-1])
        sumsq = 2.0 * sum_dsq1[(-1)]
        Saabb = sumsq - np.concatenate(([0.0], sum_dsq1[:-1])) - np.concatenate(([0.0], sum_dsq2[:-1]))
        Saabb = Saabb / (len(dsq) - np.arange(len(dsq)))
        Sab = 2.0 * correlation(atomSubTrajectory)
        return Saabb - Sab

    def step(self, index):
        """
        analysis step of calculation method.

        :Parameters:
            #. atomIndex (int): the atom step index

        :Returns:
            #. stepData (object): object used in combine method
        """
        atomIndex = self.targetAtomsIndexes[index]
        atomTrajectory = self._trajectory.get_atom_trajectory(atomIndex, self.configurationsIndexes)
        inside, outside, inCylBasisAtomTraj = self.__split_trajectory_to_inside_outside__(atomTrajectory)
        element = self.elements[index]
        residencyInside = [
         0, 0]
        residencyOutside = [0, 0]
        axialTraj = np.zeros((inCylBasisAtomTraj.shape[0], 1))
        transTraj = np.zeros((inCylBasisAtomTraj.shape[0], 2))
        for item in inside:
            self.results[('histogram_inside_%s' % element)][int(len(item) / self.histBin)] += 1
            if len(item) == 1:
                continue
            residencyInside[0] += self.results['time'][item[(-1)]] - self.results['time'][item[0]]
            residencyInside[1] += 1
            atomicMSD = self.__get_sub_trajectory_msd__(inCylBasisAtomTraj[item])
            self.results[('msd_inside_%s' % element)][0:atomicMSD.shape[0]] += atomicMSD
            axialTraj[(item, 0)] = inCylBasisAtomTraj[(item, 0)]
            axialAtomicMSD = self.__get_sub_trajectory_msd__(axialTraj[item])
            self.results[('msd_inside_axial_%s' % element)][0:axialAtomicMSD.shape[0]] += axialAtomicMSD
            transTraj[item, 0:] = inCylBasisAtomTraj[item, 1:]
            transAtomicMSD = self.__get_sub_trajectory_msd__(transTraj[item])
            self.results[('msd_inside_transversal_%s' % element)][0:transAtomicMSD.shape[0]] += transAtomicMSD
            self.insideNormalization[element][0:atomicMSD.shape[0]] += 1

        for item in outside:
            self.results[('histogram_outside_%s' % element)][int(len(item) / self.histBin)] += 1
            if len(item) == 1:
                continue
            residencyOutside[0] += self.results['time'][item[(-1)]] - self.results['time'][item[0]]
            residencyOutside[1] += 1
            atomicMSD = self.__get_sub_trajectory_msd__(atomTrajectory[item])
            self.results[('msd_outside_%s' % element)][0:atomicMSD.shape[0]] += atomicMSD
            self.outsideNormalization[element][0:atomicMSD.shape[0]] += 1

        return (index, (residencyInside, residencyOutside))

    def combine(self, index, stepData):
        """
        analysis combine method called after each step.

        :Parameters:
            #. atomIndex (int): the atomIndex of the last calculated atom
            #. stepData (object): the returned data from step method
        """
        element = self.elements[index]
        self.results[('residency_time_inside_%s' % element)][0] += stepData[0][0]
        self.results[('residency_time_inside_%s' % element)][1] += stepData[0][1]
        self.results[('residency_time_outside_%s' % element)][0] += stepData[1][0]
        self.results[('residency_time_outside_%s' % element)][1] += stepData[1][1]

    def finalize(self):
        """
        called once all the steps has been run.

        """
        for el in set(self.elements):
            whereInside = np.where(self.insideNormalization[el] == 0)[0]
            if len(whereInside) == 0:
                self.results[('msd_inside_%s' % el)][:] /= self.insideNormalization[el]
                self.results[('msd_inside_axial_%s' % el)][:] /= self.insideNormalization[el]
                self.results[('msd_inside_transversal_%s' % el)][:] /= self.insideNormalization[el]
            else:
                self.results[('msd_inside_%s' % el)][:whereInside[0]] /= self.insideNormalization[el][:whereInside[0]]
                self.results[('msd_inside_axial_%s' % el)][:whereInside[0]] /= self.insideNormalization[el][:whereInside[0]]
                self.results[('msd_inside_transversal_%s' % el)][:whereInside[0]] /= self.insideNormalization[el][:whereInside[0]]
            whereOutside = np.where(self.outsideNormalization[el] == 0)[0]
            if len(whereOutside) == 0:
                self.results[('msd_outside_%s' % el)][:] /= self.outsideNormalization[el]
            else:
                self.results[('msd_outside_%s' % el)][:whereOutside[0]] /= self.outsideNormalization[el][:whereOutside[0]]

        msdsInside = {}
        msdsAxialInside = {}
        msdsTransInside = {}
        msdsOutside = {}
        for el in set(self.elements):
            msdsInside[el] = self.results[('msd_inside_%s' % el)]
            msdsAxialInside[el] = self.results[('msd_inside_axial_%s' % el)]
            msdsTransInside[el] = self.results[('msd_inside_transversal_%s' % el)]
            msdsOutside[el] = self.results[('msd_outside_%s' % el)]

        self.results['msd_inside_total'] = get_data_weighted_sum(msdsInside, numbers=(self.elementsNumber), weights=(self.elementsWeights))
        self.results['msd_inside_axial_total'] = get_data_weighted_sum(msdsAxialInside, numbers=(self.elementsNumber), weights=(self.elementsWeights))
        self.results['msd_inside_transversal_total'] = get_data_weighted_sum(msdsTransInside, numbers=(self.elementsNumber), weights=(self.elementsWeights))
        self.results['msd_outside_total'] = get_data_weighted_sum(msdsOutside, numbers=(self.elementsNumber), weights=(self.elementsWeights))
        self.results['residency_time_inside_total'] = np.array([0.0])
        self.results['residency_time_outside_total'] = np.array([0.0])
        for el in set(self.elements):
            if self.results[('residency_time_inside_%s' % el)][1] == 0:
                self.results[('residency_time_inside_%s' % el)][1] = 1.0
            if self.results[('residency_time_outside_%s' % el)][1] == 0:
                self.results[('residency_time_outside_%s' % el)][1] = 1.0
            self.results['residency_time_inside_%s' % el] = np.array([self.results[('residency_time_inside_%s' % el)][0] / self.results[('residency_time_inside_%s' % el)][1]])
            self.results['residency_time_outside_%s' % el] = np.array([self.results[('residency_time_outside_%s' % el)][0] / self.results[('residency_time_outside_%s' % el)][1]])
            self.results['residency_time_inside_total'] += self.results[('residency_time_inside_%s' % el)]
            self.results['residency_time_outside_total'] += self.results[('residency_time_outside_%s' % el)]

        self.results['residency_time_inside_total'] /= len(set(self.elements))
        self.results['residency_time_outside_total'] /= len(set(self.elements))
        self.results['histogram_inside_total'] = np.zeros((int(len(self.configurationsIndexes) / self.histBin) + 1), dtype=(np.float))
        self.results['histogram_outside_total'] = np.zeros((int(len(self.configurationsIndexes) / self.histBin) + 1), dtype=(np.float))
        for el in set(self.elements):
            self.results['histogram_inside_total'] += self.results[('histogram_inside_%s' % el)]
            self.results['histogram_outside_total'] += self.results[('histogram_outside_%s' % el)]