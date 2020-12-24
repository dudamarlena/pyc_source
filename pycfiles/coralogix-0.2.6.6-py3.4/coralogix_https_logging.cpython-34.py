# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\coralogix\coralogix_https_logging.py
# Compiled at: 2016-09-26 16:54:25
# Size of source mod 2**32: 17648 bytes
import sys, time, json, signal, logging, threading
from socket import getfqdn
from logging import Handler
try:
    from urllib.request import Request, urlopen
    from urllib.error import URLError, HTTPError
    from http.client import UNAUTHORIZED
    from queue import Queue, Empty
except ImportError:
    from urllib2 import Request, urlopen
    from urllib2 import URLError, HTTPError
    from httplib import UNAUTHORIZED
    from Queue import Queue, Empty

try:
    from enum34 import Enum, IntEnum
except ImportError:
    from enum import Enum, IntEnum

if sys.version_info[0] == 2:
    from threading import _Timer as Timer
else:
    from threading import Timer

class Severity(IntEnum):
    Debug = 1
    Verbose = 2
    Info = 3
    Warning = 4
    Error = 5
    Critical = 6


VERBOSE = 15
logging.addLevelName(VERBOSE, 'VERBOSE')
LOGGING_LEVEL_MAP = {logging.DEBUG: Severity.Debug, 
 VERBOSE: Severity.Verbose, 
 logging.INFO: Severity.Info, 
 logging.WARNING: Severity.Warning, 
 logging.ERROR: Severity.Error, 
 logging.CRITICAL: Severity.Critical}

class DaemonTimer(Timer, object):
    __doc__ = '\n    A threading.Timer object which is automatically set to self.daemon=True\n    '

    def __init__(self, interval, function, *args, **kwargs):
        super(DaemonTimer, self).__init__(interval, function, *args, **kwargs)
        self.daemon = True


class CoralogixHandlerTasks(object):

    class CoralogixHandlerTask(object):

        def __init__(self, task_name, function, trigger_interval):
            self.task_name = task_name
            self.function = function
            self.trigger_interval = trigger_interval
            self.finished = True

        def check_interval(self, timebins):
            """ Returns True if task should execute at the current timebin provided. """
            return timebins % self.trigger_interval == 0

        def run_by_interval(self, timebins, *args, **kwargs):
            """ Checks if the task should run by self.check_interval(), and runs the task with *args and **kwargs. """
            if self.check_interval(timebins):
                self.run(*args, **kwargs)

        def run(self, *args, **kwargs):
            """ Runs the task with *args and **kwargs, and self.untrigger() the task if asked by turn_off_trigger. """
            if self.finished:
                self.finished = False
                self.function(*args, **kwargs)
                self.finished = True

    def __init__(self):
        self.tasks = dict()
        self.task_names = list()

    def add_task(self, task_name, function, trigger_interval):
        task = self.CoralogixHandlerTask(task_name, function, trigger_interval)
        self.tasks[task_name] = task
        self.task_names.append(task_name)

    def remove_task(self, task_name):
        task = self.tasks.get(task_name)
        if task:
            del self.tasks[task_name]
            self.task_names.remove(task_name)

    def get_task_order(self):
        return self.task_names

    def get_task(self, task_name):
        return self.tasks.get(task_name)


