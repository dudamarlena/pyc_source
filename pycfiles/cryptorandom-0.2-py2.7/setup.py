# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/cryptorandom/setup.py
# Compiled at: 2018-09-06 14:58:55
from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext
import numpy
ext_modules = [
 Extension('sha256prng', ['sha256prng.pyx'], include_dirs=[
  numpy.get_include()])]
setup(name='SHA-256 PRNG', cmdclass={'build_ext': build_ext}, ext_modules=ext_modules, include_dirs=[
 numpy.get_include()])