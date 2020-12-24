# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dmitry/dev/ImageProj/media_field/tests/test_field.py
# Compiled at: 2015-02-14 07:35:19
from django.test import TestCase
from .. import models
from .. import forms

class TestMediaModelField(TestCase):

    def test_media_field_inherits_from_image_field(self):
        """MediaField should inherit from standard ImageField.
        """
        from django.db.models import ImageField
        self.assertIn(ImageField, models.MediaField.__bases__)

    def test_media_field_referres_the_correct_form_field(self):
        media_field = models.MediaField()
        print media_field.formfield()