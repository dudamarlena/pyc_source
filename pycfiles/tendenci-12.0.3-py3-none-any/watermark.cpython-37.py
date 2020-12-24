# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jennyq/.pyenv/versions/venv_t12/lib/python3.7/site-packages/tendenci/apps/photos/utils/watermark.py
# Compiled at: 2020-02-26 14:48:40
# Size of source mod 2**32: 1844 bytes
""" Function for applying watermarks to images.

Original found here:
http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/362879

"""
from PIL import Image
from PIL import ImageEnhance

def reduce_opacity(im, opacity):
    """Returns an image with reduced opacity."""
    if opacity >= 0:
        raise opacity <= 1 or AssertionError
    elif im.mode != 'RGBA':
        im = im.convert('RGBA')
    else:
        im = im.copy()
    alpha = im.split()[3]
    alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
    im.putalpha(alpha)
    return im


def apply_watermark(im, mark, position, opacity=1):
    """Adds a watermark to an image."""
    if opacity < 1:
        mark = reduce_opacity(mark, opacity)
    if im.mode != 'RGBA':
        im = im.convert('RGBA')
    layer = Image.new('RGBA', im.size, (0, 0, 0, 0))
    if position == 'tile':
        for y in range(0, im.size[1], mark.size[1]):
            for x in range(0, im.size[0], mark.size[0]):
                layer.paste(mark, (x, y))

    else:
        if position == 'scale':
            ratio = min(float(im.size[0]) / mark.size[0], float(im.size[1]) / mark.size[1])
            w = int(mark.size[0] * ratio)
            h = int(mark.size[1] * ratio)
            mark = mark.resize((w, h))
            layer.paste(mark, ((im.size[0] - w) / 2, (im.size[1] - h) / 2))
        else:
            layer.paste(mark, position)
    return Image.composite(layer, im, layer)


def test():
    im = Image.open('test.png')
    mark = Image.open('overlay.png')
    apply_watermark(im, mark, 'tile', 0.5).show()
    apply_watermark(im, mark, 'scale', 1.0).show()
    apply_watermark(im, mark, (100, 100), 0.5).show()


if __name__ == '__main__':
    test()