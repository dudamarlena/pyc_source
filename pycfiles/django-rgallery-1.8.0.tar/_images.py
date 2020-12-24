# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/_images.py
# Compiled at: 2014-11-03 11:26:04
import os, errno, re, sys, time, datetime, gzip, glob
from datetime import datetime
from pprint import pprint
from django.core.management.base import BaseCommand, CommandError
from django.template.defaultfilters import slugify
from django.template import Context, Template
from django.conf import settings as conf
import Image, ExifTags
from ExifTags import TAGS
from sorl.thumbnail import get_thumbnail

def get_exif(fn):
    """
    data = get_exif('img/2013-04-13 12.17.09.jpg')
    print data
    """
    ret = {}
    i = Image.open(fn)
    info = i._getexif()
    try:
        for tag, value in info.items():
            decoded = TAGS.get(tag, tag)
            ret[decoded] = value

    except:
        now = datetime.now()
        ret['DateTimeOriginal'] = now.strftime('%Y:%m:%d %H:%M:%S')

    try:
        str(ret['DateTimeOriginal'])
    except:
        now = datetime.now()
        ret['DateTimeOriginal'] = now.strftime('%Y:%m:%d %H:%M:%S')

    return ret


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def img_rotate(im2):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = dict(im2._getexif().items())
        if exif[orientation] == 3:
            im2 = im2.rotate(180, expand=True)
        elif exif[orientation] == 6:
            im2 = im2.rotate(270, expand=True)
        elif exif[orientation] == 8:
            im2 = im2.rotate(90, expand=True)
    except:
        pass

    return im2