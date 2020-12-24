# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-buckets/buckets/serializers.py
# Compiled at: 2016-07-07 10:06:59
# Size of source mod 2**32: 196 bytes
from rest_framework.serializers import Field

class S3Field(Field):

    def to_internal_value(self, value):
        return value

    def to_representation(self, value):
        return value.url