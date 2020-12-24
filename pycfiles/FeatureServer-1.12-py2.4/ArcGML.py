# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/FeatureServer/Service/ArcGML.py
# Compiled at: 2008-02-09 10:51:09
from FeatureServer.Service import Request, Action
import re, xml.dom.minidom as m, uuid

class ArcGML(Request):
    __module__ = __name__

    def encode(self, result):
        results = ['\n        <gml:FeatureCollection xmlns:gml="http://www.opengis.net/gml" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:fme="http://www.safe.com/gml/fme" \n        xsi:schemaLocation="http://www.safe.com/gml/fme fs.xsd">\n        ']
        for action in result:
            for i in action:
                results.append(self.encode_feature(i))

        results.append('</gml:FeatureCollection>')
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
            attr_fields.append('<fme:%s>%s</fme:%s>' % (key.title(), attr_value, key.title()))

        xml = '\n        <gml:featureMember><fme:fs gml:id="%s">\n        <fme:OBJECTID>%s</fme:OBJECTID> \n        %s\n        <gml:surfaceProperty>\n        %s\n        </gml:surfaceProperty>\n        </fme:fs></gml:featureMember>' % (str(uuid.uuid1()), feature.id, ('\n').join(attr_fields), self.geometry_to_gml(feature.geometry))
        return xml

    def geometry_to_gml(self, geometry):
        coords = (' ').join(map(lambda x: '%s %s' % (x[0], x[1]), geometry['coordinates']))
        if geometry['type'] == 'Point':
            raise Exception('Not implemented')
            return '<gml:Point><gml:coordinates>%s</gml:coordinates></gml:Point>' % coords
        elif geometry['type'] == 'Line':
            raise Exception('Not implemented')
            return '<gml:LineString><gml:coordinates>%s</gml:coordinates></gml:LineString>' % coords
        elif geometry['type'] == 'Polygon':
            coords = (' ').join(map(lambda x: '%s %s' % (x[1], x[0]), geometry['coordinates'][0]))
            out = '\n<gml:Surface srsName="EPSG:4326" srsDimension="2"> \n<gml:patches> \n<gml:PolygonPatch> \n<gml:exterior> \n<gml:LinearRing> \n<gml:posList>%s</gml:posList> \n</gml:LinearRing> \n</gml:exterior> \n</gml:PolygonPatch> \n</gml:patches> \n</gml:Surface> \n            ' % coords
            return out
        else:
            raise Exception('Could not convert geometry of type %s.' % geometry['type'])