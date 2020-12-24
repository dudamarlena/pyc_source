# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/espenmoe-nilssen/Plone/zinstance/src/collective.js.supersized/collective/js/supersized/browser/views.py
# Compiled at: 2014-09-16 06:53:54
from Products.Five.browser import BrowserView
try:
    from zope.app.pagetemplate.viewpagetemplatefile import ViewPageTemplateFile
except ImportError:
    from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile

from zope.interface import implements, Interface
from Products.Five import BrowserView
from plone import api
from collective.js.supersized.interfaces import ISupersizedSettings

class SupersizedView(BrowserView):
    """
    A browser view to be used on news items. It will show the news image as background image as background
    """
    template = ViewPageTemplateFile('supersized.pt')

    def javascript(self):
        image_url = self.context.absolute_url() + '/@@images/image'
        size = api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.imagesize')
        if size != 'original':
            image_url += '/'
            image_url += size
        return '\n<script type="text/javascript" charset="utf-8">\n$(document).ready(function(){\n    $.supersized({\n        // Size & Position\t\t\t\t\t\t   \n        min_width\t\t        :   %(min_width)i,\t\t\t// Min width allowed (in pixels)\n        min_height\t\t        :   %(min_height)i,\t\t\t// Min height allowed (in pixels)\n        vertical_center         :   %(vertical_center)i,\t// Vertically center background\n        horizontal_center       :   %(horizontal_center)i,\t// Horizontally center background\n        fit_always\t\t\t\t:\t%(fit_always)i,\t\t// Image will never exceed browser width or height (Ignores min. dimensions)\n        fit_portrait         \t:   %(fit_portrait)i,\t\t// Portrait images will not exceed browser height\n        fit_landscape\t\t\t:   %(fit_landscape)i,\t\t// Landscape images will not exceed browser width\n                                                   \n        // Components\t\t\t\t\t\t\t\n        slide_links\t\t\t\t:\t\'blank\',\t// Individual links for each slide (Options: false, \'num\', \'name\', \'blank\')\n        thumb_links\t\t\t\t:\t1,\t\t\t// Individual thumb links for each slide\n        slides \t\t\t\t\t:  \t[{image : \'%(image)s\'},\n                                    ],\n                                    \n        // Theme Options\t\t\t   \n        mouse_scrub\t\t\t\t:\t0\n    });\n});\n</script>\n' % {'image': image_url, 
           'min_width': api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.min_width'), 
           'min_height': api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.min_height'), 
           'vertical_center': api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.vertical_center'), 
           'horizontal_center': api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.horizontal_center'), 
           'fit_always': api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.fit_always'), 
           'fit_portrait': api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.fit_portrait'), 
           'fit_landscape': api.portal.get_registry_record('collective.js.supersized.interfaces.ISupersizedSettings.fit_landscape')}