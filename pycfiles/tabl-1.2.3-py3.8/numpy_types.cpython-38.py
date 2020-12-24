# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/tabl/numpy_types.py
# Compiled at: 2020-03-12 15:31:38
# Size of source mod 2**32: 361 bytes
"""
.. module:: tabl.numpy_types
.. moduleauthor:: Bastiaan Bergman <Bastiaan.Bergman@gmail.com>

"""
from __future__ import absolute_import, division, print_function, unicode_literals
import numpy as np
NP_FLOAT_TYPES = [
 np.float, np.float32, np.float64, np.float16]
NP_INT_TYPES = [np.int, np.int32, np.int64]