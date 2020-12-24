# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nicolas/src/django-rest-framework-jwt-refresh-token/refreshtoken/views.py
# Compiled at: 2016-01-28 09:27:04
# Size of source mod 2**32: 2400 bytes
from calendar import timegm
from datetime import datetime
from django.utils.translation import ugettext as _
from rest_framework import exceptions, generics, mixins, status, viewsets
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings
from .models import RefreshToken
from .serializers import DelegateJSONWebTokenSerializer, RefreshTokenSerializer
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_response_payload_handler = api_settings.JWT_RESPONSE_PAYLOAD_HANDLER

class DelegateJSONWebToken(generics.CreateAPIView):
    __doc__ = '\n    API View that checks the veracity of a refresh token, returning a JWT if it\n    is valid.\n    '
    permission_classes = [AllowAny]
    serializer_class = DelegateJSONWebTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        if not user.is_active:
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        payload = jwt_payload_handler(user)
        if api_settings.JWT_ALLOW_REFRESH:
            payload['orig_iat'] = timegm(datetime.utcnow().utctimetuple())
        token = jwt_encode_handler(payload)
        response_data = jwt_response_payload_handler(token, user, request)
        return Response(response_data, status=status.HTTP_200_OK)


class RefreshTokenViewSet(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.DestroyModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    __doc__ = '\n    API View that will Create/Delete/List `RefreshToken`.\n\n    https://auth0.com/docs/refresh-token\n    '
    serializer_class = RefreshTokenSerializer
    queryset = RefreshToken.objects.all()
    lookup_field = 'key'

    def get_queryset(self):
        queryset = super(RefreshTokenViewSet, self).get_queryset()
        if self.request.user.is_superuser or self.request.user.is_staff:
            return queryset
        else:
            return queryset.filter(user=self.request.user)


delegate_jwt_token = DelegateJSONWebToken.as_view()