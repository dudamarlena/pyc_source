# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dmitry/dev/ImageProj/media_field/tests/test_forms.py
# Compiled at: 2015-02-14 08:25:48
from django.test import TestCase
from ..forms import MediaField, MediaFieldWidget

class TestMediaFormField(TestCase):

    def test_media_field_inherits_from_image_field(self):
        """MediaField should inherit from standard ImageField.
        """
        from django.forms import ImageField
        self.assertIn(ImageField, MediaField.__bases__)

    def test_media_field_should_have_correct_widget(self):
        """MediaField of a form should have MediaFieldWidget.
        """
        self.assertEqual(MediaField.widget, MediaFieldWidget)


class TestMediaFieldWidget(TestCase):

    def test_widget_renders_correct_string(self):
        """test_widget_renders_correct_string.
        """
        widget = MediaFieldWidget()
        self.assertEqual(widget.render('hello', 'world'), 'hello world!!!')