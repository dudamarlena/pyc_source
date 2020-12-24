# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/webhdfs_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5124 bytes
from hdfs import InsecureClient, HdfsError
from airflow import configuration
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin
_kerberos_security_mode = configuration.conf.get('core', 'security') == 'kerberos'
if _kerberos_security_mode:
    try:
        from hdfs.ext.kerberos import KerberosClient
    except ImportError:
        log = LoggingMixin().log
        log.error('Could not load the Kerberos extension for the WebHDFSHook.')
        raise

class AirflowWebHDFSHookException(AirflowException):
    pass


class WebHDFSHook(BaseHook):
    __doc__ = '\n    Interact with HDFS. This class is a wrapper around the hdfscli library.\n\n    :param webhdfs_conn_id: The connection id for the webhdfs client to connect to.\n    :type webhdfs_conn_id: str\n    :param proxy_user: The user used to authenticate.\n    :type proxy_user: str\n    '

    def __init__(self, webhdfs_conn_id='webhdfs_default', proxy_user=None):
        super(WebHDFSHook, self).__init__(webhdfs_conn_id)
        self.webhdfs_conn_id = webhdfs_conn_id
        self.proxy_user = proxy_user

    def get_conn(self):
        """
        Establishes a connection depending on the security mode set via config or environment variable.

        :return: a hdfscli InsecureClient or KerberosClient object.
        :rtype: hdfs.InsecureClient or hdfs.ext.kerberos.KerberosClient
        """
        connections = self.get_connections(self.webhdfs_conn_id)
        for connection in connections:
            try:
                self.log.debug('Trying namenode %s', connection.host)
                client = self._get_client(connection)
                client.status('/')
                self.log.debug('Using namenode %s for hook', connection.host)
                return client
            except HdfsError as hdfs_error:
                self.log.debug('Read operation on namenode %s failed with error: %s', connection.host, hdfs_error)

        hosts = [connection.host for connection in connections]
        error_message = 'Read operations failed on the namenodes below:\n{hosts}'.format(hosts=('\n'.join(hosts)))
        raise AirflowWebHDFSHookException(error_message)

    def _get_client(self, connection):
        connection_str = 'http://{host}:{port}'.format(host=(connection.host), port=(connection.port))
        if _kerberos_security_mode:
            client = KerberosClient(connection_str)
        else:
            proxy_user = self.proxy_user or connection.login
            client = InsecureClient(connection_str, user=proxy_user)
        return client

    def check_for_path(self, hdfs_path):
        """
        Check for the existence of a path in HDFS by querying FileStatus.

        :param hdfs_path: The path to check.
        :type hdfs_path: str
        :return: True if the path exists and False if not.
        :rtype: bool
        """
        conn = self.get_conn()
        status = conn.status(hdfs_path, strict=False)
        return bool(status)

    def load_file(self, source, destination, overwrite=True, parallelism=1, **kwargs):
        r"""
        Uploads a file to HDFS.

        :param source: Local path to file or folder.
            If it's a folder, all the files inside of it will be uploaded.
            .. note:: This implies that folders empty of files will not be created remotely.

        :type source: str
        :param destination: PTarget HDFS path.
            If it already exists and is a directory, files will be uploaded inside.
        :type destination: str
        :param overwrite: Overwrite any existing file or directory.
        :type overwrite: bool
        :param parallelism: Number of threads to use for parallelization.
            A value of `0` (or negative) uses as many threads as there are files.
        :type parallelism: int
        :param \**kwargs: Keyword arguments forwarded to :meth:`hdfs.client.Client.upload`.
        """
        conn = self.get_conn()
        (conn.upload)(hdfs_path=destination, local_path=source, 
         overwrite=overwrite, 
         n_threads=parallelism, **kwargs)
        self.log.debug('Uploaded file %s to %s', source, destination)