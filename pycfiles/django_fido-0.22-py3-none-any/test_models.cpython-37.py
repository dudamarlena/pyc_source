# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/tests/test_models.py
# Compiled at: 2019-09-25 06:48:47
# Size of source mod 2**32: 3402 bytes
"""Test `django_fido.models`."""
from __future__ import unicode_literals
import base64
from django.core.exceptions import ValidationError
from django.test import SimpleTestCase
from fido2.cose import ES256
from fido2.ctap2 import AttestationObject, AuthenticatorData
from django_fido.models import Authenticator, TransportsValidator
from .data import ATTESTATION_OBJECT, CREDENTIAL_ID

class TestTransportsValidator(SimpleTestCase):
    __doc__ = 'Test `TransportsValidator`.'
    valid_values = ('bt', 'ble', 'nfc', 'usb', 'usb-internal', 'bt,ble', 'nfc,usb',
                    'bt,ble,nfc,usb,usb-internal')

    def test_valid(self):
        validator = TransportsValidator()
        for value in self.valid_values:
            validator(value)

    invalid_values = (('', ''), (' ', ' '), (',', ''), ('junk', 'junk'), ('bt, ble', ' ble'),
                      ('nfc ,usb', 'nfc '))

    def test_invalid(self):
        validator = TransportsValidator()
        for value, invalid_chunk in self.invalid_values:
            with self.assertRaisesMessage(ValidationError, 'Select a valid choice.') as (catcher):
                validator(value)
            self.assertEqual(catcher.exception.code, 'invalid_choice')
            self.assertEqual(catcher.exception.params, {'value': invalid_chunk})

    def test_custom_choices(self):
        validator = TransportsValidator(choices=['foo', 'bar'])
        validator('foo,bar')
        self.assertRaisesMessage(ValidationError, 'Select a valid choice.', validator, 'usb')

    def test_custom_code(self):
        validator = TransportsValidator(code='smeghead')
        with self.assertRaisesMessage(ValidationError, 'Select a valid choice.') as (catcher):
            validator('rimmer')
        self.assertEqual(catcher.exception.code, 'smeghead')

    def test_custom_message(self):
        validator = TransportsValidator(message="You're a smeghead.")
        self.assertRaisesMessage(ValidationError, "You're a smeghead.", validator, 'rimmer')


class TestAuthenticator(SimpleTestCase):
    __doc__ = 'Test `Authenticator` model.'

    def test_credential_id_getter(self):
        authenticator = Authenticator(credential_id_data='Q1JFREVOVElBTF9JRA==')
        self.assertEqual(authenticator.credential_id, b'CREDENTIAL_ID')

    def test_credential_getter(self):
        authenticator = Authenticator(attestation_data=ATTESTATION_OBJECT)
        self.assertEqual(authenticator.credential.aaguid, b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00')
        self.assertEqual(authenticator.credential.credential_id, base64.b64decode(CREDENTIAL_ID))
        self.assertIsInstance(authenticator.credential.public_key, ES256)

    def test_attestation_getter(self):
        authenticator = Authenticator(attestation_data=ATTESTATION_OBJECT)
        self.assertEqual(authenticator.attestation.fmt, 'fido-u2f')
        self.assertIsInstance(authenticator.attestation.auth_data, AuthenticatorData)

    def test_attestation_setter(self):
        authenticator = Authenticator()
        authenticator.attestation = AttestationObject(base64.b64decode(ATTESTATION_OBJECT))
        self.assertEqual(authenticator.attestation_data, ATTESTATION_OBJECT)
        self.assertEqual(authenticator.credential_id_data, CREDENTIAL_ID)