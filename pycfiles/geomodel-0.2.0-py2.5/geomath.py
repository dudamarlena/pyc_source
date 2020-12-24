# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/geo/geomath.py
# Compiled at: 2009-07-28 20:05:00
"""Defines common geo math functions used throughout the library."""
__author__ = 'api.roman.public@gmail.com (Roman Nurik)'
import math, geotypes
RADIUS = 6378135

def distance(p1, p2):
    """Calculates the great circle distance between two points (law of cosines).

  Args:
    p1: A geotypes.Point or db.GeoPt indicating the first point.
    p2: A geotypes.Point or db.GeoPt indicating the second point.

  Returns:
    The 2D great-circle distance between the two given points, in meters.
  """
    p1lat, p1lon = math.radians(p1.lat), math.radians(p1.lon)
    p2lat, p2lon = math.radians(p2.lat), math.radians(p2.lon)
    return RADIUS * math.acos(math.sin(p1lat) * math.sin(p2lat) + math.cos(p1lat) * math.cos(p2lat) * math.cos(p2lon - p1lon))