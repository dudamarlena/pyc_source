# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Frameworks/Python.framework/Versions/3.7/lib/python3.7/site-packages/pdbparser/Utilities/Math.py
# Compiled at: 2019-02-16 11:53:41
# Size of source mod 2**32: 7518 bytes
"""
This module contains general math functions.
"""
from __future__ import print_function
import numpy as np
from ..log import Logger

def rotate_array(rotationMatrix, array):
    """
        applies rotation matrix to an array of vectors.

        :Parameters:
            #. rotationMatrix (numpy.ndarray): the 3X3 rotation tensor.
            #. array (numpy.ndarray): the NX3 array to rotate.

        :Returns:
            #. array (numpy.ndarray): the rotated numpy.ndarray.
    """
    if not isinstance(array, np.ndarray):
        raise AssertionError(Logger.error('array must be numpy.ndarray instance'))
    elif not len(array.shape) <= 2:
        raise AssertionError(Logger.error('array must be a vector or a matrix'))
    elif len(array.shape) == 2 and not array.shape[1] == 3:
        raise AssertionError(Logger.error('array number of columns must be 3'))
    else:
        assert array.shape[1] == 3, Logger.error('vector array number of columns must be 3')
    assert isinstance(rotationMatrix, np.ndarray), Logger.error('rotationMatrix must be numpy.ndarray instance')
    assert rotationMatrix.shape == (3, 3), Logger.error('rotationMatrix must be a (3X3) tensor')
    return np.dot(rotationMatrix, np.transpose(array).reshape(1, 3, -1)).transpose().reshape(-1, 3)


