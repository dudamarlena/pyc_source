# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ledermac/devel/plone41/zeocluster/src/collective.geo.opensearch/collective/geo/opensearch/browser/utils.py
# Compiled at: 2013-02-11 09:32:48
import logging
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
try:
    import shapely.geometry as geom
except ImportError:
    import pygeoif.geometry as geom

logger = logging.getLogger('collective.geo.opensearch')

def _parse_georss_box(value):
    try:
        (lat0, lon0, lat1, lon1) = value.replace(',', ' ').split()
        if abs(int(float(lat0))) == 90 and abs(int(float(lon0))) == 180 and abs(int(float(lat1))) == 90 and abs(int(float(lon1))) == 180:
            return
        if float(lon0) < float(lon1):
            return {'type': 'Polygon', 'coordinates': (
                             (
                              (
                               float(lon0), float(lat0)),
                              (
                               float(lon0), float(lat1)),
                              (
                               float(lon1), float(lat1)),
                              (
                               float(lon1), float(lat0)),
                              (
                               float(lon0), float(lat0))),)}
        return {'type': 'MultiPolygon', 'coordinates': (
                         (
                          (
                           float(lon0), float(lat0)),
                          (
                           float(lon0), float(lat1)),
                          (
                           -180.0, float(lat1)),
                          (
                           -180.0, float(lat0)),
                          (
                           float(lon0), float(lat0))),
                         (
                          (
                           180.0, float(lat0)),
                          (
                           180.0, float(lat1)),
                          (
                           float(lon1), float(lat1)),
                          (
                           float(lon1), float(lat0)),
                          (
                           180.0, float(lat0))))}
    except Exception, e:
        logger.info('exeption raised in _parse_georss_box: %s' % e)


def _parse_georss_point(value):
    try:
        (lat, lon) = value.replace(',', ' ').split()
        return {'type': 'Point', 'coordinates': (float(lon), float(lat))}
    except Exception, e:
        logger.info('exeption raised in _parse_georss_point: %s' % e)


def _parse_georss_line(value):
    try:
        latlons = value.replace(',', ' ').split()
        coords = []
        for i in range(0, len(latlons), 2):
            lat = float(latlons[i])
            lon = float(latlons[(i + 1)])
            coords.append((lon, lat))

        return {'type': 'LineString', 'coordinates': tuple(coords)}
    except Exception, e:
        logger.info('exeption raised in _parse_georss_line: %s' % e)


def _parse_georss_polygon(value):
    try:
        latlons = value.replace(',', ' ').split()
        coords = []
        for i in range(0, len(latlons), 2):
            lat = float(latlons[i])
            lon = float(latlons[(i + 1)])
            coords.append((lon, lat))

        return {'type': 'Polygon', 'coordinates': (tuple(coords),)}
    except Exception, e:
        logger.info('exeption raised in _parse_georss_polygon: %s' % e)


def parse_geo_rss(entry):
    """ This parses the georss of a feedparser entry
    @return None if no georss was found or
            GeoJSON-like Python geo interface
    """
    if 'georss_where' in entry:
        if 'gml_envelope' in entry and 'gml_lowercorner' in entry and 'gml_uppercorner' in entry:
            return _parse_georss_box(entry['gml_lowercorner'] + ' ' + entry['gml_uppercorner'])
        if 'gml_point' in entry and 'gml_pos' in entry:
            return _parse_georss_point(entry['gml_pos'])
        if 'gml_polygon' in entry and 'gml_exterior' in entry and 'gml_linearring' in entry and 'gml_poslist' in entry:
            return _parse_georss_polygon(entry['gml_poslist'])
        if 'gml_linestring' in entry and 'gml_poslist' in entry:
            return _parse_georss_line(entry['gml_poslist'])
    elif 'where' in entry:
        if 'envelope' in entry and 'lowercorner' in entry and 'uppercorner' in entry:
            return _parse_georss_box(entry['lowercorner'] + ' ' + entry['uppercorner'])
        if 'point' in entry and 'pos' in entry:
            return _parse_georss_point(entry['pos'])
        if 'polygon' in entry and 'exterior' in entry and 'linearring' in entry and 'poslist' in entry:
            return _parse_georss_polygon(entry['poslist'])
        if 'linestring' in entry and 'poslist' in entry:
            return _parse_georss_line(entry['poslist'])
    else:
        if 'georss_point' in entry:
            return _parse_georss_point(entry['georss_point'])
        if 'georss_line' in entry:
            return _parse_georss_line(entry['georss_line'])
        if 'georss_polygon' in entry:
            return _parse_georss_polygon(entry['georss_polygon'])
        if 'georss_box' in entry:
            return _parse_georss_box(entry['georss_box'])
        if 'georss_circle' in entry:
            pass
        if 'point' in entry:
            return _parse_georss_point(entry['point'])
        if 'line' in entry:
            return _parse_georss_line(entry['line'])
        if 'polygon' in entry:
            return _parse_georss_polygon(entry['polygon'])
        if 'box' in entry:
            return _parse_georss_box(entry['box'])
        if 'circle' in entry:
            pass


def get_geo_rss(context, brain):
    if brain.zgeo_geometry:
        if brain.zgeo_geometry['type'] == None:
            return
        if brain.zgeo_geometry['type'] == 'Point':
            coords = (
             brain.zgeo_geometry['coordinates'],)
            template = ViewPageTemplateFile('point.pt')
        elif brain.zgeo_geometry['type'] == 'Polygon':
            coords = brain.zgeo_geometry['coordinates'][0]
            template = ViewPageTemplateFile('polygon.pt')
        elif brain.zgeo_geometry['type'] == 'LineString':
            coords = brain.zgeo_geometry['coordinates']
            template = ViewPageTemplateFile('linestring.pt')
        elif brain.zgeo_geometry['type'] == 'MultiPoint':
            geometry = geom.MultiPoint(brain.zgeo_geometry['coordinates']).bounds
            coords = [geometry]
            template = ViewPageTemplateFile('envelope.pt')
        elif brain.zgeo_geometry['type'] == 'MultiLineString':
            geometry = geom.MultiLineString(brain.zgeo_geometry['coordinates']).bounds
            coords = [geometry]
            template = ViewPageTemplateFile('envelope.pt')
        elif brain.zgeo_geometry['type'] == 'MultiPolygon':
            geometry = geom.MultiPolygon(brain.zgeo_geometry['coordinates']).bounds
            coords = [geometry]
            template = ViewPageTemplateFile('envelope.pt')
        else:
            raise ValueError, 'Invalid geometry type'
        if len(coords[0]) == 2 or len(coords[0]) == 3:
            tuples = ('%f %f' % (c[1], c[0]) for c in coords)
            return ('\n').join(template(context, coords=(' ').join(tuples)).split('\n')[1:])
        if len(coords[0]) == 4 and len(coords) == 1:
            upper_corner = coords[0][2:4]
            lower_corner = coords[0][0:2]
            return ('\n').join(template(context, upper='%f %f' % upper_corner, lower='%f %f' % lower_corner).split('\n')[1:])
        raise ValueError, 'Invalid dimensions'
    return