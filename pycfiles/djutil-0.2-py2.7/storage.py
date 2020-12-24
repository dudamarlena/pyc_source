# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\djutil\storage.py
# Compiled at: 2013-08-27 09:32:46
from __future__ import unicode_literals
import logging
from django.core.files.storage import get_storage_class
from boto.utils import parse_ts
from storages.backends.s3boto import S3BotoStorage
logger = logging.getLogger(b'app.util.storage')

class S3StaticStorage(S3BotoStorage):
    """
    Subclasses :class:`storages.backends.s3boto.S3BotoStorage` and
    sets base location for files to ``/static``.
    """

    def __init__(self, *args, **kwargs):
        kwargs[b'location'] = b'static'
        kwargs.setdefault(b'preload_metadata', True)
        super(S3StaticStorage, self).__init__(*args, **kwargs)


class S3MediaStorage(S3BotoStorage):
    """
    Subclasses :class:`storages.backends.s3boto.S3BotoStorage` and
    sets base location for files to ``/media``.
    """

    def __init__(self, *args, **kwargs):
        kwargs[b'location'] = b'media'
        super(S3MediaStorage, self).__init__(*args, **kwargs)


class NonDeletingS3MediaStorage(S3MediaStorage):

    def delete(self, name):
        logger.debug(b'NOOP file delete: %s', name)


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

    def modified_time(self, name):
        name = self._normalize_name(self._clean_name(name))
        entry = self.entries.get(name)
        if entry is None:
            entry = self.bucket.get_key(self._encode_name(name))
        return parse_ts(entry.last_modified)


class CachedS3StaticStorage(CachedS3BotoStorage):
    """
    Mix of the :class:`S3StaticStorage` and :class:`CachedS3BotoStorage`,
    saves files in ``/static`` subdirectory
    """

    def __init__(self, *args, **kwargs):
        kwargs[b'location'] = b'static'
        super(CachedS3StaticStorage, self).__init__(*args, **kwargs)