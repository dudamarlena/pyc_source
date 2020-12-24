# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ungarj/virtualenvs/mapchete/lib/python3.5/site-packages/mapchete/io/_geometry_operations.py
# Compiled at: 2020-03-05 08:05:21
# Size of source mod 2**32: 7318 bytes
from fiona.transform import transform_geom
from rasterio.crs import CRS
from shapely.errors import TopologicalError
from shapely.geometry import box, shape, mapping, MultiPoint, MultiLineString, MultiPolygon, Polygon, LinearRing, LineString, base
from shapely.validation import explain_validity
from mapchete.errors import GeometryTypeError
from mapchete.validate import validate_crs
CRS_BOUNDS = {'epsg:4326': (-180.0, -90.0, 180.0, 90.0), 
 'epsg:3857': (-180.0, -85.0511, 180.0, 85.0511), 
 'epsg:3035': (-10.67, 34.5, 31.55, 71.05)}

def reproject_geometry(geometry, src_crs=None, dst_crs=None, error_on_clip=False, validity_check=True, antimeridian_cutting=False):
    """
    Reproject a geometry to target CRS.

    Also, clips geometry if it lies outside the destination CRS boundary.
    Supported destination CRSes for clipping: 4326 (WGS84), 3857 (Spherical
    Mercator) and 3035 (ETRS89 / ETRS-LAEA).

    Parameters
    ----------
    geometry : ``shapely.geometry``
    src_crs : ``rasterio.crs.CRS`` or EPSG code
        CRS of source data
    dst_crs : ``rasterio.crs.CRS`` or EPSG code
        target CRS
    error_on_clip : bool
        raises a ``RuntimeError`` if a geometry is outside of CRS bounds
        (default: False)
    validity_check : bool
        checks if reprojected geometry is valid and throws ``TopologicalError``
        if invalid (default: True)
    antimeridian_cutting : bool
        cut geometry at Antimeridian; can result in a multipart output geometry

    Returns
    -------
    geometry : ``shapely.geometry``
    """
    src_crs = validate_crs(src_crs)
    dst_crs = validate_crs(dst_crs)

    def _reproject_geom(geometry, src_crs, dst_crs):
        if geometry.is_empty:
            return geometry
        else:
            out_geom = to_shape(transform_geom(src_crs.to_dict(), dst_crs.to_dict(), mapping(geometry), antimeridian_cutting=antimeridian_cutting))
            if validity_check:
                return _repair(out_geom)
            return out_geom

    if src_crs == dst_crs or geometry.is_empty:
        return _repair(geometry)
    else:
        if dst_crs.is_epsg_code and dst_crs.get('init') in CRS_BOUNDS and dst_crs.get('init') != 'epsg:4326':
            wgs84_crs = CRS().from_epsg(4326)
            crs_bbox = box(*CRS_BOUNDS[dst_crs.get('init')])
            geometry_4326 = _reproject_geom(geometry, src_crs, wgs84_crs)
            if error_on_clip and not geometry_4326.within(crs_bbox):
                raise RuntimeError('geometry outside target CRS bounds')
            return _reproject_geom(crs_bbox.intersection(geometry_4326), wgs84_crs, dst_crs)
        return _reproject_geom(geometry, src_crs, dst_crs)


def _repair(geom):
    repaired = geom.buffer(0) if geom.geom_type in ('Polygon', 'MultiPolygon') else geom
    if repaired.is_valid:
        return repaired
    raise TopologicalError('geometry is invalid (%s) and cannot be repaired' % explain_validity(repaired))


def segmentize_geometry(geometry, segmentize_value):
    """
    Segmentize Polygon outer ring by segmentize value.

    Just Polygon geometry type supported.

    Parameters
    ----------
    geometry : ``shapely.geometry``
    segmentize_value: float

    Returns
    -------
    geometry : ``shapely.geometry``
    """
    if geometry.geom_type != 'Polygon':
        raise TypeError('segmentize geometry type must be Polygon')
    return Polygon(LinearRing([p for l in map(lambda x: LineString([x[0], x[1]]), zip(geometry.exterior.coords[:-1], geometry.exterior.coords[1:])) for p in [l.interpolate(segmentize_value * i).coords[0] for i in range(int(l.length / segmentize_value))] + [
     l.coords[1]]]))


def to_shape(geom):
    """
    Convert geometry to shapely geometry if necessary.

    Parameters
    ----------
    geom : shapely geometry or GeoJSON mapping

    Returns
    -------
    shapely geometry
    """
    if isinstance(geom, dict):
        return shape(geom)
    return geom


def multipart_to_singleparts(geom):
    """
    Yield single part geometries if geom is multipart, otherwise yield geom.

    Parameters
    ----------
    geom : shapely geometry

    Returns
    -------
    shapely single part geometries
    """
    if isinstance(geom, base.BaseGeometry):
        if hasattr(geom, 'geoms'):
            for subgeom in geom:
                yield subgeom

    else:
        yield geom


def clean_geometry_type(geometry, target_type, allow_multipart=True):
    """
    Return geometry of a specific type if possible.

    Filters and splits up GeometryCollection into target types. This is
    necessary when after clipping and/or reprojecting the geometry types from
    source geometries change (i.e. a Polygon becomes a LineString or a
    LineString becomes Point) in some edge cases.

    Parameters
    ----------
    geometry : ``shapely.geometry``
    target_type : string
        target geometry type
    allow_multipart : bool
        allow multipart geometries (default: True)

    Returns
    -------
    cleaned geometry : ``shapely.geometry``
        returns None if input geometry type differs from target type

    Raises
    ------
    GeometryTypeError : if geometry type does not match target_type
    """
    multipart_geoms = {'Point': MultiPoint, 
     'LineString': MultiLineString, 
     'Polygon': MultiPolygon, 
     'MultiPoint': MultiPoint, 
     'MultiLineString': MultiLineString, 
     'MultiPolygon': MultiPolygon}
    if target_type not in multipart_geoms.keys():
        raise TypeError('target type is not supported: %s' % target_type)
    if geometry.geom_type == target_type:
        return geometry
    if allow_multipart:
        target_multipart_type = multipart_geoms[target_type]
        if geometry.geom_type == 'GeometryCollection':
            return target_multipart_type([clean_geometry_type(g, target_type, allow_multipart) for g in geometry])
        if any([
         isinstance(geometry, target_multipart_type),
         multipart_geoms[geometry.geom_type] == target_multipart_type]):
            pass
        return geometry
    raise GeometryTypeError('geometry type does not match: %s, %s' % (geometry.geom_type, target_type))