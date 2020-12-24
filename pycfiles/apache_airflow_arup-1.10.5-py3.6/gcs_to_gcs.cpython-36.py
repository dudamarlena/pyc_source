# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/gcs_to_gcs.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 9058 bytes
from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
from airflow.exceptions import AirflowException
WILDCARD = '*'

class GoogleCloudStorageToGoogleCloudStorageOperator(BaseOperator):
    __doc__ = "\n    Copies objects from a bucket to another, with renaming if requested.\n\n    :param source_bucket: The source Google cloud storage bucket where the\n         object is. (templated)\n    :type source_bucket: str\n    :param source_object: The source name of the object to copy in the Google cloud\n        storage bucket. (templated)\n        You can use only one wildcard for objects (filenames) within your\n        bucket. The wildcard can appear inside the object name or at the\n        end of the object name. Appending a wildcard to the bucket name is\n        unsupported.\n    :type source_object: str\n    :param destination_bucket: The destination Google cloud storage bucket\n        where the object should be. If the destination_bucket is None, it defaults\n        to source_bucket. (templated)\n    :type destination_bucket: str\n    :param destination_object: The destination name of the object in the\n        destination Google cloud storage bucket. (templated)\n        If a wildcard is supplied in the source_object argument, this is the\n        prefix that will be prepended to the final destination objects' paths.\n        Note that the source path's part before the wildcard will be removed;\n        if it needs to be retained it should be appended to destination_object.\n        For example, with prefix ``foo/*`` and destination_object ``blah/``, the\n        file ``foo/baz`` will be copied to ``blah/baz``; to retain the prefix write\n        the destination_object as e.g. ``blah/foo``, in which case the copied file\n        will be named ``blah/foo/baz``.\n    :type destination_object: str\n    :param move_object: When move object is True, the object is moved instead\n        of copied to the new location. This is the equivalent of a mv command\n        as opposed to a cp command.\n    :type move_object: bool\n    :param google_cloud_storage_conn_id: The connection ID to use when\n        connecting to Google cloud storage.\n    :type google_cloud_storage_conn_id: str\n    :param delegate_to: The account to impersonate, if any.\n        For this to work, the service account making the request must have\n        domain-wide delegation enabled.\n    :type delegate_to: str\n    :param last_modified_time: When specified, the objects will be copied or moved,\n        only if they were modified after last_modified_time.\n        If tzinfo has not been set, UTC will be assumed.\n    :type last_modified_time: datetime.datetime\n\n    :Example:\n\n    The following Operator would copy a single file named\n    ``sales/sales-2017/january.avro`` in the ``data`` bucket to the file named\n    ``copied_sales/2017/january-backup.avro`` in the ``data_backup`` bucket ::\n\n        copy_single_file = GoogleCloudStorageToGoogleCloudStorageOperator(\n            task_id='copy_single_file',\n            source_bucket='data',\n            source_object='sales/sales-2017/january.avro',\n            destination_bucket='data_backup',\n            destination_object='copied_sales/2017/january-backup.avro',\n            google_cloud_storage_conn_id=google_cloud_conn_id\n        )\n\n    The following Operator would copy all the Avro files from ``sales/sales-2017``\n    folder (i.e. with names starting with that prefix) in ``data`` bucket to the\n    ``copied_sales/2017`` folder in the ``data_backup`` bucket. ::\n\n        copy_files = GoogleCloudStorageToGoogleCloudStorageOperator(\n            task_id='copy_files',\n            source_bucket='data',\n            source_object='sales/sales-2017/*.avro',\n            destination_bucket='data_backup',\n            destination_object='copied_sales/2017/',\n            google_cloud_storage_conn_id=google_cloud_conn_id\n        )\n\n    The following Operator would move all the Avro files from ``sales/sales-2017``\n    folder (i.e. with names starting with that prefix) in ``data`` bucket to the\n    same folder in the ``data_backup`` bucket, deleting the original files in the\n    process. ::\n\n        move_files = GoogleCloudStorageToGoogleCloudStorageOperator(\n            task_id='move_files',\n            source_bucket='data',\n            source_object='sales/sales-2017/*.avro',\n            destination_bucket='data_backup',\n            move_object=True,\n            google_cloud_storage_conn_id=google_cloud_conn_id\n        )\n\n    "
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