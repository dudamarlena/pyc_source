# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/executionplugins/processpoolexecution.py
# Compiled at: 2018-12-19 07:29:10
# Size of source mod 2**32: 5148 bytes
import multiprocessing, os, subprocess, sys, traceback, fastr
from fastr.abc.baseplugin import PluginState
from fastr.plugins.executionplugin import ExecutionPlugin
from fastr.execution.job import JobState
from fastr.helpers.classproperty import classproperty
from fastr.utils.multiprocesswrapper import function_wrapper

def run_job(job, job_status):
    errors = []
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
        errors.append((exc_type.__name__, exc_info, trace[0], trace[1]))

    return (job.id, errors)


class ProcessPoolExecution(ExecutionPlugin):
    __doc__ = '\n    A local execution plugin that uses multiprocessing to create a pool of\n    worker processes. This allows fastr to execute jobs in parallel with\n    true concurrency. The number of workers can be specified in the fastr\n    configuration, but the default amount is the ``number of cores - 1``\n    with a minimum of ``1``.\n\n    .. warning::\n\n        The ProcessPoolExecution does not check memory requirements of jobs\n        and running many workers might lead to memory starvation and thus an\n        unresponsive system.\n    '
    _status = (PluginState.uninitialized, 'Please use the test() function to check DRMAA capability')

    def __init__(self, finished_callback=None, cancelled_callback=None, nr_of_workers=None):
        super(ProcessPoolExecution, self).__init__(finished_callback, cancelled_callback)
        if nr_of_workers is None:
            nr_of_workers = fastr.config.process_pool_worker_number
        self.pool = multiprocessing.Pool(processes=nr_of_workers)

    @classproperty
    def configuration_fields(cls):
        return {'process_pool_worker_number': (
                                        int,
                                        max(multiprocessing.cpu_count() - 1, 1),
                                        'Number of workers to use in a process pool')}

    def cleanup(self):
        super(ProcessPoolExecution, self).cleanup()
        fastr.log.debug('Stopping ProcessPool')
        fastr.log.debug('Terminating worker processes...')
        self.pool.terminate()
        fastr.log.debug('Joining worker processes...')
        self.pool.join()
        fastr.log.debug('ProcessPool stopped!')

    @classmethod
    def test(cls):
        try:
            fastr.log.debug('Creating Pool')
            pool = multiprocessing.Pool(processes=1)
            fastr.log.debug('Terminating Pool')
            pool.terminate()
            del pool
            _status = ('Loaded', '')
        except OSError:
            _status = (
             'Failed',
             'Multiprocessing Failed ({}):\n{}'.format(sys.exc_info()[0].__name__, traceback.format_exc()))

        cls._status = _status

    def _job_finished(self, result):
        pass

    def _queue_job(self, job):
        self.pool.apply_async(function_wrapper, [
         os.path.abspath(__file__), 'run_job', job, self.job_status], callback=self.job_finished_callback)

    def job_finished_callback(self, result):
        """
        Reciever for the callback, it will split the result tuple and call job_finished

        :param tuple result: return value of run_job
        """
        job_id, errors = result
        self.job_finished(self.job_dict[job_id], errors)


if __name__ == '__main__':
    multiprocessing.freeze_support()