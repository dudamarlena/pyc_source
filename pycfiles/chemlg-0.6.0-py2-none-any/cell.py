# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gabriele/workspace/chemlab/chemlab/core/spacegroup/cell.py
# Compiled at: 2015-01-08 16:33:19
import numpy as np
from numpy import pi, sin, cos, tan, arcsin, arccos, arctan, sqrt
from numpy import dot
from numpy.linalg import norm
__all__ = [
 'cell_to_cellpar', 'cellpar_to_cell', 'metric_from_cell']

def unit_vector(x):
    """Return a unit vector in the same direction as x."""
    y = np.array(x, dtype='float')
    return y / norm(y)


def angle(x, y):
    """Return the angle between vectors a and b in degrees."""
    return arccos(dot(x, y) / (norm(x) * norm(y))) * 180.0 / pi


def cell_to_cellpar(cell):
    """Returns the cell parameters [a, b, c, alpha, beta, gamma] as a
    numpy array."""
    va, vb, vc = cell
    a = np.linalg.norm(va)
    b = np.linalg.norm(vb)
    c = np.linalg.norm(vc)
    alpha = 180.0 / pi * arccos(dot(vb, vc) / (b * c))
    beta = 180.0 / pi * arccos(dot(vc, va) / (c * a))
    gamma = 180.0 / pi * arccos(dot(va, vb) / (a * b))
    return np.array([a, b, c, alpha, beta, gamma])


def cellpar_to_cell(cellpar, ab_normal=(0, 0, 1), a_direction=None):
    """Return a 3x3 cell matrix from `cellpar` = [a, b, c, alpha,
    beta, gamma].  The returned cell is orientated such that a and b
    are normal to `ab_normal` and a is parallel to the projection of
    `a_direction` in the a-b plane.

    Default `a_direction` is (1,0,0), unless this is parallel to
    `ab_normal`, in which case default `a_direction` is (0,0,1).

    The returned cell has the vectors va, vb and vc along the rows. The
    cell will be oriented such that va and vb are normal to `ab_normal`
    and va will be along the projection of `a_direction` onto the a-b
    plane.

    Example:

    >>> cell = cellpar_to_cell([1, 2, 4,  10,  20, 30], (0,1,1), (1,2,3))
    >>> np.round(cell, 3)
    array([[ 0.816, -0.408,  0.408],
           [ 1.992, -0.13 ,  0.13 ],
           [ 3.859, -0.745,  0.745]])

    """
    if a_direction is None:
        if np.linalg.norm(np.cross(ab_normal, (1, 0, 0))) < 1e-05:
            a_direction = (0, 0, 1)
        else:
            a_direction = (1, 0, 0)
    ad = np.array(a_direction)
    Z = unit_vector(ab_normal)
    X = unit_vector(ad - dot(ad, Z) * Z)
    Y = np.cross(Z, X)
    alpha, beta, gamma = (90.0, 90.0, 90.0)
    if isinstance(cellpar, (int, float)):
        a = b = c = cellpar
    elif len(cellpar) == 1:
        a = b = c = cellpar[0]
    elif len(cellpar) == 3:
        a, b, c = cellpar
        alpha, beta, gamma = (90.0, 90.0, 90.0)
    else:
        a, b, c, alpha, beta, gamma = cellpar
    alpha *= pi / 180.0
    beta *= pi / 180.0
    gamma *= pi / 180.0
    va = a * np.array([1, 0, 0])
    vb = b * np.array([cos(gamma), sin(gamma), 0])
    cx = cos(beta)
    cy = (cos(alpha) - cos(beta) * cos(gamma)) / sin(gamma)
    cz = sqrt(1.0 - cx * cx - cy * cy)
    vc = c * np.array([cx, cy, cz])
    abc = np.vstack((va, vb, vc))
    T = np.vstack((X, Y, Z))
    cell = dot(abc, T)
    return cell


def metric_from_cell(cell):
    """Calculates the metric matrix from cell, which is given in the
    Cartesian system."""
    cell = np.asarray(cell, dtype=float)
    return np.dot(cell, cell.T)


if __name__ == '__main__':
    import doctest