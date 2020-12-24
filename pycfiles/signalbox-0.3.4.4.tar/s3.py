# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/s3.py
# Compiled at: 2014-08-27 19:26:12
from storages.backends.s3boto import S3BotoStorage
from django.utils.functional import SimpleLazyObject
from django.core.files.storage import get_storage_class

class CustomS3BotoStorage(S3BotoStorage):
    """
    S3 storage backend that saves the files locally, too.
    """

    def __init__(self, *args, **kwargs):
        super(CustomS3BotoStorage, self).__init__(*args, **kwargs)
        self.local_storage = get_storage_class('compressor.storage.CompressorFileStorage')()

    def url(self, name):
        url = super(CustomS3BotoStorage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url

    def save(self, name, content):
        name = super(CustomS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name


StaticRootS3BotoStorage = lambda : CustomS3BotoStorage(location='static/')
MediaRootS3BotoStorage = lambda : CustomS3BotoStorage(location='media/')
PrivateRootS3BotoStorage = lambda : CustomS3BotoStorage(location='private/')