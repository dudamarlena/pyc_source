# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/organization_incident_comment_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.bases.incident import IncidentEndpoint, IncidentPermission
from sentry.api.serializers import serialize
from sentry.incidents.models import IncidentActivity, IncidentActivityType
from sentry.incidents.logic import delete_comment, update_comment

class CommentSerializer(serializers.Serializer):
    comment = serializers.CharField(required=True)


class CommentDetailsEndpoint(IncidentEndpoint):

    def convert_args(self, request, activity_id, *args, **kwargs):
        if not request.user.is_authenticated():
            raise PermissionDenied(detail="Key doesn't have permission to delete Note")
        args, kwargs = super(CommentDetailsEndpoint, self).convert_args(request, *args, **kwargs)
        try:
            kwargs['activity'] = IncidentActivity.objects.get(id=activity_id, user=request.user, incident=kwargs['incident'], type=IncidentActivityType.COMMENT.value)
        except IncidentActivity.DoesNotExist:
            raise ResourceDoesNotExist

        return (args, kwargs)


class OrganizationIncidentCommentDetailsEndpoint(CommentDetailsEndpoint):
    permission_classes = (
     IncidentPermission,)

    def delete(self, request, organization, incident, activity):
        """
        Delete a comment
        ````````````````
        :auth: required
        """
        try:
            delete_comment(activity)
        except IncidentActivity.DoesNotExist:
            raise ResourceDoesNotExist

        return Response(status=204)

    def put(self, request, organization, incident, activity):
        """
        Update an existing comment
        ``````````````````````````
        :auth: required
        """
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid():
            result = serializer.validated_data
            try:
                comment = update_comment(activity=activity, comment=result.get('comment'))
            except IncidentActivity.DoesNotExist:
                raise ResourceDoesNotExist

            return Response(serialize(comment, request.user), status=200)
        return Response(serializer.errors, status=400)