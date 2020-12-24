# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/nodeshot/interop/sync/synchronizers/openwisp.py
# Compiled at: 2014-09-26 13:44:07
from __future__ import absolute_import
from django.contrib.gis.geos import Point
from .base import XMLParserMixin, GenericGisSynchronizer

class OpenWisp(XMLParserMixin, GenericGisSynchronizer):
    """ OpenWisp GeoRSS synchronizer class """

    def parse(self):
        """ parse data """
        super(OpenWisp, self).parse()
        self.parsed_data = self.parsed_data.getElementsByTagName('item')

    def parse_item(self, item):
        guid = self.get_text(item, 'guid')
        name, created_at = guid.split('201', 1)
        name = name.replace('_', ' ')
        created_at = '201%s' % created_at
        updated_at = self.get_text(item, 'updated')
        description = self.get_text(item, 'title')
        address = self.get_text(item, 'description')
        try:
            lat, lng = self.get_text(item, 'georss:point').split(' ')
        except IndexError:
            lat = self.get_text(item, 'georss:lat')
            lng = self.get_text(item, 'georss:long')

        geometry = Point(float(lng), float(lat))
        result = {'name': name, 
           'status': None, 
           'address': address, 
           'is_published': True, 
           'user': None, 
           'geometry': geometry, 
           'elev': None, 
           'description': description, 
           'notes': guid, 
           'added': created_at, 
           'updated': updated_at, 
           'data': {}}
        return result