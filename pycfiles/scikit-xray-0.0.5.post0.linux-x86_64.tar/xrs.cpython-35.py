# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/edill/mc/lib/python3.5/site-packages/skxray/core/constants/xrs.py
# Compiled at: 2016-03-04 05:19:32
# Size of source mod 2**32: 10527 bytes
"""
Module for xray scattering
"""
from __future__ import absolute_import, division, print_function
from collections import namedtuple
from itertools import repeat
import logging, numpy as np
from ..utils import q_to_d, d_to_q, twotheta_to_q, q_to_twotheta
logger = logging.getLogger(__name__)

class HKL(namedtuple('HKL', 'h k l')):
    __doc__ = '\n    Namedtuple sub-class miller indicies (HKL)\n\n    This class enforces that the values are integers.\n\n    Parameters\n    ----------\n    h : int\n    k : int\n    l : int\n\n    Attributes\n    ----------\n    length\n    h\n    k\n    l\n    '
    __slots__ = ()

    def __new__(cls, *args, **kwargs):
        args = [int(_) for _ in args]
        for k in list(kwargs):
            kwargs[k] = int(kwargs[k])

        return super(HKL, cls).__new__(cls, *args, **kwargs)

    @property
    def length(self):
        """
        The L2 norm (length) of the hkl vector.
        """
        return np.linalg.norm(self)


class Reflection(namedtuple('Reflection', ('d', 'hkl', 'q'))):
    __doc__ = '\n    Namedtuple sub-class for scattering reflection information\n\n    Parameters\n    ----------\n    d : float\n        Plane-spacing\n\n    hkl : `hkl`\n        miller indicies\n\n    q : float\n        q-value of the reflection\n\n    Attributes\n    ----------\n    d\n    HKL\n    q\n    '
    __slots__ = ()


class PowderStandard(object):
    __doc__ = '\n    Class for providing safe access to powder calibration standards\n    data.\n\n    Parameters\n    ----------\n    name : str\n        Name of the standard\n\n    reflections : list\n        A list of (d, (h, k, l), q) values.\n    '

    def __init__(self, name, reflections):
        self._reflections = [Reflection(d, HKL(*hkl), q) for d, hkl, q in reflections]
        self._reflections.sort(key=lambda x: x[(-1)])
        self._name = name

    def __str__(self):
        return 'Calibration standard: {}'.format(self.name)

    __repr__ = __str__

    @property
    def name(self):
        """
        Name of the calibration standard
        """
        return self._name

    @property
    def reflections(self):
        """
        List of the known reflections
        """
        return self._reflections

    def __iter__(self):
        return iter(self._reflections)

    def convert_2theta(self, wavelength):
        """
        Convert the measured 2theta values to a different wavelength

        Parameters
        ----------
        wavelength : float
            The new lambda in Angstroms

        Returns
        -------
        two_theta : array
            The new 2theta values in radians
        """
        q = np.array([_.q for _ in self])
        return q_to_twotheta(q, wavelength)

    @classmethod
    def from_lambda_2theta_hkl(cls, name, wavelength, two_theta, hkl=None):
        r"""
        Method to construct a PowderStandard object from calibrated
        :math:`2\theata` values.

        Parameters
        ----------
        name : str
            The name of the standard

        wavelength : float
            The wavelength that the calibration data was taken at

        two_theta : array
            The calibrated :math:`2\theta` values

        hkl : list, optional
            List of (h, k, l) tuples of the Miller indicies that go
            with each measured :math:`2\theta`.  If not given then
            all of the miller indicies are stored as (0, 0, 0).

        Returns
        -------
        standard : PowderStandard
            The standard object
        """
        q = twotheta_to_q(two_theta, wavelength)
        d = q_to_d(q)
        if hkl is None:
            hkl = repeat((0, 0, 0))
        return cls(name, zip(d, hkl, q))

    @classmethod
    def from_d(cls, name, d, hkl=None):
        r"""
        Method to construct a PowderStandard object from known
        :math:`d` values.

        Parameters
        ----------
        name : str
            The name of the standard

        d : array
            The known plane spacings

        hkl : list, optional
            List of (h, k, l) tuples of the Miller indicies that go
            with each measured :math:`2\theta`.  If not given then
            all of the miller indicies are stored as (0, 0, 0).

        Returns
        -------
        standard : PowderStandard
            The standard object
        """
        q = d_to_q(d)
        if hkl is None:
            hkl = repeat((0, 0, 0))
        return cls(name, zip(d, hkl, q))

    def __len__(self):
        return len(self._reflections)


