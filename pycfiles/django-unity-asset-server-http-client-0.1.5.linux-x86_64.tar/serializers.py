# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/duashttp/serializers.py
# Compiled at: 2014-10-30 10:12:39
from duashttp.models import AssetVersion
from rest_framework import serializers

class AssetVersionSerializer(serializers.HyperlinkedModelSerializer):
    hash = serializers.SerializerMethodField('get_digest')
    guid = serializers.SerializerMethodField('get_guid')

    def get_digest(self, obj):
        return str(hex(obj.get_digest())).replace('0x', '').replace('L', '')

    def get_guid(self, obj):
        guid = obj.asset.get_guid()
        return str(hex(guid)).replace('0x', '').replace('L', '')

    class Meta:
        model = AssetVersion
        fields = ('serial', 'name', 'revision', 'created_in', 'hash', 'guid')