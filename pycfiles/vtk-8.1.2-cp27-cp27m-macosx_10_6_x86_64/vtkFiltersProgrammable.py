# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/prabhu/src/git/VTKPythonPackage/VTK-osx_2.7/Wrapping/Python/vtk/vtkFiltersProgrammable.py
# Compiled at: 2018-11-28 17:05:58
"""
This module is an adapter for scripts that explicitly import from named
submodules as opposed to from the top-level vtk module. This is necessary
because the specific submodules might not exist when VTK_ENABLE_KITS is enabled.
"""
from __future__ import absolute_import
try:
    from .vtkFiltersKitPython import *
except ImportError:
    from vtkFiltersKitPython import *