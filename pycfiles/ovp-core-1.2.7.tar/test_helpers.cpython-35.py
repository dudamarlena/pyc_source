# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/ovp/suzano-ovp/django-ovp-core/ovp_core/tests/test_helpers.py
# Compiled at: 2017-06-19 15:08:31
# Size of source mod 2**32: 662 bytes
from django.test import TestCase
from django.test.utils import override_settings
from ovp_core.helpers import get_address_model
from ovp_core.models import SimpleAddress, GoogleAddress

class GetAddressModelHelperTestCase(TestCase):

    def test_default_model(self):
        """Assert GoogleAddress is the default address model"""
        model = get_address_model()
        self.assertTrue(model == GoogleAddress)

    @override_settings(OVP_CORE={'ADDRESS_MODEL': 'ovp_core.models.SimpleAddress'})
    def test_setting(self):
        """Assert it's possible to modify the model by changing the setting"""
        model = get_address_model()
        self.assertTrue(model == SimpleAddress)