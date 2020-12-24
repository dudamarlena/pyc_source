# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyfeld/upnpService.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
import urllib3
from xml.dom import minidom
from pyfeld.upnpsoap import UpnpSoap
from pyfeld.xmlHelper import XmlHelper

class Services:

    @staticmethod
    def get_services_from_location(location):
        try:
            xml_headers, xml_data = UpnpSoap.get(location)
            if xml_data is not False:
                xml_root = minidom.parseString(xml_data)
                services_list = list()
                for service in xml_root.getElementsByTagName(b'service'):
                    service_dict = XmlHelper.xml_extract_dict(service, [b'serviceType',
                     b'controlURL',
                     b'eventSubURL',
                     b'SCPDURL',
                     b'serviceId'])
                    services_list.append(service_dict)

                return services_list
        except Exception as e:
            print (b'Error get_subscription_urls:{0}').format(e)

        return


class UpnpService:

    def __init__(self):
        self.services_list = list()
        self.xml_location = b''
        self.network_location = b''

    def set_location(self, location):
        self.xml_location = location
        result = urllib3.util.parse_url(location)
        self.network_location = result.netloc
        self.services_list = Services.get_services_from_location(location)

    def get_network_location(self):
        return self.network_location

    def get_services_list(self):
        return self.services_list