# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_fit/__init__.py
# Compiled at: 2020-04-20 10:00:06
# Size of source mod 2**32: 508 bytes
from eddington_fit.fit_functions_list import constant, linear, exponential, parabolic, hyperbolic
from eddington_fit.fit_function_generators_list import polynom, straight_power, inverse_power
from eddington_fit.fitting import fit_to_data
from eddington_fit.util import get_a0
__all__ = [
 'constant',
 'linear',
 'exponential',
 'parabolic',
 'hyperbolic',
 'polynom',
 'straight_power',
 'inverse_power',
 'fit_to_data',
 'get_a0']