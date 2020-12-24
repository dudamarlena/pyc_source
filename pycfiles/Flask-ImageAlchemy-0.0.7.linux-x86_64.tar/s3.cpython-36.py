# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ppoteralski/PycharmProjects/sqlalchemy-stdimage/.venv/lib/python3.6/site-packages/flask_image_alchemy/storages/s3.py
# Compiled at: 2017-02-20 07:09:47
# Size of source mod 2**32: 1857 bytes
from boto3 import client
from botocore.config import Config
from flask_image_alchemy.storages.base import BaseStorage
try:
    from flask import _app_ctx_stack as stack
except ImportError:
    from flask import _request_ctx_stack as stack

class S3Storage(BaseStorage):

    def __init__(self, app=None, config=None):
        if app:
            self.init_app(app, config=config)

    def _create_client(self):
        return client('s3',
          aws_access_key_id=(self.ACCESS_KEY),
          aws_secret_access_key=(self.SECRET),
          region_name=(self.REGION_NAME),
          config=(self.config))

    @property
    def client(self):
        ctx = stack.top
        if ctx is not None:
            if not hasattr(ctx, 's3_service'):
                ctx.s3_service = self._create_client()
            return ctx.s3_service
        else:
            return self._create_client()

    def init_app(self, app, config=None):
        self.app = app
        self.ACCESS_KEY = app.config.get('AWS_ACCESS_KEY_ID')
        self.SECRET = app.config.get('AWS_SECRET_ACCESS_KEY')
        self.REGION_NAME = app.config.get('AWS_REGION_NAME')
        self.BUCKET_NAME = app.config.get('S3_BUCKET_NAME')
        self.config = config if config else Config(signature_version='s3v4')

    def read(self, file_name):
        self.client.download_fileobj(self.BUCKET_NAME, file_name)

    def write(self, data, file_name):
        self.client.upload_fileobj(data, self.BUCKET_NAME, file_name)

    def delete(self, file_name):
        self.client.delete_object(Bucket=(self.BUCKET_NAME), Key=file_name)