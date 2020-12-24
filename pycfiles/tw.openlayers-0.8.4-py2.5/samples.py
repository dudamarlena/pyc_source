# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/openlayers/samples.py
# Compiled at: 2008-06-17 09:02:14
from tw.openlayers import Map

class DemoMap(Map):
    layers = [
     {'layer_type': 'WMS', 'layer_name': 'OpenLayers WMS', 
        'layer_url': [
                    'http://labs.metacarta.com/wms/vmap0'], 
        'layer_opts': {'layers': 'basic'}},
     {'layer_type': 'WMS', 'layer_name': 'NASA Global Mosaic', 
        'layer_url': [
                    'http://t1.hypercube.telascience.org/cgi-bin/landsat7'], 
        'layer_opts': {'layers': 'landsat7'}},
     {'layer_type': 'Google', 'layer_name': 'Google Map'},
     {'layer_type': 'Yahoo', 'layer_name': 'Yahoo Map'},
     {'layer_type': 'WMS', 'layer_name': 'DM Solutions Demo', 
        'layer_url': [
                    'http://www2.dmsolutions.ca/cgi-bin/mswms_gmap'], 
        'layer_opts': {'layers': 'bathymetry,land_fn,park,drain_fn,drainage,prov_bound,fedlimit,rail,road,popplace', 'transparent': True, 
                       'opacity': 0.4, 
                       'format': 'image/png'}, 
        'display_opts': {'minResolution': '0.17578125', 'maxResolution': '0.703125'}}]