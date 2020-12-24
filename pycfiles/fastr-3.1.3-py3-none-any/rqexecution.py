# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/executionplugins/rqexecution.py
# Compiled at: 2019-06-04 03:03:06
import os, subprocess, sys, threading, time, traceback, fastr, fastr.resources
from fastr.core.baseplugin import PluginState
from fastr.execution.executionpluginmanager import ExecutionPlugin, JobAction
from fastr.execution.job import Job, JobState
from fastr.utils.classproperty import classproperty
try:
    from rq import Queue
    from redis import Redis
    IMPORT_SUCCESS = True
except ImportError:
    IMPORT_SUCCESS = False

class RQExecution(ExecutionPlugin):
    """
    A execution plugin based on Redis Queue. Fastr will submit jobs to the
    redis queue and workers will peel the jobs from the queue and process
    them.

    This system requires a running redis database and the database url has to
    be set in the fastr configuration.

    .. note::

        This execution plugin required the ``redis`` and ``rq`` packages to
        be installed before it can be loaded properly.
    """
    if not IMPORT_SUCCESS:
        _status = (
         PluginState.failed, 'Could not load rq and/or redis!')

    def __init__(self, finished_callback=None, cancelled_callback=None, status_callback=None):
        super(RQExecution, self).__init__(finished_callback, cancelled_callback, status_callback)
        redis = Redis.from_url(fastr.config.rq_host)
        self.queue = Queue(name=fastr.config.rq_queue, connection=redis, default_timeout=-1)
        self.rq_jobs = {}
        self.running = True
        fastr.log.debug('Creating rq job collector')
        self.collector = threading.Thread(name='RQJobCollector-0', target=self.check_finished, args=())
        self.collector.daemon = True
        fastr.log.debug('Starting rq job collector')
        self.collector.start()

    @classmethod
    def test(cls):
        if not IMPORT_SUCCESS:
            raise ImportError('Cannot import required modules (rq and redis are required)')

    @classproperty
    def configuration_fields(cls):
        return {'rq_host': (
                     str, 'redis://localhost:6379/0', 'The url of the redis serving the redis queue'), 
           'rq_queue': (
                      str, 'default', 'The redis queue to use')}

    def cleanup(self):
        super(RQExecution, self).cleanup()

    def _job_finished(self, result):
        pass

    def _cancel_job(self, job):
        pass

    def _queue_job(self, job):
        rq_job = self.queue.enqueue(self.run_job, job.id, job.commandfile, job.stdoutfile, job.stderrfile, job_id=job.id, ttl=-1)
        self.rq_jobs[job.id] = rq_job

    def check_finished(self):
        while self.running:
            for job_id, rq_job in self.rq_jobs.items():
                if rq_job.is_finished or rq_job.is_failed:
                    job = self.job_dict[job_id]
                    self.job_finished(job)
                    del self.rq_jobs[job_id]

            time.sleep(1.0)

    @classmethod
    def run_job(cls, job_id, job_command, job_stdout, job_stderr):
        try:
            fastr.log.debug(('Running job {}').format(job_id))
            command = [
             sys.executable,
             os.path.join(fastr.config.executionscript),
             job_command]
            with open(job_stdout, 'w') as (fh_stdout):
                with open(job_stderr, 'w') as (fh_stderr):
                    proc = subprocess.Popen(command, stdout=fh_stdout, stderr=fh_stderr)
                    proc.wait()
                    fastr.log.debug('Subprocess finished')
            fastr.log.debug(('Finished {}').format(job_id))
        except Exception:
            exc_type, _, trace = sys.exc_info()
            exc_info = traceback.format_exc()
            fastr.log.error(('Encountered exception ({}) during execution:\n{}').format(exc_type.__name__, exc_info))
            raise