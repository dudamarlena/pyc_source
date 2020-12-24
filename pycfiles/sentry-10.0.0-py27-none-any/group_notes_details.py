# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/endpoints/group_notes_details.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
from rest_framework import status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from sentry.api.bases.group import GroupEndpoint
from sentry.api.exceptions import ResourceDoesNotExist
from sentry.api.serializers import serialize
from sentry.api.serializers.rest_framework.group_notes import NoteSerializer
from sentry.models import Activity

class GroupNotesDetailsEndpoint(GroupEndpoint):

    def delete(self, request, group, note_id):
        if not request.user.is_authenticated():
            raise PermissionDenied(detail="Key doesn't have permission to delete Note")
        try:
            note = Activity.objects.get(group=group, type=Activity.NOTE, user=request.user, id=note_id)
        except Activity.DoesNotExist:
            raise ResourceDoesNotExist

        note.delete()
        return Response(status=204)

    def put(self, request, group, note_id):
        if not request.user.is_authenticated():
            raise PermissionDenied(detail="Key doesn't have permission to edit Note")
        try:
            note = Activity.objects.get(group=group, type=Activity.NOTE, user=request.user, id=note_id)
        except Activity.DoesNotExist:
            raise ResourceDoesNotExist

        serializer = NoteSerializer(data=request.data)
        if serializer.is_valid():
            note.data.update(dict(serializer.validated_data))
            note.save()
            if note.data.get('external_id'):
                self.update_external_comment(request, group, note)
            return Response(serialize(note, request.user), status=200)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)