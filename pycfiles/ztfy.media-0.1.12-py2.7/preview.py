# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/media/browser/preview.py
# Compiled at: 2012-10-15 09:59:26
from zope.app.file.interfaces import IFile
from zope.browser.interfaces import IBrowserView
from zope.pagetemplate.interfaces import IPageTemplate
from ztfy.file.interfaces import IImageDisplay
from ztfy.media.interfaces import IMediaConversions, CUSTOM_VIDEO_TYPES, CUSTOM_AUDIO_TYPES
from ztfy.media.browser.interfaces import IMediaPreview
from ztfy.skin.layer import IZTFYBrowserLayer
from z3c.template.template import getPageTemplate
from zope.component import adapter, adapts, getMultiAdapter, queryAdapter, queryMultiAdapter
from zope.interface import implementer, implements
from ztfy.skin.page import BaseTemplateBasedPage
DEFAULT_VIDEO_WIDTH = 700

class BaseMediaPreviewAdapter(object):
    """Base media preview adapter"""
    adapts(IFile, IZTFYBrowserLayer)
    implements(IMediaPreview)

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def update(self):
        self.conversions = IMediaConversions(self.context)

    template = getPageTemplate()

    def render(self):
        if self.template is None:
            template = getMultiAdapter((self, self.request), IPageTemplate)
            return template(self)
        else:
            return self.template()


class VideoPreviewAdapter(BaseMediaPreviewAdapter):
    """Video preview adapter"""

    def __new__(cls, context, request):
        if not (context.contentType.startswith('video/') or context.contentType in CUSTOM_VIDEO_TYPES):
            return None
        else:
            return BaseMediaPreviewAdapter.__new__(cls, context, request)

    @property
    def size(self):
        display = queryAdapter(self.context, IImageDisplay, name='video')
        if display is not None:
            width, height = display.getImageSize()
            return (
             DEFAULT_VIDEO_WIDTH, int(1.0 * DEFAULT_VIDEO_WIDTH * height / width))
        else:
            return (
             DEFAULT_VIDEO_WIDTH, 500)
            return


class AudioPreviewAdapter(BaseMediaPreviewAdapter):
    """Audio preview adapter"""

    def __new__(cls, context, request):
        if not (context.contentType.startswith('audio/') or context.contentType in CUSTOM_AUDIO_TYPES):
            return None
        else:
            return BaseMediaPreviewAdapter.__new__(cls, context, request)


class MediaView(BaseTemplateBasedPage):
    """Media view"""

    def __init__(self, context, request, preview):
        BaseTemplateBasedPage.__init__(self, context, request)
        self.preview = preview

    def update(self):
        super(MediaView, self).update()
        self.preview.update()


@adapter(IFile, IZTFYBrowserLayer)
@implementer(IBrowserView)
def MediaViewFactory(context, request):
    if context.contentType.startswith('audio/') or context.contentType in CUSTOM_AUDIO_TYPES:
        preview = queryMultiAdapter((context, request), IMediaPreview, name='audio')
    elif context.contentType.startswith('video/') or context.contentType in CUSTOM_VIDEO_TYPES:
        preview = queryMultiAdapter((context, request), IMediaPreview, name='video')
    else:
        preview = None
    if preview is None:
        return
    else:
        return MediaView(context, request, preview)