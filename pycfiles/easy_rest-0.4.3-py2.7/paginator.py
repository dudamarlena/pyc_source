# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/easyapi/paginator.py
# Compiled at: 2014-08-13 22:19:24
from rest_framework import pagination
from rest_framework import serializers
from easyapi.serializer import AutoModelSerializer
__author__ = 'mikhailturilin'

class EasyPaginationSerializer(pagination.PaginationSerializer):
    num_pages = serializers.Field(source='paginator.num_pages')
    number = serializers.Field(source='number')