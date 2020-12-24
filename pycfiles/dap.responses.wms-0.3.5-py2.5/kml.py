# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dap/responses/wms/kml.py
# Compiled at: 2007-03-02 10:29:55
from __future__ import division
__author__ = 'Roberto De Almeida <rob@pydap.org>'
import urlparse
from paste.request import construct_url, parse_dict_querystring
from dap.lib import __dap__
from dap.responses.wms import templess, _islayer
xml = '<?xml version="1.0" encoding="UTF-8"?>\n<kml xmlns="http://earth.google.com/kml/2.0" xmlns:t="http://johnnydebris.net/xmlns/templess">\n<Document>\n<name t:content="name" />\n<description t:content="description" />\n<visibility>1</visibility>\n<open>1</open>\n<NetworkLink t:content="layer">\n  <name t:content="name" />\n  <flyToView>0</flyToView>\n  <visibility>0</visibility>\n  <Url>\n    <href t:content="location" />\n    <viewRefreshMode>onStop</viewRefreshMode>\n    <viewRefreshTime>1</viewRefreshTime>\n    <ViewFormat>BBOX=[bboxWest],[bboxSouth],[bboxEast],[bboxNorth]</ViewFormat>\n  </Url>\n<refreshVisibility>1</refreshVisibility>\n</NetworkLink>\n</Document>\n</kml>'
overlay = '<?xml version="1.0" encoding="UTF-8"?>\n<GroundOverlay xmlns:t="http://johnnydebris.net/xmlns/templess">\n  <Name t:content="name" />\n  <Icon>\n    <href t:content="location" />\n  </Icon>\n  <LatLonBox>\n    <north t:content="north" />\n    <south t:content="south" />\n    <east t:content="east" />\n    <west t:content="west" />\n  </LatLonBox>\n</GroundOverlay>'

def build(self, constraints=None):
    headers = [('Content-type', 'application/vnd.google-earth.kml+xml'),
     (
      'XDODS-Server', 'dods/%s' % ('.').join([ str(i) for i in __dap__ ]))]
    query = parse_dict_querystring(self.environ)
    layers = query.get('LAYERS')
    location = construct_url(self.environ, with_query_string=True)
    (scheme, netloc, path, queries, fragment) = urlparse.urlsplit(location)
    queries = queries.split('&')
    queries = [ q for q in queries if q ]
    if layers:
        format = self.environ.get('dap.responses.kml.format', 'image/png')
        path = '%s.wms' % path[:-4]
        queries.append('SERVICE=WMS&VERSION=1.1.1&REQUEST=GetMap&SRS=EPSG:4326&WIDTH=512&HEIGHT=512&TRANSPARENT=TRUE&FORMAT=%s' % format)
        location = urlparse.urlunsplit((scheme, netloc, path, ('&').join(queries), fragment))
        location = templess.cdatanode(location, None)
        bbox = query.get('BBOX', '-180,-90,180,90')
        bbox = bbox.split(',')
        context = {'name': layers, 'location': location, 
           'north': bbox[3], 
           'south': bbox[1], 
           'east': bbox[2], 
           'west': bbox[0]}
        t = templess.template(overlay)
    else:
        layers = []
        dataset = self._parseconstraints(constraints)
        for var in dataset.walk():
            if _islayer(var):
                location = urlparse.urlunsplit((scheme, netloc, path, ('&').join(queries + ['LAYERS=%s' % var.id]), fragment))
                c = {'name': getattr(var, 'long_name', var.name), 'location': location}
                layers.append(c)

        context = {'description': self.description, 'name': dataset.name, 'layer': layers}
        t = templess.template(xml)
    output = ['<?xml version="1.0" encoding="UTF-8"?>\n', t.unicode(context).encode('utf-8')]
    return (
     headers, output)