# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/gcs_task_handler.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 7527 bytes
import os
from cached_property import cached_property
from airflow import configuration
from airflow.exceptions import AirflowException
from airflow.utils.log.logging_mixin import LoggingMixin
from airflow.utils.log.file_task_handler import FileTaskHandler

class GCSTaskHandler(FileTaskHandler, LoggingMixin):
    __doc__ = "\n    GCSTaskHandler is a python log handler that handles and reads\n    task instance logs. It extends airflow FileTaskHandler and\n    uploads to and reads from GCS remote storage. Upon log reading\n    failure, it reads from host machine's local disk.\n    "

    def __init__(self, base_log_folder, gcs_log_folder, filename_template):
        super(GCSTaskHandler, self).__init__(base_log_folder, filename_template)
        self.remote_base = gcs_log_folder
        self.log_relative_path = ''
        self._hook = None
        self.closed = False
        self.upload_on_close = True

    @cached_property
    def hook(self):
        remote_conn_id = configuration.conf.get('core', 'REMOTE_LOG_CONN_ID')
        try:
            from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
            return GoogleCloudStorageHook(google_cloud_storage_conn_id=remote_conn_id)
        except Exception as e:
            self.log.error('Could not create a GoogleCloudStorageHook with connection id "%s". %s\n\nPlease make sure that airflow[gcp] is installed and the GCS connection exists.', remote_conn_id, str(e))

    def set_context(self, ti):
        super(GCSTaskHandler, self).set_context(ti)
        self.log_relative_path = self._render_filename(ti, ti.try_number)
        self.upload_on_close = not ti.raw

    def close(self):
        if self.closed:
            return
        else:
            super(GCSTaskHandler, self).close()
            if not self.upload_on_close:
                return
            local_loc = os.path.join(self.local_base, self.log_relative_path)
            remote_loc = os.path.join(self.remote_base, self.log_relative_path)
            if os.path.exists(local_loc):
                with open(local_loc, 'r') as (logfile):
                    log = logfile.read()
                self.gcs_write(log, remote_loc)
        self.closed = True

    def _read(self, ti, try_number, metadata=None):
        """
        Read logs of given task instance and try_number from GCS.
        If failed, read the log from task instance host machine.
        :param ti: task instance object
        :param try_number: task instance try_number to read logs from
        :param metadata: log metadata,
                         can be used for steaming log reading and auto-tailing.
        """
        log_relative_path = self._render_filename(ti, try_number)
        remote_loc = os.path.join(self.remote_base, log_relative_path)
        try:
            remote_log = self.gcs_read(remote_loc)
            log = '*** Reading remote log from {}.\n{}\n'.format(remote_loc, remote_log)
            return (log, {'end_of_log': True})
        except Exception as e:
            log = '*** Unable to read remote log from {}\n*** {}\n\n'.format(remote_loc, str(e))
            self.log.error(log)
            local_log, metadata = super(GCSTaskHandler, self)._read(ti, try_number)
            log += local_log
            return (log, metadata)

    def gcs_read(self, remote_log_location):
        """
        Returns the log found at the remote_log_location.
        :param remote_log_location: the log's location in remote storage
        :type remote_log_location: str (path)
        """
        bkt, blob = self.parse_gcs_url(remote_log_location)
        return self.hook.download(bkt, blob).decode()

    def gcs_write(self, log, remote_log_location, append=True):
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
            try:
                old_log = self.gcs_read(remote_log_location)
                log = '\n'.join([old_log, log]) if old_log else log
            except Exception as e:
                if not hasattr(e, 'resp') or e.resp.get('status') != '404':
                    log = '*** Previous log discarded: {}\n\n'.format(str(e)) + log

        try:
            bkt, blob = self.parse_gcs_url(remote_log_location)
            from tempfile import NamedTemporaryFile
            with NamedTemporaryFile(mode='w+') as (tmpfile):
                tmpfile.write(log)
                tmpfile.flush()
                self.hook.upload(bkt, blob, tmpfile.name)
        except Exception as e:
            self.log.error('Could not write logs to %s: %s', remote_log_location, e)

    @staticmethod
    def parse_gcs_url(gsurl):
        """
        Given a Google Cloud Storage URL (gs://<bucket>/<blob>), returns a
        tuple containing the corresponding bucket and blob.
        """
        try:
            from urllib.parse import urlparse
        except ImportError:
            from urlparse import urlparse

        parsed_url = urlparse(gsurl)
        if not parsed_url.netloc:
            raise AirflowException('Please provide a bucket name')
        else:
            bucket = parsed_url.netloc
            blob = parsed_url.path.strip('/')
            return (bucket, blob)