# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: E:\cd2\env\lib\site-packages\httplog\serializers.py
# Compiled at: 2016-11-28 23:27:29
from __future__ import absolute_import
from .base import DynamicFieldsModelSerializer, UserField
from .models.httplog import HttpLog

class HttpLogSerializer(DynamicFieldsModelSerializer):
    user = UserField()

    class Meta:
        model = HttpLog