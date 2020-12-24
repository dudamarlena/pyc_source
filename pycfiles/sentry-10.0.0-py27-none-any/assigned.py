# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/plugins/sentry_mail/activity/assigned.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.models import User, Team
from .base import ActivityEmail

class AssignedActivityEmail(ActivityEmail):

    def get_activity_name(self):
        return 'Assigned'

    def get_description(self):
        activity = self.activity
        data = activity.data
        if 'assigneeType' not in data or data['assigneeType'] == 'user':
            if activity.user_id and six.text_type(activity.user_id) == data['assignee']:
                return '{author} assigned {an issue} to themselves'
            try:
                assignee = User.objects.get_from_cache(id=data['assignee'])
            except User.DoesNotExist:
                pass
            else:
                return ('{author} assigned {an issue} to {assignee}', {'assignee': assignee.get_display_name()})

            if data.get('assigneeEmail'):
                return (
                 '{author} assigned {an issue} to {assignee}', {'assignee': data['assigneeEmail']})
            return '{author} assigned {an issue} to an unknown user'
        if data['assigneeType'] == 'team':
            try:
                assignee_team = Team.objects.get(id=data['assignee'], organization=self.organization)
            except Team.DoesNotExist:
                return '{author} assigned {an issue} to an unknown team'

            return (
             '{author} assigned {an issue} to the {assignee} team', {'assignee': assignee_team.slug})
        raise NotImplementedError('Unknown Assignee Type ')