# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/anz/ijabbar/tests/test_viewlets.py
# Compiled at: 2010-04-15 21:25:08
import os, sys, cjson
from time import sleep
import transaction
if __name__ == '__main__':
    execfile(os.path.join(sys.path[0], 'framework.py'))
from anz.ijabbar.browser.viewlets import IJabbarViewlet
from anz.ijabbar.tests.base import AnzIJabbarTestCase

class TestIJabbarViewlet(AnzIJabbarTestCase):
    __module__ = __name__

    def afterSetUp(self):
        request = self.app.REQUEST
        context = self.folder
        self.viewlet = IJabbarViewlet(context, request, None, None)
        return

    def test_update(self):
        ap = self.portal.portal_properties.anz_ijabbar_properties
        self.viewlet.update()
        iJabConf = cjson.decode(self.viewlet.iJabConf)
        self.assertEqual(iJabConf['expand_bar_default'], True)
        self.assertEqual(iJabConf['expand_bar_default'], getattr(ap, 'expand_bar_default'))
        self.viewlet.update()
        iJabConf = cjson.decode(self.viewlet.iJabConf)
        self.assertEqual(iJabConf['expand_bar_default'], True)
        self.assertEqual(iJabConf['expand_bar_default'], getattr(ap, 'expand_bar_default'))
        sleep(3)
        self._setProperty(ap, 'expand_bar_default', False, 'boolean')
        transaction.commit()
        self.viewlet.update()
        iJabConf = cjson.decode(self.viewlet.iJabConf)
        self.assertEqual(iJabConf['expand_bar_default'], False)
        self.assertEqual(iJabConf['expand_bar_default'], getattr(ap, 'expand_bar_default'))

    def test_render(self):
        ret = self.viewlet.render()
        self.assert_(ret.find('<div id="ijabbar"') != -1)

    def _setProperty(self, sheet, id, value, type):
        if sheet.hasProperty(id):
            sheet.manage_delProperties(ids=[id])
        sheet.manage_addProperty(id, value, type)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(TestIJabbarViewlet))
    return suite


if __name__ == '__main__':
    framework()