# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jmusilek/github/django-fido/django_fido/models.py
# Compiled at: 2020-02-24 10:26:32
# Size of source mod 2**32: 3525 bytes
"""Models for storing keys."""
from __future__ import unicode_literals
import base64, warnings
from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.deconstruct import deconstructible
from django.utils.encoding import force_text
import django.utils.translation as _
from fido2.ctap2 import AttestationObject, AttestedCredentialData
TRANSPORT_CHOICES = (
 (
  'bt', _('Bluetooth Classic (Bluetooth BR/EDR)')),
 (
  'ble', _('Bluetooth Low Energy (Bluetooth Smart)')),
 (
  'nfc', _('Near-Field Communications')),
 (
  'usb', _('USB HID')),
 (
  'usb-internal', _('Non-removable USB HID')))

@deconstructible
class TransportsValidator(object):
    __doc__ = 'Validator for comma separated transport values.\n\n    @ivar choices: List/tuple of available values.\n    '
    choices = tuple((choice for choice, label in TRANSPORT_CHOICES))
    code = 'invalid_choice'
    message = _('Select a valid choice. %(value)s is not one of the available choices.')

    def __init__(self, choices=None, code=None, message=None):
        """Set custom `choices`, `code` or `message`."""
        warnings.warn('TransportsValidator is deprecated. It is kept only for migrations.', DeprecationWarning)
        if choices is not None:
            self.choices = choices
        if code is not None:
            self.code = code
        if message is not None:
            self.message = message

    def __call__(self, value):
        """Validate the input."""
        for chunk in force_text(value).split(','):
            if chunk not in self.choices:
                raise ValidationError((self.message), code=(self.code), params={'value': chunk})


class Authenticator(models.Model):
    __doc__ = 'Represents a registered FIDO2 authenticator.\n\n    Autheticator fields, see https://www.w3.org/TR/webauthn/#sec-authenticator-data\n     * credential_id_data - base64 encoded credential ID https://www.w3.org/TR/webauthn/#credential-id\n       * This field should be used for readonly purposes only.\n     * attestation_data - base64 encoded attestation object\n     * counter\n    '
    user = models.ForeignKey((settings.AUTH_USER_MODEL), related_name='authenticators', on_delete=(models.CASCADE))
    create_datetime = models.DateTimeField(auto_now_add=True)
    credential_id_data = models.TextField(unique=True)
    attestation_data = models.TextField()
    counter = models.PositiveIntegerField(default=0)
    label = models.TextField(max_length=255, blank=True)

    class Meta:
        unique_together = [
         [
          'user', 'label']]

    @property
    def credential_id(self) -> bytes:
        """Return raw credential ID."""
        return base64.b64decode(self.credential_id_data)

    @property
    def credential(self) -> AttestedCredentialData:
        """Return AttestedCredentialData object."""
        return self.attestation.auth_data.credential_data

    @property
    def attestation(self) -> AttestationObject:
        """Return AttestationObject object."""
        return AttestationObject(base64.b64decode(self.attestation_data))

    @attestation.setter
    def attestation(self, value: AttestationObject):
        self.attestation_data = base64.b64encode(value).decode('utf-8')
        self.credential_id_data = base64.b64encode(value.auth_data.credential_data.credential_id).decode('utf-8')