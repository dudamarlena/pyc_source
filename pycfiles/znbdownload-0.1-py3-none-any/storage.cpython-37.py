# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/project/znbdownload/storage.py
# Compiled at: 2019-07-03 12:41:27
# Size of source mod 2**32: 669 bytes
from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings

class S3MediaStorage(S3Boto3Storage):
    __doc__ = '\n    Media files stored on Amazon S3.\n    See storages.backends.s3boto.S3BotoStorage for other attributes.\n    Requires AWS_STORAGE_MEDIA_BUCKET_NAME setting.\n    '
    bucket_name = getattr(settings, 'AWS_STORAGE_MEDIA_BUCKET_NAME', '')


class S3PrivateStorage(S3Boto3Storage):
    __doc__ = '\n    Private files stored on Amazon S3.\n    See storages.backends.s3boto.S3BotoStorage for other attributes.\n    Requires AWS_STORAGE_PRIVATE_BUCKET_NAME setting.\n    '
    bucket_name = getattr(settings, 'AWS_STORAGE_PRIVATE_BUCKET_NAME', '')