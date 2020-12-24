# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/toutpt/workspace/collective.googlelibraries/collective/googlelibraries/googleapi.py
# Compiled at: 2010-12-01 19:05:47
from collective.googlelibraries import libraries

class MapsLibrary(libraries.Library):
    """Google Maps library
    http://code.google.com/apis/maps
    
    notes:
    v3 doesn't need a api key
    """

    def __init__(self, version='3'):
        super(MapsLibrary, self).__init__('maps', version=version)
        self.sensor = 'false'
        self.region = ''
        self.callback = ''

    @property
    def url(self):
        return 'http://maps.google.com/maps/api/js?sensor=%s' % self.sensor

    def check_id(self, id):
        pass

    @property
    def versions(self):
        return [
         '3']