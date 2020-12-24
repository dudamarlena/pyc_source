# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ralph/Development/django-internationalflavor/tests/test_iban.py
# Compiled at: 2016-08-20 07:59:21
from __future__ import unicode_literals
from django.core.exceptions import ValidationError, ImproperlyConfigured
from django.test import TestCase
from internationalflavor.iban import IBANValidator, IBANFormField, IBANField, BICValidator, BICFormField, BICField

class IBANTestCase(TestCase):
    valid = {b'GB82WeST12345698765432': b'GB82WEST12345698765432', 
       b'GB82 WEST 1234 5698 7654 32': b'GB82WEST12345698765432', 
       b'GR1601101250000000012300695': b'GR1601101250000000012300695', 
       b'GR16-0110-1250-0000-0001-2300-695': b'GR1601101250000000012300695', 
       b'GB29NWBK60161331926819': b'GB29NWBK60161331926819', 
       b'GB29N-WB K6016-13319-26819': b'GB29NWBK60161331926819', 
       b'SA0380000000608010167519': b'SA0380000000608010167519', 
       b'SA0380 0 0000 06 0 8 0 1 0 1 6 7 519 ': b'SA0380000000608010167519', 
       b'CH9300762011623852957': b'CH9300762011623852957', 
       b'IL620108000000099999999': b'IL620108000000099999999', 
       b'EE982200221111099080': b'EE982200221111099080', 
       b'NL02ABNA0123456789': b'NL02ABNA0123456789', 
       b'Nl02aBNa0123456789': b'NL02ABNA0123456789', 
       b'NL02 ABNA 0123 4567 89': b'NL02ABNA0123456789', 
       b'NL02-ABNA-0123-4567-89': b'NL02ABNA0123456789', 
       b'NL91ABNA0417164300': b'NL91ABNA0417164300', 
       b'NL91 ABNA 0417 1643 00': b'NL91ABNA0417164300', 
       b'NL91-ABNA-0417-1643-00': b'NL91ABNA0417164300', 
       b'MU17BOMM0101101030300200000MUR': b'MU17BOMM0101101030300200000MUR', 
       b'MU17 BOMM 0101 1010 3030 0200 000M UR': b'MU17BOMM0101101030300200000MUR', 
       b'MU 17BO MM01011010 3030-02 000-00M UR': b'MU17BOMM0101101030300200000MUR', 
       b'BE68539007547034': b'BE68539007547034', 
       b'BE68 5390 0754 7034': b'BE68539007547034', 
       b'BE-685390075470 34': b'BE68539007547034', 
       b'LC55HEMM000100010012001200023015': b'LC55HEMM000100010012001200023015', 
       b'TR330006100519786457841326': b'TR330006100519786457841326', 
       b'KW81CBKU0000000000001234560101': b'KW81CBKU0000000000001234560101', 
       b'ST68000100010051845310112': b'ST68000100010051845310112', 
       b'MD24AG000225100013104168': b'MD24AG000225100013104168', 
       b'UA213996220000026007233566001': b'UA213996220000026007233566001', 
       b'JO94CBJO0010000000000131000302': b'JO94CBJO0010000000000131000302', 
       b'KZ86125KZT5004100100': b'KZ86125KZT5004100100', 
       b'PL61109010140000071219812874': b'PL61109010140000071219812874', 
       b'SC18SSCB11010000000000001497USD': b'SC18SSCB11010000000000001497USD'}
    invalid = {b'GB82WEST1234569876543': [
                                b'This IBAN does not match the requirements for GB.'], 
       b'CA34CIBC123425345': [
                            b'CA IBANs are not allowed in this field.'], 
       b'GB29ÉWBK60161331926819': [
                                 b'This IBAN does not start with a country code and checksum, or contains invalid characters.'], 
       b'123456': [
                 b'This IBAN does not start with a country code and checksum, or contains invalid characters.',
                 b'Ensure this value has at least 16 characters (it has 6).'], 
       b'SA0380000000608019167519': [
                                   b'This IBAN does not have a valid checksum.'], 
       b'EE012200221111099080': [
                               b'This IBAN does not have a valid checksum.'], 
       b'NL91ABNB0417164300': [
                             b'This IBAN does not have a valid checksum.'], 
       b'MU17BOMM0101101030300200000MUR12345': [
                                              b'This IBAN does not match the requirements for MU.',
                                              b'Ensure this value has at most 34 characters (it has 35).'], 
       b'EG1100006001880800100014553': [
                                      b'EG IBANs are not allowed in this field.']}

    def test_validator(self):
        validator = IBANValidator()
        for iban, cleaned in self.valid.items():
            if iban == cleaned:
                validator(iban)
            else:
                validator(cleaned)
                self.assertRaises(ValidationError, validator, iban)

        for iban, message in self.invalid.items():
            self.assertRaisesMessage(ValidationError, message[0], validator, iban)

        self.assertRaisesMessage(ValidationError, b'This IBAN does not start with a country code and checksum, or contains invalid characters.', validator, b'NL02 ABNA 0123 4567 89')

    def test_form_field(self):
        self.assertFieldOutput(IBANFormField, valid=self.valid, invalid=self.invalid)

    def test_form_field_formatting(self):
        form_field = IBANFormField()
        self.assertEqual(form_field.prepare_value(b'NL02ABNA0123456789'), b'NL02 ABNA 0123 4567 89')
        self.assertEqual(form_field.prepare_value(b'NL02 ABNA 0123 4567 89'), b'NL02 ABNA 0123 4567 89')
        self.assertIsNone(form_field.prepare_value(None))
        return

    def test_model_field(self):
        iban_model_field = IBANField()
        for input, output in self.valid.items():
            self.assertEqual(iban_model_field.clean(input, None), output)

        for input, errors in self.invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                iban_model_field.clean(input, None)
            if input == b'123456':
                self.assertEqual(context_manager.exception.messages, errors[0:1])
            else:
                self.assertEqual(context_manager.exception.messages, errors[::-1])

        return

    def test_use_nordea_extensions(self):
        validator = IBANValidator(accept_nordea_extensions=True)
        validator(b'EG1100006001880800100014553')

    include_countries = ('NL', 'BE', 'LU')
    include_countries_valid = {b'NL02ABNA0123456789': b'NL02ABNA0123456789', 
       b'BE68539007547034': b'BE68539007547034', 
       b'LU280019400644750000': b'LU280019400644750000'}
    include_countries_invalid = {b'GB82WEST12345698765432': [
                                 b'GB IBANs are not allowed in this field.']}

    def test_include_countries_form_field(self):
        self.assertFieldOutput(IBANFormField, field_kwargs={b'countries': self.include_countries}, valid=self.include_countries_valid, invalid=self.include_countries_invalid)

    def test_include_countries_model_field(self):
        iban_model_field = IBANField(countries=self.include_countries)
        for input, output in self.include_countries_valid.items():
            self.assertEqual(iban_model_field.clean(input, None), output)

        for input, errors in self.include_countries_invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                iban_model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

        return


