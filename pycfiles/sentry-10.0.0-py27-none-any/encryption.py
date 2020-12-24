# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/utils/encryption.py
# Compiled at: 2019-08-16 17:27:46
from __future__ import absolute_import
import six
from base64 import b64encode, b64decode
from collections import OrderedDict
from django.conf import settings
from django.utils.encoding import smart_bytes
MARKER = 'ï»¿'
_marker_length = len(MARKER)

class EncryptionManager(object):

    def __init__(self, schemes=()):
        for key, value in schemes:
            if not isinstance(key, six.string_types):
                raise ValueError(('Encryption scheme type must be a string. Value was: {!r}').format(value))
            if not hasattr(value, 'encrypt') or not hasattr(value, 'decrypt'):
                raise ValueError(("Encryption scheme value must have 'encrypt' and 'decrypt' callables. Value was: {!r}").format(value))

        self.schemes = OrderedDict(schemes)
        if not schemes:
            self.default_scheme = None
        else:
            self.default_scheme = schemes[0][0]
        return

    def encrypt(self, value):
        if self.default_scheme is None:
            return value
        else:
            value = smart_bytes(value)
            scheme = self.schemes[self.default_scheme]
            return ('{}{}${}').format(MARKER, self.default_scheme, b64encode(scheme.encrypt(value)))

    def decrypt(self, value):
        if not self.schemes:
            return value
        if not value.startswith(MARKER):
            return value
        try:
            enc_method, enc_data = value[_marker_length:].split('$', 1)
        except (ValueError, IndexError):
            return value

        if not enc_method:
            return value
        enc_data = b64decode(enc_data)
        try:
            scheme = self.schemes[enc_method]
        except KeyError:
            raise ValueError(('Unknown encryption scheme: {!r}').format(enc_method))

        return scheme.decrypt(enc_data)


default_manager = EncryptionManager(settings.SENTRY_ENCRYPTION_SCHEMES)
encrypt = default_manager.encrypt
decrypt = default_manager.decrypt