# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/local_worker/core/task.py
# Compiled at: 2016-10-19 13:19:48
"""
this module contains the Task class, which handles a scan for a given sample
on one ativirus inside a virtual device
"""
import subprocess, tempfile, os
from datetime import datetime
import sys, logging
from contextlib import contextmanager
import io, logging
from multiprocessing import Queue, Process
from adapters.base import ScanTimeout
import lockfile
from utils import import_test_by_name, pick_unused_port
import virtualdevice
from utils import DEVICES_DATA_DIR
logger = logging.getLogger('andrototal.task')

class Task(object):
    """
  the Task object handles the scan procedure
  for a given sample on one antivirus.
  Every scan will start a virtual device
  and interract with an adapter object
  in order to get the scan results.
  """

    def __init__(self, sample_path, test, window, antivirus_info):
        self.sample_path = sample_path
        self.test = test
        self.num_tries = 0
        self.window = window
        self.antivirus_info = antivirus_info
        self.data = None
        return

    def run(self):
        """
    run the avd, which contains the given antivirus, and 
    run the scan on the sample

    :return: 
    * the scan result: NO_THREAT_FOUND, THREAD_FOUND or the name of the malware
    * scan status: SUCCESS with termination time or FAILURE with the cause of the failuer
        (traceback of an exception)
    """
        self.num_tries = self.num_tries + 1
        avd_name = self.test['avd_name']
        test_module_name = self.test['test_module_name']
        test_method_name = self.test['detection_method']
        self.job_result = {'started_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 
           'antivirus': self.antivirus_info, 
           'detected_threat': None}
        subprocess.call(['adb', 'start-server'], stdout=subprocess.PIPE)
        with virtualdevice.AVD(avd_name) as (avd):
            self.data = tempfile.NamedTemporaryFile(prefix='AT_avd', delete=False)
            self.data.close()
            self.data = self.data.name
            avd.start(data=self.data, wipe_data=True, no_window=not self.window)
            test_module = import_test_by_name(test_module_name)
            monkey_port = pick_unused_port()
            view_server_port = pick_unused_port()
            logger.debug('Device: %s for %s waiting for boot' % (
             avd.device_serial, test_module_name))
            avd.wait_for_boot()
            logger.debug('Device: %s starting test for %s' % (
             avd.device_serial, test_module_name))
            device_folder = ('_').join([test_module_name,
             self.sample_path.split('/')[(-1)].replace('.', '_'),
             self.job_result['started_at'].replace(' ', '_').replace(':', '_')])
            try:
                os.mkdir(DEVICES_DATA_DIR + '/' + device_folder)
            except:
                pass

            logcat_location = DEVICES_DATA_DIR + '/' + device_folder + '/logcat'
            screeshot_location = DEVICES_DATA_DIR + '/' + device_folder + '/screenshot'
            ts = test_module.TestSuite(avd.device_serial, monkey_port, view_server_port, logcat_location, screeshot_location)
            result = _test_handler(getattr(ts, test_method_name), self.sample_path)
            self.job_result.update(result)
            logger.debug('task completed!')
            self.set_result()
            self.cleanup_files()
            return self.job_result
        return

    def failure(self, excetpion, traceback):
        """
    set the scan status to "FAILURE" and its failure cause
    """
        return {'status': 'FAILURE', 'excetpion': excetpion, 
           'traceback': traceback, 
           'antivirus': self.test['test_module_name']}

    def set_result(self):
        """
    set the scan status to "SUCCESS" and its termination time
    """
        self.job_result['ended_at'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.job_result['status'] = 'SUCCESS'

    def cleanup_files(self):
        """
    delete the user-data of the virtualdevice
    """
        if self.data:
            try:
                logger.debug('removing %s' % self.data)
                os.unlink(self.data)
            except:
                logger.exception("error, didn't remove userdata")


def _test_handler(test_module, sample):

    def _sub_handler(f, arg, q):
        with _stdout_redirector():
            q.put(f(arg))

    q = Queue()
    p = Process(target=_sub_handler, args=(test_module, sample, q))
    p.start()
    p.join()
    return q.get()


@contextmanager
def _stdout_redirector():
    original_stdout_fd = sys.stdout.fileno()
    original_stderr_fd = sys.stderr.fileno()

    def _redirect_to(out_to_fd, err_to_fd):
        sys.stdout.close()
        sys.stderr.close()
        os.dup2(out_to_fd, original_stdout_fd)
        os.dup2(err_to_fd, original_stderr_fd)
        sys.stdout = os.fdopen(original_stdout_fd, 'wb')
        sys.stderr = os.fdopen(original_stderr_fd, 'wb')

    saved_stdout_fd = os.dup(original_stdout_fd)
    saved_stderr_fd = os.dup(original_stderr_fd)
    try:
        out_file = tempfile.NamedTemporaryFile(prefix='temp_out', delete=True)
        err_file = tempfile.NamedTemporaryFile(prefix='temp_err', delete=True)
        _redirect_to(out_file.fileno(), err_file.fileno())
        yield
        _redirect_to(saved_stdout_fd, saved_stderr_fd)
    finally:
        out_file.close()
        err_file.close()
        os.close(saved_stdout_fd)
        os.close(saved_stderr_fd)