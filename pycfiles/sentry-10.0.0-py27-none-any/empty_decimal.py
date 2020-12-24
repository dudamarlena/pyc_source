# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/fields/empty_decimal.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import serializers
from rest_framework.fields import empty

class EmptyDecimalField(serializers.DecimalField):
    """
    DRF used to translate a blank field as a null decimal, but after 3.x it
    doesn't accept an empty string as a value. We rely on this behaviour in some
    cases, so this restores it.
    """

    def to_internal_value(self, data):
        if data == '':
            return None
        else:
            return super(EmptyDecimalField, self).to_internal_value(data)

    def run_validation(self, data=empty):
        if data == '':
            return None
        else:
            return super(EmptyDecimalField, self).run_validation(data)