# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Analysis/Structure/SolventAccessibleSurfaceArea.py
# Compiled at: 2019-02-16 12:15:09
# Size of source mod 2**32: 10672 bytes
"""
This module provides all solvent accessible surface area analysis classes.

.. inheritance-diagram:: pdbparser.Analysis.Structure.SolventAccessibleSurfaceArea
    :parts: 2
"""
from __future__ import print_function
import os, atexit, copy, numpy as np
from pdbparser.log import Logger
from pdbparser.Analysis.Core import Analysis
from pdbparser.Utilities.Information import get_records_database_property_values
from pdbparser.Utilities.Collection import is_number, generate_sphere_points

class _AtomsData(object):

    def __init__(self, tempdir=None):
        self._AtomsData__tempdir = tempdir
        if tempdir is None:
            self._AtomsData__dirExists = True
        else:
            if not isinstance(tempdir, str):
                raise AssertionError('tempdir must be a string')
            elif os.path.isdir(tempdir):
                self._AtomsData__dirExists = True
            else:
                self._AtomsData__dirExists = False
                os.makedirs(tempdir)
            atexit.register(self.on_exit)
        self._AtomsData__data = {}
        self._AtomsData__points = {}
        self._AtomsData__radius = {}

    def __get_sphere_points(self, radius, resolution, center):
        if radius not in self._AtomsData__data:
            surface = 4.0 * np.pi * radius ** 2
            npoints = int(np.ceil(surface / resolution))
            self._AtomsData__data[radius] = np.array(generate_sphere_points(radius=radius, nPoints=npoints, center=center)).astype(float)
        return self._AtomsData__data[radius]

    def get(self, idx, radius, center, resolution):
        if idx not in self._AtomsData__points:
            points = self._AtomsData__get_sphere_points(radius=radius, resolution=resolution, center=[0, 0, 0]) + center
            if self._AtomsData__tempdir is None:
                self._AtomsData__points[idx] = points
            else:
                pointsPath = os.path.join(self._AtomsData__tempdir, '%i_points' % idx)
                np.save(pointsPath, points)
                self._AtomsData__points[idx] = pointsPath + '.npy'
            self._AtomsData__radius[idx] = radius
        else:
            if self._AtomsData__tempdir is not None:
                points = np.load(self._AtomsData__points[idx])
            else:
                points = self._AtomsData__points[idx]
        return (
         self._AtomsData__radius[idx], points)

    def get_copy(self, idx, radius, center, resolution):
        radius, points = self.get(idx=idx, radius=radius, center=center, resolution=resolution)
        if self._AtomsData__tempdir is None:
            points = copy.deepcopy(points)
        return (
         radius, points)

    def update(self, idx, points):
        if not idx in self._AtomsData__points:
            raise AssertionError('points for atom %i are not defined' % idx)
        elif self._AtomsData__tempdir is None:
            self._AtomsData__points[idx] = points
        else:
            np.save(self._AtomsData__points[idx], points)

    def get_all_points(self):
        points = list(self._AtomsData__points.values())
        if self._AtomsData__tempdir is not None:
            points = [np.load(path) for path in points]
        return np.concatenate(points, axis=0)

    def number_of_points(self):
        points = list(self._AtomsData__points.values())
        if self._AtomsData__tempdir is None:
            pointsLen = [v.shape[0] for v in points]
        else:
            pointsLen = [np.load(path).shape[0] for path in points]
        return sum(pointsLen)

    def reset(self):
        if self._AtomsData__tempdir is not None:
            [os.remove(path) for path in self._AtomsData__points.values()]
        self._AtomsData__data = {}
        self._AtomsData__points = {}
        self._AtomsData__radius = {}

    def on_exit(self):
        self.reset()
        if not self._AtomsData__dirExists:
            os.rmdir(self._AtomsData__tempdir)


