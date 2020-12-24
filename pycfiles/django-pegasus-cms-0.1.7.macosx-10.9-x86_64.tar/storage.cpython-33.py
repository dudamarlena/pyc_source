# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mattcaldwell/.virtualenvs/pegasus/lib/python3.3/site-packages/pegasus/storage.py
# Compiled at: 2015-02-18 13:07:40
# Size of source mod 2**32: 1688 bytes
from __future__ import absolute_import, division
from boto.s3.connection import OrdinaryCallingFormat
from precompressed.storage.s3boto import CachedPrecompressedS3BotoStorage
from storages.backends.s3boto import S3BotoStorage
from storages.utils import setting

class CelerityStaticFilesStorage(CachedPrecompressedS3BotoStorage):

    def __init__(self, acl=None, bucket=None, **settings):
        settings['headers'] = {'Cache-Control': 'max-age=%s' % str(31536000)}
        settings['querystring_auth'] = False
        super(CelerityStaticFilesStorage, self).__init__(acl, (bucket or setting('CELERITY_STATICFILES_BUCKET')), **settings)

    def url(self, name, force=False):
        _url = super(CelerityStaticFilesStorage, self).url(name, force)
        if name.endswith('/'):
            if not _url.endswith('/'):
                _url += '/'
        return _url


class CelerityMediaFilesStorage(S3BotoStorage):

    def __init__(self, acl=None, bucket=None, **settings):
        settings['headers'] = {'Cache-Control': 'max-age=%s' % str(3600)}
        settings['querystring_auth'] = False
        super(CelerityMediaFilesStorage, self).__init__(acl, (bucket or setting('CELERITY_MEDIAFILES_BUCKET')), **settings)