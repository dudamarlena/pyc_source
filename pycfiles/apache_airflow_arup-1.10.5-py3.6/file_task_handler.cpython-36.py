# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/file_task_handler.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 8848 bytes
import logging, os, requests
from airflow import configuration as conf
from airflow.configuration import AirflowConfigException
from airflow.utils.file import mkdirs
from airflow.utils.helpers import parse_template_string

class FileTaskHandler(logging.Handler):
    __doc__ = "\n    FileTaskHandler is a python log handler that handles and reads\n    task instance logs. It creates and delegates log handling\n    to `logging.FileHandler` after receiving task instance context.\n    It reads logs from task instance's host machine.\n    "

    def __init__(self, base_log_folder, filename_template):
        super(FileTaskHandler, self).__init__()
        self.handler = None
        self.local_base = base_log_folder
        self.filename_template, self.filename_jinja_template = parse_template_string(filename_template)

    def set_context(self, ti):
        """
        Provide task_instance context to airflow task handler.
        :param ti: task instance object
        """
        local_loc = self._init_file(ti)
        self.handler = logging.FileHandler(local_loc)
        self.handler.setFormatter(self.formatter)
        self.handler.setLevel(self.level)

    def emit(self, record):
        if self.handler is not None:
            self.handler.emit(record)

    def flush(self):
        if self.handler is not None:
            self.handler.flush()

    def close(self):
        if self.handler is not None:
            self.handler.close()

    def _render_filename(self, ti, try_number):
        if self.filename_jinja_template:
            jinja_context = ti.get_template_context()
            jinja_context['try_number'] = try_number
            return (self.filename_jinja_template.render)(**jinja_context)
        else:
            return self.filename_template.format(dag_id=(ti.dag_id), task_id=(ti.task_id),
              execution_date=(ti.execution_date.isoformat()),
              try_number=try_number)

    def _read(self, ti, try_number, metadata=None):
        """
        Template method that contains custom logic of reading
        logs given the try_number.
        :param ti: task instance record
        :param try_number: current try_number to read log from
        :param metadata: log metadata,
                         can be used for steaming log reading and auto-tailing.
        :return: log message as a string and metadata.
        """
        log_relative_path = self._render_filename(ti, try_number)
        location = os.path.join(self.local_base, log_relative_path)
        log = ''
        if os.path.exists(location):
            try:
                with open(location) as (f):
                    log += '*** Reading local file: {}\n'.format(location)
                    log += ''.join(f.readlines())
            except Exception as e:
                log = '*** Failed to load local log file: {}\n'.format(location)
                log += '*** {}\n'.format(str(e))

        else:
            url = os.path.join('http://{ti.hostname}:{worker_log_server_port}/log', log_relative_path).format(ti=ti,
              worker_log_server_port=(conf.get('celery', 'WORKER_LOG_SERVER_PORT')))
            log += '*** Log file does not exist: {}\n'.format(location)
            log += '*** Fetching from: {}\n'.format(url)
            try:
                timeout = None
                try:
                    timeout = conf.getint('webserver', 'log_fetch_timeout_sec')
                except (AirflowConfigException, ValueError):
                    pass

                response = requests.get(url, timeout=timeout)
                response.raise_for_status()
                log += '\n' + response.text
            except Exception as e:
                log += '*** Failed to fetch log file from worker. {}\n'.format(str(e))

            return (log, {'end_of_log': True})

    def read(self, task_instance, try_number=None, metadata=None):
        """
        Read logs of given task instance from local machine.
        :param task_instance: task instance object
        :param try_number: task instance try_number to read logs from. If None
                           it returns all logs separated by try_number
        :param metadata: log metadata,
                         can be used for steaming log reading and auto-tailing.
        :return: a list of logs
        """
        if try_number is None:
            next_try = task_instance.next_try_number
            try_numbers = list(range(1, next_try))
        else:
            if try_number < 1:
                logs = ['Error fetching the logs. Try number {} is invalid.'.format(try_number)]
                return logs
            try_numbers = [try_number]
        logs = [''] * len(try_numbers)
        metadatas = [{}] * len(try_numbers)
        for i, try_number in enumerate(try_numbers):
            log, metadata = self._read(task_instance, try_number, metadata)
            logs[i] += log
            metadatas[i] = metadata

        return (logs, metadatas)

    def _init_file(self, ti):
        """
        Create log directory and give it correct permissions.
        :param ti: task instance object
        :return: relative log path of the given task instance
        """
        relative_path = self._render_filename(ti, ti.try_number)
        full_path = os.path.join(self.local_base, relative_path)
        directory = os.path.dirname(full_path)
        if not os.path.exists(directory):
            mkdirs(directory, 511)
        if not os.path.exists(full_path):
            open(full_path, 'a').close()
            os.chmod(full_path, 438)
        return full_path