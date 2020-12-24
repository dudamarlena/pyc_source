# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imaging/specs.py
# Compiled at: 2012-06-06 15:56:17
from imagekit.specs import ImageSpec
from imagekit import processors

class ResizeImagingThumb(processors.Resize):
    width = 200
    height = 200
    crop = True


class ResizeSmallThumb(processors.Resize):
    width = 200
    height = 200
    crop = True


class ResizeDisplay(processors.Resize):
    width = 600


class ImagingThumbnail(ImageSpec):
    access_as = 'imaging_thumbnail'
    pre_cache = True
    processors = [ResizeImagingThumb]


class Display(ImageSpec):
    processors = [
     ResizeDisplay]


class SmallThumbnail(ImageSpec):
    access_as = 'small_thumbnail'
    pre_cache = True
    processors = [ResizeSmallThumb]