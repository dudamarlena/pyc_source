# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/quintagroup/pingtool/tests/testPropertiesToolConf.py
# Compiled at: 2009-03-31 04:47:32
from base import TestCase
from config import NT_PROPERTIES, S_PROPERTIES

class TestPropertiesToolConf(TestCase):
    __module__ = __name__

    def afterSetUp(self):
        self.ptool = self.portal.portal_properties

    def testConfigurationNavtreePropertiesTool(self):
        props = self.ptool.navtree_properties
        for (prop_id, prop_type, prop_value) in NT_PROPERTIES:
            self.assertTrue(prop_id in props.propertyIds())
            self.assertEqual(props.getPropertyType(prop_id), prop_type)
            p_value = list(props.getProperty(prop_id))
            prop_value.sort()
            p_value.sort()
            self.assertEqual([ v for v in prop_value if v in p_value ], prop_value)

    def testConfigurationSitePropertiesTool(self):
        props = self.ptool.site_properties
        for (prop_id, prop_type, prop_value) in S_PROPERTIES:
            self.assertTrue(prop_id in props.propertyIds())
            self.assertEqual(props.getPropertyType(prop_id), prop_type)
            p_value = list(props.getProperty(prop_id))
            prop_value.sort()
            p_value.sort()
            self.assertEqual([ v for v in prop_value if v in p_value ], prop_value)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestPropertiesToolConf))
    return suite