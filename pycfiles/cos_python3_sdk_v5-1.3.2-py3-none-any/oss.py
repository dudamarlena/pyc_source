# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/migrate_tool/services/oss.py
# Compiled at: 2017-03-29 00:21:31
from logging import getLogger
from migrate_tool import storage_service
from migrate_tool.task import Task
import oss2
logger = getLogger(__name__)

class OssStorageService(storage_service.StorageService):

    def __init__(self, *args, **kwargs):
        endpoint = kwargs['endpoint']
        accesskeyid = kwargs['accesskeyid']
        accesskeysecret = kwargs['accesskeysecret']
        bucket = kwargs['bucket']
        self._oss_api = oss2.Bucket(oss2.Auth(accesskeyid, accesskeysecret), endpoint, bucket)
        self._prefix = kwargs['prefix'] if 'prefix' in kwargs else ''
        if self._prefix.startswith('/'):
            self._prefix = self._prefix[1:]

    def download(self, task, local_path):
        for i in range(20):
            logger.info(('download file with rety {0}').format(i))
            import os
            try:
                os.remove(task.key)
            except:
                pass

            self._oss_api.get_object_to_file(task.key, local_path)
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
            raise IOError('Download Failed with 20 retry')

        return

    def upload(self, cos_path, local_path):
        raise NotImplementedError

    def list(self):
        for obj in oss2.ObjectIterator(self._oss_api, prefix=self._prefix):
            if obj.key[(-1)] == '/':
                continue
            logger.info(('yield new object: {}').format(obj.key))
            yield Task(obj.key, obj.size, None)

        return

    def exists(self, _path):
        raise NotImplementedError