# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/agroapi10/polygon.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 2652 bytes
from pyowm.utils.geo import Polygon as GeoPolygon
from pyowm.utils.geo import Point as GeoPoint
from pyowm.utils.geo import GeometryBuilder

class Polygon:
    __doc__ = "\n    A Polygon feature, foundational element for all Agro API operations\n\n    :param id: the polygon's ID\n    :type id: str\n    :param name: the polygon's name\n    :type namr: str\n    :param geopolygon: the `pyowm.utils.geo.Polygon` instance that represents this polygon\n    :type geopolygon: `pyowm.utils.geo.Polygon`\n    :param center: the `pyowm.utils.geo.Point` instance that represents the central point of the polygon\n    :type center: `pyowm.utils.geo.Point`\n    :param area: the area of the polygon in hectares\n    :type area: float or int\n    :param user_id: the ID of the user owning this polygon\n    :type user_id: str\n    :returns: a `Polygon` instance\n    :raises: `AssertionError` when either id is `None` or geopolygon, center or area have wrong type\n    "

    def __init__(self, id, name=None, geopolygon=None, center=None, area=None, user_id=None):
        assert id is not None, 'Polygon ID cannot be None'
        if geopolygon is not None:
            assert isinstance(geopolygon, GeoPolygon), 'Polygon must be a valid geopolygon type'
        if center is not None:
            assert isinstance(center, GeoPoint), 'Polygon center must be a valid geopoint type'
        if area is not None:
            if not isinstance(area, float):
                assert isinstance(area, int), 'Area must be a numeric type'
                assert area >= 0, 'Area must not be negative'
        self.id = id
        self.name = name
        self.geopolygon = geopolygon
        self.center = center
        self.area = area
        self.user_id = user_id

    @property
    def area_km(self):
        if self.area:
            return self.area * 0.01

    @classmethod
    def from_dict(cls, the_dict):
        assert isinstance(the_dict, dict)
        the_id = the_dict.get('id', None)
        geojson = the_dict.get('geo_json', {}).get('geometry', None)
        name = the_dict.get('name', None)
        center = the_dict.get('center', None)
        area = the_dict.get('area', None)
        user_id = the_dict.get('user_id', None)
        geopolygon = GeometryBuilder.build(geojson)
        try:
            center = GeoPoint(center[0], center[1])
        except:
            raise ValueError('Wrong format for polygon center coordinates')

        return Polygon(the_id, name, geopolygon, center, area, user_id)

    def __repr__(self):
        return '<%s.%s - id=%s, name=%s, area=%s>' % (__name__,
         self.__class__.__name__, self.id, self.name, str(self.area))