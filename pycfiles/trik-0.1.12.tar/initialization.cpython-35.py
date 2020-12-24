# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\trik\trik\yu\initialization.py
# Compiled at: 2020-04-12 22:57:27
# Size of source mod 2**32: 553 bytes
import numpy

def xavier_initialization(shape):
    matrix = numpy.random.randn(*shape) / numpy.sqrt(shape[(-2)])
    return matrix


def he_initialization(shape):
    matrix = numpy.random.randn(*shape) / numpy.sqrt(shape[(-2)] / 2)
    return matrix


def bias_initialization(shape):
    matrix = numpy.random.normal(0, 1, shape) / shape[(-1)]
    return matrix


def normal_initialization(shape):
    matrix = numpy.random.normal(0, 1, shape)
    return matrix


def uniform_initialization(shape):
    matrix = numpy.random.randn(*shape)
    return matrix