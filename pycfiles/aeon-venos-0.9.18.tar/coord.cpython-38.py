# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aeolus/coord.py
# Compiled at: 2020-04-29 11:39:12
# Size of source mod 2**32: 21299 bytes
__doc__ = 'Functionality related to coordinates of cubes.'
from warnings import warn
from cartopy.util import add_cyclic_point
import iris
from iris.analysis.cartography import wrap_lons
from iris.coord_categorisation import _months_in_season, add_categorised_coord
from iris.util import broadcast_to_shape, guess_coord_axis, is_regular
import numpy as np
from .const import get_planet_radius
from .exceptions import AeolusWarning, ArgumentError, NotFoundError
__all__ = ('UM_TIME', 'UM_HGT', 'UM_LEV', 'UM_LATLON', 'UM_Z_COORDS', 'UM_TIME_COORDS',
           'add_binned_lon_lat', 'add_cyclic_point_to_cube', 'area_weights_cube',
           'coarsen_cube', 'coord_to_cube', 'ensure_bounds', 'get_cube_datetimes',
           'get_dim_coord', 'nearest_coord_value', 'not_equal_coord_axes', 'regrid_3d',
           'replace_z_coord', 'roll_cube_0_360', 'roll_cube_pm180', 'vertical_cross_section_area')
UM_TIME = 'time'
UM_HGT = 'level_height'
UM_LATLON = ['latitude', 'longitude']
UM_SIGMA = 'sigma'
UM_LEV = 'model_level_number'
UM_Z_COORDS = [UM_SIGMA, UM_LEV]
UM_TIME_COORDS = ['forecast_reference_time', 'forecast_period', UM_TIME]

def _is_longitude_global(lon_points):
    """Return True if array of longitudes covers the whole sphere."""
    dx = np.diff(lon_points)[0]
    case_0_360 = lon_points[0] - dx <= 0 and lon_points[(-1)] + dx >= 360
    case_pm180 = lon_points[0] - dx <= -180 and lon_points[(-1)] + dx >= 180
    return case_0_360 or 


