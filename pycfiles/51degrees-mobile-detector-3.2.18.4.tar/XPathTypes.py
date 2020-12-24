# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPath\XPathTypes.py
# Compiled at: 2005-08-02 17:43:00
__doc__ = '\nMappings between Python types and standard XPath object types\n\nCopyright 2004 Fourthought, Inc. (USA).\nDetailed license and copyright information: http://4suite.org/COPYRIGHT\nProject home, documentation, distributions: http://4suite.org/\n'
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