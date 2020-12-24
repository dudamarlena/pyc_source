# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/content.py
# Compiled at: 2017-10-20 19:10:24
from plone.dexterity.content import Container
from sc.photogallery.interfaces import IPhotoGallery
from zope.interface import implementer
import sys
sys.modules['sc.photogallery.content.photogallery'] = sys.modules[__name__]

@implementer(IPhotoGallery)
class PhotoGallery(Container):
    """A Photo Gallery content type with a slideshow view."""

    def image(self):
        """Return the first image on a Photo Gallery."""
        images = self.listFolderContents()
        if len(images) > 0:
            return images[0]
        else:
            return

    def image_caption(self):
        """Return the description of the first image in a Photo Gallery."""
        try:
            return self.image().Description()
        except AttributeError:
            return ''

    image_thumb = image

    def tag(self, **kwargs):
        """Return a tag for the first image in a Photo Gallery."""
        try:
            scales = self.image().restrictedTraverse('@@images')
            return scales.tag('image', **kwargs)
        except AttributeError:
            return

        return