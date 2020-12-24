# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/siddon/phantom.py
# Compiled at: 2010-10-14 04:08:10
"""
To Generate phantoms. You can call the following functions with the
desired phantom shape as input :

- modified_shepp_logan
- shepp_logan
- yu_ye_wang

You can generate a custom phantom by specifying a list of
ellipsoid parameters by calling the phantom function.

Ellipsoid parameters are as follows:
- A : value inside the ellipsoid
- a, b, c : axis length of the ellipsoid (in % of the cube shape)
- x0, y0, z0 : position of the center (in % of the cube shape)
- phi, theta, psi : Euler angles defining the orientation (in degrees)

Alternatively, you can generate only one ellipsoid by calling
the ellipsoid function.

Exemple
-------
To generate a phantom cube of size 32 * 32 * 32 :

>>> from siddon.phantom import *
>>> my_phantom = shepp_logan((32, 32, 32))
>>> assert my_phantom[16, 16, 16] == -0.8

Notes
-----
You can take a look at those links for explanations:
http://en.wikipedia.org/wiki/Imaging_phantom
http://en.wikipedia.org/wiki/Ellipsoid
http://en.wikipedia.org/wiki/Euler_angles

This module is largely inspired by :
http://www.mathworks.com/matlabcentral/fileexchange/9416-3d-shepp-logan-phantom

Author
------
Nicolas Barbey

"""
import numpy as np
__all__ = [
 'phantom', 'shepp_logan', 'modified_shepp_logan', 'yu_ye_wang']

def phantom(shape, parameters_list, dtype=np.float64):
    """
    Generate a cube of given shape using a list of ellipsoid
    parameters.

    Inputs
    ------
    shape: tuple of ints
        Shape of the output cube.

    parameters_list: list of dictionaries
        List of dictionaries with the parameters defining the ellipsoids to
        include in the cube.

    dtype: data-type
        Data type of the output ndarray.

    Output
    ------
    cube: 3-dimensional ndarray
        A 3-dimensional ndarray filled with the specified ellipsoids.

    See Also
    --------
    shepp_logan : Generates the Shepp Logan phantom in any shape.
    modified_shepp_logan : Modified Shepp Logan phantom in any shape.
    yu_ye_wang : The Yu Ye Wang phantom in any shape.
    ellipsoid : Generates a cube filled with an ellipsoid of any shape.

    Notes
    -----
    http://en.wikipedia.org/wiki/Imaging_phantom
    """
    cube = np.zeros(shape, dtype=dtype)
    coordinates = define_coordinates(shape)
    for parameters in parameters_list:
        ellipsoid(parameters, out=cube, coordinates=coordinates)

    return cube


def ellipsoid(parameters, shape=None, out=None, coordinates=None):
    """
    Generate a cube containing an ellipsoid defined by its parameters.
    If out is given, fills the given cube instead of creating a new
    one.
    """
    if shape is None and out is None:
        raise ValueError('You need to set shape or out')
    if out is None:
        out = np.zeros(shape)
    if shape is None:
        shape = out.shape
    if len(shape) == 1:
        shape = (
         shape, shape, shape)
    elif len(shape) == 2:
        shape = (
         shape[0], shape[1], 1)
    elif len(shape) > 3:
        raise ValueError('input shape must be lower or equal to 3')
    if coordinates is None:
        coordinates = define_coordinates(shape)
    coords = transform(coordinates, parameters)
    coords = [ np.asarray(u) for u in coords ]
    x, y, z = coords
    x.resize(shape)
    y.resize(shape)
    z.resize(shape)
    out[(x ** 2 + y ** 2 + z ** 2 <= 1.0)] += parameters['A']
    return out


def rotation_matrix(p):
    """
    Defines an Euler rotation matrix from angles phi, theta and psi.

    Notes
    -----
    http://en.wikipedia.org/wiki/Euler_angles
    """
    cphi = np.cos(np.radians(p['phi']))
    sphi = np.sin(np.radians(p['phi']))
    ctheta = np.cos(np.radians(p['theta']))
    stheta = np.sin(np.radians(p['theta']))
    cpsi = np.cos(np.radians(p['psi']))
    spsi = np.sin(np.radians(p['psi']))
    alpha = [
     [cpsi * cphi - ctheta * sphi * spsi,
      cpsi * sphi + ctheta * cphi * spsi,
      spsi * stheta],
     [
      -spsi * cphi - ctheta * sphi * cpsi,
      -spsi * sphi + ctheta * cphi * cpsi,
      cpsi * stheta],
     [
      stheta * sphi,
      -stheta * cphi,
      ctheta]]
    return np.asarray(alpha)


def define_coordinates(shape):
    """
    Generate a tuple of coordinates in 3d with a given shape
    """
    mgrid = np.lib.index_tricks.nd_grid()
    cshape = np.asarray(complex(0.0, 1.0)) * shape
    x, y, z = mgrid[-1:1:cshape[0], -1:1:cshape[1], -1:1:cshape[2]]
    return (x, y, z)


