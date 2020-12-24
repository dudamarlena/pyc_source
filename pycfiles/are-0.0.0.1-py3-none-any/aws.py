# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/prometeo/projects/ardy/ardy/utils/aws.py
# Compiled at: 2018-03-24 11:47:25
from __future__ import unicode_literals, print_function
import boto3
from ardy.config import ConfigMixin

class AWSCli(ConfigMixin):

    def __init__(self, *args, **kwargs):
        self.config = kwargs.get(b'config', False)
        if not self.config:
            super(AWSCli, self).__init__(*args, **kwargs)

    def _get_aws_cretentials_from_config(self):
        conf = {}
        aws_credentials = self.config.get(b'aws_credentials', {})
        aws_access_key_id = aws_credentials.get(b'aws_access_key_id', False)
        aws_secret_access_key = aws_credentials.get(b'aws_secret_access_key', False)
        region = aws_credentials.get(b'region', False)
        if aws_access_key_id:
            conf.update({b'aws_access_key_id': aws_access_key_id})
        if aws_secret_access_key:
            conf.update({b'aws_secret_access_key': aws_secret_access_key})
        if region:
            conf.update({b'region_name': region})
        return conf

    def _get_client(self, client):
        return boto3.client(client, **self._get_aws_cretentials_from_config())

    def _get_resource(self, client):
        return boto3.resource(client, **self._get_aws_cretentials_from_config())

    def get_lambda_client(self):
        return self._get_client(b'lambda')

    def get_s3_resource(self):
        return self._get_resource(b's3')

    def get_sns_client(self):
        return self._get_client(b'sns')

    def get_cloudwatchevent_client(self):
        return self._get_client(b'events')