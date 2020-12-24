# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/dicom_tools/convertTypes.py
# Compiled at: 2018-05-21 04:28:19
# Size of source mod 2**32: 543 bytes
from __future__ import print_function
import numpy as np

def convertTypes(input_type):
    if input_type is np.uint8:
        return '%d'
    if input_type is np.float16:
        return '%.18e'
    if input_type is np.string_:
        return '%s'
    raise TypeError(input_type, 'not recognized.')


def convertTypesROOT(input_type):
    if input_type is np.uint8:
        return 'I'
    if input_type is np.float16:
        return 'F'
    if input_type is np.string_:
        return 'C'
    raise TypeError(input_type, 'not recognized.')