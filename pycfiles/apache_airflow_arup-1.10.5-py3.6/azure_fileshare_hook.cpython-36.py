# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/azure_fileshare_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 8331 bytes
from airflow.hooks.base_hook import BaseHook
from azure.storage.file import FileService

class AzureFileShareHook(BaseHook):
    __doc__ = "\n    Interacts with Azure FileShare Storage.\n\n    Additional options passed in the 'extra' field of the connection will be\n    passed to the `FileService()` constructor.\n\n    :param wasb_conn_id: Reference to the wasb connection.\n    :type wasb_conn_id: str\n    "

    def __init__(self, wasb_conn_id='wasb_default'):
        self.conn_id = wasb_conn_id
        self.connection = self.get_conn()

    def get_conn(self):
        """Return the FileService object."""
        conn = self.get_connection(self.conn_id)
        service_options = conn.extra_dejson
        return FileService(account_name=conn.login, account_key=conn.password, **service_options)

    def check_for_directory(self, share_name, directory_name, **kwargs):
        """
        Check if a directory exists on Azure File Share.

        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.exists()` takes.
        :type kwargs: object
        :return: True if the file exists, False otherwise.
        :rtype: bool
        """
        return (self.connection.exists)(share_name, directory_name, **kwargs)

    def check_for_file(self, share_name, directory_name, file_name, **kwargs):
        """
        Check if a file exists on Azure File Share.

        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param file_name: Name of the file.
        :type file_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.exists()` takes.
        :type kwargs: object
        :return: True if the file exists, False otherwise.
        :rtype: bool
        """
        return (self.connection.exists)(share_name, directory_name, 
         file_name, **kwargs)

    def list_directories_and_files(self, share_name, directory_name=None, **kwargs):
        """
        Return the list of directories and files stored on a Azure File Share.

        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.list_directories_and_files()` takes.
        :type kwargs: object
        :return: A list of files and directories
        :rtype: list
        """
        return (self.connection.list_directories_and_files)(share_name, 
         directory_name, **kwargs)

    def create_directory(self, share_name, directory_name, **kwargs):
        """
        Create a new directory on a Azure File Share.

        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.create_directory()` takes.
        :type kwargs: object
        :return: A list of files and directories
        :rtype: list
        """
        return (self.connection.create_directory)(share_name, directory_name, **kwargs)

    def get_file(self, file_path, share_name, directory_name, file_name, **kwargs):
        """
        Download a file from Azure File Share.

        :param file_path: Where to store the file.
        :type file_path: str
        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param file_name: Name of the file.
        :type file_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.get_file_to_path()` takes.
        :type kwargs: object
        """
        (self.connection.get_file_to_path)(share_name, directory_name, 
         file_name, file_path, **kwargs)

    def get_file_to_stream(self, stream, share_name, directory_name, file_name, **kwargs):
        """
        Download a file from Azure File Share.

        :param stream: A filehandle to store the file to.
        :type stream: file-like object
        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param file_name: Name of the file.
        :type file_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.get_file_to_stream()` takes.
        :type kwargs: object
        """
        (self.connection.get_file_to_stream)(share_name, directory_name, 
         file_name, stream, **kwargs)

    def load_file(self, file_path, share_name, directory_name, file_name, **kwargs):
        """
        Upload a file to Azure File Share.

        :param file_path: Path to the file to load.
        :type file_path: str
        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param file_name: Name of the file.
        :type file_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.create_file_from_path()` takes.
        :type kwargs: object
        """
        (self.connection.create_file_from_path)(share_name, directory_name, 
         file_name, file_path, **kwargs)

    def load_string(self, string_data, share_name, directory_name, file_name, **kwargs):
        """
        Upload a string to Azure File Share.

        :param string_data: String to load.
        :type string_data: str
        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param file_name: Name of the file.
        :type file_name: str
        :param kwargs: Optional keyword arguments that
            `FileService.create_file_from_text()` takes.
        :type kwargs: object
        """
        (self.connection.create_file_from_text)(share_name, directory_name, 
         file_name, string_data, **kwargs)

    def load_stream(self, stream, share_name, directory_name, file_name, count, **kwargs):
        """
        Upload a stream to Azure File Share.

        :param stream: Opened file/stream to upload as the file content.
        :type stream: file-like
        :param share_name: Name of the share.
        :type share_name: str
        :param directory_name: Name of the directory.
        :type directory_name: str
        :param file_name: Name of the file.
        :type file_name: str
        :param count: Size of the stream in bytes
        :type count: int
        :param kwargs: Optional keyword arguments that
            `FileService.create_file_from_stream()` takes.
        :type kwargs: object
        """
        (self.connection.create_file_from_stream)(share_name, directory_name, 
         file_name, stream, count, **kwargs)