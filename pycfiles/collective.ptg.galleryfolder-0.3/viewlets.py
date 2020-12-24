# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Applications/Plone/zinstance/src/collective.ptg.galleryfolder/collective/ptg/galleryfolder/browser/viewlets.py
# Compiled at: 2012-12-21 05:38:44
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from plone.app.layout.viewlets.common import ViewletBase

class GalleryInfo(ViewletBase):
    render = ViewPageTemplateFile('galleryinfo.pt')
    images = 1