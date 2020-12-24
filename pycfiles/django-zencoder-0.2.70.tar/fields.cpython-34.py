# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cameronlowe/Development/django-zencoder/zencoder/utils/fields.py
# Compiled at: 2017-01-17 11:33:39
# Size of source mod 2**32: 296 bytes
from rest_framework import serializers

class PlaceholderField(serializers.Field):

    def __init__(self, value=None, *args, **kwargs):
        self.value = value
        return super(PlaceholderField, self).__init__(*args, **kwargs)

    def to_representation(self):
        return self.value