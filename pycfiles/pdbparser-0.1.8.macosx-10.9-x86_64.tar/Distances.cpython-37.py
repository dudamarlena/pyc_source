# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Analysis/Structure/Distances.py
# Compiled at: 2019-02-16 11:56:00
# Size of source mod 2**32: 6668 bytes
"""
This module provides classes to analyse distances

.. inheritance-diagram:: pdbparser.Analysis.Structure.Distances
    :parts: 2

"""
from __future__ import print_function
from collections import Counter
import numpy as np
from pdbparser.log import Logger
from pdbparser.Analysis.Core import Analysis, AxisDefinition
from pdbparser.Utilities.Database import get_element_property, is_element_property

class InsideCylinderDistances(Analysis):
    __doc__ = '\n    Computes the mean minimum distance between two atoms subset.\n    '

    def __init__(self, trajectory, configurationsIndexes, cylinderAtomsIndexes, targetAtomsIndexes, axis=None, *args, **kwargs):
        (super(InsideCylinderDistances, self).__init__)(trajectory, *args, **kwargs)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        self.numberOfSteps = len(self.configurationsIndexes)
        self.targetAtomsIndexes = self.get_atoms_indexes(targetAtomsIndexes)
        self.cylinderAtomsIndexes = self.get_atoms_indexes(cylinderAtomsIndexes)
        self.__initialize_variables__(axis)
        self.__initialize_results__()

    def __initialize_variables__(self, axis):
        if len(set.intersection(set(self.cylinderAtomsIndexes), set(self.targetAtomsIndexes))):
            raise AssertionError(Logger.error("cylinderAtomsIndexes and targetAtomsIndexes can't have any index in common"))
        if axis is None:
            axis = {'principal': self.cylinderAtomsIndexes}
        self.axis = AxisDefinition(self._trajectory, axis)

    def __initialize_results__(self):
        self.results['time'] = np.array([self.time[idx] for idx in self.configurationsIndexes], dtype=(np.float))
        self.results['mean_minimum_distance'] = np.zeros((self.numberOfSteps), dtype=(np.float))
        self.results['minimum_distance'] = np.zeros((self.numberOfSteps), dtype=(np.float))
        self.results['mean_shell_thickness'] = np.zeros((self.numberOfSteps), dtype=(np.float))
        self.results['cylinder_radius'] = np.zeros((self.numberOfSteps), dtype=(np.float))

    def step(self, index):
        """"
        analysis step of calculation method.

        :Parameters:
            #. index (int): the step index

        :Returns:
            #. stepData (object): object used in combine method
        """
        confIdx = self.configurationsIndexes[index]
        self._trajectory.set_configuration_index(confIdx)
        coordinates = self._trajectory.get_configuration_coordinates(confIdx)
        targetAtomsCoordinates = coordinates[self.targetAtomsIndexes]
        cylinderAtomsCoordinates = coordinates[self.cylinderAtomsIndexes]
        center, rotationMatrix = self.axis.get_center_rotationMatrix(coordinates)
        targetAtomsCoordinates -= center
        cylinderAtomsCoordinates -= center
        targetAtomsCoordinates = np.dot(targetAtomsCoordinates, rotationMatrix)
        cylinderAtomsCoordinates = np.dot(cylinderAtomsCoordinates, rotationMatrix)
        cylRadiusSquared = np.mean(cylinderAtomsCoordinates[:, 1] ** 2 + cylinderAtomsCoordinates[:, 2] ** 2)
        cylLength = np.abs(np.max(cylinderAtomsCoordinates[:, 0]) - np.min(cylinderAtomsCoordinates[:, 0]))
        radiiSquared = targetAtomsCoordinates[:, 1] ** 2 + targetAtomsCoordinates[:, 2] ** 2
        outOfLengthIdx = list(np.nonzero(targetAtomsCoordinates[:, 0] < -cylLength / 2.0)[0])
        outOfLengthIdx += list(np.nonzero(targetAtomsCoordinates[:, 0] > cylLength / 2.0)[0])
        outOfLengthIdx = set(outOfLengthIdx)
        outOfRadiusIdx = set(np.nonzero(radiiSquared > cylRadiusSquared)[0])
        indexes = set(range(len(self.targetAtomsIndexes)))
        indexes -= outOfLengthIdx
        indexes -= outOfRadiusIdx
        indexes = list(indexes)
        targetAtomsCoordinates = targetAtomsCoordinates[indexes, :]
        return (
         index, (cylinderAtomsCoordinates, targetAtomsCoordinates, np.sqrt(cylRadiusSquared), cylLength))

    def combine(self, index, stepData):
        """
        analysis combine method called after each step.

        :Parameters:
            #. index (int): the index of the last calculated step
            #. stepData (object): the returned data from step method
        """
        cylinderAtomsCoordinates = stepData[0]
        targetAtomsCoordinates = stepData[1]
        cylRadius = stepData[2]
        cylLength = stepData[3]
        self.results['cylinder_radius'][index] = cylRadius
        if not len(targetAtomsCoordinates):
            self.results['mean_minimum_distance'][index] = np.nan
            self.results['minimum_distance'][index] = np.nan
        else:
            distances = np.zeros(cylinderAtomsCoordinates.shape[0])
            for ntIndex in range(cylinderAtomsCoordinates.shape[0]):
                difference = targetAtomsCoordinates - cylinderAtomsCoordinates[ntIndex, :]
                distances[ntIndex] = np.sqrt(np.min(np.add.reduce(difference ** 2, 1)))

            self.results['mean_minimum_distance'][index] = np.mean(distances)
            self.results['minimum_distance'][index] = np.min(distances)
        targetAtomsDistances = np.sqrt(np.add.reduce(targetAtomsCoordinates[:, 1:3] ** 2, 1))
        self.results['mean_shell_thickness'][index] = np.mean(targetAtomsDistances)

    def finalize(self):
        """
        called once all the steps has been run.

        """
        pass