class CoralogixHTTPSHandler(Handler, object):
    _default_endpoint = 'https://api.coralogix.com'
    _get_time_uri = '{0}/sdk/v1/time'
    _post_uri = '{0}/api/v1/logs'
    _post_headers = {'Content-Type': 'application/json'}
    _post_timeout = 5
    _post_max_log_entries = 2000
    _timebin_base_unit = 1
    _send_logs_interval = 5
    _check_log_buffer_interval = 1
    _update_server_timedelta_interval = 600
    _log_count_trigger = 1000

    def __init__(self, company_id, private_key, application, subsystem, computer_name=None, endpoint=None, silence_exceptions=True):
        """
        If silence_exceptions is True, exceptions will be silenced when encountered.
        :param company_id: int; integer representing the company_id
        :param private_key: str; company private key UUID
        :param application: str; name of the application the logger belongs to
        :param subsystem: str; name of the subsystem the logger belongs to
        :param computer_name: str; computer name the logger runs from; automatically retrieved from socket.getfqdn() if None
        :param endpoint: str; override the _default_endpoint URL
        :param silence_exceptions: bool; flag for silencing internal exceptions
        """
        super(CoralogixHTTPSHandler, self).__init__()
        self.endpoint = endpoint or self._default_endpoint
        if self.endpoint.endswith('/'):
            self.endpoint = self.endpoint[:-1]
        self._exception_formatter = logging.Formatter().formatException
        self._post_url = self._post_uri.format(self.endpoint)
        self._get_time_url = self._get_time_uri.format(self.endpoint)
        self.silence_exceptions = silence_exceptions
        self.company_id = company_id
        self.private_key = private_key
        self.application = application
        self.subsystem = subsystem
        self.computer_name = computer_name or getfqdn()
        self._queue = Queue()
        self._received_logs_counter = 0
        self._sent_logs_counter = 0
        self._server_timedelta = 0
        self._CoralogixHTTPSHandler__trigger_update_timedelta = threading.Event()
        self._CoralogixHTTPSHandler__trigger_send = threading.Event()
        self._CoralogixHTTPSHandler__trigger_stop = threading.Event()
        self.send_logs_thread = threading.Thread(target=self.send_logs)
        self.send_logs_thread.daemon = True
        self.send_logs_thread.start()
        signal.signal(signal.SIGINT, self.close)
        signal.signal(signal.SIGTERM, self.close)
        self.get_server_timedelta_thread = threading.Thread(target=self.get_server_timedelta)
        self.get_server_timedelta_thread.daemon = True
        self.get_server_timedelta_thread.start()
        self._time_bins_counter = 0
        self.handler_tasks = CoralogixHandlerTasks()
        handler_tasks = [
         (
          'update_server_timedelta', self._CoralogixHTTPSHandler__trigger_update_timedelta.set, self._update_server_timedelta_interval),
         (
          'check_log_buffer', self.trigger_by_log_num, self._check_log_buffer_interval),
         (
          'send_logs', self._trigger_send, self._send_logs_interval)]
        for task in handler_tasks:
            self.handler_tasks.add_task(*task)

        self.handler_tasks.get_task('update_server_timedelta').run()
        self._CoralogixHTTPSHandler__trigger_tasks = DaemonTimer(self._timebin_base_unit, self.trigger_tasks)
        self._CoralogixHTTPSHandler__trigger_tasks.daemon = True
        self._CoralogixHTTPSHandler__trigger_tasks.start()

    def trigger_tasks(self):
        start_time = time.time()
        self._CoralogixHTTPSHandler__trigger_tasks.cancel()
        self._time_bins_counter += 1
        for task_name in self.handler_tasks.get_task_order():
            if self._stopped():
                break
            self.handler_tasks.get_task(task_name).run_by_interval(self._time_bins_counter)

        execution_time = time.time() - start_time
        new_timer_time = max(0, self._timebin_base_unit - execution_time)
        if not self._stopped():
            self._CoralogixHTTPSHandler__trigger_tasks = DaemonTimer(new_timer_time, self.trigger_tasks)
            self._CoralogixHTTPSHandler__trigger_tasks.daemon = True
            self._CoralogixHTTPSHandler__trigger_tasks.start()
        else:
            del self._CoralogixHTTPSHandler__trigger_tasks

    def emit(self, record):
        try:
            log_entry = dict()
            timestamp = record.__dict__.get('override_timestamp') or record.created
            log_entry['timestamp'] = record.__dict__['override_timestamp'] if 'override_timestamp' in record.__dict__ else timestamp * 1000.0 + self._server_timedelta
            log_entry['severity'] = record.__dict__['override_severity'] if 'override_severity' in record.__dict__ else self.convert_severity(record.levelno).value
            log_entry['category'] = record.__dict__['override_category'] if 'override_category' in record.__dict__ else record.name
            log_entry['className'] = record.__dict__['override_className'] if 'override_className' in record.__dict__ else record.filename
            log_entry['methodName'] = record.__dict__['override_methodName'] if 'override_methodName' in record.__dict__ else record.funcName
            log_entry['threadId'] = record.__dict__['override_thread'] if 'override_thread' in record.__dict__ else record.thread
            log_entry['text'] = record.getMessage()
            if record.exc_info:
                if record.exc_info[0] and record.exc_info[1] and record.exc_info[2]:
                    try:
                        exception_text = self._exception_formatter(record.exc_info)
                        log_entry['text'] += '\n' + exception_text
                    except Exception:
                        pass

            self._queue.put_nowait(log_entry)
            self._received_logs_counter += 1
        except Exception:
            self.handleError(record)

    def send_logs(self):
        while not (self._stopped() and self._queue.empty()):
            self._CoralogixHTTPSHandler__trigger_send.wait()
            self._CoralogixHTTPSHandler__trigger_send.clear()
            try:
                if not self._queue.empty():
                    post_message = dict(privateKey=self.private_key, applicationName=self.application, subsystemName=self.subsystem, logEntries=list())
                    if self.computer_name:
                        post_message['computerName'] = self.computer_name
                    log_entries_count = 0
                    log_entries = list()
                    while not self._queue.empty() and log_entries_count < self._post_max_log_entries:
                        try:
                            log_message = self._queue.get_nowait()
                            log_entries.append(log_message)
                            log_entries_count += 1
                        except Empty:
                            pass

                    if log_entries_count > 0:
                        post_message['logEntries'] = log_entries
                        json_message = json.dumps(post_message).encode('UTF-8')
                        response = self.post(json_message)
                        if response is not None:
                            if 199 < response.getcode() < 400:
                                self._sent_logs_counter += log_entries_count
            except Exception as e:
                if self.silence_exceptions is False:
                    raise

            if self.trigger_by_log_num_condition():
                continue
                continue

        self._CoralogixHTTPSHandler__trigger_send.clear()
        del self._CoralogixHTTPSHandler__trigger_send

    @staticmethod
    def convert_severity(python_severity):
        """
        Converts Python's Logging severity level to Coralogix' severity level.
        :param python_severity: int
        :return: int
        """
        level = LOGGING_LEVEL_MAP.get(python_severity)
        if level is None:
            level = LOGGING_LEVEL_MAP[min(LOGGING_LEVEL_MAP, key=lambda x: abs(x - python_severity))]
        return level

    def get_server_timedelta(self):
        """ Updates self._server_timedelta """
        while not self._stopped():
            self._CoralogixHTTPSHandler__trigger_update_timedelta.wait()
            self._CoralogixHTTPSHandler__trigger_update_timedelta.clear()
            for i in range(3):
                if self._stopped():
                    break
                try:
                    time_url_response = self.post(None, self._get_time_url).read()
                    server_time = int(time_url_response) / 10000.0
                    local_time = time.time() * 1000.0
                    if server_time:
                        self._server_timedelta = server_time - local_time
                        break
                except Exception:
                    continue

        self._CoralogixHTTPSHandler__trigger_update_timedelta.clear()
        del self._CoralogixHTTPSHandler__trigger_update_timedelta

    def post(self, data, url=None):
        response = None
        url = url or self._post_url
        try:
            request = Request(url, data, self._post_headers)
            response = urlopen(request, timeout=self._post_timeout)
        except Exception as e:
            if self.silence_exceptions is False:
                print('CoralogixHTTPSHandler.post(): caught exception= {0}'.format(e))

        return response

    def trigger_by_log_num(self):
        """ Triggers self.__trigger_send if number of logs exceeds self._log_count_trigger. """
        if self.trigger_by_log_num_condition():
            self._trigger_send()

    def trigger_by_log_num_condition(self):
        return self._log_count_trigger <= self._queue.qsize()

    def flush(self):
        self._trigger_send()
        self._trigger_update_timedelta()

    def close(self, frame=None, signal_code=None):
        self._post_timeout = 2
        self.flush()
        self._trigger_stop()
        self.send_logs_thread.join()

    def _trigger_update_timedelta(self):
        self._CoralogixHTTPSHandler__trigger_update_timedelta.set()

    def _trigger_send(self):
        self._CoralogixHTTPSHandler__trigger_send.set()

    def _trigger_stop(self):
        self._CoralogixHTTPSHandler__trigger_stop.set()

    def _stopped(self):
        return self._CoralogixHTTPSHandler__trigger_stop.is_set()