def get_superposition_transformation_elements(weights, totalWeight, refArray, array):
    """
        Calculates the rotation matrix and the translations that minimizes the root mean
        square deviation between and array of vectors and a reference array.

        :Parameters:
            #. weights (list, set, tuple, numpy.ndarray): the weights array. must have the same length as refArray and array
            #. totalWeight (number): must be equal to the sum of all weights array. For optimization reason it must be given as an argument
            #. refArray (numpy.ndarray): the NX3 reference array to superpose to.
            #. array (numpy.ndarray): the NX3 array to calculate the transformation of.

        :Returns:
            #. rotationMatrix (numpy.ndarray): the 3X3 rotation tensor.
            #. refArrayCOM (numpy.ndarray): the 1X3 vector center of mass of refArray.
            #. arrayCOM (numpy.ndarray): the 1X3 vector center of mass of array.
            #. rms (number)
    """
    if not isinstance(array, np.ndarray):
        raise AssertionError(Logger.error('array must be numpy.ndarray instance'))
    elif not len(array.shape) <= 2:
        raise AssertionError(Logger.error('array must be a vector or a matrix'))
    elif len(array.shape) == 2 and not array.shape[1] == 3:
        raise AssertionError(Logger.error('array number of columns must be 3'))
    else:
        assert array.shape[1] == 3, Logger.error('vector array number of columns must be 3')
    assert isinstance(refArray, np.ndarray), Logger.error('refArray must be numpy.ndarray instance')
    assert len(refArray.shape) <= 2, Logger.error('refArray must be a vector or a matrix')
    if len(refArray.shape) == 2 and not refArray.shape[1] == 3:
        raise AssertionError(Logger.error('refArray number of columns must be 3'))
    else:
        if not refArray.shape[1] == 3:
            raise AssertionError(Logger.error('vector refArray number of columns must be 3'))
        else:
            if not isinstance(weights, (list, set, tuple, np.ndarray)):
                raise AssertionError(Logger.error('weights must be numpy.ndarray instance'))
            else:
                weights = np.array(weights)
                assert len(weights.shape) == 1, Logger.error('weights must be a vector of N elements')
                assert array.shape == refArray.shape, Logger.error('refArray and array must have the same number of vectors')
                assert array.shape[0] == len(weights), Logger.error('weights number of elements must be equal to the number of vectors in array and refArray')
                try:
                    totalWeight = float(totalWeight)
                except:
                    raise Logger.error('totalWeight must be a number')

            assert totalWeight > 0, Logger.error('totalWeight must be a strictly positive number')
            a = array[:, 0] * weights
            b = array[:, 1] * weights
            c = array[:, 2] * weights
            arrayCOM = np.array([np.sum(a) / totalWeight, np.sum(b) / totalWeight, np.sum(c) / totalWeight])
            r_ref = array - arrayCOM
            a = refArray[:, 0] * weights
            b = refArray[:, 1] * weights
            c = refArray[:, 2] * weights
            r = np.array([a, b, c]) / totalWeight
            refArrayCOM = np.sum(r, 1)
            cross = np.dot(r, r_ref)
            possq = weights * np.add.reduce(refArray * refArray, 1) / totalWeight + weights * np.add.reduce(r_ref * r_ref, 1) / totalWeight
            possq = np.sum(possq)
            k = np.zeros((4, 4), np.float)
            k[(0, 0)] = -cross[(0, 0)] - cross[(1, 1)] - cross[(2, 2)]
            k[(0, 1)] = cross[(1, 2)] - cross[(2, 1)]
            k[(0, 2)] = cross[(2, 0)] - cross[(0, 2)]
            k[(0, 3)] = cross[(0, 1)] - cross[(1, 0)]
            k[(1, 1)] = -cross[(0, 0)] + cross[(1, 1)] + cross[(2, 2)]
            k[(1, 2)] = -cross[(0, 1)] - cross[(1, 0)]
            k[(1, 3)] = -cross[(0, 2)] - cross[(2, 0)]
            k[(2, 2)] = cross[(0, 0)] - cross[(1, 1)] + cross[(2, 2)]
            k[(2, 3)] = -cross[(1, 2)] - cross[(2, 1)]
            k[(3, 3)] = cross[(0, 0)] + cross[(1, 1)] - cross[(2, 2)]
            for i in range(1, 4):
                for j in range(i):
                    k[(i, j)] = k[(j, i)]

            k = 2.0 * k
            for i in range(4):
                k[(i, i)] = k[(i, i)] + possq - np.add.reduce(refArrayCOM * refArrayCOM)

            e, v = np.linalg.eig(k)
            i = np.argmin(e)
            v = np.array(v[:, i])
            if v[0] < 0:
                v = -v
            if e[i] <= 0.0:
                rms = 0.0
            else:
                rms = np.sqrt(e[i])
        rot = np.zeros((3, 3, 4, 4))
        rot[(0, 0, 0, 0)] = 1
        rot[(0, 0, 1, 1)] = 1
        rot[(0, 0, 2, 2)] = -1
        rot[(0, 0, 3, 3)] = -1
        rot[(1, 1, 0, 0)] = 1
        rot[(1, 1, 1, 1)] = -1
        rot[(1, 1, 2, 2)] = 1
        rot[(1, 1, 3, 3)] = -1
        rot[(2, 2, 0, 0)] = 1
        rot[(2, 2, 1, 1)] = -1
        rot[(2, 2, 2, 2)] = -1
        rot[(2, 2, 3, 3)] = 1
        rot[(0, 1, 1, 2)] = 2
        rot[(0, 1, 0, 3)] = -2
        rot[(0, 2, 0, 2)] = 2
        rot[(0, 2, 1, 3)] = 2
        rot[(1, 0, 0, 3)] = 2
        rot[(1, 0, 1, 2)] = 2
        rot[(1, 2, 0, 1)] = -2
        rot[(1, 2, 2, 3)] = 2
        rot[(2, 0, 0, 2)] = -2
        rot[(2, 0, 1, 3)] = 2
        rot[(2, 1, 0, 1)] = 2
        rot[(2, 1, 2, 3)] = 2
        rotationMatrix = np.dot(np.dot(rot, v), v)
        return (rotationMatrix, refArrayCOM, arrayCOM, rms)


def get_superposed_array(weights, totalWeight, refArray, array):
    """
        Calculates the rotation matrix and the translations that minimizes the root mean
        square deviation between and array of vectors and a reference array.

        :Parameters:
            #. weights (list, set, tuple, numpy.ndarray): the weights array. must have the same length as refArray and array
            #. totalWeight (number): must be equal to the sum of all weights array. For optimization reason it must be given as an argument
            #. refArray (numpy.ndarray): the NX3 reference array to superpose to.
            #. array (numpy.ndarray): the NX3 array to calculate the transformation of.

        :Returns:
            #. array (numpy.ndarray): the NX3 superposed array.
    """
    rotationMatrix, refArrayCOM, arrayCOM, rms = get_superposition_transformation_elements(weights, totalWeight, refArray, array)
    array -= arrayCOM
    array = np.dot(rotationMatrix, np.transpose(array).reshape(1, 3, -1)).transpose().reshape(-1, 3)
    array += refArrayCOM
    return array