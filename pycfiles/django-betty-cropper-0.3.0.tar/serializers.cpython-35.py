# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /app/djbetty/serializers.py
# Compiled at: 2016-09-14 16:35:12
# Size of source mod 2**32: 823 bytes
from rest_framework import serializers

class ImageFieldSerializer(serializers.Field):

    def to_representation(self, obj):
        if isinstance(obj, dict):
            data = {'id': obj.get('id'), 
             'alt': obj.get('alt'), 
             'caption': obj.get('caption')}
        else:
            if obj is None or obj.id is None:
                return
            data = {'id': obj.id}
        if obj.field.alt_field:
            data['alt'] = obj.alt
        if obj.field.caption_field:
            data['caption'] = obj.caption
        return data

    def to_internal_value(self, data):
        if data is not None and 'id' in data:
            data['id'] = int(data['id'])
            return data