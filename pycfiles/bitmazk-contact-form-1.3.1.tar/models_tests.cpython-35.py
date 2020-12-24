# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/tests/models_tests.py
# Compiled at: 2016-04-11 01:51:28
# Size of source mod 2**32: 449 bytes
"""Tests for the models of the ``contact_form`` app."""
from django.test import TestCase
from mixer.backend.django import mixer

class ContactFormCategoryTestCase(TestCase):
    __doc__ = 'Tests for the ``ContactFormCategory`` model.'
    longMessage = True

    def test_model(self):
        obj = mixer.blend('contact_form.ContactFormCategory')
        self.assertTrue(str(obj), msg='Should be able to instantiate and save the model.')