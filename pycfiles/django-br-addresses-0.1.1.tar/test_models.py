# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/lucas/workspace-python/django-br-addresses/tests/test_models.py
# Compiled at: 2014-11-15 16:00:31
from __future__ import unicode_literals
import unittest2 as unittest
from django.test import TestCase
from model_mommy import mommy
from django_br_addresses.models import City, Address

class CityTest(TestCase):
    """
    Class to test a model City
    """

    def setUp(self):
        """
        Setup a test class
        """
        self.city = mommy.make(City)

    def test_city_create_instance(self):
        """
        Test if instance of the model City was created
        """
        self.assertIsInstance(self.city, City)

    def test_return_unicode_method(self):
        """
        Test the return of method unicode in model City
        """
        self.assertEqual((b'{} - {}').format(self.city.state, self.city.name), self.city.__unicode__())


class AddressTest(TestCase):
    """
    Class to test a model Address
    """

    def setUp(self):
        """
        Setup a test class
        """
        self.address = mommy.make(Address)

    def test_addresses_create_instance(self):
        """
        Test if instance of the model Address was created
        """
        self.assertIsInstance(self.address, Address)

    def test_return_unicode_method(self):
        """
        Test the return of method unicode in model Address
        """
        self.assertEqual((b'{}, {} - {} , {} , {}').format(self.address.city.state, self.address.city.name, self.address.street, self.address.number, self.address.neighborhood), self.address.__unicode__())