# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/pythonids/components/pypythonids/tests/__init__.py
# Compiled at: 2019-05-04 21:41:48
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
__uuid__ = '4135ab0f-fbb8-45a2-a6b1-80d96c164b72'
__package__ = 'filesysobjects_pyunit'
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