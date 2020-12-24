# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 9058 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
WILDCARD = '*'

class GoogleCloudStorageToGoogleCloudStorageOperator(BaseOperator):
    """GoogleCloudStorageToGoogleCloudStorageOperator"""
    template_fields = ('source_bucket', 'source_object', 'destination_bucket', 'destination_object')
    ui_color = '#f0eee4'

    @apply_defaults
    def __init__(self, source_bucket, source_object, destination_bucket=None, destination_object=None, move_object=False, google_cloud_storage_conn_id='google_cloud_default', delegate_to=None, last_modified_time=None, *args, **kwargs):
        (super(GoogleCloudStorageToGoogleCloudStorageOperator, self).__init__)(*args, **kwargs)
        self.source_bucket = source_bucket
        self.source_object = source_object
        self.destination_bucket = destination_bucket
        self.destination_object = destination_object
        self.move_object = move_object
        self.google_cloud_storage_conn_id = google_cloud_storage_conn_id
        self.delegate_to = delegate_to
        self.last_modified_time = last_modified_time

    def execute(self, context):
        hook = GoogleCloudStorageHook(google_cloud_storage_conn_id=(self.google_cloud_storage_conn_id),
          delegate_to=(self.delegate_to))
        if self.destination_bucket is None:
            self.log.warning('destination_bucket is None. Defaulting it to source_bucket (%s)', self.source_bucket)
            self.destination_bucket = self.source_bucket
        else:
            if WILDCARD in self.source_object:
                total_wildcards = self.source_object.count(WILDCARD)
                if total_wildcards > 1:
                    error_msg = "Only one wildcard '*' is allowed in source_object parameter. Found {} in {}.".format(total_wildcards, self.source_object)
                    raise AirflowException(error_msg)
                prefix, delimiter = self.source_object.split(WILDCARD, 1)
                objects = hook.list((self.source_bucket), prefix=prefix, delimiter=delimiter)
                for source_object in objects:
                    if self.destination_object is None:
                        destination_object = source_object
                    else:
                        destination_object = source_object.replace(prefix, self.destination_object, 1)
                    self._copy_single_object(hook=hook, source_object=source_object, destination_object=destination_object)

            else:
                self._copy_single_object(hook=hook, source_object=(self.source_object), destination_object=(self.destination_object))

    def _copy_single_object(self, hook, source_object, destination_object):
        if self.last_modified_time is not None:
            if hook.is_updated_after(self.source_bucket, source_object, self.last_modified_time):
                self.log.debug('Object has been modified after %s ', self.last_modified_time)
            else:
                return
        self.log.info('Executing copy of gs://%s/%s to gs://%s/%s', self.source_bucket, source_object, self.destination_bucket, destination_object)
        hook.rewrite(self.source_bucket, source_object, self.destination_bucket, destination_object)
        if self.move_object:
            hook.delete(self.source_bucket, source_object)