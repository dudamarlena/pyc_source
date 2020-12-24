# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/task_runner.py
# Compiled at: 2018-02-02 22:01:21
# Size of source mod 2**32: 4880 bytes
import logging, threading, time
from mercury.common.clients.rpc.backend import BackEndClient
from mercury.common.exceptions import fancy_traceback_short, parse_exception
log = logging.getLogger(__name__)

class TaskRunner(object):
    __doc__ = '\n    '

    def __init__(self, job_id, task_id, entry, backend_url, entry_args=None, entry_kwargs=None, lock=None, timeout=0, task_id_kwargs=False):
        """

        :param job_id:
        :param task_id:
        :param entry:
        :param backend_url:
        :param entry_args:
        :param entry_kwargs:
        :param lock:
        :param timeout:
        :param task_id_kwargs:
        """
        self.job_id = job_id
        self.task_id = task_id
        self.entry = entry
        self.args = entry_args or ()
        self.kwargs = entry_kwargs or {}
        if task_id_kwargs:
            self.kwargs['task_id'] = self.task_id
        self.lock = lock
        self.timeout = timeout
        self.time_started = None
        self.time_completed = None
        self.backend = BackEndClient(backend_url)

    def __management_thread(self):
        """
        Thread to support shared locking.
        :return:
        """
        self.time_started = time.time()
        self.backend.update_task({'task_id':self.task_id, 
         'status':'STARTED', 
         'time_started':self.time_started})
        traceback = None
        try:
            try:
                return_data = (self.entry)(*self.args, **self.kwargs)
                if isinstance(return_data, dict):
                    if return_data.get('error'):
                        status = 'ERROR'
                else:
                    status = 'SUCCESS'
            except Exception:
                exc_dict = parse_exception()
                log.error((fancy_traceback_short(exc_dict, 'Critical error while running task: %s [%s], elapsed' % (
                 self.entry.__name__,
                 self.task_id))),
                  extra={'task_id':self.task_id, 
                 'job_id':self.job_id})
                traceback = parse_exception()
                status = 'ERROR'
                return_data = None

        finally:
            if self.lock:
                log.debug(('Releasing lock for %s' % self.lock.task_id), extra={'task_id':self.task_id, 
                 'job_id':self.job_id})
                self.lock.release()

        self.time_completed = time.time()
        log.info(('Task completed: %s [%s], elapsed %s' % (self.entry.__name__,
         self.task_id,
         self.time_completed - self.time_started)),
          extra={'task_id':self.task_id, 
         'job_id':self.job_id})
        log.debug(('Publishing response to: %s' % self.backend.zmq_url), extra={'task_id':self.task_id, 
         'job_id':self.job_id})
        response = self.backend.complete_task({'status':status, 
         'message':return_data, 
         'traceback':traceback, 
         'job_id':self.job_id, 
         'task_id':self.task_id, 
         'time_started':self.time_started, 
         'time_completed':self.time_completed, 
         'action':'Completed'})
        if response.get('error'):
            log.error('Error dispatching message. [timeout]', extra={'task_id':self.task_id, 
             'job_id':self.job_id})
        else:
            log.info(('Dispatch successful : %s' % response), extra={'task_id':self.task_id, 
             'job_id':self.job_id})

    def run(self):
        log.info(('Starting task: %s [%s]' % (self.entry.__name__, self.task_id)), extra={'task_id':self.task_id, 
         'job_id':self.job_id})
        t = threading.Thread(target=(self._TaskRunner__management_thread), name=('_{}_{}'.format(self.job_id, self.task_id)))
        t.start()