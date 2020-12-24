# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/Products/slideshowfolder/browser.py
# Compiled at: 2008-07-10 01:59:37
__doc__ = '\nmodule: slideshowfolder\ncreated by: Johnpaul Burbank <jpburbank@tegus.ca>\nDate: July 8, 2007\n'
import re
from zope.interface import implements, providedBy, alsoProvides
try:
    from zope.interface import noLongerProvides
    has_zope_3_3 = True
except ImportError:
    has_zope_3_3 = False
    from zope.interface import directlyProvides, directlyProvidedBy

try:
    from plone.memoize.view import memoize
    has_memoize = True
except ImportError:
    has_memoize = False

from Products.Five.browser import BrowserView
from Acquisition import aq_inner
from zope.formlib import form
from plone.app.form import base as ploneformbase
from Products.slideshowfolder import SlideshowFolderMessageFactory as _
from Products.CMFCore.utils import getToolByName
from Products.ATContentTypes.interface.topic import IATTopic
from Products.ATContentTypes.interface.image import IATImage
from Products.ATContentTypes.content.image import ATImageSchema
from Products.slideshowfolder.interfaces import ISlideShowSettings, ISlideShowView, IFolderSlideShowView, ISlideShowFolder, ISlideshowImage
from Products.slideshowfolder.slideshowsetting import SlideShowSettings
from Products.slideshowfolder.config import PROJ
from Products.slideshowfolder import HAS_PLONE30
try:
    from zope.annotation.interfaces import IAttributeAnnotatable
    from zope.annotation.interfaces import IAnnotations
except ImportError:
    from zope.app.annotation.interfaces import IAttributeAnnotatable
    from zope.app.annotation.interfaces import IAnnotations

if HAS_PLONE30:
    WF_FILTER = None
    IMAGE_FILTER = dict(object_provides=(IATImage.__identifier__, ISlideshowImage.__identifier__))
else:
    WF_FILTER = 'published'
    IMAGE_FILTER = dict(meta_type='ATImage')
image_re = re.compile('^.*\\.jpe?g$|\\.gif$|\\.png$', re.IGNORECASE)

class SlideShowFolderView(BrowserView):
    __module__ = __name__
    implements(ISlideShowView)
    __catalog_args = IMAGE_FILTER
    wf_filter = WF_FILTER

    def __init__(self, context, request):
        super(BrowserView, self).__init__(context, request)
        self.settings = SlideShowSettings(self.context)

    def setWorkflowFilter(self, wf_filter=WF_FILTER):
        self.wf_filter = wf_filter

    def _uncached_getSlideshowElements(self):
        """Convenience method to do the actual catalog calls.  Returns a list of brains or None"""
        if IATTopic.providedBy(self.context):
            results = self.context.queryCatalog(**self.__catalog_args)
        else:
            cat = getToolByName(self.context, 'portal_catalog')
            args = dict(**self.__catalog_args)
            path = ('/').join(self.context.getPhysicalPath())
            args['path'] = {'query': path, 'depth': 1}
            args['sort_on'] = 'getObjPositionInParent'
            if self.wf_filter is not None:
                args['review_state'] = self.wf_filter
            results = cat(**args)
        return results

    def _getImageCaption(self, item):
        caption = item.Description
        if not caption:
            caption = item.Title
            if image_re.match(caption):
                caption = ''
        caption = caption.decode('UTF-8')
        caption = caption.replace("'", "\\'")
        caption = caption.replace('\n', ' ')
        caption = caption.replace('\r', ' ')
        return caption

    def getSlideshowImages(self):
        brains = self._getSlideshowElements()
        pics = []
        for item in brains:
            pic_info = dict(name='%s/image_large' % item.getURL(), caption=self._getImageCaption(item))
            pics.append(pic_info)

        return pics

    def getSlideshowSettings(self):
        """Returns a list of settings for the current slideshowfolder in a dict."""
        options = {}
        if self.settings.transitionTime:
            options['duration'] = int(self.settings.transitionTime * 1000)
        if self.settings.slideDuration:
            options['delay'] = int(self.settings.slideDuration * 1000)
        options['thumbnails'] = self.settings.thumbnails and 'true' or 'false'
        options['captions'] = self.settings.captions and 'true' or 'false'
        options['loop'] = self.settings.loop and 'true' or 'false'
        options['linked'] = self.settings.linked and 'true' or 'false'
        size = self.getSlideshowSize()
        options['replace'] = "[/image_%s/, 'image_tile']" % size['name']
        options['width'] = size['width']
        options['height'] = size['height']
        options['paused'] = 'false'
        options['random'] = self.settings.random and 'true' or 'false'
        options['controller'] = self.settings.arrows and 'true' or 'false'
        options['fast'] = self.settings.fast and 'true' or 'false'
        return options

    def getSlideshowSize(self):
        return dict(name='large', width=self.settings.showWidth, height=self.settings.showHeight)

    def getControllerTranslations(self):
        play_pause = 'pause'
        translations = {'first': _('title_controller_first', default='First [Shift + Left arrow]'), 'prev': _('title_controller_prev', default='Previous [Left arrow]'), play_pause: _('title_controller_pause', default='Play / Pause [P]'), 'next': _('title_controller_next', default='Next [Right arrow]'), 'last': _('title_controller_last', default='Last [Shift + Right arrow]')}
        return [ {'id': id, 'msg': msg} for (id, msg) in translations.items() ]

    if has_memoize and HAS_PLONE30:

        @memoize
        def _getSlideshowElements(self):
            return self._uncached_getSlideshowElements()

    else:
        _getSlideshowElements = _uncached_getSlideshowElements


