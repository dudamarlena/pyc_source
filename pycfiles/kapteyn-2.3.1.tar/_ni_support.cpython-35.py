# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/jansky/data/users/breddels/src/kapteyn-sky2/kapteyn/_ni_support.py
# Compiled at: 2016-03-21 10:33:38
# Size of source mod 2**32: 3755 bytes
import types, numpy

def _extend_mode_to_code(mode):
    """Convert an extension mode to the corresponding integer code.
    """
    if mode == 'nearest':
        return 0
    if mode == 'wrap':
        return 1
    if mode == 'reflect':
        return 2
    if mode == 'mirror':
        return 3
    if mode == 'constant':
        return 4
    raise RuntimeError('boundary mode not supported')


def _normalize_sequence(input, rank, array_type=None):
    """If input is a scalar, create a sequence of length equal to the
    rank by duplicating the input. If input is a sequence,
    check if its length is equal to the length of array.
    """
    if isinstance(input, (int,
     float)):
        normalized = [
         input] * rank
    else:
        normalized = list(input)
    if len(normalized) != rank:
        err = 'sequence argument must have length equal to input rank'
        raise RuntimeError(err)
    return normalized


import warnings

def _get_output(output, input, output_type=None, shape=None):
    if output_type is not None:
        msg = "'output_type' argument is deprecated."
        msg += " Assign type to 'output' instead."
        raise RuntimeError(msg)
        warnings.warn(msg, DeprecationWarning)
        if output is None:
            output = output_type
        else:
            if type(output) is not type(type) or output.dtype != output_type:
                raise RuntimeError("'output' type and 'output_type' not equal")
            if shape is None:
                shape = input.shape
            if output is None:
                output = numpy.zeros(shape, dtype=input.dtype.name)
                return_value = output
            else:
                if type(output) in [type(type), type(numpy.zeros((4, )).dtype)]:
                    output = numpy.zeros(shape, dtype=output)
                    return_value = output
                else:
                    if type(output) is bytes:
                        output = numpy.typeDict[output]
                        output = numpy.zeros(shape, dtype=output)
                        return_value = output
                    else:
                        if output.shape != shape:
                            raise RuntimeError('output shape not correct')
                        return_value = None
        return (
         output, return_value)


def _check_axis(axis, rank):
    if axis < 0:
        axis += rank
    if axis < 0 or axis >= rank:
        raise ValueError('invalid axis')
    return axis