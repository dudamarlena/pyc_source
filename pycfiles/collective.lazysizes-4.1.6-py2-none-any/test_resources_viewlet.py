# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/lazysizes/src/collective/lazysizes/tests/test_resources_viewlet.py
# Compiled at: 2018-09-06 16:06:10
from collective.lazysizes.testing import INTEGRATION_TESTING
from lxml import etree
from Products.Five.browser import BrowserView
from zope.component import getMultiAdapter
from zope.viewlet.interfaces import IViewletManager
import unittest

class ResourcesViewletTestCase(unittest.TestCase):
    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.viewlet = self.get_viewlet(self.portal)

    def get_viewlet_manager(self, context, name='plone.htmlhead'):
        request = self.request
        view = BrowserView(context, request)
        manager = getMultiAdapter((
         context, request, view), IViewletManager, name)
        return manager

    def get_viewlet(self, context, name='collective.lazysizes.resources'):
        manager = self.get_viewlet_manager(context)
        manager.update()
        viewlet = [ v for v in manager.viewlets if v.__name__ == name ]
        assert len(viewlet) == 1
        return viewlet[0]

    def test_viewlet(self):
        html = etree.HTML(self.viewlet())
        self.assertIn('async', html.xpath('//script')[0].attrib)
        regexp = 'lazysizes-[\\da-f]{7}\\.js$'
        self.assertRegexpMatches(html.xpath('//script')[0].attrib['src'], regexp)