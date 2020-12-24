# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tim/unleashed/django-smsgateway/smsgateway/tests/test_utils.py
# Compiled at: 2019-04-19 04:31:39
# Size of source mod 2**32: 1002 bytes
from __future__ import absolute_import
from mock import patch
from django.test import TestCase
from smsgateway.utils import check_cell_phone_number, is_pre_django2

class CheckNumberTest(TestCase):

    def test_international_format(self):
        return check_cell_phone_number('+32478123456') == '32478123456'

    def test_international_format_without_plus(self):
        return check_cell_phone_number('32478123456') == '32478123456'

    def test_national_format(self):
        return check_cell_phone_number('0478123456') == '32478123456'

    def test_national_format_without_leading_zero(self):
        return check_cell_phone_number('478123456') == '32478123456'


class CheckPreDjango2(TestCase):

    def test_check_pre2(self):
        with patch('smsgateway.utils.django_version', return_value='1.11'):
            assert is_pre_django2()

    def test_check_post2(self):
        with patch('smsgateway.utils.django_version', return_value='2.0.2'):
            assert not is_pre_django2()