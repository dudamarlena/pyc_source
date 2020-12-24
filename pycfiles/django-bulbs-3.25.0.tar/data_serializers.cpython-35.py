# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/utils/data_serializers.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 671 bytes
from rest_framework import serializers
from djbetty.serializers import ImageFieldSerializer
from bulbs.utils.fields import RichTextField

class BaseEntrySerializer(serializers.Serializer):

    def __init__(self, *args, **kwargs):
        self.child_label = kwargs.pop('child_label', None)
        super(BaseEntrySerializer, self).__init__(*args, **kwargs)


class CopySerializer(serializers.Serializer):
    copy = RichTextField(required=True, field_size='long')


class EntrySerializer(BaseEntrySerializer, CopySerializer):
    title = RichTextField(required=False, field_size='short')
    image = ImageFieldSerializer(required=False, default=None, allow_null=True)