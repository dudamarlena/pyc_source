# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/FeatureServer/Service/WFS.py
# Compiled at: 2008-01-01 03:15:59
__author__ = 'MetaCarta'
__copyright__ = 'Copyright (c) 2006-2008 MetaCarta'
__license__ = 'Clear BSD'
__version__ = '$Id: WFS.py 412 2008-01-01 08:15:59Z crschmidt $'
from FeatureServer.Service import Request
from FeatureServer.Service import Action
import re, xml.dom.minidom as m

class WFS(Request):
    __module__ = __name__

    def encode(self, result):
        results = ['<wfs:FeatureCollection\n   xmlns:fs="http://example.com/featureserver"\n   xmlns:wfs="http://www.opengis.net/wfs"\n   xmlns:gml="http://www.opengis.net/gml"\n   xmlns:ogc="http://www.opengis.net/ogc"\n   xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n   xsi:schemaLocation="http://www.opengis.net/wfs http://schemas.opengeospatial.net//wfs/1.0.0/WFS-basic.xsd">\n        ']
        for action in result:
            for i in action:
                results.append(self.encode_feature(i))

        results.append('</wfs:FeatureCollection>')
        return ('text/xml', ('\n').join(results))

    def encode_feature(self, feature):
        layername = re.sub('\\W', '_', self.datasource)
        attr_fields = []
        for (key, value) in feature.properties.items():
            key = re.sub('\\W', '_', key)
            attr_value = value
            if hasattr(attr_value, 'replace'):
                attr_value = attr_value.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
            if isinstance(attr_value, str):
                attr_value = unicode(attr_value, 'utf-8')
            attr_fields.append('<fs:%s>%s</fs:%s>' % (key, attr_value, key))

        xml = '\n        <gml:featureMember><fs:%s fid="%s">\n        <fs:geometry>\n        %s\n        </fs:geometry>\n        %s\n        </fs:%s></gml:featureMember>' % (layername, feature.id, self.geometry_to_gml(feature.geometry), ('\n').join(attr_fields), layername)
        return xml

    def geometry_to_gml(self, geometry):
        coords = (' ').join(map(lambda x: (',').join(map(str, x)), geometry['coordinates']))
        if geometry['type'] == 'Point':
            return '<gml:Point><gml:coordinates>%s</gml:coordinates></gml:Point>' % coords
        elif geometry['type'] == 'Line':
            return '<gml:LineString><gml:coordinates>%s</gml:coordinates></gml:LineString>' % coords
        elif geometry['type'] == 'Polygon':
            coords = (' ').join(map(lambda x: (',').join(map(str, x)), geometry['coordinates'][0]))
            out = '\n              <gml:outerBoundaryIs><gml:LinearRing>\n              <gml:coordinates>%s</gml:coordinates>\n              </gml:LinearRing></gml:outerBoundaryIs>\n            ' % coords
            inner_rings = []
            for inner_ring in geometry['coordinates'][1:]:
                coords = (' ').join(map(lambda x: (',').join(map(str, x)), inner_ring))
                inner_rings.append('\n                  <gml:innerBoundaryIs><gml:LinearRing>\n                  <gml:coordinates>%s</gml:coordinates>\n                  </gml:LinearRing></gml:innerBoundaryIs>\n                ' % coords)

            return '<gml:Polygon>\n              %s %s\n              </gml:Polygon>' % (out, ('\n').join(inner_rings))
        else:
            raise Exception('Could not convert geometry of type %s.' % geometry['type'])