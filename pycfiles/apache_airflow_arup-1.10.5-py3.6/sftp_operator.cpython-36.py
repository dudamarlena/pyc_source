# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/sftp_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 7840 bytes
import os
from airflow.contrib.hooks.ssh_hook import SSHHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class SFTPOperation(object):
    PUT = 'put'
    GET = 'get'


class SFTPOperator(BaseOperator):
    __doc__ = '\n    SFTPOperator for transferring files from remote host to local or vice a versa.\n    This operator uses ssh_hook to open sftp transport channel that serve as basis\n    for file transfer.\n\n    :param ssh_hook: predefined ssh_hook to use for remote execution.\n        Either `ssh_hook` or `ssh_conn_id` needs to be provided.\n    :type ssh_hook: airflow.contrib.hooks.ssh_hook.SSHHook\n    :param ssh_conn_id: connection id from airflow Connections.\n        `ssh_conn_id` will be ignored if `ssh_hook` is provided.\n    :type ssh_conn_id: str\n    :param remote_host: remote host to connect (templated)\n        Nullable. If provided, it will replace the `remote_host` which was\n        defined in `ssh_hook` or predefined in the connection of `ssh_conn_id`.\n    :type remote_host: str\n    :param local_filepath: local file path to get or put. (templated)\n    :type local_filepath: str\n    :param remote_filepath: remote file path to get or put. (templated)\n    :type remote_filepath: str\n    :param operation: specify operation \'get\' or \'put\', defaults to put\n    :type operation: str\n    :param confirm: specify if the SFTP operation should be confirmed, defaults to True\n    :type confirm: bool\n    :param create_intermediate_dirs: create missing intermediate directories when\n        copying from remote to local and vice-versa. Default is False.\n\n        Example: The following task would copy ``file.txt`` to the remote host\n        at ``/tmp/tmp1/tmp2/`` while creating ``tmp``,``tmp1`` and ``tmp2`` if they\n        don\'t exist. If the parameter is not passed it would error as the directory\n        does not exist. ::\n\n            put_file = SFTPOperator(\n                task_id="test_sftp",\n                ssh_conn_id="ssh_default",\n                local_filepath="/tmp/file.txt",\n                remote_filepath="/tmp/tmp1/tmp2/file.txt",\n                operation="put",\n                create_intermediate_dirs=True,\n                dag=dag\n            )\n\n    :type create_intermediate_dirs: bool\n    '
    template_fields = ('local_filepath', 'remote_filepath', 'remote_host')

    @apply_defaults
    def __init__(self, ssh_hook=None, ssh_conn_id=None, remote_host=None, local_filepath=None, remote_filepath=None, operation=SFTPOperation.PUT, confirm=True, create_intermediate_dirs=False, *args, **kwargs):
        (super(SFTPOperator, self).__init__)(*args, **kwargs)
        self.ssh_hook = ssh_hook
        self.ssh_conn_id = ssh_conn_id
        self.remote_host = remote_host
        self.local_filepath = local_filepath
        self.remote_filepath = remote_filepath
        self.operation = operation
        self.confirm = confirm
        self.create_intermediate_dirs = create_intermediate_dirs
        if not (self.operation.lower() == SFTPOperation.GET or self.operation.lower() == SFTPOperation.PUT):
            raise TypeError('unsupported operation value {0}, expected {1} or {2}'.format(self.operation, SFTPOperation.GET, SFTPOperation.PUT))

    def execute(self, context):
        file_msg = None
        try:
            if self.ssh_conn_id:
                if self.ssh_hook:
                    if isinstance(self.ssh_hook, SSHHook):
                        self.log.info('ssh_conn_id is ignored when ssh_hook is provided.')
                else:
                    self.log.info('ssh_hook is not provided or invalid. Trying ssh_conn_id to create SSHHook.')
                    self.ssh_hook = SSHHook(ssh_conn_id=(self.ssh_conn_id))
            else:
                if not self.ssh_hook:
                    raise AirflowException('Cannot operate without ssh_hook or ssh_conn_id.')
                if self.remote_host is not None:
                    self.log.info('remote_host is provided explicitly. It will replace the remote_host which was defined in ssh_hook or predefined in connection of ssh_conn_id.')
                    self.ssh_hook.remote_host = self.remote_host
            with self.ssh_hook.get_conn() as (ssh_client):
                sftp_client = ssh_client.open_sftp()
                if self.operation.lower() == SFTPOperation.GET:
                    local_folder = os.path.dirname(self.local_filepath)
                    if self.create_intermediate_dirs:
                        try:
                            os.makedirs(local_folder)
                        except OSError:
                            if not os.path.isdir(local_folder):
                                raise

                    file_msg = 'from {0} to {1}'.format(self.remote_filepath, self.local_filepath)
                    self.log.info('Starting to transfer %s', file_msg)
                    sftp_client.get(self.remote_filepath, self.local_filepath)
                else:
                    remote_folder = os.path.dirname(self.remote_filepath)
                    if self.create_intermediate_dirs:
                        _make_intermediate_dirs(sftp_client=sftp_client,
                          remote_directory=remote_folder)
                    file_msg = 'from {0} to {1}'.format(self.local_filepath, self.remote_filepath)
                    self.log.info('Starting to transfer file %s', file_msg)
                    sftp_client.put((self.local_filepath), (self.remote_filepath),
                      confirm=(self.confirm))
        except Exception as e:
            raise AirflowException('Error while transferring {0}, error: {1}'.format(file_msg, str(e)))

        return self.local_filepath


def _make_intermediate_dirs(sftp_client, remote_directory):
    """
    Create all the intermediate directories in a remote host

    :param sftp_client: A Paramiko SFTP client.
    :param remote_directory: Absolute Path of the directory containing the file
    :return:
    """
    if remote_directory == '/':
        sftp_client.chdir('/')
        return
    else:
        if remote_directory == '':
            return
        try:
            sftp_client.chdir(remote_directory)
        except IOError:
            dirname, basename = os.path.split(remote_directory.rstrip('/'))
            _make_intermediate_dirs(sftp_client, dirname)
            sftp_client.mkdir(basename)
            sftp_client.chdir(basename)
            return