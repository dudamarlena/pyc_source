# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramzi/drf-social-auth/drf_social/view.py
# Compiled at: 2020-03-05 08:42:32
# Size of source mod 2**32: 667 bytes
from django.http import HttpResponse
from rest_framework.views import APIView
from social_django.utils import load_strategy, Strategy, load_backend
from drf_social.serializers import SocialInputSerializer

class SocialLoginView(APIView):
    permission_classes = []
    authentication_classes = []
    _strategy: Strategy

    def post(self, *args, **kwargs):
        token_serializer = SocialInputSerializer(data=(self.request.data))
        token_serializer.is_valid(raise_exception=True)
        self._strategy = load_strategy(self.request)
        backend = load_backend(self._strategy, token_serializer.data['provider'].lower(), '/')
        return HttpResponse()