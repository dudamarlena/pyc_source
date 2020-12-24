# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/rest_framework/sentry_app.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from jsonschema.exceptions import ValidationError as SchemaValidationError
from rest_framework import serializers
from rest_framework.serializers import Serializer, ValidationError
from django.template.defaultfilters import slugify
from sentry.api.validators.sentry_apps.schema import validate as validate_schema
from sentry.models import ApiScopes, SentryApp
from sentry.models.sentryapp import VALID_EVENT_RESOURCES, REQUIRED_EVENT_PERMISSIONS

class ApiScopesField(serializers.Field):

    def to_internal_value(self, data):
        valid_scopes = ApiScopes()
        if not data:
            return
        for scope in data:
            if scope not in valid_scopes:
                raise ValidationError(('{} not a valid scope').format(scope))

        return data


class EventListField(serializers.Field):

    def to_internal_value(self, data):
        if data is None:
            return
        else:
            if not set(data).issubset(VALID_EVENT_RESOURCES):
                raise ValidationError(('Invalid event subscription: {}').format((', ').join(set(data).difference(VALID_EVENT_RESOURCES))))
            return data


class SchemaField(serializers.Field):

    def to_internal_value(self, data):
        if data is None:
            return
        else:
            if data == '' or data == {}:
                return {}
            try:
                validate_schema(data)
            except SchemaValidationError as e:
                raise ValidationError(e.message)

            return data


class URLField(serializers.URLField):

    def to_internal_value(self, url):
        if url and not url.startswith('http'):
            raise ValidationError('URL must start with http[s]://')
        return url


class SentryAppSerializer(Serializer):
    name = serializers.CharField()
    author = serializers.CharField()
    scopes = ApiScopesField(allow_null=True)
    status = serializers.CharField(required=False, allow_null=True)
    events = EventListField(required=False, allow_null=True)
    schema = SchemaField(required=False, allow_null=True)
    webhookUrl = URLField()
    redirectUrl = URLField(required=False, allow_null=True, allow_blank=True)
    isAlertable = serializers.BooleanField(required=False, default=False)
    overview = serializers.CharField(required=False, allow_null=True)
    verifyInstall = serializers.BooleanField(required=False, default=True)

    def validate_name(self, value):
        if not value:
            return value
        queryset = SentryApp.with_deleted.filter(slug=slugify(value))
        if self.instance:
            queryset = queryset.exclude(id=self.instance.id)
        if queryset.exists():
            raise ValidationError(('Name {} is already taken, please use another.').format(value))
        return value

    def validate(self, attrs):
        if not attrs.get('scopes'):
            return attrs
        for resource in attrs.get('events'):
            needed_scope = REQUIRED_EVENT_PERMISSIONS[resource]
            if needed_scope not in attrs['scopes']:
                raise ValidationError({'events': ('{} webhooks require the {} permission.').format(resource, needed_scope)})

        return attrs