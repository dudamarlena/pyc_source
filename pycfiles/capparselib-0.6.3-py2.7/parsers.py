# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/capparselib/parsers.py
# Compiled at: 2020-04-01 06:58:04
"""
    capparselib.CAPParser
    ~~~~~~~~~~~~~

    :copyright: Kelvin Nicholson (kelvin@kelvinism.com), see AUTHORS for more details
    :license: MOZILLA PUBLIC LICENSE (v1.1), see LICENSE for more details
"""
from __future__ import unicode_literals
import os, logging
from lxml import objectify, etree
ATOM_URI = b'http://www.w3.org/2005/Atom'
CAP1_1_URN = b'urn:oasis:names:tc:emergency:cap:1.1'
CAP1_2_URN = b'urn:oasis:names:tc:emergency:cap:1.2'
EDXL_DE_URN = b'urn:oasis:names:tc:emergency:EDXL:DE:1.0'
XML_TYPE = None
CAPLIBRARY_PATH = os.path.realpath(os.path.dirname(__file__))
CAP_MAPPINGS = {b'title': b'cap_headline', 
   b'summary': b'cap_description', 
   b'description': b'cap_description', 
   b'expires': b'cap_expires', 
   b'responseType': b'cap_response_type', 
   b'severity': b'cap_severity', 
   b'urgency': b'cap_urgency', 
   b'onset': b'cap_effective', 
   b'web': b'cap_link', 
   b'sent': b'cap_sent', 
   b'category': b'cap_category', 
   b'certainty': b'cap_certainty', 
   b'event': b'cap_event', 
   b'headline': b'cap_headline', 
   b'instruction': b'cap_instruction', 
   b'language': b'cap_language', 
   b'link': b'cap_link', 
   b'author': b'cap_sender', 
   b'areaDesc': b'cap_area_description', 
   b'effective': b'cap_effective', 
   b'sender': b'cap_sender', 
   b'contact': b'cap_contact', 
   b'senderName': b'cap_sender_name', 
   b'note': b'cap_note', 
   b'code': b'cap_code', 
   b'id': b'cap_id', 
   b'identifier': b'cap_id', 
   b'msgType': b'cap_message_type', 
   b'scope': b'cap_scope', 
   b'status': b'cap_status', 
   b'restriction': b'cap_restriction', 
   b'source': b'cap_source', 
   b'incidents': b'cap_incidents', 
   b'references': b'cap_references', 
   b'addresses': b'cap_addresses', 
   b'area': b'area', 
   b'eventCode': b'event_code', 
   b'parameter': b'parameter', 
   b'resource': b'resource'}
XML_TYPE_XSD_MAPPINGS = {b'ATOM': b'schema/atom.xsd', 
   b'CAP1_2': b'schema/cap12_extended.xsd', 
   b'CAP1_1': b'schema/cap11_extended.xsd', 
   b'EDXL_DE': b'schema/edxl-de.xsd', 
   b'RSS': b'schema/rss-2_0.xsd'}

