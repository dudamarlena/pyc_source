# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/geomet/wkt.py
# Compiled at: 2020-01-11 13:59:55
# Size of source mod 2**32: 17964 bytes
import geomet, itertools, six, tokenize
try:
    import StringIO
except ImportError:
    import io
    StringIO = io

from geomet import util
INVALID_WKT_FMT = 'Invalid WKT: `%s`'

def dump(obj, dest_file):
    """
    Dump GeoJSON-like `dict` to WKT and write it to the `dest_file`.

    :param dict obj:
        A GeoJSON-like dictionary. It must at least the keys 'type' and
        'coordinates'.
    :param dest_file:
        Open and writable file-like object.
    """
    dest_file.write(dumps(obj))


def load(source_file):
    """
    Load a GeoJSON `dict` object from a ``source_file`` containing WKT.

    :param source_file:
        Open and readable file-like object.

    :returns:
        A GeoJSON `dict` representing the geometry read from the file.
    """
    return loads(source_file.read())


def dumps(obj, decimals=16):
    """
    Dump a GeoJSON-like `dict` to a WKT string.
    """
    try:
        geom_type = obj['type']
        exporter = _dumps_registry.get(geom_type)
        if exporter is None:
            _unsupported_geom_type(geom_type)
        if geom_type == 'GeometryCollection':
            if len(obj['geometries']) == 0:
                return 'GEOMETRYCOLLECTION EMPTY'
        else:
            if len(list(util.flatten_multi_dim(obj['coordinates']))) == 0:
                return '%s EMPTY' % geom_type.upper()
    except KeyError:
        raise geomet.InvalidGeoJSONException('Invalid GeoJSON: %s' % obj)

    result = exporter(obj, decimals)
    meta_srid = obj.get('meta', {}).get('srid')
    crs_srid = obj.get('crs', {}).get('properties', {}).get('name')
    if crs_srid is not None:
        crs_srid = crs_srid.replace('EPSG', '')
    if meta_srid is not None and crs_srid is not None and str(meta_srid) != str(crs_srid):
        raise ValueError('Ambiguous CRS/SRID values: %s and %s' % (meta_srid, crs_srid))
    srid = meta_srid or crs_srid
    if srid is not None:
        result = 'SRID=%s;%s' % (srid, result)
    return result


def _assert_next_token(sequence, expected):
    next_token = next(sequence)
    if not next_token == expected:
        raise ValueError('Expected "%s" but found "%s"' % (expected, next_token))


def loads(string):
    """
    Construct a GeoJSON `dict` from WKT (`string`).
    """
    sio = StringIO.StringIO(string)
    tokens = (x[1] for x in tokenize.generate_tokens(sio.readline))
    tokens = _tokenize_wkt(tokens)
    geom_type_or_srid = next(tokens)
    srid = None
    geom_type = geom_type_or_srid
    if geom_type_or_srid == 'SRID':
        _assert_next_token(tokens, '=')
        srid = int(next(tokens))
        _assert_next_token(tokens, ';')
        geom_type = next(tokens)
    else:
        geom_type = geom_type_or_srid
    importer = _loads_registry.get(geom_type)
    if importer is None:
        _unsupported_geom_type(geom_type)
    peek = six.advance_iterator(tokens)
    if peek == 'EMPTY':
        if geom_type == 'GEOMETRYCOLLECTION':
            return dict(type='GeometryCollection', geometries=[])
        return dict(type=(_type_map_caps_to_mixed[geom_type]), coordinates=[])
    else:
        tokens = itertools.chain([peek], tokens)
        result = importer(tokens, string)
        if srid is not None:
            result['meta'] = dict(srid=srid)
        return result


def _tokenize_wkt(tokens):
    """
    Since the tokenizer treats "-" and numeric strings as separate values,
    combine them and yield them as a single token. This utility encapsulates
    parsing of negative numeric values from WKT can be used generically in all
    parsers.
    """
    negative = False
    for t in tokens:
        if t == '-':
            negative = True
            continue
        else:
            if negative:
                yield '-%s' % t
            else:
                yield t
            negative = False


def _unsupported_geom_type(geom_type):
    raise ValueError("Unsupported geometry type '%s'" % geom_type)


def _round_and_pad(value, decimals):
    """
    Round the input value to `decimals` places, and pad with 0's
    if the resulting value is less than `decimals`.

    :param value:
        The value to round
    :param decimals:
        Number of decimals places which should be displayed after the rounding.
    :return:
        str of the rounded value
    """
    if isinstance(value, int):
        if decimals != 0:
            value = float(value)
    if decimals == 0:
        return repr(int(round(value, decimals)))
    rounded = repr(round(value, decimals))
    rounded += '0' * (decimals - len(rounded.split('.')[1]))
    return rounded


def _dump_point(obj, decimals):
    """
    Dump a GeoJSON-like Point object to WKT.

    :param dict obj:
        A GeoJSON-like `dict` representing a Point.
    :param int decimals:
        int which indicates the number of digits to display after the
        decimal point when formatting coordinates.

    :returns:
        WKT representation of the input GeoJSON Point ``obj``.
    """
    coords = obj['coordinates']
    pt = 'POINT (%s)' % ' '.join(_round_and_pad(c, decimals) for c in coords)
    return pt


