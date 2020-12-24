# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\aws\minisite\browser\phantasy_properties.py
# Compiled at: 2010-04-08 08:46:15
import os
from Globals import DTMLFile
from Acquisition import aq_inner
from Products.ResourceRegistries.tools.packer import CSSPacker
from collective.phantasy.browser.phantasy_properties import PhantasyThemeProperties
this_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(this_dir, 'css')
stylesheet_dtml = DTMLFile('minisite.css', templates_dir)

class MiniSiteThemeProperties(PhantasyThemeProperties):
    __module__ = __name__

    def __call__(self, *args, **kw):
        """Return a dtml file when calling the view (more easy thx to Gillux)"""
        context = aq_inner(self.context)
        template = stylesheet_dtml.__of__(context)
        self.getHeader()
        phantasy_props = self.getPhantasyCssProperties()
        csscontent = template(context, phantasy_properties=phantasy_props, css_url=self.getPhantasyThemeUrl(), portal_url=self.getPortalUrl())
        return CSSPacker('safe').pack(csscontent)