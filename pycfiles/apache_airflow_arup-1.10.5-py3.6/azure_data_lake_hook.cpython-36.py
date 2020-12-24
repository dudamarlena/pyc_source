# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/azure_data_lake_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 6397 bytes
from airflow.hooks.base_hook import BaseHook
from azure.datalake.store import core, lib, multithread

class AzureDataLakeHook(BaseHook):
    __doc__ = '\n    Interacts with Azure Data Lake.\n\n    Client ID and client secret should be in user and password parameters.\n    Tenant and account name should be extra field as\n    {"tenant": "<TENANT>", "account_name": "ACCOUNT_NAME"}.\n\n    :param azure_data_lake_conn_id: Reference to the Azure Data Lake connection.\n    :type azure_data_lake_conn_id: str\n    '

    def __init__(self, azure_data_lake_conn_id='azure_data_lake_default'):
        self.conn_id = azure_data_lake_conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        """Return a AzureDLFileSystem object."""
        conn = self.get_connection(self.conn_id)
        service_options = conn.extra_dejson
        self.account_name = service_options.get('account_name')
        adlCreds = lib.auth(tenant_id=(service_options.get('tenant')), client_secret=(conn.password),
          client_id=(conn.login))
        adlsFileSystemClient = core.AzureDLFileSystem(adlCreds, store_name=(self.account_name))
        adlsFileSystemClient.connect()
        return adlsFileSystemClient

    def check_for_file(self, file_path):
        """
        Check if a file exists on Azure Data Lake.

        :param file_path: Path and name of the file.
        :type file_path: str
        :return: True if the file exists, False otherwise.
        :rtype: bool
        """
        try:
            files = self.connection.glob(file_path, details=False, invalidate_cache=True)
            return len(files) == 1
        except FileNotFoundError:
            return False

    def upload_file(self, local_path, remote_path, nthreads=64, overwrite=True, buffersize=4194304, blocksize=4194304):
        """
        Upload a file to Azure Data Lake.

        :param local_path: local path. Can be single file, directory (in which case,
            upload recursively) or glob pattern. Recursive glob patterns using `**`
            are not supported.
        :type local_path: str
        :param remote_path: Remote path to upload to; if multiple files, this is the
            directory root to write within.
        :type remote_path: str
        :param nthreads: Number of threads to use. If None, uses the number of cores.
        :type nthreads: int
        :param overwrite: Whether to forcibly overwrite existing files/directories.
            If False and remote path is a directory, will quit regardless if any files
            would be overwritten or not. If True, only matching filenames are actually
            overwritten.
        :type overwrite: bool
        :param buffersize: int [2**22]
            Number of bytes for internal buffer. This block cannot be bigger than
            a chunk and cannot be smaller than a block.
        :type buffersize: int
        :param blocksize: int [2**22]
            Number of bytes for a block. Within each chunk, we write a smaller
            block for each API call. This block cannot be bigger than a chunk.
        :type blocksize: int
        """
        multithread.ADLUploader((self.connection), lpath=local_path,
          rpath=remote_path,
          nthreads=nthreads,
          overwrite=overwrite,
          buffersize=buffersize,
          blocksize=blocksize)

    def download_file(self, local_path, remote_path, nthreads=64, overwrite=True, buffersize=4194304, blocksize=4194304):
        """
        Download a file from Azure Blob Storage.

        :param local_path: local path. If downloading a single file, will write to this
            specific file, unless it is an existing directory, in which case a file is
            created within it. If downloading multiple files, this is the root
            directory to write within. Will create directories as required.
        :type local_path: str
        :param remote_path: remote path/globstring to use to find remote files.
            Recursive glob patterns using `**` are not supported.
        :type remote_path: str
        :param nthreads: Number of threads to use. If None, uses the number of cores.
        :type nthreads: int
        :param overwrite: Whether to forcibly overwrite existing files/directories.
            If False and remote path is a directory, will quit regardless if any files
            would be overwritten or not. If True, only matching filenames are actually
            overwritten.
        :type overwrite: bool
        :param buffersize: int [2**22]
            Number of bytes for internal buffer. This block cannot be bigger than
            a chunk and cannot be smaller than a block.
        :type buffersize: int
        :param blocksize: int [2**22]
            Number of bytes for a block. Within each chunk, we write a smaller
            block for each API call. This block cannot be bigger than a chunk.
        :type blocksize: int
        """
        multithread.ADLDownloader((self.connection), lpath=local_path,
          rpath=remote_path,
          nthreads=nthreads,
          overwrite=overwrite,
          buffersize=buffersize,
          blocksize=blocksize)