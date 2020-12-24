# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/rest_framework/origin.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import serializers
from sentry.utils.http import parse_uri_match

class OriginField(serializers.CharField):
    WHITELIST_ORIGINS = '*'

    def to_internal_value(self, data):
        rv = super(OriginField, self).to_internal_value(data)
        if not rv:
            return
        if not self.is_valid_origin(rv):
            raise serializers.ValidationError('%s is not an acceptable domain' % rv)
        return rv

    def is_valid_origin(self, value):
        if value in self.WHITELIST_ORIGINS:
            return True
        bits = parse_uri_match(value)
        if ':' in bits.domain:
            return False
        return True