# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/a3cosmos_gas_evolution/__init__.py
# Compiled at: 2019-10-25 10:11:18
# Size of source mod 2**32: 658 bytes
name = 'a3cosmos_gas_evolution'
from .Common_Python_Code import calc_galaxy_main_sequence
from .Common_Python_Code import calc_gas_fraction
from .Common_Python_Code import calc_gas_depletion_time
from .Common_Python_Code import calc_alpha_CO
from .Common_Python_Code import calc_delta_GD
from .Common_Python_Code import calc_metal_Z
from .Common_Python_Code import calc_fmol
from .Common_Python_Code import calc_gas_mass_from_dust
from .Common_Python_Code import apply_cosmology
cosmo = apply_cosmology.cosmo
from .__main__ import help
from .__main__ import load_all_modules
load_all_modules()
from .__main__ import *