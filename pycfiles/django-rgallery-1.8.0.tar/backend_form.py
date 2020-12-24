# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/oscar/Webs/Python/django-rgallery/rgallery/management/commands/backend_form.py
# Compiled at: 2015-04-10 08:09:22
import os, glob
from StringIO import StringIO
from mimetypes import MimeTypes
from django.conf import settings as conf
from utils import *

class File(object):
    path = ''
    mime_type = ''

    def __init__(self, path):
        self.path = path
        try:
            mime = MimeTypes()
            m = str(mime.guess_type(self.path)[0])
        except:
            m = ''

        self.mime_type = m


def name():
    return 'form'


def set_dirs(source):
    source = source
    photo_target = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'photos')
    video_target = os.path.join(conf.PROJECT_DIR, 'media', 'uploads', 'videos')
    if os.path.exists(photo_target) is False:
        mkdir_p(photo_target)
    if os.path.exists(video_target) is False:
        mkdir_p(video_target)
    return (
     source, photo_target, video_target)


def get_contents(srcdir):
    types = (
     os.path.join(srcdir, '*'),)
    bucket = []
    for files in types:
        bucket.extend(glob.glob(files))

    file2 = []
    for file in bucket:
        file2.append(File(file))

    return (
     False, file2)


def filepath(file):
    return file.name


def is_image(file):
    if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
        return True
    return False


def is_video(file):
    if file.content_type == 'video/mp4' or file.content_type == 'video/3gpp' or file.content_type == 'video/quicktime' or file.content_type == 'video/x-msvideo':
        return True
    return False


def download(client, file, nombre_imagen, srcdir, destdir):
    if is_image(file):
        image = os.path.join(destdir, nombre_imagen)
        data = ''
        for c in file.chunks():
            data += c

        imagefile = StringIO(data)
        img = Image.open(imagefile)
        img = img_rotate(img)
        img.save(image, img.format)
        return image
    if is_video(file):
        myfile = os.path.join(destdir, nombre_imagen)
        with open(myfile, 'wb+') as (destination):
            for chunk in file.chunks():
                destination.write(chunk)

        return myfile