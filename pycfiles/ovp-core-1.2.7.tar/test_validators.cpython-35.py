# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/tests/test_validators.py
# Compiled at: 2017-02-22 17:56:49
# Size of source mod 2**32: 317 bytes
from django.test import TestCase
from ovp_core import validators

class TestAddressValidator(TestCase):

    def test_validation_functionn(self):
        """Assert that address_validate doesn't raise exception on valid address"""
        validators.address_validate({'typed_address': 'R. Abc'})