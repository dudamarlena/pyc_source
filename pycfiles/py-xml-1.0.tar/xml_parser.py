# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\MyWork\python\pinae\py-xml\py_xml\xml_parser.py
# Compiled at: 2016-01-28 08:46:31
import types, xml.dom.minidom

class XmlParser:

    def __init__(self):
        pass

    def parse(self, filename):
        dom = xml.dom.minidom.parse(filename)
        return self.__parse(dom)

    def parse_string(self, xml_str):
        dom = xml.dom.minidom.parseString(xml_str)
        return self.__parse(dom)

    def __parse(self, node):
        if node == None:
            return
        else:
            node_data = {}
            children = node.childNodes
            if len(children) > 0:
                for child in children:
                    child_name = child.nodeName
                    if child_name != None and child_name.strip() != '':
                        if child.nodeType == child.ELEMENT_NODE:
                            child_value = self.__parse(child)
                        elif child.nodeType == child.TEXT_NODE or child.nodeType == child.CDATA_SECTION_NODE:
                            child_value = child.data.strip() if child.data != None else child.data
                        temp_node = node_data.get(child_name)
                        if temp_node == None and child_value != None and child_value != '':
                            temp_node = child_value
                        elif type(temp_node) == types.DictionaryType or type(temp_node) == types.UnicodeType:
                            temp_node = [
                             temp_node, child_value]
                        elif type(temp_node) == types.ListType:
                            temp_node.append(child_value)
                        if temp_node != None:
                            if child.nodeType == child.TEXT_NODE:
                                child_name = '_node_'
                            elif child.nodeType == child.CDATA_SECTION_NODE:
                                child_name = '_cdata_'
                            node_data[child_name] = temp_node

            if node.attributes != None:
                for attr_key in node.attributes.keys():
                    attribute = node.attributes[attr_key]
                    attr_name = attribute.name
                    if attr_name != None and attr_name != '':
                        attr_value = {'_attr_': attribute.value}
                        temp_node = node_data.get(attr_name)
                        if temp_node == None:
                            temp_node = attr_value
                        elif type(temp_node) == types.DictionaryType:
                            temp_node = [
                             temp_node, attr_value]
                        elif type(temp_node) == types.ListType:
                            temp_node.append(attr_value)
                        if temp_node != None:
                            node_data[attr_name] = temp_node

            return node_data