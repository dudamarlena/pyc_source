# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/byk/Documents/Projects/sentry/sentry/src/sentry/analytics/events/sentry_app_schema_validation_error.py
# Compiled at: 2019-09-04 11:05:35
from __future__ import absolute_import
from sentry import analytics

class SentryAppSchemaValidationError(analytics.Event):
    type = 'sentry_app.schema_validation_error'
    attributes = (
     analytics.Attribute('schema'),
     analytics.Attribute('user_id'),
     analytics.Attribute('sentry_app_id', required=False),
     analytics.Attribute('sentry_app_name'),
     analytics.Attribute('organization_id'),
     analytics.Attribute('error_message'))


analytics.register(SentryAppSchemaValidationError)