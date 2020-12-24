# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/s3_task_handler.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 7043 bytes
import os
from cached_property import cached_property
from airflow import configuration
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.log.file_task_handler import FileTaskHandler

class S3TaskHandler(FileTaskHandler, LoggingMixin):
    __doc__ = '\n    S3TaskHandler is a python log handler that handles and reads\n    task instance logs. It extends airflow FileTaskHandler and\n    uploads to and reads from S3 remote storage.\n    '

    def __init__(self, base_log_folder, s3_log_folder, filename_template):
        super(S3TaskHandler, self).__init__(base_log_folder, filename_template)
        self.remote_base = s3_log_folder
        self.log_relative_path = ''
        self._hook = None
        self.closed = False
        self.upload_on_close = True

    @cached_property
    def hook(self):
        remote_conn_id = configuration.conf.get('core', 'REMOTE_LOG_CONN_ID')
        try:
            from airflow.hooks.S3_hook import S3Hook
            return S3Hook(remote_conn_id)
        except Exception:
            self.log.error('Could not create an S3Hook with connection id "%s". Please make sure that airflow[s3] is installed and the S3 connection exists.', remote_conn_id)

    def set_context(self, ti):
        super(S3TaskHandler, self).set_context(ti)
        self.log_relative_path = self._render_filename(ti, ti.try_number)
        self.upload_on_close = not ti.raw

    def close(self):
        if self.closed:
            return
        else:
            super(S3TaskHandler, self).close()
            if not self.upload_on_close:
                return
            local_loc = os.path.join(self.local_base, self.log_relative_path)
            remote_loc = os.path.join(self.remote_base, self.log_relative_path)
            if os.path.exists(local_loc):
                with open(local_loc, 'r') as (logfile):
                    log = logfile.read()
                self.s3_write(log, remote_loc)
        self.closed = True

    def _read(self, ti, try_number, metadata=None):
        """
        Read logs of given task instance and try_number from S3 remote storage.
        If failed, read the log from task instance host machine.
        :param ti: task instance object
        :param try_number: task instance try_number to read logs from
        :param metadata: log metadata,
                         can be used for steaming log reading and auto-tailing.
        """
        log_relative_path = self._render_filename(ti, try_number)
        remote_loc = os.path.join(self.remote_base, log_relative_path)
        if self.s3_log_exists(remote_loc):
            remote_log = self.s3_read(remote_loc, return_error=True)
            log = '*** Reading remote log from {}.\n{}\n'.format(remote_loc, remote_log)
            return (
             log, {'end_of_log': True})
        else:
            return super(S3TaskHandler, self)._read(ti, try_number)

    def s3_log_exists(self, remote_log_location):
        """
        Check if remote_log_location exists in remote storage
        :param remote_log_location: log's location in remote storage
        :return: True if location exists else False
        """
        try:
            return self.hook.get_key(remote_log_location) is not None
        except Exception:
            pass

        return False

    def s3_read(self, remote_log_location, return_error=False):
        """
        Returns the log found at the remote_log_location. Returns '' if no
        logs are found or there is an error.
        :param remote_log_location: the log's location in remote storage
        :type remote_log_location: str (path)
        :param return_error: if True, returns a string error message if an
            error occurs. Otherwise returns '' when an error occurs.
        :type return_error: bool
        """
        try:
            return self.hook.read_key(remote_log_location)
        except Exception:
            msg = 'Could not read logs from {}'.format(remote_log_location)
            self.log.exception(msg)
            if return_error:
                return msg

    def s3_write(self, log, remote_log_location, append=True):
        """
        Writes the log to the remote_log_location. Fails silently if no hook
        was created.
        :param log: the log to write to the remote_log_location
        :type log: str
        :param remote_log_location: the log's location in remote storage
        :type remote_log_location: str (path)
        :param append: if False, any existing log file is overwritten. If True,
            the new log is appended to any existing logs.
        :type append: bool
        """
        if append:
            if self.s3_log_exists(remote_log_location):
                old_log = self.s3_read(remote_log_location)
                log = '\n'.join([old_log, log]) if old_log else log
        try:
            self.hook.load_string(log,
              key=remote_log_location,
              replace=True,
              encrypt=(configuration.conf.getboolean('core', 'ENCRYPT_S3_LOGS')))
        except Exception:
            self.log.exception('Could not write logs to %s', remote_log_location)