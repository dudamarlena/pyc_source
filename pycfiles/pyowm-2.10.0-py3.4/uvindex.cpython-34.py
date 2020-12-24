# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/uvindexapi30/uvindex.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 6201 bytes
import json, xml.etree.ElementTree as ET
from pyowm.uvindexapi30.xsd.xmlnsconfig import UVINDEX_XMLNS_URL, UVINDEX_XMLNS_PREFIX
from pyowm.utils import timeformatutils, xmlutils

def uv_intensity_to_exposure_risk(uv_intensity):
    if 0.0 <= uv_intensity < 2.9:
        return 'low'
    else:
        if 2.9 <= uv_intensity < 5.9:
            return 'moderate'
        if 5.9 <= uv_intensity < 7.9:
            return 'high'
        if 7.9 <= uv_intensity < 10.9:
            return 'very high'
        return 'extreme'


class UVIndex(object):
    __doc__ = '\n    A class representing the UltraViolet Index observed in a certain location\n    in the world. The location is represented by the encapsulated *Location* object.\n\n    :param reference_time: GMT UNIXtime telling when the UV data have been measured\n    :type reference_time: int\n    :param location: the *Location* relative to this UV observation\n    :type location: *Location*\n    :param value: the observed UV intensity value\n    :type value: float\n    :param reception_time: GMT UNIXtime telling when the observation has\n        been received from the OWM Weather API\n    :type reception_time: int\n    :returns: an *UVIndex* instance\n    :raises: *ValueError* when negative values are provided as reception time or\n      UV intensity value\n\n    '

    def __init__(self, reference_time, location, value, reception_time):
        if reference_time < 0:
            raise ValueError("'referencetime' must be greater than 0")
        self._reference_time = reference_time
        self._location = location
        if value < 0.0:
            raise ValueError("'UV intensity must be greater than 0")
        self._value = value
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time

    def get_reference_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the UV has been observed
          from the OWM Weather API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return timeformatutils.timeformat(self._reference_time, timeformat)

    def get_reception_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the UV has been received from the API

        :param timeformat: the format for the time value. May be:
            '*unix*' (default) for UNIX time
            '*iso*' for ISO8601-formatted string in the format ``YYYY-MM-DD HH:MM:SS+00``
            '*date* for ``datetime.datetime`` object instance
        :type timeformat: str
        :returns: an int or a str
        :raises: ValueError when negative values are provided

        """
        return timeformatutils.timeformat(self._reception_time, timeformat)

    def get_location(self):
        """
        Returns the *Location* object for this UV observation

        :returns: the *Location* object

        """
        return self._location

    def get_value(self):
        """
        Returns the UV intensity for this observation

        :returns: float

        """
        return self._value

    def get_exposure_risk(self):
        """
        Returns a string stating the risk of harm from unprotected sun exposure
        for the average adult on this UV observation
        :return: str
        """
        return uv_intensity_to_exposure_risk(self._value)

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({'reference_time': self._reference_time,  'location': json.loads(self._location.to_JSON()), 
         'value': self._value, 
         'reception_time': self._reception_time})

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
            xmlutils.annotate_with_XMLNS(root_node, UVINDEX_XMLNS_PREFIX, UVINDEX_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element('uvindex')
        reference_time_node = ET.SubElement(root_node, 'reference_time')
        reference_time_node.text = str(self._reference_time)
        reception_time_node = ET.SubElement(root_node, 'reception_time')
        reception_time_node.text = str(self._reception_time)
        value_node = ET.SubElement(root_node, 'value')
        value_node.text = str(self._value)
        root_node.append(self._location._to_DOM())
        return root_node

    def __repr__(self):
        return '<%s.%s - reference time=%s, reception time=%s, location=%s, value=%s>' % (
         __name__,
         self.__class__.__name__,
         self.get_reference_time('iso'),
         self.get_reception_time('iso'),
         str(self._location),
         str(self._value))