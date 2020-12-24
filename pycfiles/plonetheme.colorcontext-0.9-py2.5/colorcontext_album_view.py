# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/colorcontext/browser/colorcontext_album_view.py
# Compiled at: 2010-09-15 08:23:40
import time, string
from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
from Products.CMFCore.utils import getToolByName
from collective.flowplayer.interfaces import IFlowPlayable

class ColorContextAlbumView(BrowserView):

    @property
    def prefs(self):
        portal = getUtility(IPloneSiteRoot)
        return ILeadImagePrefsForm(portal)

    def tag(self, obj, css_class='tileImage'):
        context = aq_inner(obj)
        field = context.getField(IMAGE_FIELD_NAME)
        if field is not None:
            if field.get_size(context) != 0:
                scale = self.prefs.desc_scale_name
                return field.tag(context, scale=scale, css_class=css_class)
        return ''

    def currenttime(self):
        return time.time()

    def trimDescription(self, desc):
        if len(desc) > 250:
            res = desc[0:250]
            lastspace = res.rfind(' ')
            res = res[0:lastspace] + ' ...'
            return res
        else:
            return desc

    def getFolderContents(self):
        catalog = getToolByName(self, 'portal_catalog')
        folder_url = ('/').join(self.context.getPhysicalPath())
        results = catalog.searchResults(path={'query': folder_url, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                               'File'))
        return results

    def isVideo(self, item):
        result = IFlowPlayable.providedBy(item)
        return result