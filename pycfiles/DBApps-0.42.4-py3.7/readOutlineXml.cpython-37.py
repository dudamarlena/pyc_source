# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/DBApps/TBRCSrc/readOutlineXml.py
# Compiled at: 2019-04-22 11:39:38
# Size of source mod 2**32: 1259 bytes
"""
Created on Feb 28, 2018

@author: jsk

@summary: Library to parse input xml
"""
from lxml import etree

class OutlineReader:

    def get_attr_text(self, doc, attrName, path):
        """Returns a list of tuples of: the values of attrName, the text
        of the nodes which contain the attribute attrName
         @param doc: XML document
         @param attrName: attribute whose value we want
         @param path: XPath expression locating the node which contains
         attrName
     """
        _path = path + '[@' + attrName + ']'
        work_nodes = doc.xpath(_path)
        return [self.get_value(aNode, attrName) for aNode in work_nodes]

    @staticmethod
    def get_value(node, attrName):
        """
        @summary Extract the given attributes value and the node's text
        @param node: XML node containing attribute attrName
        @param attrName: which attribute to extract the value from
        """
        return (
         node.xpath('@' + attrName)[0], node.text)