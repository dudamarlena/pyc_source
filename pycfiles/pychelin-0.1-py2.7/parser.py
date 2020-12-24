# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pychelin/parser.py
# Compiled at: 2014-06-13 10:51:28
from lxml import etree
__all__ = [
 'getParser',
 'ParseError']

class ParseError(Exception):
    pass


class XMLParser(object):

    def __init__(self):
        pass

    def __call__(self, xml):
        """
        @type xml: unicode object
        """
        assert isinstance(xml, unicode), 'xml should be a unicode object'
        res = []
        response = etree.XML(xml.encode('utf-8'))
        if response[0].tag == 'error':
            raise ParseError(response.xpath('//errorCode')[0], response.xpath('//errorMsg')[0])
        items = response.xpath('locationList')[0].xpath('item')
        for item in items:
            coherence_street = item.xpath('coherenceDegree/street')[0].text
            coherence_city = item.xpath('coherenceDegree/city')[0].text
            location = item.xpath('location')[0]
            type_response = item.xpath('type')
            streetLabel = location.xpath('streetLabel')
            city = location.xpath('city')
            postalCode = location.xpath('postalCode')
            countryLabel = location.xpath('countryLabel')
            countryOfficial = location.xpath('countryOfficial')
            formattedAddressLine = location.xpath('formattedAddressLine')
            formattedCityLine = location.xpath('formattedCityLine')
            area = location.xpath('area')
            data = {'type': type_response[0].text if type_response else '', 
               'streetLabel': streetLabel[0].text if streetLabel else '', 
               'city': city[0].text if city else '', 
               'postalCode': postalCode[0].text if postalCode else '', 
               'countryLabel': countryLabel[0].text if countryLabel else '', 
               'countryOfficial': countryOfficial[0].text if countryOfficial else '', 
               'formattedAddressLine': formattedAddressLine[0].text if formattedAddressLine else '', 
               'formattedCityLine': formattedCityLine[0].text if formattedCityLine else '', 
               'area': area[0].text if area else '', 
               'latitude': location.xpath('coords/lat')[0].text, 
               'longitude': location.xpath('coords/lon')[0].text, 
               'coherence_street': coherence_street, 
               'coherence_city': coherence_city}
            res.append(data)

        return res


def getParser(parser_type):
    if parser_type == 'xml':
        return XMLParser()
    else:
        return