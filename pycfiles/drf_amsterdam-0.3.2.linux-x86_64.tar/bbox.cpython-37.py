# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3393)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/stephan/.virtualenvs/drf_amsterdam/lib/python3.7/site-packages/datapunt_api/bbox.py
"""Bounding box methods usefull for Amsterdam."""
from math import pi, cos
from django.contrib.gis.geos import Point
from rest_framework.serializers import ValidationError
BBOX = [
 52.0356, 4.58565,
 52.48769, 5.3136]

def parse_xyr(value: str) -> (Point, int):
    """Parse x, y, radius input.

    Intput can be RD and lon, lat (WGS84) for coordinates
    WITHIN the Netherlands

    returns wgs84 point and radius.
    """
    try:
        x, y, radius = value.split(',')
    except ValueError:
        raise ValidationError('Locatie must be rdx,rdy,radius(m) or lat,long,radius(m)')

    try:
        x = float(x)
        y = float(y)
        radius = float(radius)
        assert x > 0
        assert y > 0
    except (ValueError, AssertionError):
        raise ValidationError('Locatie must be x: float, y: float, r: int')

    if x > 10:
        if x > y:
            raise ValidationError('RD x must be < then y')
        point = Point(x, y, srid=28992).transform(4326, clone=True)
        radius = dist_to_deg(radius, point.y)
    else:
        radius = dist_to_deg(radius, y)
        point = Point(x, y, srid=4326)
    return (point, radius)


def dist_to_deg(distance, latitude):
    """
    Convert meters to degrees.

    distance = distance in meters, latitude = latitude in degrees

    At the equator, the distance of one degree is equal in latitude and longitude.
    at higher latitudes, a degree longitude is shorter in length, proportional to cos(latitude)
    http://en.wikipedia.org/wiki/Decimal_degrees
    This function is part of a distance filter where the database 'distance' is in degrees.
    There's no good single-valued answer to this problem.
    The distance/ degree is quite constant N/S around the earth (latitude),
    but varies over a huge range E/W (longitude).
    Split the difference: I'm going to average the the degrees latitude and degrees longitude
    corresponding to the given distance. At high latitudes, this will be too short N/S
    and too long E/W. It splits the errors between the two axes.
    Errors are < 25 percent for latitudes < 60 degrees N/S.
    """
    lat = latitude if latitude >= 0 else -1 * latitude
    rad2deg = 180 / pi
    earthRadius = 6378160.0
    latitudeCorrection = 0.5 * (1 + cos(lat * pi / 180))
    return distance / (earthRadius * latitudeCorrection) * rad2deg


def determine_bbox(request):
    """Create a bounding box if it is given with the request."""
    err = 'invalid bbox given'
    if 'bbox' not in request.query_params:
        return (BBOX, None)
    bboxp = request.query_params['bbox']
    bbox, err = valid_bbox(bboxp)
    if err:
        return (
         None, err)
    return (bbox, err)


def valid_bbox(bboxp, srid=4326):
    """Check if bbox is a valid bounding box. (wgs84) for now.

    TODO write tests.
    """
    bbox = bboxp.split(',')
    err = None
    if not len(bbox) == 4:
        return ([], 'wrong numer of arguments (lon, lat, lon, lat)')
    try:
        bbox = [float(f) for f in bbox]
    except ValueError:
        return ([], 'Did not recieve floats')
    else:
        lat_min = 52.0356
        lat_max = 52.48769
        lon_min = 4.58565
        lon_max = 5.3136
        if srid == 28992:
            lat_min = 465000
            lat_max = 514000
            lon_min = 94000
            lon_max = 170000
        lon1, lat1, lon2, lat2 = bbox
        if not lat_max >= lat1 >= lat_min:
            err = f"lat not within max bbox {lat_max} > {lat1} > {lat_min}"
        if not lat_max >= lat2 >= lat_min:
            err = f"lat not within max bbox {lat_max} > {lat2} > {lat_min}"
        if not lon_max >= lon2 >= lon_min:
            err = f"lon not within max bbox {lon_max} > {lon2} > {lon_min}"
        if not lon_max >= lon1 >= lon_min:
            err = f"lon not within max bbox {lon_max} > {lon1} > {lon_min}"
        bbox = [
         lon1, lat1, lon2, lat2]
        return (
         bbox, err)