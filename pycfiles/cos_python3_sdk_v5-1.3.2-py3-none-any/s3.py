# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/migrate_tool/services/s3.py
# Compiled at: 2017-03-29 00:21:31
from logging import getLogger
from migrate_tool import storage_service
from migrate_tool.task import Task
from boto.s3.connection import S3Connection
logger = getLogger(__name__)

class S3StorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        bucket = kwargs['bucket']
        self._prefix = kwargs['prefix'] if 'prefix' in kwargs else ''
        _s3_api = S3Connection(aws_access_key_id=accesskeyid, aws_secret_access_key=accesskeysecret)
        self._bucket_api = _s3_api.get_bucket(bucket)

    def download(self, task, local_path):
        for i in range(20):
            key = self._bucket_api.get_key(task.key)
            if key is not None:
                key.get_contents_to_filename(local_path)
            else:
                raise IOError('Download failed 404')
            if task.size is None:
                logger.info("task's size is None, skip check file size on local")
                break
            from os import path
            if path.getsize(local_path) != int(task.size):
                logger.error(('Download Failed, size1: {size1}, size2: {size2}').format(size1=path.getsize(local_path), size2=task.size))
            else:
                logger.info('Download Successfully, break')
                break
        else:
            raise IOError('download failed with 20 retry')

        return

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self):
        for obj in self._bucket_api.list(prefix=self._prefix):
            if obj.name[(-1)] == '/':
                continue
            logger.info(('yield new object: {}').format(obj.key))
            yield Task(obj.name, obj.size, None)

        return

    def exists(self, _path):
        raise NotImplementedError