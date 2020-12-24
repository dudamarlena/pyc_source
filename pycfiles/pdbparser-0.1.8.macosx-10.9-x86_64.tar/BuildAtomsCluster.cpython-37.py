# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Analysis/Trajectory/BuildAtomsCluster.py
# Compiled at: 2019-02-16 11:55:45
# Size of source mod 2**32: 4765 bytes
"""
This module provides trajectory rebuilding atoms clusters analysis

.. inheritance-diagram:: pdbparser.Analysis.Trajectory.BuildAtomsCluster
    :parts: 2

"""
from __future__ import print_function
import numpy as np
from pdbparser.log import Logger
from pdbparser.Analysis.Core import Analysis
from pdbparser.Utilities.Math import get_superposition_transformation_elements
from pdbparser.Utilities.Information import get_records_database_property_values
from pdbparser.Utilities.BoundaryConditions import PeriodicBoundaries

class BuildAtomsCluster(Analysis):
    __doc__ = '\n    Build atoms cluster trajectory.\n    '

    def __init__(self, trajectory, configurationsIndexes, clusterIndexes, clusterToBoxCenter=True, fold=True, *args, **kwargs):
        (super(BuildAtomsCluster, self).__init__)(trajectory, *args, **kwargs)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        self.numberOfSteps = len(self.configurationsIndexes)
        self.clusterIndexes = self.get_atoms_indexes(clusterIndexes)
        self.__initialize_variables__(clusterToBoxCenter, fold)

    def __initialize_variables__(self, clusterToBoxCenter, fold):
        self.restOfAtomsIndexes = list(set(self._trajectory.atomsIndexes) - set(self.clusterIndexes))
        assert isinstance(clusterToBoxCenter, bool), Logger.error('clusterToBoxCenter must be boolean')
        self.clusterToBoxCenter = clusterToBoxCenter
        assert isinstance(fold, bool), Logger.error('fold must be boolean')
        self.fold = fold

    def step(self, index):
        """"
        analysis step of calculation method.

        :Parameters:
            #. index (int): the step index

        :Returns:
            #. stepData (object): object used in combine method
        """
        if not isinstance(self._trajectory._boundaryConditions, PeriodicBoundaries):
            raise Logger.error('rebuild cluster is not possible with infinite boundaries trajectory')
        confIdx = self.configurationsIndexes[index]
        boxCoords = self._trajectory.get_configuration_coordinates(confIdx)
        boxCoords = self._trajectory._boundaryConditions.real_to_box_array(realArray=boxCoords, index=confIdx)
        clusterBoxCoords = boxCoords[self.clusterIndexes, :]
        incrementalCenter = np.array([0.0, 0.0, 0.0])
        centerNumberOfAtoms = 0.0
        for idx in range(clusterBoxCoords.shape[0]):
            if idx > 0:
                diff = clusterBoxCoords[idx, :] - incrementalCenter / centerNumberOfAtoms
                intDiff = diff.astype(int)
                clusterBoxCoords[idx, :] -= intDiff
                diff -= intDiff
                clusterBoxCoords[idx, :] = np.where(np.abs(diff) < 0.5, clusterBoxCoords[idx, :], clusterBoxCoords[idx, :] - np.sign(diff))
            incrementalCenter += clusterBoxCoords[idx, :]
            centerNumberOfAtoms += 1.0

        boxCoords[self.clusterIndexes, :] = clusterBoxCoords
        if self.clusterToBoxCenter:
            center = np.sum(clusterBoxCoords, 0) / len(self.clusterIndexes)
            boxCoords += np.array([0.5, 0.5, 0.5]) - center
        if self.fold:
            boxCoords[self.restOfAtomsIndexes, :] %= 1
        coords = self._trajectory._boundaryConditions.box_to_real_array(boxArray=boxCoords, index=confIdx)
        self._trajectory.set_configuration_coordinates(confIdx, coords)
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