# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Tyrdall/projects/bitmazk-contact-form/src/contact_form/tests/forms_tests.py
# Compiled at: 2016-04-11 02:47:17
"""Tests for the forms of the `contact_form` app."""
from django.core import mail
from django.test import TestCase
from mixer.backend.django import mixer
from ..forms import AntiSpamContactForm

class AntiSpamContactFormTestCase(TestCase):
    """Test for the ``AntiSpamContactForm`` form class."""
    longMessage = True

    def test_form(self):
        category = mixer.blend('contact_form.ContactFormCategoryTranslation', language_code='en').master
        data = {'email': 'test@example.com', 
           'message': 'Foo', 
           'url': 'http://www.example.com', 
           'category': category.pk}
        form = AntiSpamContactForm(data=data)
        self.assertFalse(form.errors)
        form.save()
        self.assertEqual(len(mail.outbox), 0)
        data.update({'url': ''})
        form = AntiSpamContactForm(data=data)
        self.assertTrue(form.is_valid())
        form.save()
        self.assertEqual(len(mail.outbox), 1)