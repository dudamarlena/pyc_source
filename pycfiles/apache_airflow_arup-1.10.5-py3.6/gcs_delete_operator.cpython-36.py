# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_delete_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3200 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageDeleteOperator(BaseOperator):
    __doc__ = '\n    Deletes objects from a Google Cloud Storage bucket, either\n    from an explicit list of object names or all objects\n    matching a prefix.\n\n    :param bucket_name: The GCS bucket to delete from\n    :type bucket_name: str\n    :param objects: List of objects to delete. These should be the names\n        of objects in the bucket, not including gs://bucket/\n    :type objects: List[str]\n    :param prefix: Prefix of objects to delete. All objects matching this\n        prefix in the bucket will be deleted.\n    :param google_cloud_storage_conn_id: The connection ID to use for\n        Google Cloud Storage\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    '
    template_fields = ('bucket_name', 'prefix', 'objects')

    @apply_defaults
    def __init__(self, bucket_name, objects=None, prefix=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        self.bucket_name = bucket_name
        self.objects = objects
        self.prefix = prefix
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        if not objects is not None:
            if not prefix is not None:
                raise AssertionError
        (super(GoogleCloudStorageDeleteOperator, self).__init__)(*args, **kwargs)

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        if self.objects:
            objects = self.objects
        else:
            objects = hook.list(bucket=(self.bucket_name), prefix=(self.prefix))
        self.log.info('Deleting %s objects from %s', len(objects), self.bucket_name)
        for object_name in objects:
            hook.delete(bucket=(self.bucket_name), object=object_name)