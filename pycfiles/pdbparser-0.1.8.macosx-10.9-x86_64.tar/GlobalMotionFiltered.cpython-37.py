# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Analysis/Trajectory/GlobalMotionFiltered.py
# Compiled at: 2019-02-16 11:55:52
# Size of source mod 2**32: 4403 bytes
"""
This module provides classes to correct global motion and export new trajectories.

.. inheritance-diagram:: pdbparser.Analysis.Trajectory.GlobalMotionFiltered
    :parts: 2
"""
from __future__ import print_function
import numpy as np
from pdbparser.log import Logger
from pdbparser.Analysis.Core import Analysis
from pdbparser.Utilities.Math import get_superposition_transformation_elements
from pdbparser.Utilities.Information import get_records_database_property_values
from pdbparser.Utilities.BoundaryConditions import InfiniteBoundaries

class GlobalMotionFiltered(Analysis):
    __doc__ = '\n    Computes the global motion filtered trajectory.\n    '

    def __init__(self, trajectory, configurationsIndexes, globalMotionAtomsIndexes, targetAtomsIndexes, *args, **kwargs):
        (super(GlobalMotionFiltered, self).__init__)(trajectory, *args, **kwargs)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        self.numberOfSteps = len(self.configurationsIndexes)
        self.globalMotionAtomsIndexes = self.get_atoms_indexes(globalMotionAtomsIndexes)
        self.targetAtomsIndexes = self.get_atoms_indexes(globalMotionAtomsIndexes)
        self.__initialize_variables__()
        self.__initialize_results__()

    def __initialize_variables__(self):
        self.weights = np.array(get_records_database_property_values(self.globalMotionAtomsIndexes, self.structure, 'atomicWeight'))
        self.totalWeight = np.sum(self.weights)

    def __initialize_results__(self):
        pass

    def step(self, index):
        """"
        analysis step of calculation method.

        :Parameters:
            #. index (int): the step index

        :Returns:
            #. stepData (object): object used in combine method
        """
        if index == 0:
            return (
             index, None)
        confIdx = self.configurationsIndexes[index]
        refConfIdx = self.configurationsIndexes[(index - 1)]
        coordinates = self._trajectory.get_configuration_coordinates(confIdx)
        coords = coordinates[self.globalMotionAtomsIndexes, :]
        refCoords = self._trajectory.get_configuration_coordinates(refConfIdx)[self.globalMotionAtomsIndexes, :]
        rotationMatrix, refCoordsCOM, coordsCOM, rms = get_superposition_transformation_elements(self.weights, self.totalWeight, refCoords, coords)
        coordinates[self.targetAtomsIndexes] -= coordsCOM
        coordinates[self.targetAtomsIndexes] = np.dot(rotationMatrix, np.transpose(coordinates[self.targetAtomsIndexes]).reshape(1, 3, -1)).transpose().reshape(-1, 3)
        coordinates[self.targetAtomsIndexes] += refCoordsCOM
        self._trajectory.set_configuration_coordinates(confIdx, coordinates)
        return (index, None)

    def combine(self, index, stepData):
        pass

    def finalize(self):
        indexesToRemove = list(set(self._trajectory.indexes) - set(self.configurationsIndexes))
        if len(indexesToRemove) > 1:
            subs = 1 + np.arange(len(indexesToRemove) - 1)
            indexesToRemove = np.array(indexesToRemove)
            indexesToRemove[1:] -= subs
        for idx in list(indexesToRemove):
            self._trajectory.remove_configuration(idx)

        atomsIndexes = list(set(self._trajectory.atomsIndexes) - set(self.targetAtomsIndexes))
        self._trajectory.remove_atoms(atomsIndexes)
        bc = InfiniteBoundaries()
        for idx in self._trajectory.indexes:
            bc.set_vectors()

        self._trajectory._boundaryConditions = bc