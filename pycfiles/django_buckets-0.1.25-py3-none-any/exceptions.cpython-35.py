# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/Work/dev/cadasta/django-buckets/buckets/exceptions.py
# Compiled at: 2016-10-05 04:16:49
# Size of source mod 2**32: 232 bytes


class InvalidPayload(BaseException):

    def __init__(self, errors={}, *args, **kwargs):
        super(InvalidPayload, self).__init__(*args, **kwargs)
        self.errors = errors


class S3ResourceNotFound(BaseException):
    pass