# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/znbstatic/znbstatic/storage.py
# Compiled at: 2019-07-04 13:04:56
# Size of source mod 2**32: 1546 bytes
from django.contrib.staticfiles.storage import StaticFilesStorage
from django.utils.deconstruct import deconstructible
from django.conf import settings
from storages.backends.s3boto3 import S3Boto3Storage
from znbstatic.utils import add_version_to_url

@deconstructible
class VersionedStaticFilesStorage(StaticFilesStorage):
    __doc__ = '\n    A static file system storage backend that appends\n    the value from the ZNBSTATIC_VERSION setting.\n\n    The storage class must be deconstructible.\n    See `<https://docs.djangoproject.com/en/2.1/howto/custom-file-storage/>`_.\n    '

    def url(self, name):
        url = super(VersionedStaticFilesStorage, self).url(name)
        version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
        return add_version_to_url(url, version)


@deconstructible
class VersionedS3StaticFilesStorage(S3Boto3Storage):
    __doc__ = '\n    A static file system storage backend that stores files on Amazon S3 and\n    appends the value from the ZNBSTATIC_VERSION setting.\n\n    The storage class must be deconstructible.\n    See `<https://docs.djangoproject.com/en/2.1/howto/custom-file-storage/>`_.\n\n    Using bucket_name attribute to override default AWS_STORAGE_BUCKET_NAME setting.\n    See S3Boto3Storage for other available attributes.\n    '
    bucket_name = getattr(settings, 'AWS_STORAGE_STATIC_BUCKET_NAME', '')

    def url(self, name):
        url = super(VersionedS3StaticFilesStorage, self).url(name)
        version = getattr(settings, 'ZNBSTATIC_VERSION', '0.0')
        return add_version_to_url(url, version)