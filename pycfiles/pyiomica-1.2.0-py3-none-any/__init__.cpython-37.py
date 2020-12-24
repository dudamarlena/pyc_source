# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\A_MSU_NASA\VS\pyiomica\pyiomica\__init__.py
# Compiled at: 2019-10-14 13:37:44
# Size of source mod 2**32: 835 bytes
"""
PyIOmica is a general omics data analysis Python package, with a focus on the analysis and categorization of longitudinal datasets.

Usage:
    import pyiomica

Notes:
    For additional information visit: https://github.com/gmiaslab/pyiomica and https://mathiomica.org by G. Mias Lab
"""
print('Loading PyIOmica (https://github.com/gmiaslab/pyiomica by G. Mias Lab)')
from .globalVariables import *
if printPackageGlobalDefaults:
    variables = locals().copy()
    for variable in variables.items():
        if variable[0][:2] != '__' and type(variable[1]) is not types.ModuleType and type(variable[1]) is not types.FunctionType and type(variable[1]) is not types.ClassType:
            print('\n', variable[0], ':\n', variable[1], '\n')