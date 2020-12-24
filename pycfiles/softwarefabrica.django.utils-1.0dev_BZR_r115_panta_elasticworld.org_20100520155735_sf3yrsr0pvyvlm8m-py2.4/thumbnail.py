# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/templatetags/thumbnail.py
# Compiled at: 2010-05-14 03:47:11
"""
Simple thumbnail template filter.

Based on http://www.djangosnippets.org/snippets/955/

Modifications are:

Copyright (C) 2010 Marco Pantaleoni. All rights reserved.
"""
import os
try:
    from PIL import Image
except:
    import Image

from django import template
register = template.Library()

def thumbnail(imagefile, size='104x104'):
    if ',' in size:
        (size, rotate) = size.split(',')
    else:
        rotate = 0
    (x, y) = [ int(x) for x in size.split('x') ]
    rotate = int(rotate) % 360
    (imagefile_dirname, imagefile_filename) = os.path.split(imagefile.path)
    (imagefile_basename, imagefile_format) = os.path.splitext(imagefile_filename)
    miniature_dirname = imagefile_dirname
    miniature_filename = '_thumb_' + imagefile_basename
    if rotate != 0:
        miniature_filename += '_rot%s' % rotate
    miniature_filename += '_' + size + imagefile_format
    miniature_pathname = os.path.join(miniature_dirname, miniature_filename)
    (imagefile_url_dirname, imagefile_url_filename) = os.path.split(imagefile.url)
    miniature_url = imagefile_url_dirname + '/' + miniature_filename
    if os.path.exists(miniature_pathname) and os.path.getmtime(imagefile.path) > os.path.getmtime(miniature_pathname):
        os.unlink(miniature_pathname)
    if not os.path.exists(miniature_pathname):
        image = Image.open(imagefile.path)
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')
        image.thumbnail([x, y], Image.ANTIALIAS)
        if rotate != 0:
            image = image.rotate(rotate)
        try:
            image.save(miniature_pathname, image.format, quality=90, optimize=1)
        except:
            image.save(miniature_pathname, image.format, quality=90)

    return miniature_url


register.filter(thumbnail)