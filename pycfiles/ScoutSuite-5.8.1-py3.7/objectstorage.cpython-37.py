# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/oci/facade/objectstorage.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 2102 bytes
from oci.object_storage import ObjectStorageClient
from ScoutSuite.providers.oci.authentication_strategy import OracleCredentials
from oci.pagination import list_call_get_all_results
from ScoutSuite.providers.utils import run_concurrently
from ScoutSuite.core.console import print_exception

class ObjectStorageFacade:

    def __init__(self, credentials: OracleCredentials):
        self._credentials = credentials
        self._client = ObjectStorageClient(self._credentials.config)

    async def get_namespace(self):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._client.get_namespace))
            return ''.join(response.data)
        except Exception as e:
            try:
                print_exception('Failed to get Object Storage namespace: {}'.format(e))
                return
            finally:
                e = None
                del e

    async def get_bucket_details(self, namespace, bucket_name):
        try:
            response = await run_concurrently(lambda : self._client.get_bucket(namespace, bucket_name))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to get Object Storage bucket details: {}'.format(e))
                return
            finally:
                e = None
                del e

    async def get_buckets(self, namespace):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._client.list_buckets, namespace, self._credentials.get_scope()))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to get Object Storage buckets: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def get_bucket_objects(self, namespace, bucket_name):
        try:
            response = await run_concurrently(lambda : list_call_get_all_results(self._client.list_objects, namespace, bucket_name))
            return response.data
        except Exception as e:
            try:
                print_exception('Failed to get Object Storage bucket objects: {}'.format(e))
                return []
            finally:
                e = None
                del e