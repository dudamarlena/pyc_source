# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/gpa-ovp/django-ovp-uploads/ovp_uploads/tests/test_models.py
# Compiled at: 2016-11-29 13:10:10
# Size of source mod 2**32: 542 bytes
from django.test import TestCase
from ovp_uploads.models import UploadedImage
from uuid import UUID

def is_valid_uuid(uuid_to_test, version=4):
    try:
        uuid_obj = UUID(uuid_to_test, version=version)
    except:
        return False

    return str(uuid_obj) == uuid_to_test


class UploadedImageModelTestCase(TestCase):

    def test_str_return_uuid(self):
        """Assert that image model __str__ method returns uuid"""
        img = UploadedImage()
        img.save()
        uuid = img.__str__()
        self.assertTrue(is_valid_uuid(uuid))