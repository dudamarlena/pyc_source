# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/thingorderbyspecs.py
# Compiled at: 2016-01-05 12:42:25
from lxml import etree

class ThingOrderBySpecs:
    """
        Order by details for things

        Attributes:
            typeid          Datatype id
            property_name   Sort by property
            direction       Sort direction (Asc/Desc), defaults to Asc
    """

    def __init__(self, typeid, property_name):
        """
            :param typeid: Data type id
            :param property_name: Order by property name
            :type typeid: str
            :type property_name: str
        """
        self.typeid = typeid
        self.property_name = property_name
        self.direction = 'Asc'

    def write_xml(self):
        """
            :return: Xml for order by property
            :rtype: lxml.etree.Element
        """
        order_by_specs = etree.Element('order-by-property')
        order_by_specs.attrib['type-id'] = self.typeid
        order_by_specs.attrib['property-name'] = self.property_name
        order_by_specs.attrib['direction'] = self.direction
        return order_by_specs