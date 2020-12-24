# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/tests/xml_unittest.py
# Compiled at: 2010-08-27 06:32:04
"""

:unittest:
"""
import unittest, zope.component
from zope.interface.verify import verifyObject

class Test(unittest.TestCase):

    def test_verify(self):
        from ice.control.controls.tree.interfaces import IXML
        from ice.control.controls.tree.xmlbase import XMLBase
        zope.component.provideAdapter(XMLBase)
        from zope.site.folder import Folder
        from zope.publisher.browser import TestRequest
        f = Folder()
        r = TestRequest()
        xml = zope.component.getMultiAdapter((f, r), IXML)
        self.assertEqual(verifyObject(IXML, xml), True)