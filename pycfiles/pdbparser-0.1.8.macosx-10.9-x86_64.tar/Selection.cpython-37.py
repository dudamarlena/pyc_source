# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Utilities/Selection.py
# Compiled at: 2019-02-16 11:53:48
# Size of source mod 2**32: 7956 bytes
"""
This module contains classes and methods used to select atoms from a pdbparser instance.

.. inheritance-diagram:: pdbparser.Utilities.Selection
    :parts: 2

"""
from __future__ import print_function
import tempfile, os, zipfile, pickle, numpy as np
from pdbparser import pdbparser
from ..log import Logger
from .Geometry import *
from .Information import *
from .BoundaryConditions import PeriodicBoundaries

class Selection(object):
    __doc__ = "\n    The mother class of all selection classes. It can't be initialized.\n    "
    __defaults__ = {}
    __defaults__['pdb'] = None
    __defaults__['indexes'] = None
    __defaults__['selections'] = None
    __defaults__['logMode'] = True
    __defaults__['logEvery'] = 10

    def __new__(cls, *args, **kwargs):
        if cls is Selection:
            raise TypeError('Selection class may not be instantiated')
        return (object.__new__)(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        for kwarg, value in kwargs.items():
            self.__setattr__(kwarg, value)

        self.initialize_default_attributes()
        self.selections = {}

    def __setattr__(self, name, value):
        if name == 'pdb':
            Logger.error('attribute %r is protected, user set_pdb method instead' % name)
            raise
        else:
            object.__setattr__(self, name, value)

    def clear_selection(self):
        """
        clears all selections
        """
        self.selections = {}

    def set_pdb(self, pdb):
        """
        set the pdb for selection.
        indexes are changed automatically to all.

        :Parameters:
            #. pdb (pdbparser): The pdb instance replacing the constructed self.pdb.
        """
        assert isinstance(pdb, pdbparser)
        object.__setattr__(self, 'pdb', pdb)
        self.indexes = self.pdb.indexes

    def initialize_default_attributes(self):
        if not hasattr(self, 'pdb'):
            object.__setattr__(self, 'pdb', pdbparser())
        else:
            if not isinstance(self.pdb, pdbparser):
                raise AssertionError
            elif not hasattr(self, 'indexes'):
                self.indexes = self.pdb.indexes
            else:
                if self.indexes is None:
                    self.indexes = self.pdb.indexes
                else:
                    assert isinstance(self.indexes, (list, tuple))
                    self.indexes = list(self.indexes)
                    self.indexes = sorted(self.indexes)
                    assert self.indexes[0] >= 0
                    assert self.indexes[(-1)] < len(self.pdb)

    def status(self, step, numberOfSteps, stepIncrement=1, mode=True, logEvery=10):
        """
        This method is used to log selection status.

        :Parameters:
            #. step (int): The current step number
            #. numberOfSteps (int): The total number of steps
            #. stepIncrement (int): The incrementation between one step and another
            #. mode (bool): if False no status logging
            #. logEvery (float): the frequency of status logging. its a percent number.
        """
        if not mode:
            return
        if step - 1 == -1:
            return
        actualPercent = int(float(step) / float(numberOfSteps) * 100)
        previousPercent = int(float(step - stepIncrement) / float(numberOfSteps) * 100)
        if actualPercent / logEvery != previousPercent / logEvery:
            Logger.info('%s%% completed. %s left out of %s' % (actualPercent, numberOfSteps - step, numberOfSteps))

    def select(self):
        """
        This is called for selection by default
        """
        return self


class NanotubeSelection(Selection):
    __doc__ = '\n    create selections from a pdb that contains a nanotube\n    '

    def __init__(self, pdb, indexes=None, nanotubeIndexes=None, *args, **kwargs):
        """
        Initialize the PairDistributionFunction analysis.

         :Parameters:
            #. pdb (pdbparser): the pdb to analyse.
            #. indexes (list, tuple, set, numpy.ndarray): list or tuple of the indexes that must be used to calculate the selection.
            #. nanotubeIndexes (list, tuple, set, numpy.ndarray): The nanotube records indexes
        """
        self.set_pdb(pdb)
        self.indexes = indexes
        self.nanotubeIndexes = nanotubeIndexes
        (super(NanotubeSelection, self).__init__)(*args, **kwargs)
        self.initialize()

    def initialize(self):
        self.get_nanotube_indexes(self.nanotubeIndexes)
        if self.indexes is None:
            self.indexes = self.pdb.indexes
        self.indexes = list(set(self.indexes) - set(self.nanotubeIndexes))

    def set_pdb(self, pdb):
        super(NanotubeSelection, self).set_pdb(pdb)
        self.nanotubeIndexes = None
        self.indexes = None
        self.initialize()

    def get_nanotube_indexes(self, indexes=None):
        """
        get the nanotube records indexes.

         :Parameters:
            #. indexes (None, list, tuple, set, numpy.ndarray): the records indexes.
            If None records are calculated automatically when nanotube residue_name is 'CNT'.
        """
        if indexes is None:
            self.nanotubeIndexes = get_records_indexes_in_attribute_values(self.pdb.indexes, self.pdb, 'residue_name', 'CNT')
            self.nanotubeIndexes or Logger.error('nanotube records indexes must be given.')
            raise
        else:
            self.nanotubeIndexes = indexes

    def select_inside_nanotube(self):
        """
        get inside and outside nanotube's records indexes
        """
        center, _, _, _, vect1, vect2, vect3 = get_principal_axis(self.nanotubeIndexes, self.pdb)
        rotationMatrix = np.linalg.inv(np.transpose([vect1, vect2, vect3]))
        translate(self.pdb.indexes, self.pdb, -1 * np.array(center))
        rotate(self.pdb.indexes, self.pdb, rotationMatrix)
        minX, maxX, minY, maxY, minZ, maxZ = get_min_max(self.nanotubeIndexes, self.pdb)
        cntCoordinates = self.pdb.coordinates[self.nanotubeIndexes]
        radius = np.min([np.abs(maxY - minY), np.abs(maxZ - minZ)]) / 2.0
        insideIndexes = set(get_satisfactory_records_indexes(self.indexes, self.pdb, 'x>%s' % minX))
        insideIndexes = insideIndexes.intersection(set(get_satisfactory_records_indexes(self.indexes, self.pdb, 'x<%s' % maxX)))
        insideIndexes = insideIndexes.intersection(set(get_satisfactory_records_indexes(self.indexes, self.pdb, 'y>%s' % minY)))
        self.selections['inside_nanotube'] = list(insideIndexes.intersection(set(get_satisfactory_records_indexes(self.indexes, self.pdb, 'y**2+z**2<%s' % radius ** 2))))
        self.selections['outside_nanotube'] = list(set(self.indexes) - set(self.selections['inside_nanotube']))
        self.selections['nanotube'] = self.nanotubeIndexes
        return self

    def select_outside_nanotube(self):
        self.select_inside_nanotube()
        return self

    def select(self):
        self.select_inside_nanotube()
        return self