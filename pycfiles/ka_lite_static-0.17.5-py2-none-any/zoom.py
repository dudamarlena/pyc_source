# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-jkXn_D/django/django/contrib/gis/maps/google/zoom.py
# Compiled at: 2018-07-11 18:15:30
from django.contrib.gis.geos import GEOSGeometry, LinearRing, Polygon, Point
from django.contrib.gis.maps.google.gmap import GoogleMapException
from django.utils.six.moves import xrange
from math import pi, sin, log, exp, atan
DTOR = pi / 180.0
RTOD = 180.0 / pi

class GoogleZoom(object):
    """
    GoogleZoom is a utility for performing operations related to the zoom
    levels on Google Maps.

    This class is inspired by the OpenStreetMap Mapnik tile generation routine
    `generate_tiles.py`, and the article "How Big Is the World" (Hack #16) in
    "Google Maps Hacks" by Rich Gibson and Schuyler Erle.

    `generate_tiles.py` may be found at:
      http://trac.openstreetmap.org/browser/applications/rendering/mapnik/generate_tiles.py

    "Google Maps Hacks" may be found at http://safari.oreilly.com/0596101619
    """

    def __init__(self, num_zoom=19, tilesize=256):
        """Initializes the Google Zoom object."""
        self._tilesize = tilesize
        self._nzoom = num_zoom
        self._degpp = []
        self._radpp = []
        self._npix = []
        z = tilesize
        for i in xrange(num_zoom):
            self._degpp.append(z / 360.0)
            self._radpp.append(z / (2 * pi))
            self._npix.append(z / 2)
            z *= 2

    def __len__(self):
        """Returns the number of zoom levels."""
        return self._nzoom

    def get_lon_lat(self, lonlat):
        """Unpacks longitude, latitude from GEOS Points and 2-tuples."""
        if isinstance(lonlat, Point):
            lon, lat = lonlat.coords
        else:
            lon, lat = lonlat
        return (
         lon, lat)

    def lonlat_to_pixel(self, lonlat, zoom):
        """Converts a longitude, latitude coordinate pair for the given zoom level."""
        lon, lat = self.get_lon_lat(lonlat)
        npix = self._npix[zoom]
        px_x = round(npix + lon * self._degpp[zoom])
        fac = min(max(sin(DTOR * lat), -0.9999), 0.9999)
        px_y = round(npix + 0.5 * log((1 + fac) / (1 - fac)) * (-1.0 * self._radpp[zoom]))
        return (
         px_x, px_y)

    def pixel_to_lonlat(self, px, zoom):
        """Converts a pixel to a longitude, latitude pair at the given zoom level."""
        if len(px) != 2:
            raise TypeError('Pixel should be a sequence of two elements.')
        npix = self._npix[zoom]
        lon = (px[0] - npix) / self._degpp[zoom]
        lat = RTOD * (2 * atan(exp((px[1] - npix) / (-1.0 * self._radpp[zoom]))) - 0.5 * pi)
        return (
         lon, lat)

    def tile(self, lonlat, zoom):
        """
        Returns a Polygon  corresponding to the region represented by a fictional
        Google Tile for the given longitude/latitude pair and zoom level. This
        tile is used to determine the size of a tile at the given point.
        """
        delta = self._tilesize / 2
        px = self.lonlat_to_pixel(lonlat, zoom)
        ll = self.pixel_to_lonlat((px[0] - delta, px[1] - delta), zoom)
        ur = self.pixel_to_lonlat((px[0] + delta, px[1] + delta), zoom)
        return Polygon(LinearRing(ll, (ll[0], ur[1]), ur, (ur[0], ll[1]), ll), srid=4326)

    def get_zoom(self, geom):
        """Returns the optimal Zoom level for the given geometry."""
        if not isinstance(geom, GEOSGeometry) or geom.srid != 4326:
            raise TypeError('get_zoom() expects a GEOS Geometry with an SRID of 4326.')
        env = geom.envelope
        env_w, env_h = self.get_width_height(env.extent)
        center = env.centroid
        for z in xrange(self._nzoom):
            tile_w, tile_h = self.get_width_height(self.tile(center, z).extent)
            if env_w > tile_w or env_h > tile_h:
                if z == 0:
                    raise GoogleMapException('Geometry width and height should not exceed that of the Earth.')
                return z - 1

        return self._nzoom - 1

    def get_width_height(self, extent):
        """
        Returns the width and height for the given extent.
        """
        ll = Point(extent[:2])
        ul = Point(extent[0], extent[3])
        ur = Point(extent[2:])
        height = ll.distance(ul)
        width = ul.distance(ur)
        return (width, height)