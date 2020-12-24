# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/simplexmlapi/tests/test_api.py
# Compiled at: 2008-08-18 15:36:25
import unittest
TESTDOC = '\n<node1 abc="1" b="2" subnode="subnodeval">\n    <subnode>\n        Subnode 1 value.\n    </subnode>\n    <subnode c="3">\n        Subnode 2 value.\n        <subsubnode>\n            <thing>ThingVal</thing>\n            <thing x="y"/>\n        </subsubnode>\n    </subnode>\n    <othernode>Other text.</othernode>\n</node1>\n'
TESTCFG = dict(val1='abc', val2='subnode__0', val3='othernode', val4='subnode__a', val5='subnode.c', val6='subnode__1.subsubnode.thing', val7='subnode__1.subsubnode.thing__1.x')
from simplexmlapi import *

class TestAPI(unittest.TestCase):
    __module__ = __name__

    def setUp(self):
        self.xml = SimpleXmlApi(map=TESTCFG, source=TESTDOC)

    def test_traversal(self):
        self.assertEqual(self.xml._traverse('abc'), '1')
        self.assertEqual(self.xml._traverse('subnode__1.subsubnode.thing__1.x'), 'y')

    def test_properties(self):
        self.assertEqual(self.xml.val1, '1')
        self.assertEqual(self.xml.val4, 'subnodeval')

    def test_attrfailover(self):
        self.assertEqual(self.xml.subnode._, 'Subnode 1 value.')
        self.assertEqual(self.xml.subnode__1.c._, '3')

    def test_newProperties(self):
        self.xml.add_mapping('battr', 'b')
        self.assertEqual(self.xml.battr, '2')

    def test_factory(self):
        xml = loads(TESTDOC, map=TESTCFG)
        self.assertEqual(type(xml), SimpleXmlApi)

    def test_subclass(self):

        class SampleApi(SimpleXmlApi):
            __module__ = __name__
            _map = TESTCFG

        xml = loads(TESTDOC, cls=SampleApi)
        self.assertEqual(xml.val1, '1')
        self.assertEqual(xml.val4, 'subnodeval')


if __name__ == '__main__':
    unittest.main()