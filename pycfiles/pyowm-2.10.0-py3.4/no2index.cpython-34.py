# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyowm/pollutionapi30/no2index.py
# Compiled at: 2018-12-21 14:52:45
# Size of source mod 2**32: 7355 bytes
"""
Nitrogen Dioxide classes and data structures.
"""
import json, xml.etree.ElementTree as ET
from pyowm.pollutionapi30.xsd.xmlnsconfig import NO2INDEX_XMLNS_URL, NO2INDEX_XMLNS_PREFIX
from pyowm.utils import timeformatutils, timeutils, xmlutils

class NO2Index(object):
    __doc__ = '\n    A class representing the Nitrogen DiOxide Index observed in a certain location\n    in the world. The index is made up of several measurements, each one at a\n    different atmospheric levels. The location is represented by the \n    encapsulated *Location* object.\n\n    :param reference_time: GMT UNIXtime telling when the NO2 data has been measured\n    :type reference_time: int\n    :param location: the *Location* relative to this NO2 observation\n    :type location: *Location*\n    :param interval: the time granularity of the NO2 observation\n    :type interval: str\n    :param no2_samples: the NO2 samples\n    :type no2_samples: list of dicts\n    :param reception_time: GMT UNIXtime telling when the NO2 observation has\n        been received from the OWM Weather API\n    :type reception_time: int\n    :returns: a *NO2Index* instance\n    :raises: *ValueError* when negative values are provided as reception time,\n      NO2 samples are not provided in a list\n\n    '

    def __init__(self, reference_time, location, interval, no2_samples, reception_time):
        if reference_time < 0:
            raise ValueError("'reference_time' must be greater than 0")
        self._reference_time = reference_time
        self._location = location
        self._interval = interval
        if not isinstance(no2_samples, list):
            raise ValueError("'no2_samples' must be a list")
        self._no2_samples = no2_samples
        if reception_time < 0:
            raise ValueError("'reception_time' must be greater than 0")
        self._reception_time = reception_time

    def get_reference_time(self, timeformat='unix'):
        """
        Returns the GMT time telling when the NO2 samples have been measured

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
        Returns the GMT time telling when the NO2 observation has been received
        from the OWM Weather API

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
        Returns the *Location* object for this NO2 index measurement

        :returns: the *Location* object

        """
        return self._location

    def get_interval(self):
        """
        Returns the time granularity interval for this NO2 index measurement

        :return: str
        """
        return self._interval

    def get_no2_samples(self):
        """
        Returns the NO2 samples for this index

        :returns: list of dicts

        """
        return self._no2_samples

    def get_sample_by_label(self, label):
        """
        Returns the NO2 sample having the specified label or `None` if none 
        is found

        :param label: the label for the seeked NO2 sample 
        :returns: dict or `None`

        """
        for sample in self._no2_samples:
            if sample['label'] == label:
                return sample

    def is_forecast(self):
        """
        Tells if the current NO2 observation refers to the future with respect
        to the current date
        :return: bool
        """
        return timeutils.now(timeformat='unix') < self.get_reference_time(timeformat='unix')

    def to_JSON(self):
        """Dumps object fields into a JSON formatted string

        :returns:  the JSON string

        """
        return json.dumps({'reference_time': self._reference_time,  'location': json.loads(self._location.to_JSON()), 
         'interval': self._interval, 
         'no2_samples': self._no2_samples, 
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
            xmlutils.annotate_with_XMLNS(root_node, NO2INDEX_XMLNS_PREFIX, NO2INDEX_XMLNS_URL)
        return xmlutils.DOM_node_to_XML(root_node, xml_declaration)

    def _to_DOM(self):
        """
        Dumps object data to a fully traversable DOM representation of the
        object.

        :returns: a ``xml.etree.Element`` object

        """
        root_node = ET.Element('no2index')
        reference_time_node = ET.SubElement(root_node, 'reference_time')
        reference_time_node.text = str(self._reference_time)
        reception_time_node = ET.SubElement(root_node, 'reception_time')
        reception_time_node.text = str(self._reception_time)
        interval_node = ET.SubElement(root_node, 'interval')
        interval_node.text = str(self._interval)
        no2_samples_node = ET.SubElement(root_node, 'no2_samples')
        for smpl in self._no2_samples:
            s = smpl.copy()
            s['label'] = s['label']
            s['value'] = '{:.12e}'.format(s['value'])
            s['precision'] = '{:.12e}'.format(s['precision'])
            xmlutils.create_DOM_node_from_dict(s, 'no2_sample', no2_samples_node)

        root_node.append(self._location._to_DOM())
        return root_node

    def __repr__(self):
        return '<%s.%s - reference time=%s, reception time=%s, location=%s, interval=%s>' % (
         __name__,
         self.__class__.__name__,
         self.get_reference_time('iso'),
         self.get_reception_time('iso'),
         str(self._location),
         self._interval)