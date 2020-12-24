# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/arroyo/projects/cpmd/server/api/django-google-address/google_address/tests/test_models.py
# Compiled at: 2017-05-03 17:12:32
# Size of source mod 2**32: 2936 bytes
from django.test import TestCase
from django.test.utils import override_settings
from google_address.models import Address
from google_address.models import AddressComponent
from google_address.models import AddressComponentType

def remove_component(address, types):
    for component in address.address_components.all():
        for type in component.types.all():
            if type.name in types:
                component.delete()

    return address


@override_settings(GOOGLE_ADDRESS={'API_LANGUAGE': 'en_US'})
class AddressModelTestCase(TestCase):

    def test_api_call(self):
        """Assert Address calls google API and get address"""
        a = Address(raw='Rua Teçaindá, 81, SP', raw2='Casa')
        a.save()
        a = Address.objects.get(pk=a.pk)
        self.assertTrue(a.raw == 'Rua Teçaindá, 81, SP')
        self.assertTrue(a.raw2 == 'Casa')
        self.assertTrue(a.address_line == 'Rua Teçaindá, 81, Pinheiros, São Paulo, SP, Brazil')
        self.assertTrue(a.__str__() == 'Rua Teçaindá, 81, Pinheiros, São Paulo, SP, Brazil')
        self.assertTrue(a.lat)
        self.assertTrue(a.lng)
        a.raw = 'Rua Capote Valente, 701, SP'
        a.save()
        a = Address.objects.get(pk=a.pk)
        self.assertTrue(a.raw == 'Rua Capote Valente, 701, SP')
        self.assertTrue(a.raw2 == 'Casa')
        self.assertTrue(a.address_line == 'Rua Capote Valente, 701, Pinheiros, São Paulo, SP, Brazil')
        self.assertTrue(a.__str__() == 'Rua Capote Valente, 701, Pinheiros, São Paulo, SP, Brazil')
        self.assertTrue(a.lat)
        self.assertTrue(a.lng)
        a.address_line = None
        self.assertTrue(a.__str__() == '')

    def test_locality(self):
        """Assert AddressModel.get_city_state preference order is locality, administrative_area_2"""
        a = Address(raw='Chicago')
        a.save()
        self.assertTrue('Chicago' in a.get_city_state())
        a = remove_component(a, ['locality'])
        self.assertTrue('Cook' in a.get_city_state())

    def test_no_country(self):
        """Assert AddressModel.get_country_code returns None instead of rasing AttributeError if no country exists"""
        a = Address(raw='Chicago')
        a.save()
        AddressComponent.objects.all().delete()
        self.assertTrue(a.get_country_code() == None)

    def test_signal_returns_in_case_of_no_result(self):
        """Assert AddressModel.get_country_code returns None instead of rasing AttributeError if no country exists"""
        a = Address(raw='abcdefghijklmnopqrstuvwxyz')
        a.save()
        self.assertTrue(a.address_line == None)


class AddressComponentTypeModelTestCase(TestCase):

    def test_str_call(self):
        """Assert AddressComponentType __str__ returns name"""
        a = AddressComponentType(name='xyz')
        a.save()
        self.assertTrue(a.__str__() == 'xyz')


class AddressComponentModelTestCase(TestCase):

    def test_str_call(self):
        """Assert AddressComponent __str__ returns long name"""
        a = AddressComponent(short_name='short', long_name='long')
        a.save()
        self.assertTrue(a.__str__() == 'long')