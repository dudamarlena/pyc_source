# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/namedtupledefs/components/namedtupledefs3/tests/__init__.py
# Compiled at: 2019-06-19 10:51:09
# Size of source mod 2**32: 1409 bytes
"""PyUnit tests

These tests could either be called from the command line,
or within Eclipse by the plugin PyDev / PyUnit.

* CLI: '*python setup.py test*' 

* Eclipse: Install PyDev, open the view PyUnit and proceed.

**REMARK**: For additional unit tests refer to subdirectory 'UseCases' 

30_libs
-------
Provided library modules of 'epyunit'.

"""
from __future__ import print_function
__author__ = 'Arno-Can Uestuensoez'
__license__ = 'Artistic-License-2.0 + Forced-Fairplay-Constraints'
__copyright__ = 'Copyright (C) 2015-2016 Arno-Can Uestuensoez @Ingenieurbuero Arno-Can Uestuensoez'
__version__ = '0.1.0'
__uuid__ = '19683f50-48f2-4e1e-953f-640455e97340'
__package__ = 'namedtupledefs_pyunit'
import platform
print()
print()
print('#*******************************#')
print('#  Python implementation data   #')
print('#*******************************#')
print()
print()
print('python_implementation  = ' + str(platform.python_implementation()))
print('python_version         = ' + str(platform.python_version()))
try:
    print('python_build           = ' + str(platform.python_build()))
except:
    pass

try:
    print('linux_distribution     = ' + str(platform.linux_distribution()))
except:
    pass

try:
    print('python_compiler        = ' + str(platform.python_compiler()))
except:
    pass

try:
    print('libc_ver               = ' + str(platform.libc_ver()))
except:
    pass