def roll_cube_pm180(cube_in, coord_name=UM_LATLON[1], inplace=False):
    """
    Take a cube spanning 0...360 degrees in longitude and roll it to -180...180 degrees.

    Works with global model output, and in some cases for regional.

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube with longitude and latitude coordinates.
    coord_name: str, optional
        Name of the longitude coordinate.
    inplace: bool, optional
        Do this in-place or copy the cube.

    Returns
    -------
    iris.cube.Cube

    See also
    --------
    aeolus.coord.roll_cube_0_360
    """
    if inplace:
        cube = cube_in
    else:
        cube = cube_in.copy()
    xcoord = cube.coord(coord_name)
    if (xcoord.points >= 0.0).all():
        if not is_regular(xcoord):
            raise AssertionError('Operation is only valid for a regularly spaced coordinate.')
        else:
            if _is_longitude_global(xcoord.points):
                cube.data = np.roll((cube.data), (len(xcoord.points) // 2), axis=(-1))
            if xcoord.has_bounds():
                bounds = wrap_lons(xcoord.bounds, -180, 360)
                bounds = bounds[bounds[:, 0].argsort(axis=0)]
            else:
                bounds = None
        cube.replace_coord(xcoord.copy(points=(np.sort(wrap_lons(xcoord.points, -180, 360))), bounds=bounds))
    else:
        msg = f"Incorrect {coord_name} values: from {xcoord.points.min()} to {xcoord.points.max()}"
    if not ((xcoord.points >= -180.0) & (xcoord.points <= 180.0)).all():
        raise AssertionError(msg)
    else:
        return inplace or cube


def roll_cube_0_360(cube_in, inplace=False):
    """
    Take a cube spanning -180...180 degrees in longitude and roll it to 0...360 degrees.

    Works with global model output, and in some cases for regional.

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube with longitude and latitude coordinates.
    coord_name: str, optional
        Name of the longitude coordinate.
    inplace: bool, optional
        Do this in-place or copy the cube.

    Returns
    -------
    iris.cube.Cube

    See also
    --------
    aeolus.coord.roll_cube_pm180
    """
    if inplace:
        cube = cube_in
    else:
        cube = cube_in.copy()
    lon = cube.coord('longitude')
    if (lon.points < 0.0).any():
        add = 180
        cube.data = np.roll((cube.data), (len(lon.points) // 2), axis=(-1))
        if lon.has_bounds():
            bounds = lon.bounds + add
        else:
            bounds = None
        cube.replace_coord(lon.copy(points=(lon.points + add), bounds=bounds))
    else:
        return inplace or cube


def area_weights_cube(cube, r_planet=None, normalize=False):
    """
    Create a cube of area weights for an arbitrary planet.

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube with longitude and latitude coordinates
    r_planet: float, optional
        Radius of the planet.
    normalize: bool, optional
        Normalize areas.

    Returns
    -------
    iris.cube.Cube
        Cube of area weights with the same metadata as the input cube
    """
    cube = cube.copy()
    ensure_bounds(cube)
    aw = iris.analysis.cartography.area_weights(cube, normalize=normalize)
    if normalize:
        aw = cube.copy(data=aw)
        aw.rename('normalized_grid_cell_area')
        aw.units = '1'
    else:
        if r_planet is None:
            r = get_planet_radius(cube)
        else:
            r = r_planet
        aw *= (r / iris.fileformats.pp.EARTH_RADIUS) ** 2
        aw = cube.copy(data=aw)
        aw.rename('grid_cell_area')
        aw.units = 'm**2'
    return aw


def vertical_cross_section_area(cube2d, r_planet=None):
    """Create a cube of vertical cross-section areas in metres."""
    cube2d = cube2d.copy()
    if r_planet is None:
        r = get_planet_radius(cube2d)
    else:
        r = r_planet
    m_per_deg = np.pi / 180 * r
    if iris.util.guess_coord_axis(cube2d.dim_coords[1]) == 'X':
        m_per_deg *= np.cos(np.deg2rad(cube2d.coord(axis='Y').points[0]))
    for dim_coord in cube2d.dim_coords:
        if not dim_coord.has_bounds():
            dim_coord.guess_bounds()
        x_bounds = cube2d.coord(cube2d.dim_coords[1]).bounds
        z_bounds = cube2d.coord(cube2d.dim_coords[0]).bounds
        vc_area = cube2d.copy(data=((z_bounds[:, 1] - z_bounds[:, 0])[:, None] * ((x_bounds[:, 1] - x_bounds[:, 0])[None, :] * m_per_deg)))
        vc_area.units = 'm**2'
        vc_area.rename('vertical_section_area')
        for dim_coord in vc_area.dim_coords:
            dim_coord.bounds = None

        return vc_area


def _cell_bounds(points, bound_position=0.5):
    """
    Calculate coordinate cell boundaries.

    Taken from SciTools iris package.

    Parameters
    ----------
    points: numpy.array
        One-dimensional array of uniformy spaced values of shape (M,)
    bound_position: bool, optional
        The desired position of the bounds relative to the position
        of the points.

    Returns
    -------
    bounds: numpy.array
        Array of shape (M+1,)

    Examples
    --------
    >>> a = np.arange(-1, 2.5, 0.5)
    >>> a
    array([-1. , -0.5,  0. ,  0.5,  1. ,  1.5,  2. ])
    >>> cell_bounds(a)
    array([-1.25, -0.75, -0.25,  0.25,  0.75,  1.25,  1.75,  2.25])

    See Also
    --------
    aeolus.coord._cell_centres
    """
    assert points.ndim == 1, 'Only 1D points are allowed'
    diffs = np.diff(points)
    if not np.allclose(diffs, diffs[0]):
        warn('_cell_bounds() is supposed to work only for uniformly spaced points', AeolusWarning)
    delta = diffs[0] * bound_position
    bounds = np.concatenate([[points[0] - delta], points + delta])
    return bounds


def _cell_centres(bounds, bound_position=0.5):
    """
    Calculate coordinate cell centres.

    Taken from SciTools iris package.

    Parameters
    ----------
    bounds: numpy.array
        One-dimensional array of cell boundaries of shape (M,)
    bound_position: bool, optional
        The desired position of the bounds relative to the position
        of the points.

    Returns
    -------
    centres: numpy.array
        Array of shape (M-1,)

    Examples
    --------
    >>> a = np.arange(-1, 3., 1.)
    >>> a
    array([-1,  0,  1,  2])
    >>> cell_centres(a)
    array([-0.5,  0.5,  1.5])

    See Also
    --------
    aeolus.coord._cell_bounds
    """
    assert bounds.ndim == 1, 'Only 1D points are allowed'
    deltas = np.diff(bounds) * bound_position
    centres = bounds[:-1] + deltas
    return centres


def add_binned_lon_lat(cube, lon_bins, lat_bins, coord_names=UM_LATLON, inplace=False):
    """
    Add binned longitude and latitude as auxiliary coordinates to a cube.

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube with longitude and latitude coordinates.
    lon_bins: array-like
        Longitude bins.
    lat_bins: array-like
        Latitude bins.
    coord_names: list, optional
        List of latitude and longitude labels.
    inplace: bool, optional
        Do this in-place or copy the cube.

    Returns
    -------
    iris.cube.Cube
    """
    if inplace:
        cube_out = cube
    else:
        cube_out = cube.copy()
    for name, target_points in zip(coord_names, (lat_bins, lon_bins)):
        binned_points = np.digitize(cube_out.coord(name).points, target_points)
        binned_points = np.clip(binned_points, 0, len(target_points) - 1)
        new_coord = iris.coords.AuxCoord(binned_points, long_name=f"{name}_binned")
        cube_out.add_aux_coord(new_coord, cube_out.coord_dims(name))

    return cube_out


def coarsen_cube(cube, lon_bins, lat_bins, coord_names=UM_LATLON, inplace=False):
    """
    Block-average cube in longitude and latitude.

    Note: no weighting is applied!

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube with longitude and latitude coordinates.
    lon_bins: array-like
        Longitude bins.
    lat_bins: array-like
        Latitude bins.
    coord_names: list, optional
        List of latitude and longitude labels.
    inplace: bool, optional
        Do this in-place or copy the cube.

    Returns
    -------
    iris.cube.Cube
    """
    if inplace:
        cube_out = cube
    else:
        cube_out = cube.copy()
    add_binned_lon_lat(cube_out, lon_bins, lat_bins, coord_names=coord_names, inplace=True)
    for coord, target_points in zip(coord_names, (lat_bins, lon_bins)):
        cube_out = cube_out.extract((iris.Constraint)(**{coord: lambda p: target_points.min() <= p <= target_points.max()}))

    for coord in coord_names:
        cube_out = cube_out.aggregated_by([f"{coord}_binned"], iris.analysis.MEAN)

    for coord, target_points in zip(coord_names, (lat_bins, lon_bins)):
        dim = cube_out.coord_dims(coord)
        units = cube_out.coord(coord).units
        cube_out.remove_coord(coord)
        aux = cube_out.coord(f"{coord}_binned")
        new_points = target_points[aux.points]
        new_coord = iris.coords.DimCoord.from_coord(aux.copy(points=new_points, bounds=None))
        cube_out.remove_coord(f"{coord}_binned")
        new_coord.rename(coord)
        new_coord.units = units
        cube_out.add_dim_coord(new_coord, dim)

    return cube_out


def get_cube_datetimes(cube):
    """Get a list of `iris.cube.Cube`'s time points as `datetime.datetime`s."""
    return cube.coord('time').units.num2date(cube.coord('time').points)


def nearest_coord_value(cube, coord_name, val):
    """
    Get the nearest value of a coordinate.

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube with the coordinate
    coord_name: str or iris.coords.Coord
        Coordinate where to look the nearest point up
    val: int or float
        The value to find

    Returns
    -------
    int or float
        element of the coordinate array closest to the given `val`
    """
    coord = cube.coord(coord_name)
    i = coord.nearest_neighbour_index(val)
    return coord.points[i]


def coord_to_cube(cube, coord):
    """
    Convert coordinate points to a cube of the same dimension as the given cube.

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube containing the coordinate to be broadcast.
    coord: str or iris.coords.Coord
        Coordinate to be broadcast

    Returns
    -------
    iris.cube.Cube
        Cube of broadcast coordinate
    """
    if isinstance(coord, str):
        _coord = cube.coord(coord)
    else:
        _coord = coord
    dim_map = cube.coord_dims(_coord.name())
    _data = _coord.points
    if len(dim_map) > 0:
        _data = broadcast_to_shape(_data, cube.shape, dim_map)
        dc = [(c.copy(), cube.coord_dims(c)) for c in cube.dim_coords]
        ac = [(c.copy(), cube.coord_dims(c)) for c in cube.aux_coords]
        new_cube = iris.cube.Cube(data=_data,
          units=(_coord.units),
          long_name=(_coord.name()),
          dim_coords_and_dims=dc,
          aux_coords_and_dims=ac)
    else:
        new_cube = iris.cube.Cube(data=_data, standard_name=(_coord.name()), units=(_coord.units))
    return new_cube


def ensure_bounds(cube, coords=UM_LATLON):
    """Auto-generate bounds for cube coordinates."""
    for coord_name in coords:
        c = cube.coord(coord_name)
        if not c.has_bounds():
            if len(c.points) > 1:
                c.guess_bounds()


def not_equal_coord_axes(cube1, cube2):
    """Given 2 cubes, return axes of unequal dimensional coordinates."""
    coord_comp = iris.analysis.coord_comparison(cube1, cube2)
    neq_dim_coords = set(coord_comp['not_equal']).intersection(set(coord_comp['dimensioned']))
    dims = []
    for coord_pair in neq_dim_coords:
        for coord in coord_pair:
            dims.append(iris.util.guess_coord_axis(coord))

        return set(filter(None, dims))


def regrid_3d(cube, target, vert_coord=None):
    """
    Regrid a cube in the horizontal and in the vertical on to coordinates of the target cube.

    Adapted from https://github.com/LSaffin/iris-extensions

    Parameters
    ----------
    cube: iris.cube.Cube
        The cube to be regridded.
    target: iris.cube.Cube
        The cube to regrid to.
    vert_coord: str or iris.coords.Coord, optional
        The coordinate for the vertical interpolation.
        If not given, the target's z-axis `iris.coord.DimCoord` is used.

    Returns
    -------
        iris.cube.Cube
    """
    neq_axes = not_equal_coord_axes(cube, target)
    if neq_axes.intersection(['X', 'Y']):
        cube = cube.regrid(target, iris.analysis.Linear())
    if 'Z' in neq_axes:
        if vert_coord is None:
            z = get_dim_coord(target, 'z')
        else:
            z = target.coord(vert_coord)
        cube = cube.interpolate([(z.name(), z.points)], iris.analysis.Linear())
        ensure_bounds(cube, coords=[z])
    return cube


def get_dim_coord(cube, axis):
    """
    Return a coordinate from a cube based on the axis it represents.

    Uses :py:func:`iris.util.guess_coord_axis` to heuristically match a dimensional coordinate
    with the requested axis.

    Adapted from https://github.com/LSaffin/iris-extensions

    Parameters
    ----------
    cube: iris.cube.Cube
        Cube with the desired coordinate.
    axis: str
        The co-ordinate axis to take from the cube. Must be one of X, Y, Z, T.

    Returns
    -------
    iris.coords.DimCoord
        The dimensional coordinate matching the requested axis on the given cube.

    Raises
    ------
    ArgumentError: If axis is not one of {X, Y, Z, T}.
    NotFoundError: If the cube does not contain a coord with the requested axis.
    """
    _allowed = [
     'X', 'Y', 'Z', 'T']
    axis = axis.upper()
    if axis not in _allowed:
        raise ArgumentError(f"Axis must be one of {_allowed}, {axis} is given.")
    for coord in cube.dim_coords:
        if axis == guess_coord_axis(coord):
            return coord
        raise NotFoundError(f"Cube has no coordinate for axis {axis}")


def replace_z_coord(cube, promote_coord=UM_HGT, remove_coord=UM_Z_COORDS):
    """
    Replace dimensional vertical coordinate.

    Parameters
    ----------
    cube: iris.cube.Cube
        Input cube.
    promote_coord: str or iris.coords.Coord
        Coordinate to become a dimensional z-coordinate.
    remove_coord: list-like
        List of coordinates to remove.
        By default, model levels and sigma coordinates are removed.

    Returns
    -------
    iris.cube.Cube
        Copy of the input cube with a new vertical coordinate.
    """
    new_cube = cube.copy()
    new_cube.coord(promote_coord).bounds = None
    iris.util.promote_aux_coord_to_dim_coord(new_cube, promote_coord)
    ensure_bounds(new_cube, coords=[promote_coord])
    for coord in remove_coord:
        try:
            new_cube.remove_coord(coord)
        except iris.exceptions.CoordinateNotFoundError:
            pass

    return new_cube


def add_cyclic_point_to_cube--- This code section failed: ---

 L. 608         0  LOAD_DEREF               'cube'
                2  LOAD_METHOD              coord
                4  LOAD_FAST                'coord'
                6  CALL_METHOD_1         1  ''
                8  STORE_DEREF              'the_coord'

 L. 609        10  LOAD_DEREF               'cube'
               12  LOAD_METHOD              coord_dims
               14  LOAD_DEREF               'the_coord'
               16  CALL_METHOD_1         1  ''
               18  STORE_DEREF              'dim'

 L. 611        20  LOAD_GLOBAL              add_cyclic_point
               22  LOAD_DEREF               'cube'
               24  LOAD_ATTR                data
               26  LOAD_DEREF               'the_coord'
               28  LOAD_ATTR                points
               30  LOAD_DEREF               'dim'
               32  LOAD_CONST               0
               34  BINARY_SUBSCR    
               36  LOAD_CONST               ('coord', 'axis')
               38  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
               40  UNPACK_SEQUENCE_2     2 
               42  STORE_FAST               'cy_data'
               44  STORE_FAST               'cy_coord_pnts'

 L. 613        46  LOAD_CLOSURE             'cube'
               48  LOAD_CLOSURE             'the_coord'
               50  BUILD_TUPLE_2         2 
               52  LOAD_LISTCOMP            '<code_object <listcomp>>'
               54  LOAD_STR                 'add_cyclic_point_to_cube.<locals>.<listcomp>'
               56  MAKE_FUNCTION_8          'closure'

 L. 614        58  LOAD_DEREF               'cube'
               60  LOAD_ATTR                dim_coords

 L. 613        62  GET_ITER         
               64  CALL_FUNCTION_1       1  ''
               66  STORE_FAST               'dim_coords_and_dims'

 L. 616        68  LOAD_FAST                'dim_coords_and_dims'
               70  LOAD_METHOD              append
               72  LOAD_DEREF               'the_coord'
               74  LOAD_METHOD              copy
               76  LOAD_FAST                'cy_coord_pnts'
               78  CALL_METHOD_1         1  ''
               80  LOAD_DEREF               'dim'
               82  BUILD_TUPLE_2         2 
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          

 L. 618        88  LOAD_CLOSURE             'cube'
               90  LOAD_CLOSURE             'dim'
               92  BUILD_TUPLE_2         2 
               94  LOAD_LISTCOMP            '<code_object <listcomp>>'
               96  LOAD_STR                 'add_cyclic_point_to_cube.<locals>.<listcomp>'
               98  MAKE_FUNCTION_8          'closure'

 L. 620       100  LOAD_DEREF               'cube'
              102  LOAD_ATTR                aux_coords

 L. 618       104  GET_ITER         
              106  CALL_FUNCTION_1       1  ''
              108  STORE_FAST               'aux_coords_and_dims'

 L. 623       110  LOAD_CLOSURE             'cube'
              112  BUILD_TUPLE_1         1 
              114  LOAD_DICTCOMP            '<code_object <dictcomp>>'
              116  LOAD_STR                 'add_cyclic_point_to_cube.<locals>.<dictcomp>'
              118  MAKE_FUNCTION_8          'closure'

 L. 625       120  LOAD_CONST               ('attributes', 'standard_name', 'long_name', 'var_name', 'units', 'cell_methods', 'aux_factories', 'cell_measures_and_dims')

 L. 623       122  GET_ITER         
              124  CALL_FUNCTION_1       1  ''
              126  STORE_FAST               'other_kwargs'

 L. 636       128  LOAD_GLOBAL              iris
              130  LOAD_ATTR                cube
              132  LOAD_ATTR                Cube

 L. 637       134  LOAD_FAST                'cy_data'

 L. 636       136  BUILD_TUPLE_1         1 

 L. 638       138  LOAD_FAST                'dim_coords_and_dims'

 L. 639       140  LOAD_FAST                'aux_coords_and_dims'

 L. 636       142  LOAD_CONST               ('dim_coords_and_dims', 'aux_coords_and_dims')
              144  BUILD_CONST_KEY_MAP_2     2 

 L. 640       146  LOAD_FAST                'other_kwargs'

 L. 636       148  BUILD_MAP_UNPACK_WITH_CALL_2     2 
              150  CALL_FUNCTION_EX_KW     1  'keyword args'
              152  STORE_FAST               'cyclic_cube'

 L. 642       154  LOAD_FAST                'cyclic_cube'
              156  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 114


def add_planet_calendar(cube, time_coord, days_in_year, days_in_month, days_in_day, run_start_day=0, seasons=('djf', 'mam', 'jja', 'son'), planet='planet'):
    """
    Add an auxiliary time axis with the non-Earth period lengths.

    Parameters
    ----------
    cube: iris.cube.Cube
        Input cube.
    time_coord: iris.coords.Coord or str
        Original time coordinate of the cube.
    days_in_year: int or float
        Number of Earth days in one year on the given planet.
    days_in_month: int or float
        Number of Earth days in one month on the given planet.
    days_in_day: int or float
        Number of Earth days in one day on the given planet (e.g. ~16 for Titan).
    run_start_day: int or float, optional
        Earth day of the start of the simulation.
    seasons: tuple, optional
        Sequences of letters corresponding to month names.
    planet: str, optional
        Name of the planet to be used to name the new coordinate.
    """

    def rel_day(coord, value):
        start = coord.units.num2date(coord.points[0])
        current = coord.units.num2date(value)
        iday = run_start_day + (current - start).days
        return iday

    def determine_season(coord, value):
        assert coord.name() == f"{planet}_month"
        for season in seasons:
            if value + 1 in _months_in_season(season):
                return season

    new_coords = {'year':lambda c, v: rel_day(c, v) // days_in_year,  'month':lambda c, v: rel_day(c, v) % days_in_year // days_in_month, 
     'day':lambda c, v: rel_day(c, v) % days_in_month // days_in_day, 
     'season':determine_season}
    for key, op in new_coords.items():
        if key == 'season':
            coord = f"{planet}_month"
        else:
            coord = time_coord
        add_categorised_coord(cube, f"{planet}_{key}", coord, op)