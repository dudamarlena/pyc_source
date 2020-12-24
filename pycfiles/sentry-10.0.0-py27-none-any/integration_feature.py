# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/integration_feature.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from sentry.api.serializers import Serializer, register
from sentry.models import IntegrationFeature

@register(IntegrationFeature)
class IntegrationFeatureSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        return {'description': obj.description.strip(), 
           'featureGate': obj.feature_str()}