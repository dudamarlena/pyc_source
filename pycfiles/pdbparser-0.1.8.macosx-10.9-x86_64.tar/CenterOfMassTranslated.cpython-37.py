# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Analysis/Trajectory/CenterOfMassTranslated.py
# Compiled at: 2019-02-16 11:55:48
# Size of source mod 2**32: 3068 bytes
"""
This module provides classes to correct and export new trajectories.

.. inheritance-diagram:: pdbparser.Analysis.Trajectory.CenterOfMassTranslated
    :parts: 2
"""
from __future__ import print_function
from collections import Counter
import numpy as np
from pdbparser.log import Logger
from pdbparser.Analysis.Core import Analysis, AxisDefinition, CenterDefinition
from pdbparser.Utilities.Database import get_element_property, is_element_property

class CenterOfMassTranslated(Analysis):
    __doc__ = '\n    Computes the global center of mass translated trajectory.\n    '

    def __init__(self, trajectory, configurationsIndexes, center, fold=True, *args, **kwargs):
        (super(CenterOfMassTranslated, self).__init__)(trajectory, *args, **kwargs)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        self.numberOfSteps = len(self.configurationsIndexes)
        self.__initialize_variables__(center, fold)
        self.__initialize_results__()

    def __initialize_variables__(self, center, fold):
        assert isinstance(fold, bool), Logger.error('fold must be boolean')
        self.fold = fold
        self.center = CenterDefinition(self._trajectory, center)

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
        confIdx = self.configurationsIndexes[index]
        self._trajectory.set_configuration_index(confIdx)
        coordinates = self._trajectory.get_configuration_coordinates(confIdx)
        COM = self.center.get_center(coordinates)
        coordinates += self._trajectory._boundaryConditions.get_box_real_center(index=confIdx) - COM
        if self.fold:
            coordinates = self._trajectory._boundaryConditions.fold_real_array(coordinates, index=confIdx)
        self._trajectory.set_configuration_coordinates(confIdx, coordinates)
        return (
         index, None)

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