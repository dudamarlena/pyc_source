# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/sentry_app_component.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer, register
from sentry.models import SentryAppComponent

@register(SentryAppComponent)
class SentryAppComponentSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        return {'uuid': six.binary_type(obj.uuid), 
           'type': obj.type, 
           'schema': obj.schema, 
           'sentryApp': {'uuid': obj.sentry_app.uuid, 
                         'slug': obj.sentry_app.slug, 
                         'name': obj.sentry_app.name}}