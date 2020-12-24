# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/collective/mediaAlbum/browser/albumview.py
# Compiled at: 2012-02-24 11:07:48
import time, string
from zope.interface import implements
from Acquisition import aq_inner
from zope.component import getUtility
from Products.Five import BrowserView
from zope.viewlet.interfaces import IViewlet
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.CMFPlone.interfaces import IPloneSiteRoot
from zope.component import getMultiAdapter
try:
    from collective.contentleadimage.config import IMAGE_FIELD_NAME
    from collective.contentleadimage.leadimageprefs import ILeadImagePrefsForm
    LEADIMAGEINSTALLED = True
except:
    LEADIMAGEINSTALLED = False

try:
    from collective.flowplayer.interfaces import IFlowPlayable
    from collective.flowplayer.interfaces import IAudio
    FLOWPLAYERINSTALLED = True
except:
    FLOWPLAYERINSTALLED = False

from Products.CMFCore.utils import getToolByName

class AlbumView(BrowserView):
    """
    View to override atct_album_view
    """

    @property
    def prefs(self):
        if LEADIMAGEINSTALLED:
            portal = getUtility(IPloneSiteRoot)
            return ILeadImagePrefsForm(portal)
        else:
            return
            return

    def tag(self, obj, css_class='tileImage'):
        if LEADIMAGEINSTALLED:
            context = aq_inner(obj)
            field = context.getField(IMAGE_FIELD_NAME)
            if field is not None:
                if field.get_size(context) != 0:
                    scale = self.prefs.desc_scale_name
                    return field.tag(context, scale=scale, css_class=css_class)
            return ''
        else:
            return
            return

    def getMediaShow(self):
        return '<div class="embededMediaShow disableRecursive"><a href="%s">mediaShow</a></div>' % self.context.absolute_url()

    def getFolderFirstImage(self, folder):
        results = []
        catalog = getToolByName(self, 'portal_catalog')
        path = folder.getPath()
        if folder.portal_type == 'Folder':
            results = catalog.searchResults(path={'query': path}, portal_type=('Image', ), sort_on='getObjPositionInParent')
            for item in results:
                if item.portal_type == 'Image':
                    return item.getObject()

            return
        else:
            if folder.portal_type == 'Topic':
                query = folder.getObject().buildQuery()
                if query != None:
                    results = catalog.searchResults(query)
                    for item in results:
                        if item.portal_type == 'Image':
                            return item.getObject()

                    return
                return
            return

    def currenttime(self):
        return time.time()

    def trimDescription(self, desc, num):
        if len(desc) > num:
            res = desc[0:num]
            lastspace = res.rfind(' ')
            res = res[0:lastspace] + ' ...'
            return res
        else:
            return desc

    def toLocalizedTime(self, time, long_format=None, time_only=None):
        """Convert time to localized time
        """
        util = getToolByName(self.context, 'translation_service')
        try:
            return util.ulocalized_time(time, long_format, time_only, self.context, domain='plonelocales')
        except TypeError:
            return util.ulocalized_time(time, long_format, self.context, domain='plonelocales')

    def getFolderishContents(self, folder):
        catalog = getToolByName(self, 'portal_catalog')
        path = folder.getPath()
        if folder.portal_type == 'Folder':
            results = catalog.searchResults(path={'query': path, 'depth': 1}, sort_on='getObjPositionInParent')[:3]
        elif folder.portal_type == 'Topic':
            query = folder.getObject().buildQuery()
            if query != None:
                results = catalog.searchResults(query)[:3]
            else:
                results = []
        else:
            results = []
        return results

    def translateMonth(self, month):
        if self.request['LANGUAGE'][:2] == 'en':
            return month
        if self.request['LANGUAGE'][:2] == 'es':
            if month == 'Jan':
                return 'Ene'
            else:
                if month == 'Apr':
                    return 'Abr'
                if month == 'Aug':
                    return 'Ago'
                if month == 'Dec':
                    return 'Dic'
                return month
        else:
            return month

    def filterResults(self, results):
        """Removes images that will be shown on the mediaShow
        """
        filtered = []
        for item in results:
            isFolderish = item.portal_type == 'Folder' or item.portal_type == 'Topic'
            if isFolderish:
                filtered.append(item)

        return filtered

    def isVideo(self, item):
        if FLOWPLAYERINSTALLED:
            result = IFlowPlayable.providedBy(item)
            return result
        else:
            return False

    def audio_only(self, item):
        if FLOWPLAYERINSTALLED:
            result = IAudio.providedBy(item)
            return result
        else:
            return False