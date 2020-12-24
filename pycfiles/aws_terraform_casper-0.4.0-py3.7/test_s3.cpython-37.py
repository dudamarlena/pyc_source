# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tests/services/test_s3.py
# Compiled at: 2020-02-03 17:04:46
# Size of source mod 2**32: 1047 bytes
from unittest import TestCase
from moto import mock_s3
from casper.services.s3 import S3Service
from casper.services.base import get_service, BaseService
from tests.utils import aws_credentials
import boto3, pytest

@pytest.mark.usefixtures('aws_credentials')
class TestS3Service(TestCase):

    def test_get_service(self):
        test_service = 's3'
        self.assertTrue(issubclass(get_service(test_service), BaseService))
        self.assertTrue(isinstance(get_service(test_service)(), S3Service))

    @mock_s3
    def test_get_cloud_resources_aws_s3_bucket(self):
        s3 = S3Service()
        conn = boto3.resource('s3')
        count = 300
        for i in range(count):
            _ = conn.create_bucket(Bucket=f"testbucket{i}")

        test_group = 'aws_s3_bucket'
        resources = s3.get_cloud_resources(group=test_group)
        self.assertEqual(count, len(resources.keys()))
        self.assertEqual([
         'Name', 'CreationDate'], list(resources['testbucket0'].keys()))