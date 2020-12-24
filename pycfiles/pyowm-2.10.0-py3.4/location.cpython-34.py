# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/weatherapi25/location.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 6519 bytes
"""
Module containing location-related classes and data structures.
"""
import json, xml.etree.ElementTree as ET
from pyowm.weatherapi25.xsd.xmlnsconfig import LOCATION_XMLNS_URL, LOCATION_XMLNS_PREFIX
from pyowm.utils import xmlutils, geo

class Location(object):
    __doc__ = "\n    A class representing a location in the world. A location is defined through\n    a toponym, a couple of geographic coordinates such as longitude and\n    latitude and a numeric identifier assigned by the OWM Weather API that uniquely\n    spots the location in the world. Optionally, the country specification may\n    be provided.\n\n    Further reference about OWM city IDs can be found at:\n    http://bugs.openweathermap.org/projects/api/wiki/Api_2_5_weather#3-By-city-ID\n\n    :param name: the location's toponym\n    :type name: Unicode\n    :param lon: the location's longitude, must be between -180.0 and 180.0\n    :type lon: int/float\n    :param lat: the location's latitude, must be between -90.0 and 90.0\n    :type lat: int/float\n    :param ID: the location's OWM city ID\n    :type ID: int\n    :param country: the location's country (``None`` by default)\n    :type country: Unicode\n    :returns: a *Location* instance\n    :raises: *ValueError* if lon or lat values are provided out of bounds\n    "

    def __init__(self, name, lon, lat, ID, country=None):
        self._name = name
        if lon is None or lat is None:
            raise ValueError("Either 'lon' or 'lat' must be specified")
        geo.assert_is_lon(lon)
        geo.assert_is_lat(lat)
        self._lon = float(lon)
        self._lat = float(lat)
        self._ID = ID
        self._country = country

    def get_name(self):
        """
        Returns the toponym of the location

        :returns: the Unicode toponym

        """
        return self._name

    def get_lon(self):
        """
        Returns the longitude of the location

        :returns: the float longitude

        """
        return self._lon

    def get_lat(self):
        """
        Returns the latitude of the location

        :returns: the float latitude

        """
        return self._lat

    def get_ID(self):
        """
        Returns the OWM city ID of the location

        :returns: the int OWM city ID

        """
        return self._ID

    def get_country(self):
        """
        Returns the country of the location

        :returns: the Unicode country

        """
        return self._country

    def to_geopoint(self):
        """
        Returns the geoJSON compliant representation of this location

        :returns: a ``pyowm.utils.geo.Point`` instance

        """
        if self._lon is None or self._lat is None:
            return
        return geo.Point(self._lon, self._lat)

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({'name': self._name,  'coordinates': {'lon': self._lon,  'lat': self._lat}, 
         'ID': self._ID, 
         'country': self._country})

    def to_XML(self, xml_declaration=True, xmlns=True):
        """
        Dumps object fields to an XML-formatted string. The 'xml_declaration'
        switch  enables printing of a leading standard XML line containing XML
        version and encoding. The 'xmlns' switch enables printing of qualified
        XMLNS prefixes.

        :param XML_declaration: if ``True`` (default) prints a leading XML
            declaration line
        :type XML_declaration: bool
        :param xmlns: if ``True`` (default) prints full XMLNS prefixes
        :type xmlns: bool
        :returns: an XML-formatted string

        """
        root_node = self._to_DOM()
        if xmlns:
            xmlutils.annotate_with_XMLNS(root_node, LOCATION_XMLNS_PREFIX, LOCATION_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element('location')
        name_node = ET.SubElement(root_node, 'name')
        name_node.text = self._name
        coords_node = ET.SubElement(root_node, 'coordinates')
        lon_node = ET.SubElement(coords_node, 'lon')
        lon_node.text = str(self._lon)
        lat_node = ET.SubElement(coords_node, 'lat')
        lat_node.text = str(self._lat)
        id_node = ET.SubElement(root_node, 'ID')
        id_node.text = str(self._ID)
        country_node = ET.SubElement(root_node, 'country')
        country_node.text = self._country
        return root_node

    def __repr__(self):
        return '<%s.%s - id=%s, name=%s, lon=%s, lat=%s>' % (__name__,
         self.__class__.__name__, self._ID, self._name, str(self._lon),
         str(self._lat))


def location_from_dictionary(d):
    """
    Builds a *Location* object out of a data dictionary. Only certain
    properties of the dictionary are used: if these properties are not
    found or cannot be read, an error is issued.

    :param d: a data dictionary
    :type d: dict
    :returns: a *Location* instance
    :raises: *KeyError* if it is impossible to find or read the data
        needed to build the instance

    """
    country = None
    if 'sys' in d:
        if 'country' in d['sys']:
            country = d['sys']['country']
    if 'city' in d:
        data = d['city']
    else:
        data = d
    if 'name' in data:
        name = data['name']
    else:
        name = None
    if 'id' in data:
        ID = int(data['id'])
    else:
        ID = None
    if 'coord' in data:
        lon = data['coord'].get('lon', 0.0)
        lat = data['coord'].get('lat', 0.0)
    else:
        if 'coord' in data['station']:
            if 'lon' in data['station']['coord']:
                lon = data['station']['coord'].get('lon', 0.0)
            else:
                if 'lng' in data['station']['coord']:
                    lon = data['station']['coord'].get('lng', 0.0)
                else:
                    lon = 0.0
            lat = data['station']['coord'].get('lat', 0.0)
        else:
            raise KeyError('Impossible to read geographical coordinates from JSON')
    if 'country' in data:
        country = data['country']
    return Location(name, lon, lat, ID, country)