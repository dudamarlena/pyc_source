# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dana/.virtualenvs/django-cryptographic-fields/lib/python2.7/site-packages/cryptographic_fields/fields.py
# Compiled at: 2016-09-27 19:52:33
from __future__ import unicode_literals
import sys, django.db, django.db.models
from django.utils.six import PY2, string_types
from django.utils.functional import cached_property
from django.core import validators
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
import cryptography.fernet

def get_crypter():
    configured_keys = getattr(settings, b'FIELD_ENCRYPTION_KEY')
    if configured_keys is None:
        raise ImproperlyConfigured(b'FIELD_ENCRYPTION_KEY must be defined in settings')
    try:
        if isinstance(configured_keys, (tuple, list)):
            keys = [ cryptography.fernet.Fernet(str(k)) for k in configured_keys ]
        else:
            keys = [
             cryptography.fernet.Fernet(str(configured_keys))]
    except Exception as e:
        raise ImproperlyConfigured((b'FIELD_ENCRYPTION_KEY defined incorrectly: {}').format(str(e))), None, sys.exc_info()[2]

    if len(keys) == 0:
        raise ImproperlyConfigured(b'No keys defined in setting FIELD_ENCRYPTION_KEY')
    return cryptography.fernet.MultiFernet(keys)


CRYPTER = get_crypter()

def encrypt_str(s):
    return CRYPTER.encrypt(s.encode(b'utf-8'))


def decrypt_str(t):
    return CRYPTER.decrypt(t.encode(b'utf-8')).decode(b'utf-8')


def calc_encrypted_length(n):
    return len(encrypt_str(b'a' * n))


class EncryptedMixin(object):

    def to_python(self, value):
        if value is None:
            return value
        else:
            if isinstance(value, (bytes, string_types[0])):
                if isinstance(value, bytes):
                    value = value.decode(b'utf-8')
                try:
                    value = decrypt_str(value)
                except cryptography.fernet.InvalidToken:
                    pass

            return super(EncryptedMixin, self).to_python(value)

    def from_db_value(self, value, expression, connection, context):
        return self.to_python(value)

    def get_db_prep_save(self, value, connection):
        value = super(EncryptedMixin, self).get_db_prep_save(value, connection)
        if value is None:
            return value
        else:
            if PY2:
                return encrypt_str(unicode(value))
            return encrypt_str(str(value)).decode(b'utf-8')

    def get_internal_type(self):
        return b'TextField'

    def deconstruct(self):
        name, path, args, kwargs = super(EncryptedMixin, self).deconstruct()
        if b'max_length' in kwargs:
            del kwargs[b'max_length']
        return (name, path, args, kwargs)


class EncryptedCharField(EncryptedMixin, django.db.models.CharField):
    pass


class EncryptedTextField(EncryptedMixin, django.db.models.TextField):
    pass


class EncryptedDateField(EncryptedMixin, django.db.models.DateField):
    pass


class EncryptedDateTimeField(EncryptedMixin, django.db.models.DateTimeField):
    pass


class EncryptedEmailField(EncryptedMixin, django.db.models.EmailField):
    pass


class EncryptedBooleanField(EncryptedMixin, django.db.models.BooleanField):

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value
        else:
            if value is True:
                value = b'1'
            else:
                if value is False:
                    value = b'0'
                if PY2:
                    return encrypt_str(unicode(value))
            return encrypt_str(str(value)).decode(b'utf-8')


class EncryptedNullBooleanField(EncryptedMixin, django.db.models.NullBooleanField):

    def get_db_prep_save(self, value, connection):
        if value is None:
            return value
        else:
            if value is True:
                value = b'1'
            else:
                if value is False:
                    value = b'0'
                if PY2:
                    return encrypt_str(unicode(value))
            return encrypt_str(str(value)).decode(b'utf-8')


class EncryptedNumberMixin(EncryptedMixin):
    max_length = 20

    @cached_property
    def validators(self):
        range_validators = []
        internal_type = self.__class__.__name__[9:]
        min_value, max_value = django.db.connection.ops.integer_field_range(internal_type)
        if min_value is not None:
            range_validators.append(validators.MinValueValidator(min_value))
        if max_value is not None:
            range_validators.append(validators.MaxValueValidator(max_value))
        return super(EncryptedNumberMixin, self).validators + range_validators


class EncryptedIntegerField(EncryptedNumberMixin, django.db.models.IntegerField):
    description = b'An IntegerField that is encrypted before inserting into a database using the python cryptography library'


class EncryptedPositiveIntegerField(EncryptedNumberMixin, django.db.models.PositiveIntegerField):
    pass


class EncryptedSmallIntegerField(EncryptedNumberMixin, django.db.models.SmallIntegerField):
    pass


class EncryptedPositiveSmallIntegerField(EncryptedNumberMixin, django.db.models.PositiveSmallIntegerField):
    pass


class EncryptedBigIntegerField(EncryptedNumberMixin, django.db.models.BigIntegerField):
    pass