# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danvk/github/dpxdt/dpxdt/client/process_worker.py
# Compiled at: 2014-07-26 02:19:09
"""Workers for driving screen captures, perceptual diffs, and related work."""
import Queue, logging, subprocess, time, gflags
FLAGS = gflags.FLAGS
from dpxdt.client import timer_worker
from dpxdt.client import workers

class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class TimeoutError(Exception):
    """Subprocess has taken too long to complete and was terminated."""
    pass


class ProcessWorkflow(workers.WorkflowItem):
    """Workflow that runs a subprocess.

    Args:
        log_path: Path to where output from this subprocess should be written.
        timeout_seconds: How long before the process should be force killed.

    Returns:
        The return code of the subprocess.
    """

    def get_args(self):
        """Return the arguments for running the subprocess."""
        raise NotImplemented

    def run(self, log_path, timeout_seconds=30):
        start_time = time.time()
        with open(log_path, 'a') as (output_file):
            args = self.get_args()
            logging.info('item=%r Running subprocess: %r', self, args)
            try:
                process = subprocess.Popen(args, stderr=subprocess.STDOUT, stdout=output_file, close_fds=True)
            except:
                logging.error('item=%r Failed to run subprocess: %r', self, args)
                raise

            while True:
                logging.info('item=%r Polling pid=%r', self, process.pid)
                process._internal_poll(_deadstate=127)
                if process.returncode is not None:
                    logging.info('item=%r Subprocess finished pid=%r, returncode=%r', self, process.pid, process.returncode)
                    raise workers.Return(process.returncode)
                now = time.time()
                run_time = now - start_time
                if run_time > timeout_seconds:
                    logging.info('item=%r Subprocess timed out pid=%r', self, process.pid)
                    process.kill()
                    raise TimeoutError('Sent SIGKILL to item=%r, pid=%s, run_time=%s' % (
                     self, process.pid, run_time))
                yield timer_worker.TimerItem(FLAGS.polltime)

        return