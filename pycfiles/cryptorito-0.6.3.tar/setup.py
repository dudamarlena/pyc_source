# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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