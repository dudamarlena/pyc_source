# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/analytics/events/issue_ignored.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import
from sentry import analytics

class IssueIgnoredEvent(analytics.Event):
    type = 'issue.ignored'
    attributes = (
     analytics.Attribute('user_id', type=int, required=False),
     analytics.Attribute('default_user_id', type=int),
     analytics.Attribute('organization_id', type=int),
     analytics.Attribute('group_id'),
     analytics.Attribute('ignore_duration', type=int, required=False),
     analytics.Attribute('ignore_count', type=int, required=False),
     analytics.Attribute('ignore_window', type=int, required=False),
     analytics.Attribute('ignore_user_count', type=int, required=False),
     analytics.Attribute('ignore_user_window', type=int, required=False))


analytics.register(IssueIgnoredEvent)