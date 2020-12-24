# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mows/Scripts/ExoPlex/ExoPlex/burnman/eos/einstein.py
# Compiled at: 2018-03-29 19:08:50
from __future__ import absolute_import
import numpy as np
from .. import constants
eps = np.finfo(np.float).eps

def thermal_energy(T, einstein_T, n):
    """
    calculate the thermal energy of a substance.  Takes the temperature,
    the Einstein temperature, and n, the number of atoms per molecule.
    Returns thermal energy in J/mol
    """
    if T <= eps:
        return 3.0 * n * constants.gas_constant * einstein_T * 0.5
    x = einstein_T / T
    E_th = 3.0 * n * constants.gas_constant * einstein_T * (0.5 + 1.0 / (np.exp(x) - 1.0))
    return E_th


def heat_capacity_v(T, einstein_T, n):
    """
    Heat capacity at constant volume.  In J/K/mol
    """
    if T <= eps:
        return 0.0
    x = einstein_T / T
    C_v = 3.0 * n * constants.gas_constant * (x * x * np.exp(x) / np.power(np.exp(x) - 1.0, 2.0))
    return C_v