# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/user_notification_fine_tuning.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from sentry.api.bases.user import UserEndpoint
from sentry.api.serializers import serialize
from sentry.api.serializers.models import UserNotificationsSerializer
from sentry.models import OrganizationMember, OrganizationMemberTeam, OrganizationStatus, ProjectTeam, UserOption, UserEmail
KEY_MAP = {'alerts': {'key': 'mail:alert', 'type': int}, 'workflow': {'key': 'workflow:notifications', 'type': ''}, 'deploy': {'key': 'deploy-emails', 'type': ''}, 'reports': {'key': 'reports:disabled-organizations', 'type': ''}, 'email': {'key': 'mail:email', 'type': ''}}

class UserNotificationFineTuningEndpoint(UserEndpoint):

    def get(self, request, user, notification_type):
        if notification_type not in KEY_MAP:
            return Response({'detail': 'Unknown notification type: %s.' % notification_type}, status=status.HTTP_404_NOT_FOUND)
        notifications = UserNotificationsSerializer()
        serialized = serialize(user, request.user, notifications, notification_option_key=KEY_MAP[notification_type]['key'])
        return Response(serialized)

    def put(self, request, user, notification_type):
        """
        Update user notification options
        ````````````````````````````````

        Updates user's notification options on a per project or organization basis.
        Expected payload is a map/dict whose key is a project or org id and value varies depending on `notification_type`.

        For `alerts`, `workflow`, `email` it expects a key of projectId
        For `deploy` and `reports` it expects a key of organizationId

        For `alerts`, `workflow`, `deploy`, it expects a value of:
            - "-1" = for "default" value (i.e. delete the option)
            - "0"  = disabled
            - "1"  = enabled
        For `reports` it is only a boolean.
        For `email` it is a verified email (string).

        :auth required:
        :pparam string notification_type:  One of:  alerts, workflow, reports, deploy, email
        :param map: Expects a map of id -> value (enabled or email)
        """
        if notification_type not in KEY_MAP:
            return Response({'detail': 'Unknown notification type: %s.' % notification_type}, status=status.HTTP_404_NOT_FOUND)
        else:
            key = KEY_MAP[notification_type]
            filter_args = {'user': user, 'key': key['key']}
            if notification_type == 'reports':
                user_option, created = UserOption.objects.get_or_create(**filter_args)
                value = set(user_option.value or [])
                org_ids = self.get_org_ids(user)
                for org_id, enabled in request.data.items():
                    org_id = int(org_id)
                    enabled = int(enabled)
                    if org_id not in org_ids:
                        return Response({'detail': 'User does not belong to at least one of the                             requested orgs (org_id: %s).' % org_id}, status=status.HTTP_403_FORBIDDEN)
                    if enabled and org_id in value:
                        value.remove(org_id)
                    elif not enabled:
                        value.add(org_id)

                user_option.update(value=list(value))
                return Response(status=status.HTTP_204_NO_CONTENT)
            if notification_type in ('alerts', 'workflow', 'email'):
                update_key = 'project'
                parent_ids = set(self.get_project_ids(user))
            else:
                update_key = 'organization'
                parent_ids = set(self.get_org_ids(user))
            try:
                ids_to_update = set([ int(i) for i in request.data.keys() ])
            except ValueError:
                return Response({'detail': 'Invalid id value provided. Id values should be integers.'}, status=status.HTTP_400_BAD_REQUEST)

            if not ids_to_update.issubset(parent_ids):
                bad_ids = ids_to_update - parent_ids
                return Response({'detail': 'At least one of the requested projects is not                     available to this user, because the user does not belong                     to the necessary teams. (ids of unavailable projects: %s)' % bad_ids}, status=status.HTTP_403_FORBIDDEN)
            if notification_type == 'email':
                emails_to_check = set(request.data.values())
                emails = UserEmail.objects.filter(user=user, email__in=emails_to_check, is_verified=True)
                if len(emails) != len(emails_to_check):
                    return Response({'detail': 'Invalid email value(s) provided. Email values                         must be verified emails for the given user.'}, status=status.HTTP_400_BAD_REQUEST)
            with transaction.atomic():
                for id in request.data:
                    val = request.data[id]
                    int_val = int(val) if notification_type != 'email' else None
                    filter_args['%s_id' % update_key] = id
                    if int_val == -1:
                        UserOption.objects.filter(**filter_args).delete()
                    else:
                        user_option, _ = UserOption.objects.get_or_create(**filter_args)
                        user_option.update(value=int_val if key['type'] is int else six.text_type(val))

                return Response(status=status.HTTP_204_NO_CONTENT)
            return

    def get_org_ids(self, user):
        """ Get org ids for user """
        return set(OrganizationMember.objects.filter(user=user, organization__status=OrganizationStatus.ACTIVE).values_list('organization_id', flat=True))

    def get_project_ids(self, user):
        """ Get project ids that user has access to """
        return set(ProjectTeam.objects.filter(team_id__in=OrganizationMemberTeam.objects.filter(organizationmember__user=user).values_list('team_id', flat=True)).values_list('project_id', flat=True))