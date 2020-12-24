# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/gallery/skin/gallery.py
# Compiled at: 2012-06-26 16:39:45
__docformat__ = 'restructuredtext'
from ztfy.gallery.interfaces import IGalleryParagraph, IGalleryParagraphRenderer
from zope.component import adapts
from zope.interface import implements
from ztfy.gallery.defaultskin.renderers.default import DefaultGalleryParagraphRenderer
from ztfy.gallery.skin.layer import IGalleryLayer
from ztfy.gallery import _

class GalleryParagraphRenderer(DefaultGalleryParagraphRenderer):
    adapts(IGalleryParagraph, IGalleryLayer)
    implements(IGalleryParagraphRenderer)
    label = _('Gallery renderer with scrollable pages of slides')

    @property
    def pages(self):
        index = 0
        images = self.gallery.getVisibleImages()
        length = len(images)
        while index < length:
            yield images[index:index + 15]
            index += 15


class SingleImageParagraphRenderer(DefaultGalleryParagraphRenderer):
    adapts(IGalleryParagraph, IGalleryLayer)
    implements(IGalleryParagraphRenderer)
    label = _('Scrollable pages with a single image for each page')