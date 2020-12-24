# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/softwarefabrica/django/utils/IPv4MaskedAddressField.py
# Compiled at: 2010-02-19 10:47:14
"""
IPv4MaskedAddressField

A Django IPv4 model field, which supports all types of 32-bit IPv4 addresses
with an optional network mask.
It uses the ``ipaddr`` library, so all its formats are supported, namely:

- '192.168.1.1/32'
- '192.168.1.1/255.255.255.255'
- '192.168.1.1/0.0.0.255'
- '192.168.1.1'

(the above addresses are all functionally the same in IPv4).
Failing to provide a subnetmask will create an object with a mask of /32.
A netmask of '255.255.255.255' is assumed to be /32 and
'0.0.0.0' is assumed to be /0, even though other netmasks can be
expressed both as host- and net-masks.  (255.0.0.0 == 0.255.255.255)
"""
from django.db import models
from django import forms
import django.core.exceptions
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import smart_unicode, smart_str
from django.forms.util import ErrorList, ValidationError
import ipaddr
EMPTY_IPV4_ADDRESS = '0.0.0.0'

class WrappedIPv4(ipaddr.IPv4):
    """
    A wrapped ipaddr.IPv4 class which supports comparison operations
    with other types (namely empty strings, used by Django admin).
    """
    __module__ = __name__

    def __eq__(self, other):
        if other is None:
            return False
        if not isinstance(other, object):
            return False
        if not isinstance(other, ipaddr.IPv4):
            return False
        return super(WrappedIPv4, self).__eq__(other)


class IPv4MaskedAddressFormField(forms.CharField):
    __module__ = __name__
    default_error_messages = {'required': _('This field is required.'), 'invalid': _('Enter a valid IPv4 (masked) address.')}

    def clean(self, value):
        """
        Validates that the input is a valid IPv4 address (with or without a mask).
        Returns a Unicode object.
        """
        value = super(IPv4MaskedAddressFormField, self).clean(value)
        if value == '':
            return value
        if value is None:
            return value
        try:
            ip_value = WrappedIPv4(value)
        except:
            raise ValidationError(self.error_messages['invalid'])

        return value


class IPv4MaskedAddressField(models.Field):
    __module__ = __name__
    __metaclass__ = models.SubfieldBase
    empty_strings_allowed = False

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 48
        super(IPv4MaskedAddressField, self).__init__(*args, **kwargs)

    def get_internal_type(self):
        return 'CharField'

    def to_python(self, value):
        if value is None:
            return value
        if value == '':
            return value
        return WrappedIPv4(value)

    def get_db_prep_value(self, value):
        if value is not None:
            return smart_unicode(str(value))
        return super(IPv4MaskedAddressField, self).get_db_prep_value(value)

    def get_db_prep_lookup(self, lookup_type, value):
        if lookup_type == 'exact':
            return [
             self.get_db_prep_value(value)]
        elif lookup_type == 'in':
            return [ self.get_db_prep_value(v) for v in value ]
        else:
            raise TypeError('Lookup type %r not supported.' % lookup_type)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)

    def formfield(self, **kwargs):
        defaults = {'max_length': self.max_length, 'form_class': IPv4MaskedAddressFormField}
        defaults.update(kwargs)
        return super(IPv4MaskedAddressField, self).formfield(**defaults)


try:
    import django
    from django.conf import settings
    from south.modelsinspector import add_introspection_rules
    rules = [
     (
      (
       IPv4MaskedAddressField,), [], {'max_length': ['max_length', {'default': 48}]})]
    add_introspection_rules(rules, ['^softwarefabrica\\.django\\.utils'])
except ImportError:
    pass