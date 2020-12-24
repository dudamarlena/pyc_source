# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5151 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.version import version

class GoogleCloudStorageCreateBucketOperator(BaseOperator):
    __doc__ = "\n    Creates a new bucket. Google Cloud Storage uses a flat namespace,\n    so you can't create a bucket with a name that is already in use.\n\n        .. seealso::\n            For more information, see Bucket Naming Guidelines:\n            https://cloud.google.com/storage/docs/bucketnaming.html#requirements\n\n    :param bucket_name: The name of the bucket. (templated)\n    :type bucket_name: str\n    :param resource: An optional dict with parameters for creating the bucket.\n            For information on available parameters, see Cloud Storage API doc:\n            https://cloud.google.com/storage/docs/json_api/v1/buckets/insert\n    :type resource: dict\n    :param storage_class: This defines how objects in the bucket are stored\n            and determines the SLA and the cost of storage (templated). Values include\n\n            - ``MULTI_REGIONAL``\n            - ``REGIONAL``\n            - ``STANDARD``\n            - ``NEARLINE``\n            - ``COLDLINE``.\n\n            If this value is not specified when the bucket is\n            created, it will default to STANDARD.\n    :type storage_class: str\n    :param location: The location of the bucket. (templated)\n        Object data for objects in the bucket resides in physical storage\n        within this region. Defaults to US.\n\n        .. seealso:: https://developers.google.com/storage/docs/bucket-locations\n\n    :type location: str\n    :param project_id: The ID of the GCP Project. (templated)\n    :type project_id: str\n    :param labels: User-provided labels, in key/value pairs.\n    :type labels: dict\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google cloud storage.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must\n        have domain-wide delegation enabled.\n    :type delegate_to: str\n\n    The following Operator would create a new bucket ``test-bucket``\n    with ``MULTI_REGIONAL`` storage class in ``EU`` region\n\n    .. code-block:: python\n\n        CreateBucket = GoogleCloudStorageCreateBucketOperator(\n            task_id='CreateNewBucket',\n            bucket_name='test-bucket',\n            storage_class='MULTI_REGIONAL',\n            location='EU',\n            labels={'env': 'dev', 'team': 'airflow'},\n            google_cloud_storage_conn_id='airflow-service-account'\n        )\n\n    "
    template_fields = ('bucket_name', 'storage_class', 'location', 'project_id')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket_name, resource=None, storage_class='MULTI_REGIONAL', location='US', project_id=None, labels=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageCreateBucketOperator, self).__init__)(*args, **kwargs)
        self.bucket_name = bucket_name
        self.resource = resource
        self.storage_class = storage_class
        self.location = location
        self.project_id = project_id
        self.labels = labels
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        if self.labels is not None:
            self.labels.update({'airflow-version': 'v' + version.replace('.', '-').replace('+', '-')})
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        hook.create_bucket(bucket_name=(self.bucket_name), resource=(self.resource),
          storage_class=(self.storage_class),
          location=(self.location),
          project_id=(self.project_id),
          labels=(self.labels))