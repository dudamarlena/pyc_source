# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/utils/fields.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 245 bytes
from rest_framework import serializers

class RichTextField(serializers.CharField):

    def __init__(self, *args, **kwargs):
        self.field_size = kwargs.pop('field_size', None)
        super(RichTextField, self).__init__(*args, **kwargs)