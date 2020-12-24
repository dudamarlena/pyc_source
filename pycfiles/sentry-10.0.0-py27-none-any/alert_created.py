# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/analytics/events/alert_created.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import
from sentry import analytics

class AlertCreatedEvent(analytics.Event):
    type = 'alert.created'
    attributes = (
     analytics.Attribute('user_id', required=False),
     analytics.Attribute('default_user_id'),
     analytics.Attribute('organization_id'),
     analytics.Attribute('rule_id'),
     analytics.Attribute('actions', type=list))


analytics.register(AlertCreatedEvent)