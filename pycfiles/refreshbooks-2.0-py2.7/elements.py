# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/refreshbooks/elements.py
# Compiled at: 2014-01-17 12:08:47
from lxml import etree

def field(name, value):
    field_element = etree.Element(name)
    field_element.text = value
    return field_element


def type(name, fields):
    type_element = etree.Element(name)
    for field in fields:
        type_element.append(field)

    return type_element


def request(name, parameters, _element_name='request'):
    request_element = type(_element_name, parameters)
    request_element.attrib.update(dict(method=name))
    return request_element