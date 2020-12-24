# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dataprovider/setup.py
# Compiled at: 2016-11-29 20:56:28
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize('warping/*.pyx'))