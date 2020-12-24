# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/release_file.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer, register
from sentry.models import ReleaseFile

@register(ReleaseFile)
class ReleaseFileSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        return {'id': six.text_type(obj.id), 
           'name': obj.name, 
           'dist': obj.dist_id and obj.dist.name or None, 
           'headers': obj.file.headers, 
           'size': obj.file.size, 
           'sha1': obj.file.checksum, 
           'dateCreated': obj.file.timestamp}