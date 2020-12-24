# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nodeconductor_auth_valimo/serializers.py
# Compiled at: 2016-09-19 07:37:17
from __future__ import unicode_literals
from rest_framework import serializers
from . import models

class AuthResultSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = models.AuthResult
        fields = ('uuid', 'token', 'phone', 'message', 'state', 'error_message', 'details')
        write_only_fields = ('phone', )
        read_only_fields = ('uuid', 'token', 'message', 'state', 'error_message', 'details')

    def get_token(self, auth_result):
        if auth_result.user:
            return auth_result.user.auth_token.key
        else:
            return