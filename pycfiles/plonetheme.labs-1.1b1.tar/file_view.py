# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /var/plone4_dev/Python-2.6/lib/python2.6/site-packages/plonetheme/laboral/browser/file_view.py
# Compiled at: 2011-05-20 07:51:00
import time, string
from zope.interface import implements
from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five import BrowserView
from zope.viewlet.interfaces import IViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from collective.contentleadimage.config import IMAGE_FIELD_NAME
from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
from collective.flowplayer.interfaces import IFlowPlayable
from collective.flowplayer.interfaces import IAudio
from Products.CMFCore.utils import getToolByName
from plonetheme.laboral.browser.interfaces import ISlider

class FileView(BrowserView):

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