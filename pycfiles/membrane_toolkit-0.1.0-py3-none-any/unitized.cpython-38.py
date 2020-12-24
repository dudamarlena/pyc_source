# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/UNC Drive/pymemsci/membrane_toolkit/core/unitized.py
# Compiled at: 2020-04-30 23:52:07
# Size of source mod 2**32: 1228 bytes
"""
Unitized versions of all methods in membrane_toolkit.core

Unitized methods should have the same name as the base method and be wrapped with
appropriate units using pint's .wraps() decorator. Unitized methods should perform
computations in base SI units unless there is a specific reason (performance,
numerical stability, etc.) to do otherwise.
"""
from pint import UnitRegistry
from membrane_toolkit.core import diffusion_coefficient_mackie_meares, apparent_permselectivity, nernst_potential, donnan_equilibrium
ureg = UnitRegistry()
diffusion_coefficient_mackie_meares = ureg.wraps('m ** 2 / s', ('m ** 2 / s', ureg.dimensionless))(diffusion_coefficient_mackie_meares)
donnan_equilibrium = ureg.wraps('mol/L', ('mol/L', 'mol/L', None, None, None, None,
                                          None, None))(donnan_equilibrium)
apparent_permselectivity = ureg.wraps(ureg.dimensionless, ('V', 'V', None))(apparent_permselectivity)
nernst_potential = ureg.wraps('V', ('=A', '=A', None, 'degC'))(nernst_potential)