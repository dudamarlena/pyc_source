# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/plot/pv.py
# Compiled at: 2020-04-28 06:23:53
# Size of source mod 2**32: 4504 bytes
"""Prepare data in spherical coordinates for pyvista plotting."""
from warnings import warn
import numpy as np
from pyvista import grid_from_sph_coords, transform_vectors_sph_to_cart
from ..coord import _cell_bounds
from ..exceptions import AeolusWarning
__all__ = ('grid_for_scalar_cube_sph', 'grid_for_vector_cubes_sph')

def grid_for_scalar_cube_sph(cube, z_scale=1, z_offset=0, grid=None, label='scalar3d'):
    """
    Create a `pyvista` grid for an `iris` cube (2D or 3D) in spherical coordinates.

    Parameters
    ----------
    cube: iris.cube.Cube
        2D or 3D cube with (longitude, latitude, [level_height]) coordinates.
    z_scale: float, optional
        Scaling factor for the vertical level dimension.
    z_offset: float, optional
        Scaling offset for the vertical level dimension.
    grid: pyvista.StructuredGrid, optional
        If given, add data to the existing grid, otherwise create a new one from
        the input cube's coordinates.
    label: str, optional
        Label for the data within the grid.

    Returns
    -------
    pyvista.StructuredGrid
       PyVista grid with data in cell_arrays.
    """
    if grid is None:
        lons = _cell_bounds(cube.coord('longitude').points)
        lats = 90.0 - _cell_bounds(cube.coord('latitude').points)
        if cube.ndim == 3:
            levels = _cell_bounds(cube.coord('level_height').points)
        else:
            levels = np.array([0])
        levels = z_scale * levels + z_offset
        grid = grid_from_sph_coords(lons, lats, levels)
    if label in grid.cell_arrays:
        warn(f"Label '{label}' exists in {grid}", AeolusWarning)
    grid.cell_arrays[label] = np.array(cube.data).swapaxes(-2, -1).ravel('C')
    return grid


def grid_for_vector_cubes_sph(u, v, w, vector_scale=1, vertical_wind_scale=1, z_scale=1, z_offset=0, xstride=1, ystride=1, grid=None, label='vector3d'):
    """
    Take wind vectors in spherical coordinates and create a `pyvista` grid for them.

    Parameters
    ----------
    u: iris.cube.Cube
        2D or 3D cube of x-wind component (zonal wind).
    v: iris.cube.Cube
        2D or 3D cube of y-wind component (meridional wind).
    w: iris.cube.Cube
        2D or 3D cube of z-wind component (vertical wind).
    vector_scale: float, optional
        Scaling factor for vectors.
    vertical_wind_scale: float, optional
        Scaling factor for the vertical wind component (for better visibility).
    z_scale: float, optional
        Scaling factor for the vertical level dimension.
    z_offset: float, optional
        Scaling offset for the vertical level dimension.
    xstride: float, optional
        Stride along the longitude axis.
    ystride: float, optional
        Stride along the latitude axis.
    grid: pyvista.StructuredGrid, optional
        If given, add data to the existing grid, otherwise create a new one from
        the input cube's coordinates.
    label: str, optional
        Label for the data within the grid.

    Returns
    -------
    pyvista.StructuredGrid
       PyVista grid with vector data in point_arrays.
    """
    if not (u.shape == v.shape and u.shape == w.shape):
        raise AssertionError('Wind components should have the same array size!')
    lons = u.coord('longitude').points
    lats = 90.0 - u.coord('latitude').points
    levels = z_scale * u.coord('level_height').points + z_offset
    lons_s = lons[::xstride]
    lats_s = lats[::ystride]
    inv_axes = [
     *range(u.ndim - 1, -1, -1)]
    u_sdata = u.data[..., ::ystride, ::xstride].transpose(inv_axes)
    v_sdata = v.data[..., ::ystride, ::xstride].transpose(inv_axes)
    w_sdata = w.data[..., ::ystride, ::xstride].transpose(inv_axes)
    w_sdata *= vertical_wind_scale
    vectors = np.stack([i.transpose(inv_axes).swapaxes(u.ndim - 2, u.ndim - 1).ravel('C') for i in transform_vectors_sph_to_cart(lons_s, lats_s, levels, u_sdata, -v_sdata, w_sdata)],
      axis=1)
    vectors *= vector_scale
    if grid is None:
        grid = grid_from_sph_coords(lons_s, lats_s, levels)
    grid.point_arrays[label] = vectors
    return grid