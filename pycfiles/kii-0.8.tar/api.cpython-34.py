# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/eliotberriot/Seafile/kii/kii_main/kii/stream/views/api.py
# Compiled at: 2015-01-18 07:28:37
# Size of source mod 2**32: 1206 bytes
from rest_framework import generics
from rest_framework import views
from rest_framework import status
from rest_framework import authentication
from rest_framework import permissions as rest_permissions
from rest_framework.response import Response
from .. import models, serializers, permissions

class ItemCommentUpdate(generics.UpdateAPIView):
    queryset = models.ItemComment.objects.all().select_related('subject', 'user', 'user_profile')
    serializer_class = serializers.ItemCommentSerializer
    permission_classes = (
     permissions.IsCommentModerator,)


class StreamSelect(views.APIView):
    __doc__ = "Save the given stream as default in user's session"
    permissions = (
     rest_permissions.IsAuthenticated,)

    def get(self, request, format=None, **kwargs):
        try:
            stream = models.Stream.objects.get(owner=request.user, pk=kwargs.get('pk'))
            request.session['selected_stream'] = stream.pk
            return Response('', status=status.HTTP_200_OK)
        except models.Stream.DoesNotExist:
            return Response('', status=status.HTTP_404_NOT_FOUND)