# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/atlas/utils.py
# Compiled at: 2015-04-21 15:30:03
import math
from django.contrib.gis.geoip import GeoIP
from django.contrib.gis.geos import fromstr
from django.contrib.gis.measure import D
from django.conf import settings
from django.db.models.query import Q
from atlas.models import City, Region, Country
DB_ENGINE = settings.DATABASES['default']['ENGINE']
RADIUS_EARTH = 6378100

def get_city(ip=None, position=None):
    """
    Returns city based on either IP address or longitude/latitude position.
    An IP address lookup is fairly fast while a position lookup is expensive.
    """
    city = None
    city_geoip = None
    qs = None
    if ip:
        city_geoip = GeoIP().city(ip)
        if city_geoip:
            qs = City.objects.filter(country__country_code=city_geoip['country_code'])
            if not position:
                qs = qs.filter(name=city_geoip['city'])
                if 'region' in city_geoip:
                    qs = qs.filter(region__code=city_geoip['region'])
                if qs:
                    city = qs[0]
    if position:
        if not city_geoip:
            if DB_ENGINE.rfind('mysql') >= 0:
                closest_countries = Country.objects.exclude(coordinates__isnull=True).extra(select={'distance': "distance_sphere(`atlas_country`.`coordinates`, geomfromtext('%s', %d))" % (
                              str(position), position.srid)})
                closest_countries = closest_countries.order_by('distance')[:5]
                closest_countries = [ c.id for c in closest_countries ]
                regions = Region.objects.exclude(coordinates__isnull=True).filter(country__in=closest_countries)
                regions = regions.extra(select={'distance': "distance_sphere(`atlas_region`.`coordinates`, geomfromtext('%s', %d))" % (
                              str(position), position.srid)}).order_by('distance')
            else:
                closest_countries = Country.objects.exclude(coordinates__isnull=True).distance(position).order_by('distance')[:5]
                closest_countries = [ c.id for c in closest_countries ]
                regions = Region.objects.exclude(coordinates__isnull=True).filter(country__in=closest_countries).distance(position).order_by('distance')
            for region in regions:
                try:
                    closest_countries.remove(region.country_id)
                except:
                    pass

            regions = regions[:5] if len(regions) > 5 else regions
            closest_regions = [ r.id for r in regions ]
            qs = City.objects.filter(Q(region__in=closest_regions) | Q(country__in=closest_countries))
        else:
            closest_regions = Region.objects.exclude(coordinates__isnull=True).filter(country__country_code=city_geoip['country_code'])
            if DB_ENGINE.rfind('mysql') >= 0:
                closest_regions = closest_regions.extra(select={'distance': "distance_sphere(`atlas_region`.`coordinates`, geomfromtext('%s', %d))" % (
                              str(position), position.srid)}).order_by('distance')[:5]
            else:
                closest_regions = closest_regions.distance(position).order_by('distance')[:5]
            if closest_regions:
                closest_regions = [ r.id for r in closest_regions ]
                qs = qs.filter(region__in=closest_regions)
        if DB_ENGINE.rfind('mysql') >= 0:
            qs = qs.filter(coordinates__within=get_mbr_for_radius(position, 100000)).extra(select={'distance': "distance_sphere(`atlas_city`.`coordinates`,\n                geomfromtext('%s', %d))" % (str(position), position.srid)}).order_by('distance')
        else:
            qs = qs.filter(coordinates__dwithin=(position, D(m=100000))).distance(position).order_by('distance')
        if qs:
            city = qs[0]
    return city


def get_mbr_for_radius(point, radius):
    """
    Returns a polygon that encloses a circle of the specified radius, centered at the
    specified point. It takes into account the decrease in spacing between longitude lines
    towards the poles.
    """
    theta = float(radius) / RADIUS_EARTH * 180 / math.pi
    min_lat = point.y - theta
    if min_lat < -90:
        min_lat = -180 - min_lat
    max_lat = point.y + theta
    if max_lat > 90:
        max_lat = 180 - max_lat
    theta_at_min_lat = radius / (math.cos(min_lat / 180 * math.pi) * RADIUS_EARTH) * 180 / math.pi
    theta_at_max_lat = radius / (math.cos(max_lat / 180 * math.pi) * RADIUS_EARTH) * 180 / math.pi
    max_lon_at_min_lat = (point.x + theta_at_min_lat + 180) % 360 - 180
    min_lon_at_min_lat = (point.x - theta_at_min_lat + 180) % 360 - 180
    max_lon_at_max_lat = (point.x + theta_at_max_lat + 180) % 360 - 180
    min_lon_at_max_lat = (point.x - theta_at_max_lat + 180) % 360 - 180
    return fromstr('POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))' % (
     min_lon_at_min_lat, min_lat, max_lon_at_min_lat, min_lat,
     max_lon_at_max_lat, max_lat, min_lon_at_max_lat, max_lat,
     min_lon_at_min_lat, min_lat), srid=point.srid)


def locate(request):
    ip = request.META['REMOTE_ADDR'] if 'REMOTE_ADDR' in request.META else None
    location = request.COOKIES['atlas_id'] if 'atlas_id' in request.COOKIES else None
    city = None
    position = None
    if location and location != 'no-location':
        position = fromstr('POINT (%s %s)' % tuple(location.split('+')), srid=4326)
    if ip and not position:
        city = get_city(ip=ip)
    elif position:
        city = get_city(position=position)
    if city:
        request.session['location'] = {'city': city, 'position': position}
    return