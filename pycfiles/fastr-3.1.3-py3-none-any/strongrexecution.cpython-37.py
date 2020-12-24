# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/executionplugins/strongrexecution.py
# Compiled at: 2019-10-16 08:10:33
# Size of source mod 2**32: 3649 bytes
import json, base64, subprocess, threading, time, fastr, fastr.resources
from fastr.plugins.executionplugin import ExecutionPlugin
import fastr.helpers.classproperty as classproperty

class StrongrExecution(ExecutionPlugin):
    __doc__ = '\n    A execution plugin based on Redis Queue. Fastr will submit jobs to the\n    redis queue and workers will peel the jobs from the queue and process\n    them.\n\n    This system requires a running redis database and the database url has to\n    be set in the fastr configuration.\n\n    .. note::\n\n        This execution plugin required the ``redis`` and ``rq`` packages to\n        be installed before it can be loaded properly.\n    '
    _queue = []
    _mappings = {}

    def __init__(self, finished_callback=None, cancelled_callback=None):
        super(StrongrExecution, self).__init__(finished_callback, cancelled_callback)
        fastr.log.debug('Creating strongr job collector')
        self.collector = threading.Thread(name='StrongrJobCollector-0', target=(self.check_finished), args=())
        self.collector.daemon = True
        fastr.log.debug('Starting strongr job collector')
        self.collector.start()

    @classmethod
    def test(cls):
        pass

    @classproperty
    def configuration_fields(cls):
        return {}

    def _job_finished(self, result):
        pass

    def _cancel_job(self, job):
        pass

    def _queue_job(self, job):
        cmd = [
         '/opt/strongr/addtask',
         "'{}'".format(base64.b64encode('/bin/bash -c "{} {} {} {}"'.format('', 'python', "`python -c 'from fastr.execution import executionscript; print(executionscript.__file__)'`", job.commandfile))),
         '1', '1']
        print(cmd)
        with open(job.stdoutfile, 'a') as (fh_stdout):
            with open(job.stderrfile, 'a') as (fh_stderr):
                taskinfo = subprocess.check_output(cmd, stderr=fh_stderr)
        taskid = json.loads(taskinfo)['job_id']
        self._queue.append(taskid)
        self._mappings[taskid] = job

    def check_finished(self):
        while self.running:
            sout = subprocess.check_output('/opt/strongr/queryqueue')
            print(sout)
            queueinfo = json.loads(sout)
            if queueinfo == None:
                time.sleep(5.0)
                continue
            finished = [t for t in self._queue if t not in queueinfo]
            self._queue = [t for t in self._queue if t in queueinfo]
            fastr.log.info('# FINISHED: {}'.format(finished))
            fastr.log.info('# QUEUE: {}'.format(self._queue))
            for taskid in finished:
                fastr.log.info('## TASK ID: {}'.format(taskid))
                self.job_finished(self._mappings[taskid])

            time.sleep(1.0)