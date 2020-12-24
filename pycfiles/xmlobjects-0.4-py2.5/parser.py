# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/xmlobjects/parser.py
# Compiled at: 2007-02-16 01:49:39
import copy
from xml.etree import cElementTree as ElementTree
from dateutil.parser import parse as dateutil_parse
from datetime import datetime
from xmlobject import *
from elements_lib import *

class Parser(object):
    _xmlobject_class_ = XMLObject

    def parse_etree(self, etree):
        """Default etree parser"""

        def recursive_child_parser(parent=None, etree=None):
            """Simple recursive function that begins the parsing path for all elements, attributes and values"""
            if parent is None:
                parent = self._xmlobject_class_(etree.tag)
                if len(etree.attrib) is not 0:
                    for (key, value) in etree.attrib.items():
                        parent[key] = value

                for child in etree.getchildren():
                    recursive_child_parser(parent, child)

                return parent
            if len(etree.getchildren()) is not 0:
                (namespace, name) = get_namespace_and_name(etree.tag)
                if hasattr(parent, name):
                    if type(getattr(parent, name)) is not element_list:
                        setattr(parent, name, [])
                    getattr(parent, name).append(self._xmlobject_class_(name, namespace))
                    if namespace is not None:
                        getattr(parent, name)[(-1)]._namespace_ = namespace
                    if namespace is None and parent._member_inherit_namespace_ is True:
                        getattr(parent, name)[(-1)]._namespace_ = None
                    parent = getattr(parent, name)[(-1)]
                    if len(etree.attrib) is not 0:
                        for (key, value) in etree.attrib.items():
                            parent[key] = value

                else:
                    setattr(parent, name, self._xmlobject_class_(name, namespace))
                    if namespace is not None:
                        getattr(parent, name)._namespace_ = namespace
                    if namespace is None and parent._member_inherit_namespace_ is True:
                        getattr(parent, name)._namespace_ = None
                    parent = getattr(parent, name)
                    if len(etree.attrib) is not 0:
                        for (key, value) in etree.attrib.items():
                            parent[key] = value

                for child in etree.getchildren():
                    recursive_child_parser(parent, child)

            (namespace, name) = get_namespace_and_name(etree.tag)
            if hasattr(parent, name):
                if type(getattr(parent, name)) is not element_list:
                    setattr(parent, name, [])
                getattr(parent, name).append(self.fallback(etree.text))
                if namespace is not None:
                    getattr(parent, name)[(-1)]._namespace_ = namespace
                if namespace is None and parent._member_inherit_namespace_ is True:
                    getattr(parent, name)[(-1)]._namespace_ = None
                if len(etree.attrib) is not 0:
                    for (key, value) in etree.attrib.items():
                        getattr(parent, name)[(-1)][key] = value

            else:
                setattr(parent, name, self.fallback(etree.text))
                if namespace is not None:
                    getattr(parent, name)._namespace_ = namespace
                if namespace is None and parent._member_inherit_namespace_ is True:
                    getattr(parent, name)._namespace_ = None
                if len(etree.attrib) is not 0:
                    for (key, value) in etree.attrib.items():
                        getattr(parent, name)[key] = value

            return

        xobj = recursive_child_parser(etree=etree, parent=None)
        return xobj

    def fallback(self, value):
        """Fallback method to return best type converter for a given value"""
        if value is None or value == '':
            return
        if value.find('.') is not -1:
            try:
                return float(value)
            except:
                pass

        if value.find('T') is not -1:
            try:
                return dateutil_parse(value)
            except:
                pass

        try:
            return int(value)
        except:
            return str(value)

        return