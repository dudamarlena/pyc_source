# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/executionplugins/linearexecution.py
# Compiled at: 2019-06-04 03:03:06
import os
from Queue import Queue, Empty
import subprocess, sys
from threading import Thread
import traceback, fastr
from fastr.execution.executionpluginmanager import ExecutionPlugin, JobAction
from fastr.execution.job import Job, JobState

class LinearExecution(ExecutionPlugin):
    """
    An execution engine that has a background thread that executes the jobs in
    order. The queue is a simple FIFO queue and there is one worker thread that
    operates in the background. This plugin is meant as a fallback when other
    plugins do not function properly. It does not multi-processing so it is
    safe to use in environments that do no support that.
    """

    def __init__(self, finished_callback=None, cancelled_callback=None, status_callback=None):
        super(LinearExecution, self).__init__(finished_callback, cancelled_callback, status_callback)
        self.job_queue = Queue()
        self.timeout = 1.0
        self._exec_thread = Thread(None, self.exec_worker, 'ExecWorker')
        self.running = True
        self._exec_thread.start()
        return

    @classmethod
    def test(cls):
        pass

    def _queue_job(self, job):
        fastr.log.debug(('Queueing {}').format(job.id))
        self.job_queue.put(job)

    def _job_finished(self, result):
        pass

    def cleanup(self):
        super(LinearExecution, self).cleanup()
        self.running = False
        self._exec_thread.join()
        self.job_status.clear()

    def exec_worker(self):
        while self.running:
            try:
                job = self.job_queue.get(True, self.timeout)
                try:
                    try:
                        fastr.log.debug(('Running job {}').format(job.id))
                        job.status = JobState.running
                        command = [
                         sys.executable,
                         os.path.join(fastr.config.executionscript),
                         job.commandfile]
                        with open(job.stdoutfile, 'a') as (fh_stdout):
                            with open(job.stderrfile, 'a') as (fh_stderr):
                                proc = subprocess.Popen(command, stdout=fh_stdout, stderr=fh_stderr)
                                proc.wait()
                                fastr.log.debug('Subprocess finished')
                        fastr.log.debug(('Finished {}').format(job.id))
                    except Exception:
                        exc_type, _, trace = sys.exc_info()
                        exc_info = traceback.format_exc()
                        trace = traceback.extract_tb(trace, 1)[0]
                        fastr.log.error(('Encountered exception ({}) during execution:\n{}').format(exc_type.__name__, exc_info))
                        job.info_store['errors'].append((exc_type.__name__, exc_info, trace[0], trace[1]))

                finally:
                    self.job_finished(job)
                    self.job_queue.task_done()

            except Empty:
                pass