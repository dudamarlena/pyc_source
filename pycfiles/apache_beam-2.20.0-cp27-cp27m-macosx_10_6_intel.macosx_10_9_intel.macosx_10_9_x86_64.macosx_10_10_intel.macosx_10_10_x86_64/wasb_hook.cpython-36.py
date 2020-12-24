# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/wasb_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 7540 bytes
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from azure.storage.blob import BlockBlobService

class WasbHook(BaseHook):
    """WasbHook"""

    def __init__(self, wasb_conn_id='wasb_default'):
        self.conn_id = wasb_conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        """Return the BlockBlobService object."""
        conn = self.get_connection(self.conn_id)
        service_options = conn.extra_dejson
        return BlockBlobService(account_name=conn.login, account_key=conn.password, **service_options)

    def check_for_blob(self, container_name, blob_name, **kwargs):
        """
        Check if a blob exists on Azure Blob Storage.

        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.exists()` takes.
        :type kwargs: object
        :return: True if the blob exists, False otherwise.
        :rtype: bool
        """
        return (self.connection.exists)(container_name, blob_name, **kwargs)

    def check_for_prefix(self, container_name, prefix, **kwargs):
        """
        Check if a prefix exists on Azure Blob storage.

        :param container_name: Name of the container.
        :type container_name: str
        :param prefix: Prefix of the blob.
        :type prefix: str
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.list_blobs()` takes.
        :type kwargs: object
        :return: True if blobs matching the prefix exist, False otherwise.
        :rtype: bool
        """
        matches = (self.connection.list_blobs)(container_name, prefix, num_results=1, **kwargs)
        return len(list(matches)) > 0

    def load_file(self, file_path, container_name, blob_name, **kwargs):
        """
        Upload a file to Azure Blob Storage.

        :param file_path: Path to the file to load.
        :type file_path: str
        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.create_blob_from_path()` takes.
        :type kwargs: object
        """
        (self.connection.create_blob_from_path)(container_name, blob_name, 
         file_path, **kwargs)

    def load_string(self, string_data, container_name, blob_name, **kwargs):
        """
        Upload a string to Azure Blob Storage.

        :param string_data: String to load.
        :type string_data: str
        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.create_blob_from_text()` takes.
        :type kwargs: object
        """
        (self.connection.create_blob_from_text)(container_name, blob_name, 
         string_data, **kwargs)

    def get_file(self, file_path, container_name, blob_name, **kwargs):
        """
        Download a file from Azure Blob Storage.

        :param file_path: Path to the file to download.
        :type file_path: str
        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.create_blob_from_path()` takes.
        :type kwargs: object
        """
        return (self.connection.get_blob_to_path)(container_name, blob_name, 
         file_path, **kwargs)

    def read_file(self, container_name, blob_name, **kwargs):
        """
        Read a file from Azure Blob Storage and return as a string.

        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.create_blob_from_path()` takes.
        :type kwargs: object
        """
        return (self.connection.get_blob_to_text)(container_name, 
         blob_name, **kwargs).content

    def delete_file(self, container_name, blob_name, is_prefix=False, ignore_if_missing=False, **kwargs):
        """
        Delete a file from Azure Blob Storage.

        :param container_name: Name of the container.
        :type container_name: str
        :param blob_name: Name of the blob.
        :type blob_name: str
        :param is_prefix: If blob_name is a prefix, delete all matching files
        :type is_prefix: bool
        :param ignore_if_missing: if True, then return success even if the
            blob does not exist.
        :type ignore_if_missing: bool
        :param kwargs: Optional keyword arguments that
            `BlockBlobService.create_blob_from_path()` takes.
        :type kwargs: object
        """
        if is_prefix:
            blobs_to_delete = [blob.name for blob in (self.connection.list_blobs)(
 container_name, prefix=blob_name, **kwargs)]
        else:
            if self.check_for_blob(container_name, blob_name):
                blobs_to_delete = [
                 blob_name]
            else:
                blobs_to_delete = []
        if not ignore_if_missing:
            if len(blobs_to_delete) == 0:
                raise AirflowException('Blob(s) not found: {}'.format(blob_name))
        for blob_uri in blobs_to_delete:
            self.log.info('Deleting blob: ' + blob_uri)
            (self.connection.delete_blob)(container_name,
 blob_uri, delete_snapshots='include', **kwargs)