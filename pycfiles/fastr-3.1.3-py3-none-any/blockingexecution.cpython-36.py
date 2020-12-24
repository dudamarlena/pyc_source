# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/executionplugins/blockingexecution.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 2831 bytes
import os, subprocess, sys, traceback, fastr, fastr.resources
from fastr.plugins.executionplugin import ExecutionPlugin, JobAction
from fastr.execution.job import Job, JobState

def run_job(job, job_status):
    try:
        fastr.log.debug('Running job {}'.format(job.id))
        job_status[job.id] = JobState.running
        command = [
         sys.executable,
         os.path.join(fastr.config.executionscript),
         job.commandfile]
        with open(job.stdoutfile, 'a') as (fh_stdout):
            with open(job.stderrfile, 'a') as (fh_stderr):
                proc = subprocess.Popen(command, stdout=fh_stdout, stderr=fh_stderr)
                proc.wait()
                fastr.log.debug('Subprocess finished')
        fastr.log.debug('Finished {}'.format(job.id))
    except Exception:
        exc_type, _, trace = sys.exc_info()
        exc_info = traceback.format_exc()
        trace = traceback.extract_tb(trace, 1)[0]
        fastr.log.error('Encountered exception ({}) during execution:\n{}'.format(exc_type.__name__, exc_info))
        job.info_store['errors'].append((exc_type.__name__, exc_info, trace[0], trace[1]))

    return job


class BlockingExecution(ExecutionPlugin):
    __doc__ = '\n    The blocking execution plugin is a special plugin which is meant for debug\n    purposes. It will not queue jobs but immediately execute them inline,\n    effectively blocking fastr until the Job is finished. It is the simplest\n    execution plugin and can be used as a template for new plugins or for\n    testing purposes.\n    '

    def __init__(self, finished_callback=None, cancelled_callback=None):
        super(BlockingExecution, self).__init__(finished_callback, cancelled_callback)

    @classmethod
    def test(cls):
        pass

    def cleanup(self):
        super(BlockingExecution, self).cleanup()

    def _job_finished(self, result):
        pass

    def _queue_job(self, job):
        fastr.log.debug('Queueing {}'.format(job.id))
        run_job(job, self.job_status)
        self.job_finished(job, blocking=True)