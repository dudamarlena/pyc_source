# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/colorcontext/browser/colorcontext_image_view.py
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

class ColorContextImageView(BrowserView):

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

    def imageGoto(self, toNext):
        catalog = getToolByName(self, 'portal_catalog')
        inner = self.context.aq_inner
        parent = inner.aq_parent
        parent_path = parent.getPhysicalPath()
        parent_url = ('/').join(parent_path)
        results = catalog.searchResults(path={'query': parent_url, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                               'File'))
        current = self.context.absolute_url()
        prev = None
        next = None
        found = False
        for item in results:
            if not found:
                if item.getURL() == current:
                    found = True
                else:
                    prev = item.getURL()
            elif IFlowPlayable.providedBy(item.getObject()) or item.portal_type == 'Image':
                next = item.getURL()
                break

        if toNext:
            if next is None:
                return
            else:
                return next + '/view'
        elif prev is None:
            return
        else:
            return prev + '/view'
        return

    def imageGotoThumb(self, toNext):
        catalog = getToolByName(self, 'portal_catalog')
        inner = self.context.aq_inner
        parent = inner.aq_parent
        parent_path = parent.getPhysicalPath()
        parent_url = ('/').join(parent_path)
        results = catalog.searchResults(path={'query': parent_url, 'depth': 1}, sort_on='getObjPositionInParent', portal_type=('Image',
                                                                                                                               'File'))
        current = self.context.absolute_url()
        prev = None
        next = None
        found = False
        p_video = False
        n_video = False
        for item in results:
            if not found:
                if item.getURL() == current:
                    found = True
                else:
                    prev = item.getURL()
                    if IFlowPlayable.providedBy(item.getObject()):
                        p_video = True
                    else:
                        p_video = False
            elif IFlowPlayable.providedBy(item.getObject()) or item.portal_type == 'Image':
                if IFlowPlayable.providedBy(item.getObject()):
                    n_video = True
                else:
                    n_video = False
                next = item.getURL()
                break

        if toNext:
            if next is None:
                return
            elif n_video:
                return next + '/leadImage_mini'
            else:
                return next + '/image_mini'
        elif prev is None:
            return
        elif p_video:
            return prev + '/leadImage_mini'
        else:
            return prev + '/image_mini'
        return