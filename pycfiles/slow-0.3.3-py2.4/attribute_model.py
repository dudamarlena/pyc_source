# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/attribute_model.py
# Compiled at: 2006-01-10 04:15:14
from lxml import etree
from lxml.etree import SubElement, Element
from xpathmodel import XPathModel, get_first
from model import NamedObject
DB_NAMESPACE_URI = 'http://www.dvs1.informatik.tu-darmstadt.de/research/OverML/nala'

def buildTypes():
    return Element('{%s}types' % DB_NAMESPACE_URI)


def buildAttributes():
    return Element('{%s}attributes' % DB_NAMESPACE_URI)


def buildAttribute(attributes, attr_name, type_name, attribute_dict={}):
    return SubElement(attributes, ('{%s}attribute' % DB_NAMESPACE_URI), name=attr_name, type_name=type_name, **attribute_dict)


def _bool_element(name):
    tag = '{%s}%s' % (DB_NAMESPACE_URI, name)
    get = 'boolean(./%s)' % tag

    def set(self, _xpath_result, value):
        if _xpath_result:
            if not value:
                element = _xpath_result[0]
                element.getparent().remove(element)
        elif value:
            SubElement(self, tag)

    set.__doc__ = './' + tag
    return (get, set)


class TypeModel(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = DB_NAMESPACE_URI

    @get_first
    def _get_type(self, type_name):
        """./*[ @type_name = $type_name ]"""
        pass

    def _del_type(self, type_name):
        """./*[ @type_name = $type_name ]"""
        pass

    def _get_type_dict(self, _xpath_result):
        """./*[ string(@type_name) ]"""
        return dict(((child.get('type_name'), child) for child in _xpath_result))

    def _get_type_list(self):
        """./*[ string(@type_name) ]"""
        pass

    _get_type_names = './*/@type_name'


class AttributeClass(XPathModel):
    __module__ = __name__
    DEFAULT_NAMESPACE = DB_NAMESPACE_URI


class AttributeRoot(AttributeClass):
    __module__ = __name__

    def _get_attributes(self):
        """./{%(DEFAULT_NAMESPACE)s}attribute"""
        pass

    @get_first
    def _get_attribute(self, name):
        """./{%(DEFAULT_NAMESPACE)s}attribute[ @name = $name ]"""
        pass

    def _del_attribute(self, name):
        """./{%(DEFAULT_NAMESPACE)s}attribute[ @name = $name ]"""
        pass


class Attribute(AttributeClass):
    __module__ = __name__
    _val_name = NamedObject._val_name
    _attr_name = './@name'
    _attr_selected = 'bool#./@selected'
    _attr_type_name = './@type_name'
    (_get_static, _set_static) = _bool_element('static')
    (_get_transferable, _set_transferable) = _bool_element('transferable')
    (_get_identifier, _set_identifier) = _bool_element('identifier')


ns = etree.Namespace(DB_NAMESPACE_URI)
ns[None] = AttributeClass
ns['types'] = TypeModel
ns['attributes'] = AttributeRoot
ns['attribute'] = Attribute