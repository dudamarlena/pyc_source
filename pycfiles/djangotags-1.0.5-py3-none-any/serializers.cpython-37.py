# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\djangotags\src\djangotags\rest_api\serializers.py
# Compiled at: 2020-03-13 00:37:58
# Size of source mod 2**32: 194 bytes
from rest_framework.serializers import ModelSerializer
from taggit.models import Tag

class TagSerializer(ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'