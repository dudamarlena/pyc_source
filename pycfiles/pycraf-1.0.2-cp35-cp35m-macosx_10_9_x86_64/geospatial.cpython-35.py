# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/runner/runners/2.166.2/work/1/s/build/lib.macosx-10.9-x86_64-3.5/pycraf/geospatial/geospatial.py
# Compiled at: 2020-04-16 04:29:51
# Size of source mod 2**32: 24636 bytes
from __future__ import absolute_import, unicode_literals, division, print_function
from enum import Enum
import re
from functools import partial, lru_cache
import numpy as np, numbers
from astropy import units as apu
from .. import utils
__all__ = [
 'EPSG', 'ESRI', 'utm_zone_from_gps', 'epsg_from_utm_zone',
 'utm_to_wgs84', 'wgs84_to_utm',
 'etrs89_to_wgs84', 'wgs84_to_etrs89',
 'itrf2005_to_wgs84', 'wgs84_to_itrf2005',
 'itrf2008_to_wgs84', 'wgs84_to_itrf2008',
 'transform_factory']

class EPSG(Enum):
    __doc__ = '\n    Enum with often used EPSG codes.\n    '
    WGS84 = 4326
    ETRS89 = 3035
    ITRF00 = 4919
    ITRF05 = 4896
    ITRF08 = 5332
    WEB_MERC = 3857


class ESRI(Enum):
    __doc__ = '\n    Enum with often used ESRI codes.\n    '
    MERCATOR = '+proj=merc +lat_ts=0 +lon_0=0 +k=1.000000 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
    SINUSOIDAL = '+proj=sinu +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
    MOLLWEIDE = '+proj=moll +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
    GALL = '+proj=gall +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
    BONNE = '+ellps=WGS84 +datum=WGS84 +units=m no_defs'
    STEREO = '+proj=stere +lat_0=0 +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'
    ROBINSON = '+proj=robin +lon_0=0 +x_0=0 +y_0=0 +ellps=WGS84 +datum=WGS84 +units=m no_defs'


UTM_ZONE_RE = re.compile('^(?P<zone>[1-9]|[1-5][0-9]|60)(?P<ns>[nsNS])$')
DOC_TEMPLATE = '\n    Convert coordinates from `sys_in` to `sys_out`.\n\n    - `sys_in`: {sys_in}\n    - `sys_out`: {sys_out}\n\n    Parameters\n    ----------\n    {parameters}\n    Returns\n    -------\n    {returns}\n\n    '
DOC_LONLAT_2D = 'lon, lat : `~astropy.units.Quantity`\n        {} longitude and latitude [deg]\n    '
DOC_LONLAT_3D = 'lon, lat : `~astropy.units.Quantity`\n        {} longitude and latitude [deg]\n    height : `~astropy.units.Quantity`\n        Height (amsl) [m]\n    '
DOC_WORLD_2D = 'x, y : `~astropy.units.Quantity`\n        {} world coordinates [m]\n    '
DOC_WORLD_3D = 'x, y, z : `~astropy.units.Quantity`\n        {} geocentric coordinates [m]\n    '

@utils.ranged_quantity_input(glon=(
 None, None, apu.deg), glat=(
 None, None, apu.deg), strip_input_units=True, output_unit=None)
