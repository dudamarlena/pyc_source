# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/layout/geometry/index_ops.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 667 bytes
"""These are operations that transform an x, y matrix index."""

def reflect_x(x, y, matrix):
    """Reflect the index vertically."""
    return (
     matrix.columns - 1 - x, y)


def reflect_y(x, y, matrix):
    """Reflect the index horizontally."""
    return (
     x, matrix.rows - 1 - y)


def serpentine_x(x, y, matrix):
    """Every other row is indexed in reverse."""
    if y % 2:
        return (matrix.columns - 1 - x, y)
    else:
        return (
         x, y)


def serpentine_y(x, y, matrix):
    """Every other column is indexed in reverse."""
    if x % 2:
        return (x, matrix.rows - 1 - y)
    else:
        return (
         x, y)


def transpose(x, y, _):
    """Transpose rows and columns."""
    return (
     y, x)