# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/platformids/components/pyplatformids/tests/__init__.py
# Compiled at: 2019-05-04 21:41:48
__doc__ = "PyUnit tests\n\nThese tests could either be called from the command line,\nor within Eclipse by the plugin PyDev / PyUnit.\n\n* CLI: '*python setup.py test*' \n\n* Eclipse: Install PyDev, open the view PyUnit and proceed.\n\n\n**REMARK**: For additional unit tests refer to subdirectory 'UseCases' \n\n\n30_libs\n-------\nProvided library modules of 'epyunit'.\n\n"
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