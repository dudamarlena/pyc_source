# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/analytics/events/organization_created.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import, print_function
from sentry import analytics

class OrganizationCreatedEvent(analytics.Event):
    type = 'organization.created'
    attributes = (
     analytics.Attribute('id'),
     analytics.Attribute('name'),
     analytics.Attribute('slug'),
     analytics.Attribute('actor_id', required=False))


analytics.register(OrganizationCreatedEvent)