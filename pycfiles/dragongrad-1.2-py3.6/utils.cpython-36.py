# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/autograd/utils.py
# Compiled at: 2018-11-06 13:48:20
# Size of source mod 2**32: 1249 bytes
import numpy as np

def get_shape(x):
    """
    get the shape of the input, set to (1,) if it is a real number
    """
    typeOfInput = type(x)
    if typeOfInput == np.ndarray or typeOfInput == list:
        shape = np.array(x).shape
    else:
        shape = (1, )
    return shape


def data_2_numpy(data):
    """
    convert input data (np.array, list, or float) into a numpy array
    """
    typeOfInput = type(data)
    if typeOfInput == np.ndarray:
        return data
    else:
        if typeOfInput == list:
            return np.array(data)
        return np.array([data])