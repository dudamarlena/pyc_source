# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rest_signature/serializers.py
# Compiled at: 2015-04-30 01:17:41
# Size of source mod 2**32: 459 bytes
from rest_framework import serializers
from .models import *

class SiteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Site


class SignatureSerializer(serializers.ModelSerializer):

    class Meta:
        model = Signature
        fields = ('site', 'owner')


class SignatureResponseSerializer(serializers.ModelSerializer):
    site = SiteSerializer()

    class Meta:
        model = Signature
        fields = ('site', 'owner', 'key')