# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/v_m_t/s3customtransfer.py
# Compiled at: 2019-10-02 14:57:19
# Size of source mod 2**32: 5056 bytes
"""Abstractions over S3's upload/download operations.

Modified version of 

"""
from boto3.exceptions import RetriesExceededError
from s3transfer.exceptions import RetriesExceededError as S3TransferRetriesExceededError
from s3transfer.futures import NonThreadedExecutor
from s3transfer.manager import TransferConfig as S3TransferConfig
from s3transfer.manager import TransferManager
from s3transfer.subscribers import BaseSubscriber
from s3transfer.utils import OSUtils
KB = 1024
MB = KB * KB

def create_transfer_manager(client, config, osutil=None):
    executor_cls = None
    if not config.use_threads:
        executor_cls = NonThreadedExecutor
    return TransferManager(client, config, osutil, executor_cls)


class TransferConfig(S3TransferConfig):
    ALIAS = {'max_concurrency':'max_request_concurrency', 
     'max_io_queue':'max_io_queue_size'}

    def __init__(self, multipart_threshold=8 * MB, max_concurrency=10, multipart_chunksize=8 * MB, num_download_attempts=5, max_io_queue=100, io_chunksize=256 * KB, use_threads=True):
        super(TransferConfig, self).__init__(multipart_threshold=multipart_threshold,
          max_request_concurrency=max_concurrency,
          multipart_chunksize=multipart_chunksize,
          num_download_attempts=num_download_attempts,
          max_io_queue_size=max_io_queue,
          io_chunksize=io_chunksize)
        for alias in self.ALIAS:
            setattr(self, alias, getattr(self, self.ALIAS[alias]))

        self.use_threads = use_threads

    def __setattr__(self, name, value):
        if name in self.ALIAS:
            super(TransferConfig, self).__setattr__(self.ALIAS[name], value)
        super(TransferConfig, self).__setattr__(name, value)


class S3CustomTransfer(object):
    ALLOWED_DOWNLOAD_ARGS = TransferManager.ALLOWED_DOWNLOAD_ARGS
    ALLOWED_UPLOAD_ARGS = TransferManager.ALLOWED_UPLOAD_ARGS

    def __init__(self, client=None, config=None, osutil=None, manager=None):
        if not client:
            if not manager:
                raise ValueError('Either a boto3.Client or s3transfer.manager.TransferManager must be provided')
            if manager:
                if any([client, config, osutil]):
                    raise ValueError('Manager cannot be provided with client, config, nor osutil. These parameters are mutually exclusive.')
            if config is None:
                config = TransferConfig()
        else:
            if osutil is None:
                osutil = OSUtils()
            if manager:
                self._manager = manager
            else:
                self._manager = create_transfer_manager(client, config, osutil)

    def download_file(self, bucket, key, filename, extra_args=None, callback=None):
        subscribers = self._get_subscribers(callback)
        future = self._manager.download(bucket, key, filename, extra_args, subscribers)
        try:
            future.result()
        except S3TransferRetriesExceededError as e:
            raise RetriesExceededError(e.last_exception)

    def _get_subscribers(self, callback):
        if not callback:
            return
        else:
            return [
             DoneCallbackInvoker(callback)]

    def wait(self):
        self._manager._coordinator_controller.wait()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        (self._manager.__exit__)(*args)


class DoneCallbackInvoker(BaseSubscriber):

    def __init__(self, callback):
        self._callback = callback

    def on_done(self, **kwargs):
        self._callback()