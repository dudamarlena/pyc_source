# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/operators/winrm_operator.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 5787 bytes
from base64 import b64encode
import logging
from winrm.exceptions import WinRMOperationTimeoutError
from airflow import configuration
from airflow.contrib.hooks.winrm_hook import WinRMHook
from airflow.exceptions import AirflowException
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults
logging.getLogger('urllib3.connectionpool').setLevel(logging.ERROR)

class WinRMOperator(BaseOperator):
    __doc__ = '\n    WinRMOperator to execute commands on given remote host using the winrm_hook.\n\n    :param winrm_hook: predefined ssh_hook to use for remote execution\n    :type winrm_hook: airflow.contrib.hooks.winrm_hook.WinRMHook\n    :param ssh_conn_id: connection id from airflow Connections\n    :type ssh_conn_id: str\n    :param remote_host: remote host to connect\n    :type remote_host: str\n    :param command: command to execute on remote host. (templated)\n    :type command: str\n    :param timeout: timeout for executing the command.\n    :type timeout: int\n    :param do_xcom_push: return the stdout which also get set in xcom by airflow platform\n    :type do_xcom_push: bool\n    '
    template_fields = ('command', )

    @apply_defaults
    def __init__(self, winrm_hook=None, ssh_conn_id=None, remote_host=None, command=None, timeout=10, do_xcom_push=False, *args, **kwargs):
        (super(WinRMOperator, self).__init__)(*args, **kwargs)
        self.winrm_hook = winrm_hook
        self.ssh_conn_id = ssh_conn_id
        self.remote_host = remote_host
        self.command = command
        self.timeout = timeout
        self.do_xcom_push = do_xcom_push

    def execute(self, context):
        if self.ssh_conn_id:
            if not self.winrm_hook:
                self.log.info('Hook not found, creating...')
                self.winrm_hook = WinRMHook(ssh_conn_id=(self.ssh_conn_id))
            else:
                if not self.winrm_hook:
                    raise AirflowException('Cannot operate without winrm_hook or ssh_conn_id.')
                if self.remote_host is not None:
                    self.winrm_hook.remote_host = self.remote_host
            if not self.command:
                raise AirflowException('No command specified so nothing to execute here.')
        else:
            winrm_client = self.winrm_hook.get_conn()
            try:
                self.log.info("Running command: '%s'...", self.command)
                command_id = self.winrm_hook.winrm_protocol.run_command(winrm_client, self.command)
                stdout_buffer = []
                stderr_buffer = []
                command_done = False
                while not command_done:
                    try:
                        stdout, stderr, return_code, command_done = self.winrm_hook.winrm_protocol._raw_get_command_output(winrm_client, command_id)
                        if self.do_xcom_push:
                            stdout_buffer.append(stdout)
                        stderr_buffer.append(stderr)
                        for line in stdout.decode('utf-8').splitlines():
                            self.log.info(line)

                        for line in stderr.decode('utf-8').splitlines():
                            self.log.warning(line)

                    except WinRMOperationTimeoutError:
                        pass

                self.winrm_hook.winrm_protocol.cleanup_command(winrm_client, command_id)
                self.winrm_hook.winrm_protocol.close_shell(winrm_client)
            except Exception as e:
                raise AirflowException('WinRM operator error: {0}'.format(str(e)))

            if return_code == 0:
                if self.do_xcom_push:
                    enable_pickling = configuration.conf.getboolean('core', 'enable_xcom_pickling')
                    if enable_pickling:
                        return stdout_buffer
                    else:
                        return b64encode((b'').join(stdout_buffer)).decode('utf-8')
            else:
                error_msg = 'Error running cmd: {0}, return code: {1}, error: {2}'.format(self.command, return_code, (b'').join(stderr_buffer).decode('utf-8'))
                raise AirflowException(error_msg)
        self.log.info('Finished!')
        return True