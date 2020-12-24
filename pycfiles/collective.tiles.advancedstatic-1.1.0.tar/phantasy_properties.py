# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\collective\threecolorstheme\browser\phantasy_properties.py
# Compiled at: 2008-10-12 05:15:37
import os
from Globals import DTMLFile
from Acquisition import aq_inner
from Products.ResourceRegistries.tools.packer import CSSPacker
from collective.phantasy.browser.phantasy_properties import PhantasyThemeProperties
this_dir = os.path.dirname(os.path.abspath(__file__))
templates_dir = os.path.join(this_dir, 'stylesheets')
stylesheet_dtml = DTMLFile('threecolorstheme.css', templates_dir)

class ThreeColorsThemeProperties(PhantasyThemeProperties):
    __module__ = __name__

    def __call__(self, *args, **kw):
        """Return a dtml file when calling the view (more easy thx to Gillux)"""
        context = aq_inner(self.context)
        template = stylesheet_dtml.__of__(context)
        self.getHeader()
        phantasy_props = self.getPhantasyCssProperties()
        logo = getattr(context, phantasy_props['logoName'])
        csscontent = template(context, phantasy_properties=phantasy_props, css_url=self.getPhantasyThemeUrl(), portal_url=self.getPortalUrl(), logoWidth=logo.width, logoHeight=logo.height)
        return CSSPacker('safe').pack(csscontent)