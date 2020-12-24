# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/job_watcher.py
# Compiled at: 2018-09-07 06:06:50
# Size of source mod 2**32: 2332 bytes
"""a module wioth usefull function that can give insights on the state of a job"""
from .slurm_wrapper import launch_job, return_status, kill_job, exist_job
import time, os, glob
time_to_sleep = 120

class JobState:
    __doc__ = 'A class that store the state a job'

    def __init__(self, jobID=None):
        self.jobID = jobID
        self.status_string = return_status(self.jobID)
        self.error = None
        self.last_check = time.time()
        self.waiting_time = 120
        self.time_first_running = None

    def test_state(self, state):
        ctime = time.time()
        if ctime - self.last_check > self.waiting_time:
            self.status_string = return_status(self.jobID)
        if self.status_string == state:
            return True
        else:
            return False

    def wait(self):
        time.sleep(self.waiting_time)

    def is_running(self):
        return self.test_state('RUNNING')

    def is_pending(self):
        return self.test_state('PENDING')

    def is_completed(self):
        return self.test_state('COMPLETED')

    def is_unknow(self):
        return not (self.is_completed() or self.is_pending() or self.is_running())

    def wait_pending_job(self):
        """Wait and check the status of a job"""
        while self.is_pending():
            self.wait()

    def update_state(self):
        """Check the state of the job, and modify the logical attribute in function"""
        if self.is_pending() or self.is_completed:
            return
        if self.is_running():
            if self.time_first_running is None:
                self.time_first_running = self.time_last_check
                self.wait()
            if is_memo_created():
                self.weathly = True


def is_memo_created():
    return os.path.isfile('memo')


def last_file_created():
    """fine the last file created, and return the file name and the time"""
    list_of_files = glob.glob('./*')
    latest_file = max(list_of_files, key=(os.path.getctime))
    return (latest_file, os.path.getctime(latest_file))


def get_errfile_notempty(jobID):
    fpath = jobID + '.err'
    print(os.path.getsize(fpath))
    return os.path.isfile(fpath) and os.path.getsize(fpath) > 0