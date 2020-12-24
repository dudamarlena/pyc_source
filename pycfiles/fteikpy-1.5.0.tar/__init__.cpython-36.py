# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ..\fteikpy\__init__.py
# Compiled at: 2018-02-22 12:33:37
# Size of source mod 2**32: 651 bytes
"""
FTeikPy is a Python module that computes accurate first arrival traveltimes in
2-D and 3-D heterogeneous isotropic velocity model.

Author: Keurfon Luu <keurfon.luu@mines-paristech.fr>
License: MIT
"""
from .ttgrid import TTGrid
from .eikonal import Eikonal
from .ray import Ray, ray_coverage
from .layered_model import lay2vel, lay2tt
from .bspline_model import bspline1, bspline2, vel2spl, spl2vel
__version__ = '1.5.0'
__all__ = [
 'TTGrid',
 'Eikonal',
 'Ray',
 'ray_coverage',
 'lay2vel',
 'lay2tt',
 'bspline1',
 'bspline2',
 'vel2spl',
 'spl2vel']