class SolventAccessibleSurfaceArea(Analysis):
    __doc__ = '\n    '

    def __init__(self, trajectory, configurationsIndexes, targetAtomsIndexes, atomsRadius='vdwRadius', makeContiguous=False, probeRadius=1.5, resolution=0.5, storeSurfacePoints=False, tempdir=None, *args, **kwargs):
        (super(SolventAccessibleSurfaceArea, self).__init__)(trajectory, *args, **kwargs)
        self.targetAtomsIndexes = self.get_atoms_indexes(targetAtomsIndexes)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        self.numberOfSteps = len(self.configurationsIndexes)
        self.__initialize_variables__(makeContiguous=makeContiguous, atomsRadius=atomsRadius,
          probeRadius=probeRadius,
          resolution=resolution,
          storeSurfacePoints=storeSurfacePoints,
          tempdir=tempdir)
        self.__initialize_results__()

    def __initialize_variables__(self, makeContiguous, atomsRadius, probeRadius, resolution, storeSurfacePoints, tempdir):
        assert isinstance(makeContiguous, bool), 'makeContiguous must be boolean'
        self._SolventAccessibleSurfaceArea__makeContiguous = makeContiguous
        assert is_number(probeRadius), 'probeRadius must be a number'
        probeRadius = float(probeRadius)
        assert probeRadius >= 0, 'probeRadius must be bigger or equal to 0'
        if isinstance(atomsRadius, str):
            atomsRadius = get_records_database_property_values(indexes=(self.targetAtomsIndexes), pdb=(self.structure), property=atomsRadius)
        assert len(atomsRadius) == len(self.targetAtomsIndexes), 'atomsRadius must have the same number of input as target atoms'
        assert all([is_number(v) for v in atomsRadius]), 'all atomsRadius must be numbers'
        atomsRadius = [float(v) for v in atomsRadius]
        assert all([v > 0 for v in atomsRadius]), 'all atomsRadius must be >0'
        self._SolventAccessibleSurfaceArea__atomsRadius = np.array(atomsRadius).astype(float) + probeRadius
        self._SolventAccessibleSurfaceArea__atomsData = _AtomsData(tempdir=tempdir)
        assert is_number(resolution), 'resolution must be a number'
        resolution = float(resolution)
        assert resolution > 0, 'resolution must be > 0'
        self._SolventAccessibleSurfaceArea__resolution = resolution
        assert isinstance(storeSurfacePoints, bool), 'storeSurfacePoints must be boolean'
        self._SolventAccessibleSurfaceArea__storeSurfacePoints = storeSurfacePoints

    def __initialize_results__(self):
        self.results['time'] = np.array([self.time[idx] for idx in self.configurationsIndexes], dtype=(np.float))
        self.results['sasa'] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
        self.results['surface points'] = []

    @property
    def atomsData(self):
        return self._SolventAccessibleSurfaceArea__atomsData

    def step(self, index):
        """
        analysis step of calculation method.

        :Parameters:
            #. atomIndex (int): the atom step index

        :Returns:
            #. stepData (object): object used in combine method
        """
        self._SolventAccessibleSurfaceArea__atomsData.reset()
        confIdx = self.configurationsIndexes[index]
        self._trajectory.set_configuration_index(confIdx)
        if self._SolventAccessibleSurfaceArea__makeContiguous:
            coordinates = self._trajectory.get_contiguous_configuration_coordinates(confIdx)
        else:
            coordinates = self._trajectory.get_configuration_coordinates(confIdx)
        coordinates = coordinates[self.targetAtomsIndexes]
        for idx0 in range(coordinates.shape[0] - 1):
            center0 = coordinates[idx0, :]
            radius0, sphere0 = self._SolventAccessibleSurfaceArea__atomsData.get_copy(idx=idx0, radius=(self._SolventAccessibleSurfaceArea__atomsRadius[idx0]), center=center0, resolution=(self._SolventAccessibleSurfaceArea__resolution))
            nPoints0 = sphere0.shape[0]
            diff = coordinates[idx0 + 1:, :] - center0
            dist = np.sqrt(np.sum((diff ** 2), axis=1))
            comp = self._SolventAccessibleSurfaceArea__atomsRadius[idx0 + 1:] + self._SolventAccessibleSurfaceArea__atomsRadius[idx0]
            ddif = dist - comp
            for i, dval in enumerate(ddif):
                if dval > 0:
                    continue
                idx1 = i + idx0 + 1
                tolerance = self._SolventAccessibleSurfaceArea__atomsRadius[idx0] + self._SolventAccessibleSurfaceArea__atomsRadius[idx1]
                center1 = coordinates[idx1, :]
                radius1, sphere1 = self._SolventAccessibleSurfaceArea__atomsData.get_copy(idx=idx1, radius=(self._SolventAccessibleSurfaceArea__atomsRadius[idx1]), center=center1, resolution=(self._SolventAccessibleSurfaceArea__resolution))
                nPoints1 = sphere1.shape[0]
                dist0 = np.sqrt(np.sum(((sphere0 - center1) ** 2), axis=1))
                sphere0 = sphere0[dist0 > radius1, :]
                dist1 = np.sqrt(np.sum(((sphere1 - center0) ** 2), axis=1))
                sphere1 = sphere1[dist1 > radius0, :]
                if nPoints1 > sphere1.shape[0]:
                    self._SolventAccessibleSurfaceArea__atomsData.update(idx1, sphere1)

            if nPoints0 > sphere0.shape[0]:
                self._SolventAccessibleSurfaceArea__atomsData.update(idx0, sphere0)

        sasa = self._SolventAccessibleSurfaceArea__atomsData.number_of_points() * self._SolventAccessibleSurfaceArea__resolution
        surfacePoints = None
        if self._SolventAccessibleSurfaceArea__storeSurfacePoints:
            surfacePoints = self._SolventAccessibleSurfaceArea__atomsData.get_all_points()
        return (
         index, (sasa, surfacePoints))

    def combine(self, index, stepData):
        """
        analysis combine method called after each step.

        :Parameters:
            #. atomIndex (int): the atomIndex of the last calculated atom
            #. stepData (object): the returned data from step method
        """
        self.results['sasa'][index] = stepData[0]
        self.results['surface points'].append(stepData[1])

    def finalize(self):
        """
        called once all the steps has been run.

        """
        pass