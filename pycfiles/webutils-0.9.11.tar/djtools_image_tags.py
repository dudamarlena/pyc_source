# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/pjs/python-modules/webutils/djtools/templatetags/djtools_image_tags.py
# Compiled at: 2016-05-17 14:52:55
import os, urlparse
from django import template
from django.core.files.storage import get_storage_class
from django.core.files.base import ContentFile
from PIL import Image
from cStringIO import StringIO
register = template.Library()

@register.filter
def thumbnail(file, size='104x104', force_save=False):
    x, y = map(int, size.split('x'))
    try:
        filename = file.path
    except NotImplementedError:
        filename = file.name

    filehead, filetail = os.path.split(filename)
    basename, format = os.path.splitext(filetail)
    miniature = basename + '_' + size + format
    miniature_filename = os.path.join(filehead, miniature)
    filehead, filetail = os.path.split(file.url)
    miniature_url = filehead + '/' + miniature
    storage = get_storage_class()()
    if storage.exists(miniature_filename) and not force_save:
        return miniature_url
    image = Image.open(file)
    if image.size[0] < x and image.size[1] < y:
        miniature_url = file.url
    else:
        stream = StringIO()
        image.thumbnail([x, y], Image.ANTIALIAS)
        image.save(stream, image.format, quality=90)
        storage.save(miniature_filename, ContentFile(stream.getvalue()))
    file.seek(0)
    return miniature_url