# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /code/s3direct/fields.py
# Compiled at: 2019-07-27 06:20:31
# Size of source mod 2**32: 544 bytes
from django.db.models import Field
from django.conf import settings
from s3direct.widgets import S3DirectWidget

class S3DirectField(Field):

    def __init__(self, *args, **kwargs):
        dest = kwargs.pop('dest', None)
        self.widget = S3DirectWidget(dest=dest)
        (super(S3DirectField, self).__init__)(*args, **kwargs)

    def get_internal_type(self):
        return 'TextField'

    def formfield(self, *args, **kwargs):
        kwargs['widget'] = self.widget
        return (super(S3DirectField, self).formfield)(*args, **kwargs)