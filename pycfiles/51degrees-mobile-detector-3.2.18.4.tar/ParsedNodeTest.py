# uncompyle6 version 3.6.7
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: \Ft\Xml\XPointer\ParsedNodeTest.py
# Compiled at: 2001-09-15 13:20:49
__doc__ = '\nA Parsed Token that represents a node test.\nWWW: http://4suite.org/XPATH        e-mail: support@4suite.org\n\nCopyright (c) 2000-2001 Fourthought Inc, USA.   All Rights Reserved.\nSee  http://4suite.org/COPYRIGHT  for license and copyright information\n'
import Ft.Xml.XPath.ParsedNodeTest

def ParsedNameTest(name):
    return Ft.Xml.XPath.ParsedNodeTest.ParsedNameTest(name)


def ParsedNodeTest(test, literal=None):
    node_test = g_classMap.get(test)
    if node_test:
        return node_test()
    return Ft.Xml.XPath.ParsedNodeTest.ParsedNodeTest(test, literal)


class PointNodeTest(Ft.Xml.XPath.ParsedNodeTest.NodeTestBase):
    __module__ = __name__

    def match(self, context, node, principalType):
        return 0


class RangeNodeTest(Ft.Xml.XPath.ParsedNodeTest.NodeTestBase):
    __module__ = __name__

    def match(self, context, node, principalType):
        return 0


g_classMap = {'point': PointNodeTest, 'range': RangeNodeTest}