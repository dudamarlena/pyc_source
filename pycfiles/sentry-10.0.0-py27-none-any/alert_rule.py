# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/alert_rule.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer, register
from sentry.incidents.models import AlertRule

@register(AlertRule)
class AlertRuleSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        return {'id': six.text_type(obj.id), 
           'name': obj.name, 
           'projectId': six.text_type(obj.project_id), 
           'status': obj.status, 
           'thresholdType': obj.threshold_type, 
           'dataset': obj.dataset, 
           'query': obj.query, 
           'aggregations': [ agg for agg in obj.aggregations ], 'timeWindow': obj.time_window, 
           'resolution': obj.resolution, 
           'alertThreshold': obj.alert_threshold, 
           'resolveThreshold': obj.resolve_threshold, 
           'thresholdPeriod': obj.threshold_period, 
           'dateModified': obj.date_modified, 
           'dateAdded': obj.date_added}