calibration_standards = {'Si': PowderStandard.from_lambda_2theta_hkl(name='Si', wavelength=1.5405929, two_theta=np.deg2rad([28.441, 47.3, 56.119, 69.126, 76.371, 88.024,
        94.946, 106.7, 114.082, 127.532, 136.877]), hkl=((1, 1, 1), (2, 2, 0), (3, 1, 1),
                                                         (4, 0, 0), (3, 3, 1), (4, 2, 2),
                                                         (5, 1, 1), (4, 4, 0), (5, 3, 1),
                                                         (6, 2, 0), (5, 3, 3))), 
 
 'CeO2': PowderStandard.from_lambda_2theta_hkl(name='CeO2', wavelength=1.5405929, two_theta=np.deg2rad([28.61, 33.14, 47.54, 56.39, 59.14, 69.46]), hkl=((1, 1, 1),
                                                                                                                                                (2, 0, 0),
                                                                                                                                                (2, 2, 0),
                                                                                                                                                (3, 1, 1),
                                                                                                                                                (2, 2, 2),
                                                                                                                                                (4, 0, 0))), 
 
 'Al2O3': PowderStandard.from_lambda_2theta_hkl(name='Al2O3', wavelength=1.5405929, two_theta=np.deg2rad([25.574, 35.149, 37.773, 43.351, 52.548, 57.497,
           66.513, 68.203, 76.873, 77.233, 84.348, 88.994,
           91.179, 95.24, 101.07, 116.085, 116.602,
           117.835, 122.019, 127.671, 129.87, 131.098,
           136.056, 142.314, 145.153, 149.185, 150.102,
           150.413, 152.38]), hkl=((0, 1, 2), (1, 0, 4), (1, 1, 0), (1, 1, 3), (0, 2, 4),
                                   (1, 1, 6), (2, 1, 4), (3, 0, 0), (1, 0, 10), (1, 1, 9),
                                   (2, 2, 3), (0, 2, 10), (1, 3, 4), (2, 2, 6), (2, 1, 10),
                                   (3, 2, 4), (0, 1, 14), (4, 1, 0), (4, 1, 3), (1, 3, 10),
                                   (3, 0, 12), (2, 0, 14), (1, 4, 6), (1, 1, 15),
                                   (4, 0, 10), (0, 5, 4), (1, 2, 14), (1, 0, 16),
                                   (3, 3, 0))), 
 
 'LaB6': PowderStandard.from_d(name='LaB6', d=[
          4.156, 2.939, 2.399, 2.078, 1.859, 1.697, 1.469, 1.385, 1.314,
          1.253, 1.2, 1.153, 1.111, 1.039, 1.008, 0.98, 0.953, 0.929,
          0.907, 0.886, 0.848, 0.831, 0.815, 0.8]), 
 
 'Ni': PowderStandard.from_d(name='Ni', d=[
        2.03458234862, 1.762, 1.24592214845, 1.06252597829, 1.01729117431,
        0.881, 0.80846104616, 0.787990355271, 0.719333487797,
        0.678194116208, 0.622961074225, 0.595664718733, 0.587333333333,
        0.557193323722, 0.537404961852, 0.531262989146, 0.508645587156,
        0.493458701611, 0.488690872874, 0.47091430825, 0.458785722296,
        0.4405, 0.430525121912, 0.427347771314])}