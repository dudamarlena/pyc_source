# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/api/serializers/models/debug_file.py
# Compiled at: 2019-08-16 17:27:45
from __future__ import absolute_import
import six
from sentry.api.serializers import Serializer, register
from sentry.models import ProjectDebugFile

@register(ProjectDebugFile)
class DebugFileSerializer(Serializer):

    def serialize(self, obj, attrs, user):
        d = {'id': six.text_type(obj.id), 
           'uuid': obj.debug_id[:36], 
           'debugId': obj.debug_id, 
           'codeId': obj.code_id, 
           'cpuName': obj.cpu_name, 
           'objectName': obj.object_name, 
           'symbolType': obj.file_format, 
           'headers': obj.file.headers, 
           'size': obj.file.size, 
           'sha1': obj.file.checksum, 
           'dateCreated': obj.file.timestamp, 
           'data': obj.data or {}}
        return d