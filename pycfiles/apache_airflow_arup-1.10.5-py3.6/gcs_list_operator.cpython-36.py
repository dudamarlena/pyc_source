# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_list_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3703 bytes
from typing import Iterable
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class GoogleCloudStorageListOperator(BaseOperator):
    __doc__ = "\n    List all objects from the bucket with the give string prefix and delimiter in name.\n\n    This operator returns a python list with the name of objects which can be used by\n     `xcom` in the downstream task.\n\n    :param bucket: The Google cloud storage bucket to find the objects. (templated)\n    :type bucket: str\n    :param prefix: Prefix string which filters objects whose name begin with\n           this prefix. (templated)\n    :type prefix: str\n    :param delimiter: The delimiter by which you want to filter the objects. (templated)\n        For e.g to lists the CSV files from in a directory in GCS you would use\n        delimiter='.csv'.\n    :type delimiter: str\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google cloud storage.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n\n    **Example**:\n        The following Operator would list all the Avro files from ``sales/sales-2017``\n        folder in ``data`` bucket. ::\n\n            GCS_Files = GoogleCloudStorageListOperator(\n                task_id='GCS_Files',\n                bucket='data',\n                prefix='sales/sales-2017/',\n                delimiter='.avro',\n                google_cloud_storage_conn_id=google_cloud_conn_id\n            )\n    "
    template_fields = ('bucket', 'prefix', 'delimiter')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, bucket, prefix=None, delimiter=None, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, *args, **kwargs):
        (super(GoogleCloudStorageListOperator, self).__init__)(*args, **kwargs)
        self.bucket = bucket
        self.prefix = prefix
        self.delimiter = delimiter
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        self.log.info('Getting list of the files. Bucket: %s; Delimiter: %s; Prefix: %s', self.bucket, self.delimiter, self.prefix)
        return hook.list(bucket=(self.bucket), prefix=(self.prefix),
          delimiter=(self.delimiter))