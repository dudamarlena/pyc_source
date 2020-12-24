# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/archetypes/clippingimage/_field.py
# Compiled at: 2010-08-05 09:41:19
__author__ = 'Jens Klein <jens@bluedynamics.com>'
__docformat__ = 'plaintext'
from Products.Archetypes.Field import ImageField
from archetypes.clippingimage.utils import scale

class ClippingImageField(ImageField):
    """Like default ImageField from Archetypes with different scaling behaviour.

    Scales are clipped centered, the resulting image has almost (+/- 1 pixel)
    the scale.
    """
    _properties = ImageField._properties.copy()
    _properties.update({'classic_crop': []})

    def scale(self, data, w, h, default_format='PNG'):
        """ scale image"""
        return scale(self, data, w, h, default_format)