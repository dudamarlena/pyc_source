# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-uploads/ovp_uploads/helpers.py
# Compiled at: 2017-06-13 10:27:08
# Size of source mod 2**32: 736 bytes
import os
from io import BytesIO
from tempfile import TemporaryFile
from django.core.files import uploadedfile
from django.core.files.base import ContentFile
from PIL import Image

def perform_image_crop(image_obj, crop_rect=None):
    img_ext = os.path.splitext(image_obj.name)[1][1:].upper()
    img_ext = 'JPEG' if img_ext == 'JPG' else img_ext
    if crop_rect is None:
        return image_obj
    image = BytesIO(image_obj.read())
    base_image = Image.open(image)
    tmp_img, tmp_file = base_image.crop(crop_rect), BytesIO()
    tmp_img.save(tmp_file, format=img_ext)
    tmp_file = ContentFile(tmp_file.getvalue())
    return uploadedfile.InMemoryUploadedFile(tmp_file, None, image_obj.name, image_obj.content_type, tmp_file.tell, None)