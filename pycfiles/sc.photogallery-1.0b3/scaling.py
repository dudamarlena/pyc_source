# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hvelarde/collective/sc.photogallery/src/sc/photogallery/browser/scaling.py
# Compiled at: 2017-10-20 16:05:59
from plone.app.imaging.scaling import ImageScaling as BaseImageScaling

class ImageScaling(BaseImageScaling):
    """Adapter for image fields that allows generating scaled images."""

    def scale(self, fieldname=None, scale=None, height=None, width=None, **parameters):
        """Override ofiginal scale method so we can return an image scale."""
        if fieldname == 'image':
            image = self.context.image()
            scales = image.restrictedTraverse('@@images')
            return scales.scale(fieldname, scale, height, width, **parameters)
        else:
            return super(ImageScaling, self).scale(fieldname, scale, height, width, **parameters)