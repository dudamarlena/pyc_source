# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/prestapyt/xml2dict.py
# Compiled at: 2016-09-01 03:41:47
"""
  Code from https://github.com/nkchenz/lhammer/blob/master/lhammer/xml2dict.py
  Distributed under GPL2 Licence
  CopyRight (C) 2009 Chen Zheng

  Adapted for Prestapyt by Guewen Baconnier
  Copyright 2012 Camptocamp SA
"""
import re
try:
    import xml.etree.cElementTree as ET
except ImportError as err:
    import xml.etree.ElementTree as ET

def _parse_node(node):
    tree = {}
    attrs = {}
    for attr_tag, attr_value in node.attrib.items():
        if attr_tag == '{http://www.w3.org/1999/xlink}href':
            continue
        attrs.update(_make_dict(attr_tag, attr_value))

    value = node.text.strip() if node.text is not None else ''
    if attrs:
        tree['attrs'] = attrs
    has_child = False
    for child in node.getchildren():
        has_child = True
        ctag = child.tag
        ctree = _parse_node(child)
        cdict = _make_dict(ctag, ctree)
        if ctree:
            value = ''
        if ctag not in tree:
            tree.update(cdict)
            continue
        old = tree[ctag]
        if not isinstance(old, list):
            tree[ctag] = [
             old]
        tree[ctag].append(ctree)

    if not has_child:
        tree['value'] = value
    if tree.keys() == ['value']:
        tree = tree['value']
    return tree


def _make_dict(tag, value):
    """Generate a new dict with tag and value
       If tag is like '{http://cs.sfsu.edu/csc867/myscheduler}patients',
       split it first to: http://cs.sfsu.edu/csc867/myscheduler, patients
    """
    tag_values = value
    result = re.compile('\\{(.*)\\}(.*)').search(tag)
    if result:
        tag_values = {'value': value}
        tag_values['xmlns'], tag = result.groups()
    return {tag: tag_values}


def xml2dict(xml):
    """Parse xml string to dict"""
    element_tree = ET.fromstring(xml)
    return ET2dict(element_tree)


def ET2dict(element_tree):
    """Parse xml string to dict"""
    return _make_dict(element_tree.tag, _parse_node(element_tree))


if __name__ == '__main__':
    from pprint import pprint
    s = '<?xml version="1.0" encoding="UTF-8"?>\n    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">\n    <addresses>\n    <address id="1" xlink:href="http://localhost:8080/api/addresses/1"/>\n    <address id="2" xlink:href="http://localhost:8080/api/addresses/2"/>\n    <address id="3" xlink:href="http://localhost:8080/api/addresses/3"/>\n    <address id="4" xlink:href="http://localhost:8080/api/addresses/4"/>\n    <address id="5" xlink:href="http://localhost:8080/api/addresses/5"/>\n    <address id="6" xlink:href="http://localhost:8080/api/addresses/6"/>\n    <address id="7" xlink:href="http://localhost:8080/api/addresses/7"/>\n    <address id="8" xlink:href="http://localhost:8080/api/addresses/8"/>\n    </addresses>\n    </prestashop>'
    pprint(xml2dict(s))
    s = '<?xml version="1.0" encoding="UTF-8"?>\n    <prestashop xmlns:xlink="http://www.w3.org/1999/xlink">\n    <address>\n    \t<id><![CDATA[1]]></id>\n    \t<id_customer></id_customer>\n    \t<id_manufacturer xlink:href="http://localhost:8080/api/manufacturers/1"><![CDATA[1]]></id_manufacturer>\n    \t<id_supplier></id_supplier>\n    \t<id_country xlink:href="http://localhost:8080/api/countries/21"><![CDATA[21]]></id_country>\n    \t<id_state xlink:href="http://localhost:8080/api/states/5"><![CDATA[5]]></id_state>\n    \t<alias><![CDATA[manufacturer]]></alias>\n    \t<company></company>\n    \t<lastname><![CDATA[JOBS]]></lastname>\n    \t<firstname><![CDATA[STEVEN]]></firstname>\n    \t<address1><![CDATA[1 Infinite Loop]]></address1>\n    \t<address2></address2>\n    \t<postcode><![CDATA[95014]]></postcode>\n    \t<city><![CDATA[Cupertino]]></city>\n    \t<other></other>\n    \t<phone><![CDATA[(800) 275-2273]]></phone>\n    \t<phone_mobile></phone_mobile>\n    \t<dni></dni>\n    \t<vat_number></vat_number>\n    \t<deleted><![CDATA[0]]></deleted>\n    \t<date_add><![CDATA[2012-02-06 09:33:52]]></date_add>\n    \t<date_upd><![CDATA[2012-02-07 11:18:48]]></date_upd>\n    </address>\n    </prestashop>'
    pprint(xml2dict(s))
    import dict2xml
    from prestapyt import PrestaShopWebService
    prestashop = PrestaShopWebService('http://localhost:8080/api', 'BVWPFFYBT97WKM959D7AVVD0M4815Y1L')
    products_xml = prestashop.get('products', 1)
    products_dict = ET2dict(products_xml)
    pprint(dict2xml.dict2xml(products_dict))