def transform(coordinates, p):
    """
    Apply rotation, translation and rescaling to a 3-tuple of
    coordinates.
    """
    alpha = rotation_matrix(p)
    x, y, z = coordinates
    ndim = len(coordinates)
    out_coords = [ sum([ alpha[(j, i)] * coordinates[i] for i in xrange(ndim) ]) for j in xrange(ndim)
                 ]
    M0 = [p['x0'], p['y0'], p['z0']]
    sc = [p['a'], p['b'], p['c']]
    out_coords = [ (u - u0) / su for u, u0, su in zip(out_coords, M0, sc) ]
    return out_coords


parameters_tuple = [
 'A', 'a', 'b', 'c', 'x0', 'y0', 'z0', 'phi', 'theta', 'psi']
modified_shepp_logan_array = [
 [
  1, 0.69, 0.92, 0.81, 0.0, 0.0, 0, 0, 0, 0],
 [
  -0.8, 0.6624, 0.874, 0.78, 0.0, -0.0184, 0, 0, 0, 0],
 [
  -0.2, 0.11, 0.31, 0.22, 0.22, 0.0, 0, -18, 0, 10],
 [
  -0.2, 0.16, 0.41, 0.28, -0.22, 0.0, 0, 18, 0, 10],
 [
  0.1, 0.21, 0.25, 0.41, 0.0, 0.35, -0.15, 0, 0, 0],
 [
  0.1, 0.046, 0.046, 0.05, 0.0, 0.1, 0.25, 0, 0, 0],
 [
  0.1, 0.046, 0.046, 0.05, 0.0, -0.1, 0.25, 0, 0, 0],
 [
  0.1, 0.046, 0.023, 0.05, -0.08, -0.605, 0, 0, 0, 0],
 [
  0.1, 0.023, 0.023, 0.02, 0.0, -0.606, 0, 0, 0, 0],
 [
  0.1, 0.023, 0.046, 0.02, 0.06, -0.605, 0, 0, 0, 0]]
shepp_logan_array = np.copy(modified_shepp_logan_array)
shepp_logan_array[0] = [1, -0.98, -0.02, -0.02, 0.01, 0.01, 0.01, 0.01, 0.01, 0.01]
yu_ye_wang_array = [
 [
  1, 0.69, 0.92, 0.9, 0, 0, 0, 0, 0, 0],
 [
  -0.8, 0.6624, 0.874, 0.88, 0, 0, 0, 0, 0, 0],
 [
  -0.2, 0.41, 0.16, 0.21, -0.22, 0, -0.25, 108, 0, 0],
 [
  -0.2, 0.31, 0.11, 0.22, 0.22, 0, -0.25, 72, 0, 0],
 [
  0.2, 0.21, 0.25, 0.5, 0, 0.35, -0.25, 0, 0, 0],
 [
  0.2, 0.046, 0.046, 0.046, 0, 0.1, -0.25, 0, 0, 0],
 [
  0.1, 0.046, 0.023, 0.02, -0.08, -0.65, -0.25, 0, 0, 0],
 [
  0.1, 0.046, 0.023, 0.02, 0.06, -0.65, -0.25, 90, 0, 0],
 [
  0.2, 0.056, 0.04, 0.1, 0.06, -0.105, 0.625, 90, 0, 0],
 [
  -0.2, 0.056, 0.056, 0.1, 0, 0.1, 0.625, 0, 0, 0]]

def _array_to_parameters(array):
    array = np.asarray(array)
    out = []
    for i in xrange(array.shape[0]):
        tmp = dict()
        for k, j in zip(parameters_tuple, xrange(array.shape[1])):
            tmp[k] = array[(i, j)]

        out.append(tmp)

    return out


modified_shepp_logan_parameters = _array_to_parameters(modified_shepp_logan_array)
shepp_logan_parameters = _array_to_parameters(shepp_logan_array)
yu_ye_wang_parameters = _array_to_parameters(yu_ye_wang_array)

def modified_shepp_logan(shape, **kargs):
    return phantom(shape, modified_shepp_logan_parameters, **kargs)


def shepp_logan(shape, **kargs):
    return phantom(shape, shepp_logan_parameters, **kargs)


def yu_ye_wang(shape, **kargs):
    return phantom(shape, yu_ye_wang_parameters, **kargs)


common_docstring = '\n    Generates a %(name)s phantom with a given shape and\n    dtype.\n\n    Inputs\n    ------\n    shape: 3-tuple of ints\n       Shape of the 3d output cube.\n    dtype: data-type\n       Data type of the output cube.\n\n    Output\n    ------\n    cube: ndarray\n       3-dimensional phantom.\n\n'
modified_shepp_logan_docstring = common_docstring % {'name': 'Modified Shepp-Logan'}
shepp_logan_docstring = common_docstring % {'name': 'Shepp-Logan'}
yu_ye_wang_docstring = common_docstring % {'name': 'Yu Ye Wang'}