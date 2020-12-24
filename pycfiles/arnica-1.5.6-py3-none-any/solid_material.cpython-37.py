# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/duranton/Documents/CERFACS/CODES/arnica/src/arnica/phys/solid_material.py
# Compiled at: 2020-03-30 05:30:51
# Size of source mod 2**32: 872 bytes
""" module to define a solid material for thermal computations """
import numpy as np
__all__ = [
 'SolidMaterial']

class SolidMaterial:
    __doc__ = ' define properties of a solid material object'

    def __init__(self, lambda_poly, lambda_range):
        """ startup class"""
        self._lambda_range = lambda_range
        self._lambda_raw = np.poly1d(lambda_poly[::-1])

    def lambda_th(self, temperature):
        """ return the lambda of ceramics material [W/mK] """
        t_clip = np.minimum(temperature, self._lambda_range[1])
        t_clip = np.maximum(t_clip, self._lambda_range[0])
        return self._lambda_raw(t_clip)

    def thermal_resistance(self, width, t_est):
        """ return the thermal resistance  [m2.K/W]
        width : width of the layer
        t_est : estimated temperature of the layer """
        return width / self.lambda_th(t_est)