# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/providers/gcp/facade/cloudstorage.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 1447 bytes
from google.cloud import storage
from ScoutSuite.core.console import print_exception
from ScoutSuite.providers.utils import run_concurrently, get_and_set_concurrently

class CloudStorageFacade:

    async def get_buckets(self, project_id: str):
        try:
            client = storage.Client(project=project_id)
            buckets = await run_concurrently(lambda : list(client.list_buckets()))
            await get_and_set_concurrently([self._get_and_set_bucket_logging,
             self._get_and_set_bucket_iam_policy], buckets)
            return buckets
        except Exception as e:
            try:
                print_exception('Failed to retrieve storage buckets: {}'.format(e))
                return []
            finally:
                e = None
                del e

    async def _get_and_set_bucket_logging(self, bucket):
        try:
            bucket_logging = await run_concurrently(lambda : bucket.get_logging())
            setattr(bucket, 'logging', bucket_logging)
        except Exception as e:
            try:
                print_exception('Failed to retrieve bucket logging: {}'.format(e))
                setattr(bucket, 'logging', None)
            finally:
                e = None
                del e

    async def _get_and_set_bucket_iam_policy(self, bucket):
        try:
            bucket_iam_policy = await run_concurrently(lambda : bucket.get_iam_policy())
            setattr(bucket, 'iam_policy', bucket_iam_policy)
        except Exception as e:
            try:
                print_exception('Failed to retrieve bucket IAM policy: {}'.format(e))
                setattr(bucket, 'iam_policy', None)
            finally:
                e = None
                del e