def utm_zone_from_gps(glon, glat):
    """
    UTM zone code from GPS coordinates.

    Parameters
    ----------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]

    Returns
    -------
    utm_zone : `~numpy.array`, str
        UTM zone code(s)
    """
    glon = np.atleast_1d(glon)
    glat = np.atleast_1d(glat)
    glon = (glon + 180) % 360 - 180
    zone = (np.int32(np.floor(glon + 180)) // 6 + 1).astype('<U2')
    ns = np.where(glat >= 0, 'N', 'S')
    utm = np.char.add(zone, ns).squeeze()
    if utm.size == 1:
        return str(utm)
    else:
        return utm


def epsg_from_utm_zone(utm_zone):
    """
    EPSG number for UTM zone code.

    Parameters
    ----------
    utm_zone : `~numpy.array`, str
        UTM zone code(s)

    Returns
    -------
    epsg : int
        EPSG code for the UTM zone

    Notes
    -----
    Unlike `~pycraf.geospatial.utm_zone_from_gps` this function does
    not support broadcasting. This is because the transform
    functions also not allow to convert arrays of coordinates
    with different projections (or EPSG codes).
    """
    match = UTM_ZONE_RE.match(utm_zone)
    if not (match and len(match.groups()) == 2):
        raise ValueError('{} is not a valid UTM zone'.format(utm_zone))
    zone, ns = match.groups()
    if ns.upper() == 'N':
        return 32600 + int(zone)
    if ns.upper() == 'S':
        return 32700 + int(zone)


@lru_cache(maxsize=64, typed=True)
def _create_transform(sys1, sys2, code_in='epsg', code_out='epsg'):
    """
    Helper function to create and cache `~pyproj.transform` functions
    with the desired coordinate projections binded.

    Parameters
    ----------
    sys_in, sys_out : str, int, EPSG, ESRI
        Input and output projection for the desired coordinate
        transformation. If a string, this is directly fed into the
        `~pyproj.Proj` class. If an integer, it is treated as an
        *EPSG* or *ESRI* code and the `~pyproj.Proj` class is
        instantiated with `"epsg:{code}"` or
        `"esri:{code}"`, depending on the `code_[in,out]` value.
        For convenience, a couple of common systems are defined in the
        `~pycraf.geospatial.EPSG` and `~pycraf.geospatial.ESRI` Enums
        (which just hold the associated *EPSG* or *ESRI* code for each
        name), e.g., `EPSG.WGS84 == 4326`.
    code_in, code_out : {'epsg', 'esri'}
        Whether to interpret integer-valued `sys_[in,out]` arguments
        as *EPSG* or *ESRI* code. (default: 'epsg')

    Returns
    -------
    transform_func : Function
        Transform function created from binding `~pyproj.transform`
        with the two desired projections.

    Notes
    -----
    Note, that ESRI codes are not supported anymore in `pyproj>=2.0`,
    but you can still use the `proj4` string instantiation of course.
    """
    try:
        import pyproj
    except ImportError:
        raise ImportError('The "pyproj" package is necessary to use this function.')

    sys = [
     sys1, sys2]
    code = [code_in.lower(), code_out.lower()]
    for i in [0, 1]:
        if not isinstance(sys[i], (int, str, EPSG, ESRI)):
            raise TypeError('Coordinate description for sys{} must be one of (int, str, EPSG, ESRI); got {}'.format(i + 1, sys[i]))
        if code[i] not in ('epsg', 'esri'):
            raise ValueError("`code` type for sys{} must be 'epsg' or 'esri'; got {}".format(i + 1, code[i]))
        if code[i] == 'esri' and pyproj.__version__ >= '2':
            raise ValueError('ESRI codes not supported anymore with pyproj >= 2.0')
        prefix = '+init=' if pyproj.__version__ < '2.0' else ''
        if isinstance(sys[i], int):
            sys[i] = '{}{}:{:04d}'.format(prefix, code[i], sys[i])
        else:
            if isinstance(sys[i], EPSG):
                sys[i] = '{}epsg:{:04d}'.format(prefix, sys[i].value)
            elif isinstance(sys[i], ESRI):
                sys[i] = '{:s}'.format(sys[i].value)

    if pyproj.__version__ >= '2.0':
        try:
            proj1 = pyproj.Proj(init=sys[0], preserve_units=False)
        except pyproj.exceptions.CRSError:
            proj1 = pyproj.Proj(sys[0], preserve_units=False)

        try:
            proj2 = pyproj.Proj(init=sys[1], preserve_units=False)
        except pyproj.exceptions.CRSError:
            proj2 = pyproj.Proj(sys[1], preserve_units=False)

        in_islatlon = proj1.crs.is_geographic
        out_islatlon = proj2.crs.is_geographic
        needs_3d = proj1.crs.is_geocentric or proj2.crs.is_geocentric
    else:
        proj1 = pyproj.Proj(sys[0].replace('no_defs', ''), preserve_units=False)
        proj2 = pyproj.Proj(sys[1].replace('no_defs', ''), preserve_units=False)
        in_islatlon = proj1.is_latlong()
        out_islatlon = proj2.is_latlong()
        needs_3d = proj1.is_geocent() or proj2.is_geocent()
    return (
     partial(pyproj.transform, proj1, proj2),
     in_islatlon, out_islatlon, needs_3d)


@utils.ranged_quantity_input(ulon=(
 None, None, apu.m), ulat=(
 None, None, apu.m), strip_input_units=True, output_unit=(apu.deg, apu.deg))
def utm_to_wgs84(ulon, ulat, utm_zone):
    """
    Convert UTM coordinates to GPS/WGS84.

    Parameters
    ----------
    ulon, ulat : `~astropy.units.Quantity`
        UTM longitude and latitude [m]
    utm_zone : str
        UTM zone string (e.g., 32N for longitudes 6 E to 12 E,
        northern hemisphere); see `Wikipedia
        <https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system>`_
        for more information on the zones

    Returns
    -------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]

    Notes
    -----
    - This function uses only the longitudal zone scheme. There is also
      the NATO system, which introduces latitude bands.
    """
    epsg = epsg_from_utm_zone(utm_zone)
    return _create_transform(epsg, EPSG.WGS84)[0](ulon, ulat)


@utils.ranged_quantity_input(glon=(
 None, None, apu.deg), glat=(
 None, None, apu.deg), strip_input_units=True, output_unit=(apu.m, apu.m))
def wgs84_to_utm(glon, glat, utm_zone):
    """
    Convert GPS/WGS84 coordinates to UTM.

    Parameters
    ----------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]
    utm_zone : str
        UTM zone string (e.g., 32N for longitudes 6 E to 12 E,
        northern hemisphere); see `Wikipedia
        <https://en.wikipedia.org/wiki/Universal_Transverse_Mercator_coordinate_system>`_
        for more information on the zones

    Returns
    -------
    ulon, ulat : `~astropy.units.Quantity`
        UTM longitude and latitude [m]

    Notes
    -----
    - This function uses only the longitudal zone scheme. There is also
      the NATO system, which introduces latitude bands.
    """
    epsg = epsg_from_utm_zone(utm_zone)
    return _create_transform(EPSG.WGS84, epsg)[0](glon, glat)


utm_to_wgs84_32N = partial(utm_to_wgs84, utm_zone='32N')
wgs84_to_utm_32N = partial(wgs84_to_utm, utm_zone='32N')

@utils.ranged_quantity_input(elon=(
 None, None, apu.m), elat=(
 None, None, apu.m), strip_input_units=True, output_unit=(apu.deg, apu.deg))
def etrs89_to_wgs84(elon, elat):
    """
    Convert ETSR89 coordinates to GPS/WGS84.

    ETRS89 is the European Terrestrial Reference System.
    (Using a Lambert Equal Area projection.)

    Parameters
    ----------
    elon, elat : `~astropy.units.Quantity`
        ETRS89 longitude and latitude [m]

    Returns
    -------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]

    """
    return _create_transform(EPSG.ETRS89, EPSG.WGS84)[0](elon, elat)


@utils.ranged_quantity_input(glon=(
 None, None, apu.deg), glat=(
 None, None, apu.deg), strip_input_units=True, output_unit=(apu.m, apu.m))
def wgs84_to_etrs89(glon, glat):
    """
    Convert GPS/WGS84 coordinates to ETSR89.

    ETRS89 is the European Terrestrial Reference System.
    (Using a Lambert Equal Area projection.)

    Parameters
    ----------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]

    Returns
    -------
    elon, elat : `~astropy.units.Quantity`
        ETRS89 longitude and latitude [m]
    """
    return _create_transform(EPSG.WGS84, EPSG.ETRS89)[0](glon, glat)


@utils.ranged_quantity_input(glon=(
 None, None, apu.deg), glat=(
 None, None, apu.deg), height=(
 None, None, apu.m), strip_input_units=True, output_unit=(apu.m, apu.m, apu.m))
def wgs84_to_itrf2005(glon, glat, height):
    """
    Convert GPS/WGS84 coordinates to ITRF2005.

    ITRF is the `International Terrestrial Reference System
    <https://en.wikipedia.org/wiki/International_Terrestrial_Reference_System>`__.
    (A geocentric coordinate system.)

    Parameters
    ----------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]
    height : `~astropy.units.Quantity`
        Height (amsl) [m]

    Returns
    -------
    x, y, z : `~astropy.units.Quantity`
        ITRF2005 geocentric coordinates, (x, y, z) [m]
    """
    return _create_transform(EPSG.WGS84, EPSG.ITRF05)[0](glon, glat, height)


@utils.ranged_quantity_input(x=(
 None, None, apu.m), y=(
 None, None, apu.m), z=(
 None, None, apu.m), strip_input_units=True, output_unit=(apu.deg, apu.deg, apu.m))
def itrf2005_to_wgs84(x, y, z):
    """
    Convert ITRF2005 coordinates to GPS/WGS84.

    ITRF is the `International Terrestrial Reference System
    <https://en.wikipedia.org/wiki/International_Terrestrial_Reference_System>`__.
    (A geocentric coordinate system.)

    Parameters
    ----------
    x, y, z : `~astropy.units.Quantity`
        ITRF2005 geocentric coordinates, (x, y, z) [m]

    Returns
    -------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]
    height : `~astropy.units.Quantity`
        Height (amsl) [m]
    """
    return _create_transform(EPSG.ITRF05, EPSG.WGS84)[0](x, y, z)


@utils.ranged_quantity_input(glon=(
 None, None, apu.deg), glat=(
 None, None, apu.deg), height=(
 None, None, apu.m), strip_input_units=True, output_unit=(apu.m, apu.m, apu.m))
def wgs84_to_itrf2008(glon, glat, height):
    """
    Convert GPS/WGS84 coordinates to ITRF2008.

    ITRF is the `International Terrestrial Reference System
    <https://en.wikipedia.org/wiki/International_Terrestrial_Reference_System>`__.
    (A geocentric coordinate system.)

    Parameters
    ----------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]
    height : `~astropy.units.Quantity`
        Height (amsl) [m]

    Returns
    -------
    x, y, z : `~astropy.units.Quantity`
        ITRF2008 geocentric coordinates, (x, y, z) [m]
    """
    return _create_transform(EPSG.WGS84, EPSG.ITRF08)[0](glon, glat, height)


@utils.ranged_quantity_input(x=(
 None, None, apu.m), y=(
 None, None, apu.m), z=(
 None, None, apu.m), strip_input_units=True, output_unit=(apu.deg, apu.deg, apu.m))
def itrf2008_to_wgs84(x, y, z):
    """
    Convert ITRF2008 coordinates to GPS/WGS84.

    ITRF is the `International Terrestrial Reference System
    <https://en.wikipedia.org/wiki/International_Terrestrial_Reference_System>`__.
    (A geocentric coordinate system.)

    Parameters
    ----------
    x, y, z : `~astropy.units.Quantity`
        ITRF2008 geocentric coordinates, (x, y, z) [m]

    Returns
    -------
    glon, glat : `~astropy.units.Quantity`
        GPS/WGS84 longitude and latitude [deg]
    height : `~astropy.units.Quantity`
        Height (amsl) [m]
    """
    return _create_transform(EPSG.ITRF08, EPSG.WGS84)[0](x, y, z)


def transform_factory(sys_in, sys_out, code_in='epsg', code_out='epsg'):
    """
    A factory to produce conversion functions (decorated with
    `~pycraf.utils.ranged_quantity_input` for unit handling).

    The returned function will automatically have the correct
    signature (e.g., lon/lat --> x/y, or x/y/z --> lon/lat/height)
    depending on the chosen input and output projections.
    Also a proper docstring is produced.

    While `~pycraf.geospatial` comes with several convenience
    transform functions, the user could also simply built all
    of the with the `~pycraf.geospatial.transform_factory`.
    For example, the conversion from WGS84 to ETRS89 is simply::

        >>> from pycraf import geospatial
        >>> import astropy.units as u

        >>> wgs84_to_etrs89 = geospatial.transform_factory(
        ...     geospatial.EPSG.WGS84, geospatial.EPSG.ETRS89
        ...     )

    The `~pycraf.geospatial.transform_factory` can be used
    to work with more uncommon projections. As an example,
    consider the Gauss-Kruger projection, which is defined
    for various zones (like UTM) but also with different zone
    widths. This would make it completely unhandy, to wrap
    all of the `~pyproj` transforms in `~pycraf` only for adding
    unit-checking.

    A lot (thousands!) of projections are pre-defined and have
    a so-called *EPSG* code, e.g. `WGS84="EPSG:4326"`.
    The website `spatialreference.org
    <http://spatialreference.org/>`__ is very useful to find
    information on *EPSG* codes.

    Parameters
    ----------
    sys_in, sys_out : str, int, EPSG, ESRI
        Input and output projection for the desired coordinate
        transformation. If a string, this is directly fed into the
        `~pyproj.Proj` class. If an integer, it is treated as an
        *EPSG* or *ESRI* code and the `~pyproj.Proj` class is
        instantiated with `"epsg:{code}"` or
        `"esri:{code}"`, depending on the `code_[in,out]` value.
        For convenience, a couple of common systems are defined in the
        `~pycraf.geospatial.EPSG` and `~pycraf.geospatial.ESRI` Enums
        (which just hold the associated *EPSG* or *ESRI* code for each
        name), e.g., `EPSG.WGS84 == 4326`.
    code_in, code_out : {'epsg', 'esri'}
        Whether to interpret integer-valued `sys_[in,out]` arguments
        as *EPSG* or *ESRI* code. (default: 'epsg')

    Returns
    -------
    transform_func : Function
        Transform function with unit decorator
        (`~pycraf.utils.ranged_quantity_input`).

    Examples
    --------
    To define a "Gauss-Kruger Zone 4 (Germany)" to GPS/WGS84 transform::

        >>> from pycraf import geospatial
        >>> import astropy.units as u

        >>> # see http://spatialreference.org/ref/epsg/31467/
        >>> wgs84_to_etrs89 = geospatial.transform_factory(
        ...     geospatial.EPSG.WGS84, 31467
        ...     )
        >>> wgs84_to_etrs89(6 * u.deg, 50 * u.deg)  # doctest: +FLOAT_CMP
        (<Quantity 3285005.65767981 m>, <Quantity 5544721.32224115 m>)

    If an *ESRI* system is desired, either use the integer code and
    set `code_[in,out] = 'esri'`, or use the ESRI enum::

        >>> from pycraf import geospatial
        >>> import astropy.units as u

        >>> # see http://spatialreference.org/ref/esri/54009/
        >>> wgs84_to_mollweide = geospatial.transform_factory(
        ...     geospatial.EPSG.WGS84, 54009, code_out='esri'
        ...     )  # doctest: +SKIP
        >>> wgs84_to_mollweide(6 * u.deg, 50 * u.deg)  # doctest: +SKIP
        (<Quantity 456379.9117263066 m>, <Quantity 5873471.95621065 m>)

        >>> mollweide_to_wgs84 = geospatial.transform_factory(
        ...     geospatial.ESRI.MOLLWEIDE, geospatial.EPSG.WGS84
        ...     )
        >>> mollweide_to_wgs84(456379.912 * u.m, 5873471.956 * u.m)  # doctest: +FLOAT_CMP
        (<Quantity 6.000000003439825 deg>, <Quantity 49.999999997988475 deg>)

    Notes
    -----
    - `pyproj` also allows to preserve the units (`preserve_units=True`);
      some EPSG systems use different distance units, such as ft.
      Per default, `pyproj` will convert these to meters.
      The `~pycraf.utils.ranged_quantity_input` will automatically
      convert your inputs to the correct unit (i.e., 'm' for distances),
      but the outputs will always be in meters (or degrees).
      Use `~astropy.units` functions to convert to something else
      such as 'ft' if desired.

    """
    import inspect
    _transform, in_islatlon, out_islatlon, needs_3d = _create_transform(sys_in, sys_out, code_in=code_in, code_out=code_out)
    if in_islatlon:
        deco_in_kwargs = dict(lon=(
         None, None, apu.deg), lat=(
         None, None, apu.deg))
        doc_in = DOC_LONLAT_2D.format('`sys_in`')
        if needs_3d:
            deco_in_kwargs['height'] = (
             None, None, apu.m)
            doc_in = DOC_LONLAT_3D.format('`sys_in`')
    else:
        deco_in_kwargs = dict(x=(
         None, None, apu.m), y=(
         None, None, apu.m))
        doc_in = DOC_WORLD_2D.format('`sys_in`')
        if needs_3d:
            deco_in_kwargs['z'] = (
             None, None, apu.m)
            doc_in = DOC_WORLD_3D.format('`sys_in`')
        if out_islatlon:
            deco_out_tuple = (apu.deg, apu.deg, apu.m) if needs_3d else (apu.deg, apu.deg)
            doc_out = DOC_LONLAT_3D.format('`sys_out`') if needs_3d else DOC_LONLAT_2D.format('`sys_out`')
        else:
            deco_out_tuple = (apu.m, apu.m, apu.m) if needs_3d else (apu.m, apu.m)
            doc_out = DOC_WORLD_3D.format('`sys_out`') if needs_3d else DOC_WORLD_2D.format('`sys_out`')

    def transform(*args):
        return _transform(*args)

    if isinstance(sys_in, int):
        sys_in = '{}:{}'.format(code_in.upper(), sys_in)
    if isinstance(sys_out, int):
        sys_out = '{}:{}'.format(code_out.upper(), sys_out)
    doc_kwargs = dict(sys_in=sys_in, sys_out=sys_out, parameters=doc_in, returns=doc_out)
    transform.__doc__ = DOC_TEMPLATE.format(**doc_kwargs)
    oldsig = inspect.signature(transform)
    newsig = oldsig.replace(parameters=(inspect.Parameter(k, kind=inspect.Parameter.POSITIONAL_ONLY) for k in deco_in_kwargs.keys()))
    transform.__signature__ = newsig
    return utils.ranged_quantity_input(strip_input_units=True, output_unit=deco_out_tuple, **deco_in_kwargs)(transform)


if __name__ == '__main__':
    print('This not a standalone python program! Use as module.')