def _dump_linestring(obj, decimals):
    """
    Dump a GeoJSON-like LineString object to WKT.

    Input parameters and return value are the LINESTRING equivalent to
    :func:`_dump_point`.
    """
    coords = obj['coordinates']
    ls = 'LINESTRING (%s)'
    ls %= ', '.join(' '.join(_round_and_pad(c, decimals) for c in pt) for pt in coords)
    return ls


def _dump_polygon(obj, decimals):
    """
    Dump a GeoJSON-like Polygon object to WKT.

    Input parameters and return value are the POLYGON equivalent to
    :func:`_dump_point`.
    """
    coords = obj['coordinates']
    poly = 'POLYGON (%s)'
    rings = (', '.join(' '.join(_round_and_pad(c, decimals) for c in pt) for pt in ring) for ring in coords)
    rings = ('(%s)' % r for r in rings)
    poly %= ', '.join(rings)
    return poly


def _dump_multipoint(obj, decimals):
    """
    Dump a GeoJSON-like MultiPoint object to WKT.

    Input parameters and return value are the MULTIPOINT equivalent to
    :func:`_dump_point`.
    """
    coords = obj['coordinates']
    mp = 'MULTIPOINT (%s)'
    points = (' '.join(_round_and_pad(c, decimals) for c in pt) for pt in coords)
    points = ('(%s)' % pt for pt in points)
    mp %= ', '.join(points)
    return mp


def _dump_multilinestring(obj, decimals):
    """
    Dump a GeoJSON-like MultiLineString object to WKT.

    Input parameters and return value are the MULTILINESTRING equivalent to
    :func:`_dump_point`.
    """
    coords = obj['coordinates']
    mlls = 'MULTILINESTRING (%s)'
    linestrs = ('(%s)' % ', '.join(' '.join(_round_and_pad(c, decimals) for c in pt) for pt in linestr) for linestr in coords)
    mlls %= ', '.join(ls for ls in linestrs)
    return mlls


def _dump_multipolygon(obj, decimals):
    """
    Dump a GeoJSON-like MultiPolygon object to WKT.

    Input parameters and return value are the MULTIPOLYGON equivalent to
    :func:`_dump_point`.
    """
    coords = obj['coordinates']
    mp = 'MULTIPOLYGON (%s)'
    polys = ', '.join('(%s)' % ', '.join('(%s)' % ', '.join(' '.join(_round_and_pad(c, decimals) for c in pt) for pt in ring) for ring in poly) for poly in coords)
    mp %= polys
    return mp


def _dump_geometrycollection(obj, decimals):
    """
    Dump a GeoJSON-like GeometryCollection object to WKT.

    Input parameters and return value are the GEOMETRYCOLLECTION equivalent to
    :func:`_dump_point`.

    The WKT conversions for each geometry in the collection are delegated to
    their respective functions.
    """
    gc = 'GEOMETRYCOLLECTION (%s)'
    geoms = obj['geometries']
    geoms_wkt = []
    for geom in geoms:
        geom_type = geom['type']
        geoms_wkt.append(_dumps_registry.get(geom_type)(geom, decimals))

    gc %= ','.join(geoms_wkt)
    return gc


def _load_point(tokens, string):
    """
    :param tokens:
        A generator of string tokens for the input WKT, begining just after the
        geometry type. The geometry type is consumed before we get to here. For
        example, if :func:`loads` is called with the input 'POINT(0.0 1.0)',
        ``tokens`` would generate the following values:

        .. code-block:: python
            ['(', '0.0', '1.0', ')']
    :param str string:
        The original WKT string.

    :returns:
        A GeoJSON `dict` Point representation of the WKT ``string``.
    """
    if not next(tokens) == '(':
        raise ValueError(INVALID_WKT_FMT % string)
    coords = []
    try:
        for t in tokens:
            if t == ')':
                break
            else:
                coords.append(float(t))

    except tokenize.TokenError:
        raise ValueError(INVALID_WKT_FMT % string)

    return dict(type='Point', coordinates=coords)


def _load_linestring(tokens, string):
    """
    Has similar inputs and return value to to :func:`_load_point`, except is
    for handling LINESTRING geometry.

    :returns:
        A GeoJSON `dict` LineString representation of the WKT ``string``.
    """
    if not next(tokens) == '(':
        raise ValueError(INVALID_WKT_FMT % string)
    coords = []
    try:
        pt = []
        for t in tokens:
            if t == ')':
                coords.append(pt)
                break
            else:
                if t == ',':
                    coords.append(pt)
                    pt = []
                else:
                    pt.append(float(t))

    except tokenize.TokenError:
        raise ValueError(INVALID_WKT_FMT % string)

    return dict(type='LineString', coordinates=coords)


