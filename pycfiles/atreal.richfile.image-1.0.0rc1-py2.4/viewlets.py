# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/atreal/richfile/image/browser/viewlets.py
# Compiled at: 2009-09-04 10:39:07
from plone.app.layout.viewlets import ViewletBase
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from atreal.richfile.qualifier.browser.viewlets import RichfileViewlet
from atreal.richfile.image.interfaces import IImage
from atreal.richfile.image.interfaces import IImageable
from atreal.richfile.image.browser.controlpanel import IRichFileImageSchema
from atreal.richfile.image import RichFileImageMessageFactory as _

class ImageViewlet(RichfileViewlet):
    __module__ = __name__
    marker_interface = IImage
    plugin_interface = IImageable
    plugin_id = 'image'
    plugin_title = 'Image preview'
    controlpanel_interface = IRichFileImageSchema
    index = ViewPageTemplateFile('viewlet.pt')