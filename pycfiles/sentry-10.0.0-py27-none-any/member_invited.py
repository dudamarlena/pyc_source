# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/analytics/events/member_invited.py
# Compiled at: 2019-08-16 17:27:44
from __future__ import absolute_import, print_function
from sentry import analytics

class MemberInvitedEvent(analytics.Event):
    type = 'member.invited'
    attributes = (
     analytics.Attribute('inviter_user_id'),
     analytics.Attribute('invited_member_id'),
     analytics.Attribute('organization_id'),
     analytics.Attribute('referrer', required=False))


analytics.register(MemberInvitedEvent)