# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.6/site-packages/wintx/importers/Grib/Importer.py
# Compiled at: 2016-03-23 14:50:19
import wintx, wintx.interfaces.Importer
from wintx.errors import WintxImportError
import numpy as np, matplotlib
matplotlib.use('Agg')
import pygrib
from numpy import ma

class Importer(object):

    def __init__(self, dataset_name, filter_dict={}, config_file=None):
        self.importer = wintx.interfaces.Importer(dataset_name, filter_dict=filter_dict, config_file=config_file)

    def importFile(self, filename, ignore_unknowns=False, longitude_convert_east=False):
        gribs_handle = pygrib.open(filename)
        for grib in gribs_handle:
            grib_time = grib.analDate
            grib_var = grib['name']
            grib_level = grib['level']
            grib_leveltype = grib['typeOfLevel']
            if grib_leveltype.lower() == 'unknown':
                if not ignore_unknowns:
                    raise WintxImportError("Unknown level type found. Fixed surface '%s'" % grib['typeOfFirstFixedSurface'])
                else:
                    continue
            if grib_var.lower() == 'unknown':
                if not ignore_unknowns:
                    raise WintxImportError("Unknown variable name found. Fixed surface '%s'" % grib['typeOfFirstFixedSurface'])
                else:
                    continue
            if not (self.importer.checkTime(grib_time) and self.importer.checkVariableName(grib_var) and self.importer.checkLevel(grib_level) and self.importer.checkLevelType(grib_leveltype)):
                continue
            lat_lons = grib.latlons()
            latitudes = lat_lons[0]
            longitudes = lat_lons[1]
            values = grib.values
            for loc_i in range(0, len(latitudes)):
                for loc_j in range(0, len(latitudes[loc_i])):
                    if values[loc_i][loc_j] is not ma.masked:
                        grib_lat = np.asscalar(np.float32(latitudes[loc_i][loc_j]))
                        grib_lon = np.asscalar(np.float32(longitudes[loc_i][loc_j]))
                        grib_value = np.asscalar(np.float64(values[loc_i][loc_j]))
                        if longitude_convert_east and grib_lon > 180.0:
                            grib_lon = grib_lon - 360.0
                        if not (self.importer.checkLatitude(grib_lat) and self.importer.checkLongitude(grib_lon)):
                            continue
                        self.importer.addRecord(grib_lat, grib_lon, grib_leveltype, grib_level, grib_var, grib_time, grib_value)

        gribs_handle.close()
        return self.importer.importRecords()