class CAPParser(object):

    def __init__(self, raw_cap_xml=None, recover=False):
        self.xml = raw_cap_xml.encode(b'utf-8').strip() if raw_cap_xml is not None else None
        self.recover = recover
        self.objectified_xml = None
        self.cap_xml_type = None
        self.alert_list = []
        self.load()
        return

    def process_area(self, info_dict):
        new_area_list = []
        for area_obj in info_dict[b'area']:
            new_area_dict = {}
            if hasattr(area_obj, b'circle'):
                new_area_dict[b'circle'] = info_dict[b'area'].circle
            if hasattr(area_obj, b'polygon'):
                new_area_dict[b'polygon'] = info_dict[b'area'].polygon
            if hasattr(area_obj, b'geocode'):
                geocode_list = []
                for geocode in area_obj[b'geocode']:
                    geocode_list.append({b'valueName': geocode.valueName, b'value': geocode.value})

                new_area_dict[b'geocodes'] = geocode_list
            new_area_dict[b'area_description'] = area_obj.areaDesc
            new_area_list.append(new_area_dict)

        info_dict[b'cap_area'] = new_area_list
        info_dict.pop(b'area')
        return info_dict

    def process_event_code(self, info_dict):
        event_code_list = []
        for event_code in info_dict[b'event_code']:
            event_code_list.append({b'valueName': event_code.valueName, b'value': event_code.value})

        info_dict[b'cap_event_code'] = event_code_list
        info_dict.pop(b'event_code')
        return info_dict

    def process_parameter(self, info_dict):
        parameter_list = []
        for parameter in info_dict[b'parameter']:
            parameter_list.append({b'valueName': parameter.valueName, b'value': parameter.value})

        info_dict[b'cap_parameter'] = parameter_list
        info_dict.pop(b'parameter')
        return info_dict

    def process_resource(self, info_dict):
        resource_list = []
        for resource in info_dict[b'resource']:
            resource_list.append({b'resourceDesc': resource.resourceDesc, b'mimeType': resource.mimeType, 
               b'uri': resource.uri})

        info_dict[b'cap_resource'] = resource_list
        info_dict.pop(b'resource')
        return info_dict

    def parse_alert(self, alert):
        alert_dict = alert.__dict__
        for alert_key in list(alert_dict):
            if alert_key in CAP_MAPPINGS:
                new_alert_key = CAP_MAPPINGS[alert_key]
                alert_dict[new_alert_key] = alert_dict.pop(alert_key)

        if b'info' in alert_dict.keys():
            info_item_list = []
            for info_item in alert.info:
                info_dict = info_item.__dict__
                for info_key in list(info_dict):
                    if info_key in CAP_MAPPINGS:
                        new_info_key = CAP_MAPPINGS[info_key]
                        info_dict[new_info_key] = info_dict.pop(info_key)
                    else:
                        logging.info(b'Key not in CAP_MAPPINGS: %s' % info_key)

                if b'area' in info_dict.keys():
                    info_dict = self.process_area(info_dict)
                if b'event_code' in info_dict.keys():
                    info_dict = self.process_event_code(info_dict)
                if b'parameter' in info_dict.keys():
                    info_dict = self.process_parameter(info_dict)
                if b'resource' in info_dict.keys():
                    info_dict = self.process_resource(info_dict)
                info_item_list.append(info_dict)

            alert_dict[b'cap_info'] = info_item_list
            alert_dict.pop(b'info')
        return alert_dict

    def determine_cap_type(self):
        try:
            parser = etree.XMLParser(recover=self.recover, remove_blank_text=True)
            tree = etree.fromstring(self.xml, parser)
        except ValueError:
            raise Exception(b'Invalid XML')

        ns_list = tree.nsmap.values()
        if ATOM_URI in ns_list:
            self.cap_xml_type = b'ATOM'
        elif CAP1_2_URN in ns_list:
            self.cap_xml_type = b'CAP1_2'
        elif CAP1_1_URN in ns_list:
            self.cap_xml_type = b'CAP1_1'
        elif EDXL_DE_URN in ns_list:
            self.cap_xml_type = b'EDXL_DE'
        else:
            self.cap_xml_type = b'RSS'

    def dirty_invalid_xml_hacks(self):
        self.xml = bytes(self.xml).replace(b'<references />', b'')

    def get_objectified_xml(self):
        xsd_filename = XML_TYPE_XSD_MAPPINGS[self.cap_xml_type]
        with open(os.path.join(CAPLIBRARY_PATH, xsd_filename)) as (f):
            doc = etree.parse(f)
            schema = etree.XMLSchema(doc)
            try:
                parser = objectify.makeparser(schema=schema, recover=self.recover, remove_blank_text=True)
                a = objectify.fromstring(self.xml, parser)
            except etree.XMLSyntaxError:
                raise Exception(b'Error objectifying XML')

        return a

    def get_alert_list(self):
        alerts = []
        objectified_xml = self.get_objectified_xml()
        if self.cap_xml_type == b'ATOM':
            for alert in objectified_xml.entry:
                alerts.append(alert.content.getchildren()[0])

        elif self.cap_xml_type == b'CAP1_1' or self.cap_xml_type == b'CAP1_2':
            alerts.append(objectified_xml)
        elif self.cap_xml_type == b'EDXL_DE':
            for obj in objectified_xml.contentObject:
                alert = obj.xmlContent.embeddedXMLContent.getchildren()[0]
                alerts.append(alert)

        return alerts

    def load(self):
        if self.xml:
            self.dirty_invalid_xml_hacks()
            self.determine_cap_type()
            for alert in self.get_alert_list():
                self.alert_list.append(self.parse_alert(alert))

    def as_dict(self):
        return self.alert_list