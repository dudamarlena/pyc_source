# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/no_cloud/remote/minio.py
# Compiled at: 2017-03-11 18:48:33
from botocore.client import Config
from .s3 import RemoteStorage as S3RemoteStorage

class RemoteStorage(S3RemoteStorage):

    def check_s3_config(self):
        super(RemoteStorage, self).check_s3_config()
        assert 'endpoint' in self.config, '`endpoint` not found in configuration'

    def build_s3_args(self):
        args, kwargs = super(RemoteStorage, self).build_s3_args()
        if 'endpoint' in self.config:
            kwargs['endpoint_url'] = self.config['endpoint']
        if 'region' not in self.config:
            kwargs['region_name'] = 'us-east-1'
        kwargs['config'] = Config(signature_version='s3v4')
        return (
         args, kwargs)