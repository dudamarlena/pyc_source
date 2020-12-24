# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/util/image/old_gif.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 920 bytes
"""
This is probably not used and should likely be replaced by the code
in BiblioPixelAnimations.matrix.ImageAnim
"""
from .. import deprecated

def convert_mode(image, mode='RGB'):
    """Return an image in the given mode."""
    deprecated.deprecated('util.gif.convert_model')
    if image.mode == mode:
        return image
    else:
        return image.convert(mode=mode)


def image_to_colorlist(image, container=list):
    """Given a PIL.Image, returns a ColorList of its pixels."""
    deprecated.deprecated('util.gif.image_to_colorlist')
    return container(convert_mode(image).getdata())


def animated_gif_to_colorlists(image, container=list):
    """
    Given an animated GIF, return a list with a colorlist for each frame.
    """
    deprecated.deprecated('util.gif.animated_gif_to_colorlists')
    from PIL import ImageSequence
    it = ImageSequence.Iterator(image)
    return [image_to_colorlist(i, container) for i in it]