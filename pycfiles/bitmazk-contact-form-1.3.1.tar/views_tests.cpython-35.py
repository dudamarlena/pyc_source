# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/tests/views_tests.py
# Compiled at: 2016-04-11 02:48:48
# Size of source mod 2**32: 945 bytes
"""Tests for the views of the `contact_form` app."""
from django.core import mail
from django.test import TestCase
from django_libs.tests.mixins import ViewRequestFactoryTestMixin
from mixer.backend.django import mixer
from .. import views

class ContactFormViewTestCase(ViewRequestFactoryTestMixin, TestCase):
    __doc__ = 'Test for the ``ContactFormView`` view.'
    view_class = views.ContactFormView

    def test_view(self):
        self.is_callable()
        category = mixer.blend('contact_form.ContactFormCategoryTranslation', language_code='en').master
        data = {'email': 'test@example.com', 
         'message': 'Foo', 
         'category': category.pk}
        self.is_postable(data=data, ajax=True)
        self.assertEqual(len(mail.outbox), 1)