# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\XPath\XPathTypes.py
# Compiled at: 2005-08-02 17:43:00
"""
Mappings between Python types and standard XPath object types

Copyright 2004 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
__all__ = [
 'NodesetType', 'StringType', 'NumberType', 'BooleanType', 'g_xpathPrimitiveTypes', 'g_xpathRecognizedNodes']
from xml.dom import Node
from Ft.Lib import boolean
from Ft.Xml.XPath import NAMESPACE_NODE
ObjectType = object
NodesetType = list
StringType = unicode
NumberType = float
BooleanType = boolean.BooleanType
g_xpathPrimitiveTypes = {str: 'string', unicode: 'string', int: 'number', long: 'number', float: 'number', list: 'node-set', bool: 'boolean', boolean.BooleanType: 'boolean', object: 'object'}
NumberTypes = {int: True, long: True, float: True}
g_xpathRecognizedNodes = {Node.ELEMENT_NODE: True, Node.ATTRIBUTE_NODE: True, Node.TEXT_NODE: True, Node.DOCUMENT_NODE: True, Node.PROCESSING_INSTRUCTION_NODE: True, Node.COMMENT_NODE: True, NAMESPACE_NODE: True}