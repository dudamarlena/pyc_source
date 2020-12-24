# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/iterables.py
# Compiled at: 2019-02-25 04:13:09
# Size of source mod 2**32: 899 bytes
from inferpy import exceptions

def get_shape(x):
    """
    Get the shape of an element x. If it is an element with a shape attribute, return it. If it is a list,
    compute the shape by checking the len, and the shape of internal elements. In that case, the shape must
    be consistent. Finally, in other case return () as shape.

    :param x: The element to compute its shape
    :raises : class `InvalidParameterDimension`: list shape not consistent
    :returns: A tuple with the shape of `x`
    """
    if isinstance(x, list):
        shapes = [get_shape(subx) for subx in x]
        if any([s != shapes[0] for s in shapes[1:]]):
            raise exceptions.InvalidParameterDimension('Parameter dimension not consistent: {}'.format(x))
        return (len(x),) + shapes[0]
    else:
        if hasattr(x, 'shape'):
            return tuple(x.shape)
        return ()