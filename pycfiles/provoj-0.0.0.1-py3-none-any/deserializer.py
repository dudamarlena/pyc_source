# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/provneo4j/connectors/deserializer.py
# Compiled at: 2016-10-26 07:49:18
import logging
from prov.model import parse_xsd_datetime, Literal, Identifier
from prov.constants import PROV_ATTRIBUTES_ID_MAP, PROV_ATTRIBUTES, PROV_MEMBERSHIP, PROV_ATTR_ENTITY, PROV_ATTRIBUTE_QNAMES, PROV_ATTR_COLLECTION, XSD_ANYURI, PROV_QUALIFIEDNAME
from connector import *
logger = logging.getLogger(__name__)

class Deserializer:

    @staticmethod
    def decode_json_representation(literal, bundle):
        if isinstance(literal, dict):
            value = literal['$']
            datatype = literal['type'] if 'type' in literal else None
            datatype = Deserializer.valid_qualified_name(bundle, datatype)
            langtag = literal['lang'] if 'lang' in literal else None
            if datatype == XSD_ANYURI:
                return Identifier(value)
            if datatype == PROV_QUALIFIEDNAME:
                return Deserializer.valid_qualified_name(bundle, value)
            return Literal(value, datatype, langtag)
        else:
            return literal
        return

    @staticmethod
    def valid_qualified_name(bundle, value):
        if value is None:
            return
        else:
            qualified_name = bundle.valid_qualified_name(value)
            return qualified_name

    @staticmethod
    def create_prov_record(bundle, prov_type, prov_id, properties):
        """

        :param prov_type: valid prov type like prov:Entry as string
        :param prov_id: valid id as string like <namespace>:<name>
        :param properties: dict{attr_name:attr_value} dict with all properties (prov and additional)
        :return: ProvRecord
        """
        if isinstance(properties, dict):
            properties_list = properties.iteritems()
        else:
            if isinstance(properties, list):
                properties_list = properties
            else:
                raise ProvDeserializerException('please provide properties as list[(key,value)] or dict your provided: %s' % properties.__class__.__name__)
            attributes = dict()
            other_attributes = []
            membership_extra_members = None
            for attr_name, values in properties_list:
                attr = PROV_ATTRIBUTES_ID_MAP[attr_name] if attr_name in PROV_ATTRIBUTES_ID_MAP else Deserializer.valid_qualified_name(bundle, attr_name)
                if attr in PROV_ATTRIBUTES:
                    if isinstance(values, list):
                        if len(values) > 1:
                            if prov_type == PROV_MEMBERSHIP and attr == PROV_ATTR_ENTITY:
                                membership_extra_members = values[1:]
                                value = values[0]
                            else:
                                error_msg = 'The prov package does not support PROV attributes having multiple values.'
                                logger.error(error_msg)
                                raise ProvDeserializerException(error_msg)
                        else:
                            value = values[0]
                    else:
                        value = values
                    value = Deserializer.valid_qualified_name(bundle, value) if attr in PROV_ATTRIBUTE_QNAMES else parse_xsd_datetime(value)
                    attributes[attr] = value
                elif isinstance(values, list):
                    other_attributes.extend((attr, Deserializer.decode_json_representation(value, bundle)) for value in values)
                else:
                    other_attributes.append((
                     attr,
                     Deserializer.decode_json_representation(values, bundle)))

        record = bundle.new_record(prov_type, prov_id, attributes, other_attributes)
        if membership_extra_members:
            collection = attributes[PROV_ATTR_COLLECTION]
            for member in membership_extra_members:
                bundle.membership(collection, Deserializer.valid_qualified_name(bundle, member))

        return record