# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/trjg/code/venv/django-geo-db/lib/python3.5/site-packages/django_geo_db/utilities.py
# Compiled at: 2018-03-10 21:43:44
# Size of source mod 2**32: 6164 bytes
from decimal import Decimal
import random

def get_lat_lon_from_string(latLonString):
    lat, lon = latLonString.split(' ')
    lat = get_standardized_coordinate(lat)
    lon = get_standardized_coordinate(lon)
    return (Decimal(lat), Decimal(lon))


def get_standardized_coordinate(latOrLon):
    objInt, objFrac = str(latOrLon).split('.', 1)
    objFrac = str(objFrac)[0:5]
    return Decimal('{0}.{1}'.format(objInt, objFrac))


class LatLon:
    __doc__ = '\n    Represents a LatLon for manipulation\n    '
    lat = None
    lon = None

    @staticmethod
    def parse_string(coordinate_string):
        """
        Parses a coordinate string in the format of lat lon
        -lat -lon
        :param coordinate_string: The string to parse
        :return: Returns a LatLon object.
        """
        lat, lon = coordinate_string.split(' ', 1)
        latLon = LatLon()
        latLon.lat = get_standardized_coordinate(lat)
        latLon.lon = get_standardized_coordinate(lon)
        return latLon


class BoundingBox:
    __doc__ = '\n    A bounding box.\n    '

    def __init__(self, ne, sw):
        self._BoundingBox__north_east = ne
        self._BoundingBox__south_west = sw

    def get_north_east(self):
        return self._BoundingBox__north_east

    def get_south_east(self):
        return LatLon.parse_string('{0} {1}'.format(self._BoundingBox__south_west.lat, self._BoundingBox__north_east.lon))

    def get_north_west(self):
        return LatLon.parse_string('{0} {1}'.format(self._BoundingBox__north_east.lat, self._BoundingBox__south_west.lon))

    def get_south_west(self):
        return self._BoundingBox__south_west

    def is_lat_lon_inside_bounding_box(self, lat_lon):
        lat = lat_lon.lat
        lon = lat_lon.lon
        lat_passes = self.get_north_west() >= lat >= self.get_south_west().lat
        lon_passes = self.get_north_west() >= lon >= self.get_north_east().lon
        return lat_passes and lon_passes

    def random_coordinate_in_bounding_box(self):
        random_lat = random.uniform(float(self.get_north_west().lat), float(self.get_south_west().lat))
        random_lon = random.uniform(float(self.get_north_west().lon), float(self.get_north_east().lon))
        latLon = LatLon()
        latLon.lat = random_lat
        latLon.lon = random_lon
        return latLon


class GeoResolutionAlgorithm:

    def __init__(self, bounding_box):
        self._GeoResolutionAlgorithm__bb = bounding_box

    def lat_db_resolution(self):
        nw = str(self._GeoResolutionAlgorithm__bb.get_north_west().lat)
        sw = str(self._GeoResolutionAlgorithm__bb.get_south_west().lat)
        result = [
         False]
        if nw[0] is '-' and sw[0] is '-':
            result[True]
            nw = nw[1:]
            sw = sw[1:]
        else:
            if nw[0] is '-':
                return
            if sw[0] is '-':
                return
            if len(nw) != len(sw):
                return
            if nw[0] != sw[0]:
                return
        leading_zeros = 8 - len(nw)
        for i in range(0, leading_zeros):
            result.append(0)

        end_found = False
        for i in range(0, len(nw)):
            if nw[i] is '.':
                pass
            else:
                high = int(nw[i])
                low = int(sw[i])
            if end_found:
                result.append(-1)
            elif high is low:
                result.append(high)
            else:
                end_found = True
                result.append(-1)

        return result

    def lon_db_resolution(self):
        nw = str(self._GeoResolutionAlgorithm__bb.get_north_west().lon)
        ne = str(self._GeoResolutionAlgorithm__bb.get_north_east().lon)
        result = [False]
        if nw[0] is '-' and ne[0] is '-':
            result[0] = True
            nw = nw[1:]
            ne = ne[1:]
        else:
            if nw[0] is '-':
                return
            if ne[0] is '-':
                return
            if len(nw) != len(ne):
                return
            if nw[0] != ne[0]:
                return
        leading_zeros = 9 - len(nw)
        for i in range(0, leading_zeros):
            result.append(0)

        end_found = False
        for i in range(0, len(nw)):
            if nw[i] is '.':
                pass
            else:
                high = int(nw[i])
                low = int(ne[i])
            if end_found:
                result.append(-1)
            elif high is low:
                result.append(high)
            else:
                end_found = True
                result.append(-1)

        return result


class BoundingBoxAndMap:
    __doc__ = "\n    A class that allows the interactions of a GeoCoordinate bounding\n    box with it's presentation as a coordinate space Map.\n    This allows translations between the two such as finding the x,y of an arbitrary GeoCoordinate.\n    "
    bounding_box = None
    width = None
    height = None

    def get_coordinate_space(self, lat, lon):
        """
        Converts a GeoCoordinate's lat lon into coordinate space x,y
        Notes: (0,0) is the top left corner also the North West Corner.
        Lat = Y and Lon = X
        :param lat:
        :param lon:
        :return:  (x,y)
        """
        se = self.bounding_box.get_south_east()
        bb_max_lat = se.lat
        bb_max_lon = se.lon
        nw = self.bounding_box.get_north_west()
        bb_min_lat = nw.lat
        bb_min_lon = nw.lon
        change_y = bb_min_lat * -1
        change_x = bb_min_lon * -1
        bb_small_lat = bb_max_lat + change_y
        bb_small_lon = bb_max_lon + change_x
        new_coord_lat = lat + change_y
        new_coord_lon = lon + change_x
        new_y = new_coord_lat * self.height / bb_small_lat
        new_x = new_coord_lon * self.width / bb_small_lon
        return (int(new_x), int(new_y))