# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ioo/Projets/Django-billjobs/django-billjobs/billjobs/tests/tests_model_userprofile.py
# Compiled at: 2017-01-13 19:06:36
# Size of source mod 2**32: 1549 bytes
from django.test import TestCase
from django.db.models import CharField
from billjobs.models import UserProfile
from billjobs.validators import validate_accounting_number

class UserProfileTestCase(TestCase):
    __doc__ = ' Test UserProfile Model '

    def test_user_profile_accounting_number_is_a_string(self):
        """ Test UserProfile accounting_number is a string """
        self.assertTrue(isinstance(UserProfile._meta.get_field('accounting_number'), CharField))

    def test_user_profile_accounting_number_verbose_name(self):
        """ Test UserProfile accounting number verbose name string """
        self.assertEqual(UserProfile._meta.get_field('accounting_number').verbose_name.__str__(), 'Accounting number')

    def test_user_profile_accounting_number_max_len(self):
        """ Test UserProfile accounting number max len is 8 """
        self.assertEqual(UserProfile._meta.get_field('accounting_number').max_length, 8)

    def test_user_profile_accounting_number_is_null(self):
        self.assertTrue(UserProfile._meta.get_field('accounting_number').null)

    def test_user_profile_accounting_number_is_blank(self):
        self.assertTrue(UserProfile._meta.get_field('accounting_number').blank)

    def test_user_profile_accounting_number_call_validators(self):
        self.assertIn(validate_accounting_number, UserProfile._meta.get_field('accounting_number').validators)