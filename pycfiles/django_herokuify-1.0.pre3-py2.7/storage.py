# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\herokuify\storage.py
# Compiled at: 2012-10-24 18:45:29
from __future__ import unicode_literals
from django.core.files.storage import get_storage_class
from storages.backends.s3boto import S3BotoStorage

class S3StaticStorage(S3BotoStorage):
    """
    Subclasses :class:`storages.backends.s3boto.S3BotoStorage` and
    sets base location for files to ``/static``.
    """

    def __init__(self, *args, **kwargs):
        kwargs[b'location'] = b'static'
        super(S3StaticStorage, self).__init__(*args, **kwargs)


class S3MediaStorage(S3BotoStorage):
    """
    Subclasses :class:`storages.backends.s3boto.S3BotoStorage` and
    sets base location for files to ``/media``.
    """

    def __init__(self, *args, **kwargs):
        kwargs[b'location'] = b'media'
        super(S3MediaStorage, self).__init__(*args, **kwargs)


class CachedS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files both remotely and locally.

    See http://django_compressor.readthedocs.org/en/latest/remote-storages/
    """

    def __init__(self, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class(b'compressor.storage.CompressorFileStorage')()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


class CachedS3StaticStorage(CachedS3BotoStorage):
    """
    Mix of the :class:`S3MediaStorage` and :class:`CachedS3BotoStorage`,
    saves files in ``/static`` subdirectory
    """

    def __init__(self, *args, **kwargs):
        kwargs[b'location'] = b'static'
        super(CachedS3StaticStorage, self).__init__(*args, **kwargs)