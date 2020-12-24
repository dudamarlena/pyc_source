# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/IO/TrajectoryConverter.py
# Compiled at: 2019-02-16 11:54:46
# Size of source mod 2**32: 6172 bytes
"""
This module provides classes to convert molecular dynamics simulation outputs to pdbTrajectory

.. inheritance-diagram:: pdbparser.IO.TrajectoryConverter
    :parts: 2

"""
from __future__ import print_function
import numpy as np
from pdbparser.pdbparser import pdbTrajectory
from pdbparser.IO.Core import Converter, DCDFile
from pdbparser.Utilities.BoundaryConditions import InfiniteBoundaries, PeriodicBoundaries
from pdbparser.log import Logger

class DCDConverter(Converter):

    def __init__(self, pdb, dcd, indexes=None, format='charmm'):
        """
        Read new simulation trajectory

        :Parameters:
            #. pdb (string): NAMD pdb file used as trajectory structure file
            #. dcd (string): NAMD DCD output file
            #. indexes (list): the configuration indexes to convert. None converts all configurations
            #. format (string): the known formats. only charmm and dcd are supported.
        """
        super(DCDConverter, self).__init__()
        Logger.info('Converting NAMD trajectory')
        Logger.info('pdb file path: %s' % pdb)
        Logger.info('dcd file path: %s' % dcd)
        assert isinstance(format, str), Logger.error('format must be a string')
        self.format = str(format).lower()
        assert self.format in ('charmm', 'namd'), Logger.error('format must be either charmm or namd')
        if indexes is not None:
            assert isinstance(indexes, (list, tuple, set, np.ndarray)), Logger.error('indexes must be a list of 3 integers [start, end, step]')
            indexes = [int(idx) for idx in sorted(set(indexes))]
            assert indexes[0] >= 0, Logger.error('indexes start must be positive')
        self.indexes = indexes
        try:
            fd = open(pdb, 'r')
        except:
            raise Logger.error('cannot open pdb file')
        else:
            fd.close()
            self.pdb = pdb
        try:
            fd = open(dcd, 'r')
        except:
            raise Logger.error('cannot open dcd file')
        else:
            fd.close()
            self.dcd = dcd
        self.trajectory = None

    def __unit_cell_to_basis_vectors__(self, a, b, c, alpha, beta, gamma):
        X = np.array([a, 0.0, 0.0])
        Y = b * np.array([np.cos(gamma), np.sin(gamma), 0.0])
        Zx = np.cos(beta)
        Zy = (np.cos(alpha) - np.cos(beta) * np.cos(gamma)) / np.sin(gamma)
        Zz = np.sqrt(1.0 - Zx ** 2 - Zy ** 2)
        Z = c * np.array([Zx, Zy, Zz])
        return np.array((X, Y, Z))

    def __convert_charmm__(self):
        traj = pdbTrajectory()
        traj.set_structure(self.pdb)
        dcd = DCDFile(self.dcd)
        if dcd.has_pbc_data:
            traj._boundaryConditions = PeriodicBoundaries()
        else:
            traj._boundaryConditions = InfiniteBoundaries()
        if self.indexes is None:
            self.indexes = range(dcd.numberOfConfigurations)
        else:
            if self.indexes[(-1)] >= dcd.numberOfConfigurations:
                Logger.warn("Some of the given indexes exceed '%s' which is the number of configurations in dcd file" % dcd.numberOfConfigurations)
                self.indexes = [index for index in self.indexes if index < dcd.numberOfConfigurations]
        assert dcd.natoms == traj.numberOfAtoms, Logger.error('pdb file and dcd file must have the same number of atoms')
        step = dcd.istart
        stepIncrement = dcd.nsavc
        dt = np.around(dcd.delta, 6)
        info = {}
        info['software'] = 'charmm'
        info['software_version'] = dcd.charmmVersion
        traj._info = info
        self.status(0, dcd.fileSize)
        confIdx = -1
        while self.indexes:
            confIdx += 1
            if isinstance(self.indexes, list):
                idx = self.indexes.pop(0)
            else:
                idx = confIdx
            while confIdx < idx:
                try:
                    dcd.skip_step()
                except:
                    Logger.warn('file reading ended unexpectedly. Trajectory conversion stopped. all recorded data are still valid')
                    break

                confIdx += 1

            try:
                unit_cell, x, y, z = dcd.read_step()
            except:
                Logger.warn('file reading ended unexpectedly. Trajectory conversion stopped. all recorded data are still valid')
                break

            traj._coordinates.append(np.transpose([x, y, z]))
            if dcd.has_pbc_data:
                traj._boundaryConditions.set_vectors((self.__unit_cell_to_basis_vectors__)(*unit_cell))
            else:
                traj._boundaryConditions.set_vectors()
            traj._time.append(confIdx * stepIncrement * dt)
            self.status(dcd.currentPosition, dcd.fileSize)

        return traj

    def convert(self):
        if self.format in ('charmm', 'namd'):
            self.trajectory = self.__convert_charmm__()
        else:
            raise Logger.error('unsupported dcd format')
        self.trajectory._filePath = self.dcd
        return self.trajectory