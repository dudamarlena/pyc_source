# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/executors/dask_executor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3509 bytes
import distributed, subprocess, warnings
from airflow import configuration
from airflow.executors.base_executor import BaseExecutor

class DaskExecutor(BaseExecutor):
    """DaskExecutor"""

    def __init__(self, cluster_address=None):
        if cluster_address is None:
            cluster_address = configuration.conf.get('dask', 'cluster_address')
        if not cluster_address:
            raise ValueError('Please provide a Dask cluster address in airflow.cfg')
        self.cluster_address = cluster_address
        self.tls_ca = configuration.get('dask', 'tls_ca')
        self.tls_key = configuration.get('dask', 'tls_key')
        self.tls_cert = configuration.get('dask', 'tls_cert')
        super(DaskExecutor, self).__init__(parallelism=0)

    def start(self):
        if self.tls_ca or self.tls_key or self.tls_cert:
            from distributed.security import Security
            security = Security(tls_client_key=(self.tls_key),
              tls_client_cert=(self.tls_cert),
              tls_ca_file=(self.tls_ca),
              require_encryption=True)
        else:
            security = None
        self.client = distributed.Client((self.cluster_address), security=security)
        self.futures = {}

    def execute_async(self, key, command, queue=None, executor_config=None):
        if queue is not None:
            warnings.warn('DaskExecutor does not support queues. All tasks will be run in the same cluster')

        def airflow_run():
            return subprocess.check_call(command, close_fds=True)

        future = self.client.submit(airflow_run, pure=False)
        self.futures[future] = key

    def _process_future(self, future):
        if future.done():
            key = self.futures[future]
            if future.exception():
                self.log.error('Failed to execute task: %s', repr(future.exception()))
                self.fail(key)
            else:
                if future.cancelled():
                    self.log.error('Failed to execute task')
                    self.fail(key)
                else:
                    self.success(key)
            self.futures.pop(future)

    def sync(self):
        for future in self.futures.copy():
            self._process_future(future)

    def end(self):
        for future in distributed.as_completed(self.futures.copy()):
            self._process_future(future)

    def terminate(self):
        self.client.cancel(self.futures.keys())
        self.end()