# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/smithery/recipe/miners/geodata.py
# Compiled at: 2011-01-04 05:26:28
"""
Geo-miners are recipes that extract data and metadata from geographic resources.
"""
from owslib.wms import WebMapService
from .base import Miner

class WMS(Miner):
    """Tiny wrapper around OWSLib.wms.WebMapService"""
    default_url = 'http://wms.jpl.nasa.gov/wms.cgi'

    def install(self):
        url = self.options.get('url', self.default_url)
        wms = WebMapService(url)
        if wms.identification.type != 'OGC:WMS':
            raise TypeError('Not a WMS service %r returned %r type' % (url, wms.identification.type))
        print 'WMS from', wms.identification.title
        self.buildout.namespace['wms'] = wms
        return tuple()