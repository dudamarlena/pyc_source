# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/commons/tile.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 4060 bytes
import math
from pyowm.utils.geo import Polygon
from pyowm.commons.image import Image

class Tile:
    __doc__ = '\n    Wrapper class for an image tile\n    :param x: horizontal tile number in OWM tile reference system\n    :type x: int\n    :param y: vertical tile number in OWM tile reference system\n    :type y: int\n    :param zoom: zoom level for the tile\n    :type zoom: int\n    :param map_layer: the name of the OWM map layer this tile belongs to\n    :type map_layer: str\n    :param image: raw image data\n    :type image: `pyowm.commons.image.Image instance`\n    '

    def __init__(self, x, y, zoom, map_layer, image):
        assert x >= 0, 'X tile coordinate cannot be negative'
        self.x = x
        assert y >= 0, 'Y tile coordinate cannot be negative'
        self.y = y
        assert zoom >= 0, 'Tile zoom level cannot be negative'
        self.zoom = zoom
        self.map_layer = map_layer
        assert isinstance(image, Image), 'The provided image is in invalid format'
        self.image = image

    def persist(self, path_to_file):
        """
        Saves the tile to disk on a file

        :param path_to_file: path to the target file
        :type path_to_file: str
        :return: `None`
        """
        self.image.persist(path_to_file)

    def bounding_polygon(self):
        """
        Returns the bounding box polygon for this tile

        :return: `pywom.utils.geo.Polygon` instance
        """
        lon_left, lat_bottom, lon_right, lat_top = Tile.tile_coords_to_bbox(self.x, self.y, self.zoom)
        print(lon_left, lat_bottom, lon_right, lat_top)
        return Polygon([
         [[lon_left, lat_top],
          [
           lon_right, lat_top],
          [
           lon_right, lat_bottom],
          [
           lon_left, lat_bottom],
          [
           lon_left, lat_top]]])

    @classmethod
    def tile_coords_for_point(cls, geopoint, zoom):
        """
        Returns the coordinates of the tile containing the specified geopoint at the specified zoom level

        :param geopoint: the input geopoint instance
        :type geopoint: `pywom.utils.geo.Point`
        :param zoom: zoom level
        :type zoom: int
        :return: a tuple (x, y) containing the tile-coordinates
        """
        return Tile.geoocoords_to_tile_coords(geopoint.lon, geopoint.lat, zoom)

    @classmethod
    def geoocoords_to_tile_coords(cls, lon, lat, zoom):
        """
        Calculates the tile numbers corresponding to the specified geocoordinates at the specified zoom level
        Coordinates shall be provided in degrees and using the Mercator Projection (http://en.wikipedia.org/wiki/Mercator_projection)

        :param lon: longitude
        :type lon: int or float
        :param lat: latitude
        :type lat: int or float
        :param zoom: zoom level
        :type zoom: int
        :return: a tuple (x, y) containing the tile-coordinates
        """
        n = 2.0 ** zoom
        x = int((lon + 180.0) / 360.0 * n)
        y = int((1.0 - math.log(math.tan(math.radians(lat)) + 1 / math.cos(math.radians(lat))) / math.pi) / 2.0 * n)
        return (x, y)

    @classmethod
    def tile_coords_to_bbox(cls, x, y, zoom):
        """
        Calculates the lon/lat estrema of the bounding box corresponding to specific tile coordinates. Output coodinates
        are in degrees and in the Mercator Projection (http://en.wikipedia.org/wiki/Mercator_projection)

        :param x: the x tile coordinates
        :param y: the y tile coordinates
        :param zoom: the zoom level
        :return: tuple with (lon_left, lat_bottom, lon_right, lat_top)
        """

        def tile_to_geocoords(x, y, zoom):
            n = 2.0 ** zoom
            lon = x / n * 360.0 - 180.0
            lat = math.degrees(math.atan(math.sinh(math.pi * (1 - 2 * y / n))))
            return (lat, lon)

        north_west_corner = tile_to_geocoords(x, y, zoom)
        south_east_corner = tile_to_geocoords(x + 1, y + 1, zoom)
        return (north_west_corner[1], south_east_corner[0], south_east_corner[1], north_west_corner[0])