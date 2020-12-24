# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/xmlobjects/__init__.py
# Compiled at: 2007-02-16 01:49:39
from xmlobject import *
from parser import *
from elements_lib import *

def tostring(xmlobject):
    from xml.etree import cElementTree as ElementTree
    return ElementTree.tostring(xmlobject._etree_)


def fromstring(xml_string):
    from xml.etree import cElementTree as ElementTree
    parser = Parser()
    return parser.parse_etree(ElementTree.fromstring(xml_string))


def set_namespace(xmlobject, namespace):
    """Set the namespace for a given"""
    if issubclass(xmlobject.__class__, element_type) or type(xmlobject) is XMLObject:
        xmlobject._set_namespace_(namespace)
    else:
        raise TypeError, 'Not xmlobjects.element_type'


def hasattrib(xmlobject, key):
    if key in xmlobject._etree_.attrib.keys():
        return True
    else:
        return False