class FolderSlideShowView(BrowserView):
    """Provides view methods in regards to the transition from folder to slideshow folder"""
    __module__ = __name__
    implements(IFolderSlideShowView)
    iprovides = (IAttributeAnnotatable, ISlideShowFolder)

    def isSlideshow(self):
        """Returns true if we're implementing the ISlideShowFolder interface.

        (Note: we're using implementation of that interface as a proxy for a few other
        behaviors that aren't technically w/in the scope of the interface, such
        as having the view selected and the config tab added.)"""
        return ISlideShowFolder.providedBy(self.context)

    def makeSlideshow(self):
        """Make a folderish object a slideshowfolder"""
        for inter in self.iprovides:
            if not inter.providedBy(self.context):
                alsoProvides(self.context, inter)

        folder = aq_inner(self.context)
        folder.layout = 'folder_slideshow'
        plone_utils = getToolByName(self.context, 'plone_utils')
        plone_utils.addPortalMessage(_('message_slideshow_created', default='This folder is now designated a slideshow.'))
        if hasattr(self.request, 'RESPONSE'):
            self.request.RESPONSE.redirect(self.context.absolute_url())

    def unmakeSlideshow(self):
        """Remove all traces of slideshow-ness from a folder"""
        folder = aq_inner(self.context)
        if ISlideShowFolder in providedBy(folder) and has_zope_3_3:
            noLongerProvides(folder, ISlideShowFolder)
        elif ISlideShowFolder in providedBy(folder) and not has_zope_3_3:
            directlyProvides(folder, directlyProvidedBy(folder) - ISlideShowFolder)
        if hasattr(folder, 'layout'):
            delattr(folder, 'layout')
        annotations = IAnnotations(self.context)
        if annotations.has_key(PROJ):
            del annotations[PROJ]
        if hasattr(self.request, 'RESPONSE'):
            plone_utils = getToolByName(self.context, 'plone_utils')
            plone_utils.addPortalMessage(_('message_slideshow_removed', default='Completely removed slideshow capabilities.'))
            self.request.RESPONSE.redirect(self.context.absolute_url())


class SlideShowSettingsForm(ploneformbase.EditForm):
    __module__ = __name__
    form_fields = form.FormFields(ISlideShowSettings)
    label = _('heading_slideshow_settings_form', default='Slideshow folder settings')
    description = _('description_slideshow_settings_form', default='Configure the parameters for this slideshow folder.')
    form_name = _('title_slideshow_settings_form', default='Slideshow folder settings')