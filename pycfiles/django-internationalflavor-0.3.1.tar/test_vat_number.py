# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_vat_number.py
# Compiled at: 2016-12-31 10:55:29
from __future__ import unicode_literals
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test import TestCase
from internationalflavor.vat_number import VATNumberValidator
from internationalflavor.vat_number.forms import VATNumberFormField
from internationalflavor.vat_number.models import VATNumberField

class VATNumberTestCase(TestCase):
    valid = {b'NL820646660B01': b'NL820646660B01', 
       b'NL82064-6660.B01': b'NL820646660B01', 
       b'DE 114 103 379': b'DE114103379', 
       b'DE114103379': b'DE114103379', 
       b'BE 0203.201.340': b'BE0203201340', 
       b'HU99999999': b'HU99999999', 
       b'IE1234567XX': b'IE1234567XX', 
       b'IE1X23456X': b'IE1X23456X', 
       b'CH-123.456.789 MWST': b'CH123456789', 
       b'CHE-123.456.789 MWST': b'CH123456789', 
       b'CHE-123.456.789 IVA': b'CH123456789', 
       b'RU5505035011': b'RU5505035011', 
       b'RU550501929014': b'RU550501929014'}
    invalid = {b'NL820646661B01': [
                         b'This VAT number does not match the requirements for NL.'], 
       b'BE0203201341': [
                       b'This VAT number does not match the requirements for BE.'], 
       b'DE11410337': [
                     b'This VAT number does not match the requirements for DE.'], 
       b'US123414132': [
                      b'US VAT numbers are not allowed in this field.'], 
       b'123456': [
                 b'This VAT number does not start with a country code, or contains invalid characters.'], 
       b'IE0É12345A': [
                     b'This VAT number does not start with a country code, or contains invalid characters.'], 
       b'RU5505035012': [
                       b'This VAT number does not match the requirements for RU.'], 
       b'RU550501929015': [
                         b'This VAT number does not match the requirements for RU.']}

    def test_validator(self):
        validator = VATNumberValidator()
        for iban, cleaned in self.valid.items():
            if iban == cleaned:
                validator(iban)
            else:
                validator(cleaned)
                self.assertRaises(ValidationError, validator, iban)

        for iban, message in self.invalid.items():
            self.assertRaisesMessage(ValidationError, message[0], validator, iban)

    def test_validator_eu_only(self):
        validator = VATNumberValidator(eu_only=True)
        validator(b'CY12345678A')

    def test_form_field(self):
        self.assertFieldOutput(VATNumberFormField, valid=self.valid, invalid=self.invalid)

    def test_form_field_formatting(self):
        form_field = VATNumberFormField()
        self.assertEqual(form_field.prepare_value(b'DE 114 103 379'), b'DE114103379')
        self.assertEqual(form_field.prepare_value(b'CHE-123.456.789 IVA'), b'CHE123456789')
        self.assertIsNone(form_field.prepare_value(None))
        return

    def test_model_field(self):
        model_field = VATNumberField()
        for input, output in self.valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        for input, errors in self.invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

        return

    include_countries = ('NL', 'BE')
    include_countries_valid = {b'NL820646660B01': b'NL820646660B01', 
       b'BE0203201340': b'BE0203201340'}
    include_countries_invalid = {b'DE114103379': [
                      b'DE VAT numbers are not allowed in this field.']}

    def test_include_countries_form_field(self):
        self.assertFieldOutput(VATNumberFormField, field_kwargs={b'countries': self.include_countries}, valid=self.include_countries_valid, invalid=self.include_countries_invalid)

    def test_include_countries_model_field(self):
        model_field = VATNumberField(countries=self.include_countries)
        for input, output in self.include_countries_valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        for input, errors in self.include_countries_invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

        return

    def test_vies_check_validator(self):
        validator = VATNumberValidator(vies_check=True)
        validator(b'DE114103379')
        try:
            with self.assertRaises(ValidationError) as (context_manager):
                validator(b'DE999999999')
            self.assertEqual(context_manager.exception.messages, [b'This VAT number does not exist.'])
        except AssertionError:
            if validator._wsdl_exception is not None:
                print b'Suds WSDL test skipped due to connection failure'
                self.skipTest(b'Suds WSDL client failed')
            else:
                raise

        return

    def test_vies_check_validator_native(self):
        validator = VATNumberValidator(vies_check=True)
        validator._check_vies = validator._check_vies_native
        validator(b'DE114103379')
        try:
            with self.assertRaises(ValidationError) as (context_manager):
                validator(b'DE999999999')
            self.assertEqual(context_manager.exception.messages, [b'This VAT number does not exist.'])
        except AssertionError:
            if validator._wsdl_exception is not None:
                print b'Native WSDL test skipped due to connection failure'
                self.skipTest(b'Native WSDL client failed')
            else:
                raise

        return