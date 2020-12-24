# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/rest_framework/sentry_app_installation.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import serializers
from rest_framework.serializers import Serializer, ValidationError
from sentry.constants import SentryAppInstallationStatus

class SentryAppInstallationSerializer(Serializer):
    status = serializers.CharField()

    def validate_status(self, new_status):
        if new_status != SentryAppInstallationStatus.INSTALLED_STR:
            raise ValidationError(("Invalid value '{}' for status. Valid values: '{}'").format(new_status, SentryAppInstallationStatus.INSTALLED_STR))
        return new_status