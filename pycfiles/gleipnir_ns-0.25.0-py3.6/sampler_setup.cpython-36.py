# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gleipnir/sampler_setup.py
# Compiled at: 2019-03-02 21:35:51
# Size of source mod 2**32: 143 bytes
from distutils.core import setup
from Cython.Build import cythonize
setup(ext_modules=cythonize('samplers_cython.pyx', annotate=True))