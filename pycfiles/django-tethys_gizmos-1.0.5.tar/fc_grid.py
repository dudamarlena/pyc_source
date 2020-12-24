# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/swainn/projects/tethysdev/django-tethys_gizmos/tethys_gizmos/lib/fetchclimate/fc_grid.py
# Compiled at: 2014-10-02 15:19:10


class FCGrid:

    def __init__(self, regionType, a, b, c, d, e, f, name='', g_hash=''):
        self.spatialRegionType = regionType
        self.name = name
        self.hash = g_hash
        if self.spatialRegionType == 'Points':
            if not b:
                if not isinstance(a, list):
                    raise Exception('Argument must be an array')
                self.lats = []
                self.lons = []
                for i in range(0, len(a)):
                    self.lats.append(a[i]['lat'])
                    self.lons.append(a[i]['lon'])

            else:
                if not isinstance(a, list) or not isinstance(b, list) or not len(a) == len(b):
                    raise Exception('Lats and lons must be arrays of same length')
                self.lats = a
                self.lons = b
        elif isinstance(a, list) and isinstance(b, list) and not c and not d and not e and not f:
            self.lats = a
            self.lons = b
        else:
            if c == 1 and f == 1:
                self.spatialRegionType = 'Points'
            self.lats = []
            if c == 1:
                for i in range(0, f):
                    self.lats.append((a + b) / 2)

            else:
                for i in range(0, c):
                    self.lats.append(a + (b - a) * i / (c - 1))

                self.lons = []
                if f == 1:
                    for i in range(0, c):
                        self.lons.append((d + e) / 2)

                else:
                    for i in range(0, f):
                        self.lons.append(d + (e - d) * i / (f - 1))

    def fillFetchRequest(self, request):
        if 'Domain' not in request:
            request['Domain'] = {}
        request['Domain']['SpatialRegionType'] = self.spatialRegionType
        request['Domain']['Lats'] = self.lats
        request['Domain']['Lons'] = self.lons
        request['Domain']['Lats2'] = None
        request['Domain']['Lons2'] = None
        return