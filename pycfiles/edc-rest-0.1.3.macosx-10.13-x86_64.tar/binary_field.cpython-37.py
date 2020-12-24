# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/erikvw/.venvs/ambition/lib/python3.7/site-packages/edc_rest/binary_field.py
# Compiled at: 2017-04-08 11:31:14
# Size of source mod 2**32: 984 bytes
from base64 import b64encode, b64decode
from django.utils import six
from django.utils.encoding import force_bytes
import django.utils.translation as _
from rest_framework.fields import Field
from rest_framework.fields import empty

class BinaryField(Field):
    default_error_messages = {'invalid': _('Value must be valid Binary.')}

    def to_internal_value(self, data):
        if isinstance(data, six.text_type):
            return six.memoryview(b64decode(force_bytes(data))).tobytes()
        return data

    def to_representation(self, value):
        if isinstance(value, six.binary_type):
            return b64encode(force_bytes(value)).decode('ascii')
        return value

    def run_validation(self, data=empty):
        is_empty_value, data = self.validate_empty_values(data)
        if is_empty_value:
            return data
        value = self.to_internal_value(data)
        self.run_validators(value)
        return value