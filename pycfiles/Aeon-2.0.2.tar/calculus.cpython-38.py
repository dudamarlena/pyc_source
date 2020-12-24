# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/calc/calculus.py
# Compiled at: 2019-11-27 14:49:53
# Size of source mod 2**32: 1163 bytes
__doc__ = 'Generic calculus functions.'
import numpy as np
__all__ = ('integrate', )

def integrate(cube, coord):
    """
    Integrate the cube along a 1D coordinate using the trapezoidal rule.

    Note: `coord` must be one of the dimensional coordinates of the cube.

    Parameters
    ----------
    cube: iris.cube.Cube
        Input cube containing the given coordinate.
    coord: str or iris.coords.Coord
        Coordinate for integration.

    Returns
    -------
    iris.cube.Cube
        integrated cube.
    """
    c = cube.coord(coord)
    others = [dc.name() for dc in cube.dim_coords if cube.coord_dims(dc) != cube.coord_dims(c)]
    dim = cube.coord_dims(c)[0]
    data = np.trapz((cube.data), (c.points), axis=dim)
    res = next(cube.slices(others)).copy(data=data)
    res.units = cube.units * c.units
    res.remove_coord(c)
    res.rename(f"integral_of_{cube.name()}_wrt_{c.name()}")
    return res