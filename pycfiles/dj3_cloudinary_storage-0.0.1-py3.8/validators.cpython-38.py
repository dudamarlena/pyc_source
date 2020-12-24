# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/cloudinary_storage/validators.py
# Compiled at: 2019-12-17 14:08:28
# Size of source mod 2**32: 566 bytes
import os, magic
from django.core.exceptions import ValidationError
import django.utils.translation as _
from cloudinary_storage import app_settings

def validate_video(value):
    if os.name == 'nt':
        magic_object = magic.Magic(magic_file='magic', mime=True)
        mime = magic_object.from_buffer(value.file.read(1024))
    else:
        mime = magic.from_buffer((value.file.read(1024)), mime=True)
    value.file.seek(0)
    if not mime.startswith('video/'):
        raise ValidationError(_(app_settings.INVALID_VIDEO_ERROR_MESSAGE))