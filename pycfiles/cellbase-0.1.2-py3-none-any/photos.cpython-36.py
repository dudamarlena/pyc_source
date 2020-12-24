# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/doomsday/git/cellarpy/venv/lib/python3.6/site-packages/cellar/photos.py
# Compiled at: 2016-02-20 19:17:49
# Size of source mod 2**32: 2280 bytes
from PIL import Image
from PIL import ImageOps

def __transpose_exif_orientation(src, dst):

    def get_exif(img):
        from PIL.ExifTags import TAGS
        ret = {}
        info = img._getexif()
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

        return ret

    exif = get_exif(src)
    if 'Orientation' in exif:
        orientation = exif['Orientation']
        if orientation == 1:
            pass
        else:
            if orientation == 2:
                dst = dst.transpose(Image.FLIP_LEFT_RIGHT)
            else:
                if orientation == 3:
                    dst = dst.transpose(Image.ROTATE_180)
                else:
                    if orientation == 4:
                        dst = dst.transpose(Image.FLIP_TOP_BOTTOM)
                    else:
                        if orientation == 5:
                            dst = dst.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_90)
                        else:
                            if orientation == 6:
                                dst = dst.transpose(Image.ROTATE_270)
                            else:
                                if orientation == 7:
                                    dst = dst.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
                                elif orientation == 8:
                                    dst = dst.transpose(Image.ROTATE_90)
    return dst


def _transpose_exif_orientation(src, dst):
    try:
        return __transpose_exif_orientation(src, dst)
    except:
        return dst


def resize_fixed_size(src, dest, width, height):
    im = Image.open(src)
    if im.size[0] > im.size[1]:
        bg_size = (
         im.size[0], height)
    else:
        bg_size = (
         width, im.size[1])
    im.resize(bg_size, Image.ANTIALIAS)
    thumb = ImageOps.fit(image=im, size=(width, height), method=(Image.ANTIALIAS))
    thumb = _transpose_exif_orientation(im, thumb)
    thumb.save(dest, 'JPEG', quality=80, optimize=True, progressive=True)


def resize_keep_ratio(src, dest, max_width, max_height):
    im = Image.open(src)
    im.thumbnail((max_width, max_height), Image.ANTIALIAS)
    im = _transpose_exif_orientation(im, im)
    im.save(dest, 'JPEG', quality=80, optimize=True, progressive=True)