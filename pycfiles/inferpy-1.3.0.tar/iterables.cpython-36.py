# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rcabanas/GoogleDrive/UAL/inferpy/repo/InferPy/inferpy/util/iterables.py
# Compiled at: 2020-02-12 04:52:06
# Size of source mod 2**32: 1794 bytes


def get_shape(x):
    """ Get the shape of an element x. If it is an element with a shape attribute, return it. If it is a list with more than
    one element, compute the shape by checking the len, and the shape of internal elements. In that case, the shape must
    be consistent. Finally, in other case return () as shape.

    Args:
        x: The element to compute its shape

    Raises:
        class `ValueError`: list shape not consistent

    Returns:
        A tuple with the shape of `x`

    """
    if isinstance(x, list) and len(x) > 0:
        shapes = [get_shape(subx) for subx in x]
        if any([s != shapes[0] for s in shapes[1:]]):
            raise ValueError('Parameter dimension not consistent: {}'.format(x))
        return (len(x),) + shapes[0]
    else:
        if hasattr(x, '_shape_tuple'):
            return x._shape_tuple()
        if hasattr(x, 'shape'):
            return tuple(x.shape)
        return ()


def get_plate_size(variables, sample_dict):
    plate_shapes = [get_shape(v) for k, v in sample_dict.items() if k in variables if variables[k].is_datamodel]
    plate_sizes = [s[0] if len(s) > 0 else 1 for s in plate_shapes]
    if len(plate_sizes) == 0:
        return 1
    else:
        plate_size = plate_sizes[0]
        if any(plate_size != x for x in plate_sizes[1:]):
            raise ValueError('The number of elements for each mapped variable must be the same.')
        return plate_size