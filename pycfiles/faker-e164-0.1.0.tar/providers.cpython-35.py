# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/adam/Projects/faker_e164/faker_e164/providers.py
# Compiled at: 2017-04-30 21:05:16
# Size of source mod 2**32: 2363 bytes
"""
Provider for faker to generate E164 compatible phone numbers
"""
import phonenumbers
from faker.providers import BaseProvider

class E164Provider(BaseProvider):
    __doc__ = '\n    Provider to generate random yet possible phone numbers for various countries\n    \n    >>> from faker import Faker\n    >>> from faker_e164 import E164Provider\n    >>> fake = Faker()\n    >>> fake.add_provider(E164Provider)\n    '

    def _e164_phone_number(self, country, is_valid=True, is_possible=True):
        """
        Generate an e164 phone number
        """
        phone_number = self.numerify('%###########')
        while not isinstance(phone_number, phonenumbers.phonenumber.PhoneNumber):
            try:
                phone_number = phonenumbers.parse(phone_number, country)
            except phonenumbers.phonenumberutil.NumberParseException:
                phone_number = self.numerify('%###########')
                continue

            if is_valid:
                if not phonenumbers.is_valid_number(phone_number):
                    phone_number = self.numerify('%###########')
            elif is_possible:
                if not phonenumbers.is_possible_number(phone_number):
                    phone_number = self.numerify('%###########')
                continue

        return phone_number

    def invalid_e164_phone_number(self, country=None):
        """
        Return an invalid e164 phone number
        """
        countries = [
         'AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=False, is_possible=True)
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)

    def valid_e164_phone_number(self, country=None):
        """
        Return an invalid e164 phone number
        """
        countries = [
         'AU', 'US', 'GB', 'NZ']
        country = country or self.random_element(countries)
        phone_number = self._e164_phone_number(country, is_valid=True, is_possible=True)
        return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)