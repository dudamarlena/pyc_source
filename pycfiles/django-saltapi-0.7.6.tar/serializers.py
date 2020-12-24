# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/code/django-saltapi/django_saltapi/serializers.py
# Compiled at: 2013-03-11 11:28:44
from rest_framework import serializers

class LowdataSerializer(serializers.Serializer):
    client = serializers.CharField(max_length=20)
    tgt = serializers.CharField(max_length=50)
    fun = serializers.CharField(max_length=30)
    arg = serializers.CharField(max_length=100, required=False)