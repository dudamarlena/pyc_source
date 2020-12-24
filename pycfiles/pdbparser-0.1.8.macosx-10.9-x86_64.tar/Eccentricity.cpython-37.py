# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Analysis/Structure/Eccentricity.py
# Compiled at: 2019-02-16 11:56:02
# Size of source mod 2**32: 10667 bytes
"""
This moldule provides the Eccentricity analysis

.. inheritance-diagram:: pdbparser.Analysis.Structure.Eccentricity
    :parts: 2

"""
from __future__ import print_function
import numpy as np
from pdbparser.log import Logger
from pdbparser.Analysis.Core import Analysis
from pdbparser.Utilities.Information import get_records_database_property_values

class Eccentricity(Analysis):
    __doc__ = "\n    **Short description:**\n\n    Computes the eccentricity for a set of atoms.\n\n\n    **Calculation:** \n\n    Eccentricity is calculated using the inertia principal axes 'I' along x, y and z: \n\n    .. math:: Eccentricity = 1-\\frac{I_{min}}{I_{average}}\n\n    The ratio of largest to smallest is between the biggest inertia to the smallest \n\n    .. math:: ratio = \\frac{Imax}{Imin}\n\n    The semiaxes a,b and c are those of an ellipsoid \n\n    .. math:: semiaxis_a = \\sqrt{ \\frac{5}{2M} (I_{max}+I_{mid}-I_{min}) }\n    .. math:: semiaxis_b = \\sqrt{ \\frac{5}{2M} (I_{max}+I_{min}-I_{mid}) }\n    .. math:: semiaxis_c = \\sqrt{ \\frac{5}{2M} (I_{mid}+I_{min}-I_{max}) }\n\n    Where:\n\n        - M is the total mass of all the selected atoms\n        - :math:`I_{min}` , :math:`I_{mid}` and :math:`I_{max}` are respectively the smallest, the middle and the biggest inertia moment value\n\n\n    **Output:** \n\n    #. moment_of_inertia_xx: the moment of inertia in x direction acting on the surface element with its vector normal in x direction\n    #. moment_of_inertia_xy: the moment of inertia in y direction acting on the surface element with its vector normal in x direction\n    #. moment_of_inertia_xz: the moment of inertia in z direction acting on the surface element with its vector normal in x direction\n    #. moment_of_inertia_yy: the moment of inertia in y direction acting on the surface element with its vector normal in y direction\n    #. moment_of_inertia_yz: the moment of inertia in z direction acting on the surface element with its vector normal in y direction\n    #. moment_of_inertia_zz: the moment of inertia in z direction acting on the surface element with its vector normal in z direction\n    #. semiaxis_a: ellipse biggest axis\n    #. semiaxis_b: ellipse middle axis\n    #. semiaxis_c: ellipse smallest axis\n    #. ratio_of_largest_to_smallest\n    #. eccentricity\n    #. radius_of_gyration\n\n\n    **Usage:** \n\n    This analysis can be used to study macro-molecules geometry and sphericity .\n    Originally conceived to calculate the sphericity of micelles.\n\n    **Acknowledgement and publication:**\n\n    AOUN Bachir\n\n    **Job input parameters:** \n\n    +------------------------+------------------------+---------------------------------------------+\n    | Parameter              | Default                | Description                                 |\n    +========================+========================+=============================================+\n    | trajectory             |                        | MMTK trajectory path                        |\n    +------------------------+------------------------+---------------------------------------------+\n    | frames                 | '0:100:1'              | selected frames to perform the calculation  |\n    +------------------------+------------------------+---------------------------------------------+\n    | running_mode           | 'local:1'              | the job host and number of processors       |\n    +------------------------+------------------------+---------------------------------------------+\n    | output_file            | 'output_file'          | the analysis output file path               |\n    +------------------------+------------------------+---------------------------------------------+\n    | output_file_formats    | ['ascii','netcdf']     | the analysis output files formats the user  |\n    |                        |                        | wishes to export at the end of the analysis |\n    +------------------------+------------------------+---------------------------------------------+\n    | atom_selection         |                        | atoms selection formula as defined in       |\n    |                        |                        | nmoldyn, used to calculate the moment of    |\n    |                        |                        | inertia                                     |\n    +------------------------+------------------------+---------------------------------------------+\n    | center_of_mass         |                        | atoms selection formula as defined in       |\n    |                        |                        | nmoldyn, used to calculate the total mass   |\n    |                        |                        | of the system                               |\n    +------------------------+------------------------+---------------------------------------------+\n    "

    def __init__(self, trajectory, configurationsIndexes, targetAtomsIndexes, *args, **kwargs):
        (super(Eccentricity, self).__init__)(trajectory, *args, **kwargs)
        self.configurationsIndexes = self.get_trajectory_indexes(configurationsIndexes)
        self.numberOfSteps = len(self.configurationsIndexes)
        self.targetAtomsIndexes = self.get_atoms_indexes(targetAtomsIndexes)
        self.__initialize_variables__()
        self.__initialize_results__()

    def __initialize_variables__(self):
        self.weights = np.array(get_records_database_property_values(self.targetAtomsIndexes, self.structure, 'atomicWeight'))
        self.totalWeight = np.sum(self.weights)
        elements = self._trajectory.elements
        self.elements = [elements[idx] for idx in self.targetAtomsIndexes]

    def __initialize_results__(self):
        self.results['time'] = np.array([self.time[idx] for idx in self.configurationsIndexes], dtype=(np.float))
        for axis in ('xx', 'xy', 'xz', 'yy', 'yz', 'zz'):
            self.results['moment_of_inertia_%s' % axis] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))

        for axis in ('a', 'b', 'c'):
            self.results['semiaxis_%s' % axis] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))

        self.results['eccentricity'] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
        self.results['ratio_of_largest_to_smallest'] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))
        self.results['radius_of_gyration'] = np.zeros((len(self.configurationsIndexes)), dtype=(np.float))

    def step(self, index):
        """
        analysis step of calculation method.

        :Parameters:
            #. index (int): the step index

        :Returns:
            #. stepData (object): object used in combine method
        """
        confIdx = self.configurationsIndexes[index]
        coordinates = self._trajectory.get_configuration_coordinates(confIdx)
        targetAtomsCoordinates = coordinates[self.targetAtomsIndexes]
        weightedTargetAtomsCoordinates = np.transpose(np.transpose(targetAtomsCoordinates) * self.weights)
        COM = np.sum(weightedTargetAtomsCoordinates, 0) / self.totalWeight
        targetAtomsCoordinates -= COM
        rog = np.sum(self.weights / self.totalWeight * np.add.reduce(targetAtomsCoordinates ** 2, 1))
        xx = np.add.reduce(self.weights * (targetAtomsCoordinates[:, 1] * targetAtomsCoordinates[:, 1] + targetAtomsCoordinates[:, 2] * targetAtomsCoordinates[:, 2]))
        xy = -np.add.reduce(self.weights * (targetAtomsCoordinates[:, 0] * targetAtomsCoordinates[:, 1]))
        xz = -np.add.reduce(self.weights * (targetAtomsCoordinates[:, 0] * targetAtomsCoordinates[:, 2]))
        yy = np.add.reduce(self.weights * (targetAtomsCoordinates[:, 0] * targetAtomsCoordinates[:, 0] + targetAtomsCoordinates[:, 2] * targetAtomsCoordinates[:, 2]))
        yz = -np.add.reduce(self.weights * (targetAtomsCoordinates[:, 1] * targetAtomsCoordinates[:, 2]))
        zz = np.add.reduce(self.weights * (targetAtomsCoordinates[:, 0] * targetAtomsCoordinates[:, 0] + targetAtomsCoordinates[:, 1] * targetAtomsCoordinates[:, 1]))
        return (
         index, (xx, xy, xz, yy, yz, zz, rog))

    def combine(self, index, stepData):
        """
        analysis combine method called after each step.

        :Parameters:
            #. index (int): the index of the last calculated step
            #. stepData (object): the returned data from step method
        """
        Imin = min(stepData[0], stepData[3], stepData[5])
        Imax = max(stepData[0], stepData[3], stepData[5])
        Imid = [stepData[0], stepData[3], stepData[5]]
        Imid.pop(Imid.index(Imin))
        Imid.pop(Imid.index(Imax))
        Imid = Imid[0]
        average = (stepData[0] + stepData[3] + stepData[5]) / 3.0
        self.results['moment_of_inertia_xx'][index] = stepData[0]
        self.results['moment_of_inertia_xy'][index] = stepData[1]
        self.results['moment_of_inertia_xz'][index] = stepData[2]
        self.results['moment_of_inertia_yy'][index] = stepData[3]
        self.results['moment_of_inertia_yz'][index] = stepData[4]
        self.results['moment_of_inertia_zz'][index] = stepData[5]
        self.results['eccentricity'][index] = 1 - Imin / average
        self.results['ratio_of_largest_to_smallest'][index] = Imax / Imin
        self.results['semiaxis_a'][index] = np.sqrt(5.0 / (2.0 * self.totalWeight) * (Imax + Imid - Imin))
        self.results['semiaxis_b'][index] = np.sqrt(5.0 / (2.0 * self.totalWeight) * (Imax + Imin - Imid))
        self.results['semiaxis_c'][index] = np.sqrt(5.0 / (2.0 * self.totalWeight) * (Imid + Imin - Imax))
        self.results['radius_of_gyration'][index] = np.sqrt(stepData[6])

    def finalize(self):
        """
        called once all the steps has been run.

        """
        pass