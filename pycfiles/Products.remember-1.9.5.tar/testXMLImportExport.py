# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/Products/Relations/tests/testXMLImportExport.py
# Compiled at: 2008-09-11 19:48:09
import os, sys
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from App.Common import package_home
from Products.PloneTestCase import PloneTestCase
from Products.Relations import config
import common
common.installWithinPortal()

class TestXMLImportExport(PloneTestCase.PloneTestCase):
    __module__ = __name__

    def testXMLImport(self):
        self.loginAsPortalOwner()
        xmlpath = os.path.join(package_home(config.GLOBALS), 'tests', 'relations_sample.xml')
        f = open(xmlpath)
        xml = f.read()
        f.close()
        tool = self.portal.relations_library
        tool.importXML(xml)
        ruleset = tool.getRuleset('document_files')
        xml = tool.exportXML()
        tool.manage_delObjects(tool.objectIds())
        tool.importXML(xml)
        self.assertEqual(tool.getRuleset('document_files').objectIds(), ruleset.objectIds())
        rset = tool.getRuleset('document_files')
        from Products.Relations.components.contentreference import _findInstanceOf
        from Products.Relations.components import inverse
        ii = _findInstanceOf(rset.objectValues(), inverse.InverseImplicator)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestXMLImportExport))
    return suite


if __name__ == '__main__':
    framework()