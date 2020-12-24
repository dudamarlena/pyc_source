# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/casper/services/s3.py
# Compiled at: 2020-01-30 17:53:06
# Size of source mod 2**32: 502 bytes
from casper.services.base import BaseService

class S3Service(BaseService):

    def __init__(self, profile=None):
        super().__init__(profile=profile)
        self._resources_groups = ['aws_s3_bucket']

    def _get_live_aws_s3_bucket(self):
        s3_client = self.session.client('s3')
        s3_buckets = s3_client.list_buckets()
        buckets = {bucket['Name']:bucket for bucket in s3_buckets['Buckets']}
        return buckets

    def scan_service(self, ghosts):
        pass