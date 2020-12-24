# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ramzi/drf-social-auth/drf_social/serializers.py
# Compiled at: 2020-03-05 09:11:40
# Size of source mod 2**32: 711 bytes
from rest_framework import serializers
from drf_social import models
try:
    from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
except ImportError:
    raise ImportError('must install rest_framework_simplejwt first')

class SocialInputSerializer(serializers.Serializer):
    access_token = serializers.CharField(max_length=100, required=True, allow_blank=False, allow_null=False)
    provider = serializers.ChoiceField(choices=((p, p) for p in models.Providers), allow_null=False, allow_blank=False, required=True)
    client_id = serializers.CharField(max_length=100, allow_null=False, allow_blank=False, required=True)


class JWTResponseSerializer(TokenObtainPairSerializer):
    pass