class BICTestCase(TestCase):
    valid = {b'deutdeff': b'DEUTDEFF', 
       b'DEUTDEFF': b'DEUTDEFF', 
       b'NEDSZAJJxxx': b'NEDSZAJJXXX', 
       b'NEDSZAJJXXX': b'NEDSZAJJXXX', 
       b'DABADKKK': b'DABADKKK', 
       b'daBadKkK': b'DABADKKK', 
       b'UNCRIT2B912': b'UNCRIT2B912', 
       b'DSBACNBXSHA': b'DSBACNBXSHA'}
    invalid = {b'NEDSZAJJXX': [
                     b'This Bank Identifier Code (BIC) is invalid.'], 
       b'CIBCJJH2': [
                   b'JJ is not a valid country code.'], 
       b'DÉUTDEFF': [
                   b'This Bank Identifier Code (BIC) is invalid.']}

    def test_validator(self):
        validator = BICValidator()
        for bic, cleaned in self.valid.items():
            if bic == cleaned:
                validator(bic)
            else:
                validator(cleaned)
                self.assertRaises(ValidationError, validator, bic)

        for bic, message in self.invalid.items():
            self.assertRaisesMessage(ValidationError, message[0], validator, bic)

        self.assertRaisesMessage(ValidationError, b'This Bank Identifier Code (BIC) is invalid.', validator, b'deutdeff')

    def test_form_field(self):
        self.assertFieldOutput(BICFormField, valid=self.valid, invalid=self.invalid)

    def test_form_field_formatting(self):
        form_field = BICFormField()
        self.assertEqual(form_field.prepare_value(b'deutdeff'), b'DEUTDEFF')
        self.assertIsNone(form_field.prepare_value(None))
        self.assertEqual(form_field.to_python(None), b'')
        return

    def test_model_field(self):
        model_field = BICField()
        for input, output in self.valid.items():
            self.assertEqual(model_field.clean(input, None), output)

        for input, errors in self.invalid.items():
            with self.assertRaises(ValidationError) as (context_manager):
                model_field.clean(input, None)
            self.assertEqual(context_manager.exception.messages, errors[::-1])

        return