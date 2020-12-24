# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/archetypes/clippingimage/utils.py
# Compiled at: 2010-08-05 09:58:49
import PIL
from StringIO import StringIO
from Products.CMFPlone.utils import safe_hasattr

def crop(image, scale):
    """Crop given image to scale.

    @param image: PIL Image instance
    @param scale: tuple with (width, height)
    """
    (cwidth, cheight) = image.size
    cratio = float(cwidth) / float(cheight)
    (twidth, theight) = scale
    tratio = float(twidth) / float(theight)
    if cratio > tratio:
        middlepart = cheight * tratio
        offset = (cwidth - middlepart) / 2
        box = (int(round(offset)), 0, int(round(offset + middlepart)), cheight)
        image = image.crop(box)
    if cratio < tratio:
        middlepart = cwidth / tratio
        offset = (cheight - middlepart) / 2
        box = (0, int(round(offset)), cwidth, int(round(offset + middlepart)))
        image = image.crop(box)
    return image


def scale(instance, data, w, h, default_format='PNG'):
    """ scale image"""
    size = (
     int(w), int(h))
    original_file = StringIO(data)
    image = PIL.Image.open(original_file)
    format = image.format
    availableSizes = instance.getAvailableSizes(None)
    if safe_hasattr(instance, 'crop_scales'):
        if size in [ availableSizes[name] for name in instance.crop_scales ]:
            image = crop(image, size)
    original_mode = image.mode
    if original_mode == '1':
        image = image.convert('L')
    elif original_mode == 'P':
        image = image.convert('RGBA')
    image.thumbnail(size, instance.pil_resize_algo)
    format = format or default_format
    if original_mode == 'P' and format == 'GIF':
        image = image.convert('P')
    thumbnail_file = StringIO()
    image.save(thumbnail_file, format, quality=instance.pil_quality)
    thumbnail_file.seek(0)
    return (
     thumbnail_file, format.lower())