def _load_polygon(tokens, string):
    """
    Has similar inputs and return value to to :func:`_load_point`, except is
    for handling POLYGON geometry.

    :returns:
        A GeoJSON `dict` Polygon representation of the WKT ``string``.
    """
    open_parens = (
     next(tokens), next(tokens))
    if not open_parens == ('(', '('):
        raise ValueError(INVALID_WKT_FMT % string)
    coords = []
    ring = []
    on_ring = True
    try:
        pt = []
        for t in tokens:
            if t == ')' and on_ring:
                ring.append(pt)
                coords.append(ring)
                on_ring = False
            elif t == ')' and not on_ring:
                break
            elif t == '(':
                ring = []
                pt = []
                on_ring = True
            elif t == ',' and on_ring:
                ring.append(pt)
                pt = []
            else:
                if t == ',':
                    if not on_ring:
                        continue
                pt.append(float(t))

    except tokenize.TokenError:
        raise ValueError(INVALID_WKT_FMT % string)

    return dict(type='Polygon', coordinates=coords)


def _load_multipoint(tokens, string):
    """
    Has similar inputs and return value to to :func:`_load_point`, except is
    for handling MULTIPOINT geometry.

    :returns:
        A GeoJSON `dict` MultiPoint representation of the WKT ``string``.
    """
    open_paren = next(tokens)
    if not open_paren == '(':
        raise ValueError(INVALID_WKT_FMT % string)
    coords = []
    pt = []
    paren_depth = 1
    try:
        for t in tokens:
            if t == '(':
                paren_depth += 1
            elif t == ')':
                paren_depth -= 1
                if paren_depth == 0:
                    break
            else:
                if t == '':
                    pass
                else:
                    if t == ',':
                        coords.append(pt)
                        pt = []
                    else:
                        pt.append(float(t))

    except tokenize.TokenError:
        raise ValueError(INVALID_WKT_FMT % string)

    if len(pt) > 0:
        coords.append(pt)
    return dict(type='MultiPoint', coordinates=coords)


def _load_multipolygon(tokens, string):
    """
    Has similar inputs and return value to to :func:`_load_point`, except is
    for handling MULTIPOLYGON geometry.

    :returns:
        A GeoJSON `dict` MultiPolygon representation of the WKT ``string``.
    """
    open_paren = next(tokens)
    if not open_paren == '(':
        raise ValueError(INVALID_WKT_FMT % string)
    polygons = []
    while True:
        try:
            poly = _load_polygon(tokens, string)
            polygons.append(poly['coordinates'])
            t = next(tokens)
            if t == ')':
                break
        except StopIteration:
            raise ValueError(INVALID_WKT_FMT % string)

    return dict(type='MultiPolygon', coordinates=polygons)


def _load_multilinestring(tokens, string):
    """
    Has similar inputs and return value to to :func:`_load_point`, except is
    for handling MULTILINESTRING geometry.

    :returns:
        A GeoJSON `dict` MultiLineString representation of the WKT ``string``.
    """
    open_paren = next(tokens)
    if not open_paren == '(':
        raise ValueError(INVALID_WKT_FMT % string)
    linestrs = []
    while True:
        try:
            linestr = _load_linestring(tokens, string)
            linestrs.append(linestr['coordinates'])
            t = next(tokens)
            if t == ')':
                break
        except StopIteration:
            raise ValueError(INVALID_WKT_FMT % string)

    return dict(type='MultiLineString', coordinates=linestrs)


def _load_geometrycollection(tokens, string):
    """
    Has similar inputs and return value to to :func:`_load_point`, except is
    for handling GEOMETRYCOLLECTIONs.

    Delegates parsing to the parsers for the individual geometry types.

    :returns:
        A GeoJSON `dict` GeometryCollection representation of the WKT
        ``string``.
    """
    open_paren = next(tokens)
    if not open_paren == '(':
        raise ValueError(INVALID_WKT_FMT % string)
    geoms = []
    result = dict(type='GeometryCollection', geometries=geoms)
    while True:
        try:
            t = next(tokens)
            if t == ')':
                break
            else:
                if t == ',':
                    continue
                else:
                    geom_type = t
                    load_func = _loads_registry.get(geom_type)
                    geom = load_func(tokens, string)
                    geoms.append(geom)
        except StopIteration:
            raise ValueError(INVALID_WKT_FMT % string)

    return result


_dumps_registry = {'Point':_dump_point, 
 'LineString':_dump_linestring, 
 'Polygon':_dump_polygon, 
 'MultiPoint':_dump_multipoint, 
 'MultiLineString':_dump_multilinestring, 
 'MultiPolygon':_dump_multipolygon, 
 'GeometryCollection':_dump_geometrycollection}
_loads_registry = {'POINT':_load_point, 
 'LINESTRING':_load_linestring, 
 'POLYGON':_load_polygon, 
 'MULTIPOINT':_load_multipoint, 
 'MULTILINESTRING':_load_multilinestring, 
 'MULTIPOLYGON':_load_multipolygon, 
 'GEOMETRYCOLLECTION':_load_geometrycollection}
_type_map_caps_to_mixed = dict(POINT='Point',
  LINESTRING='LineString',
  POLYGON='Polygon',
  MULTIPOINT='MultiPoint',
  MULTILINESTRING='MultiLineString',
  MULTIPOLYGON='MultiPolygon',
  GEOMETRYCOLLECTION='GeometryCollection')