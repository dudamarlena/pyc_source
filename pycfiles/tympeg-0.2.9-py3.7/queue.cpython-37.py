# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tympeg/queue.py
# Compiled at: 2017-06-08 14:08:58
# Size of source mod 2**32: 3474 bytes
import time
from multiprocessing import Process
from threading import Timer
from .timecode import seconds_to_timecode
from .converter import MediaConverter

class MediaConverterQueue:

    def __init__(self, log_directory='', max_processes=1, logging=False, debug=False):
        self.job_list = []
        self.processes = []
        self.refresh_interval = 10
        self.active_processes = 0
        self.start_time = 0
        self.end_time = 0
        self.total_time = 0
        self.done = False
        self.log_directory = log_directory
        self.max_processes = max_processes

    def run(self):
        self.job_list = sorted((self.job_list), key=(lambda media: media.mediaObject.fileName))
        while self.count_active_processes() < self.max_processes and len(self.job_list) > 0:
            self.start_job()

        self.start_time = time.time()
        self.periodic()

    def count_active_processes(self):
        active = 0
        for process in self.processes:
            if process.is_alive():
                active += 1

        return active

    def start_job(self):
        if self.count_active_processes() >= self.max_processes:
            print('Failed to start a new job, would exceed maximum processes')
            return
        if len(self.job_list) < 1:
            print('Failed to start a new job, no more jobs remaining!')
            return
        next_job = self.job_list.pop()
        process = Process(target=(next_job.convert), args=())
        process.start()
        self.processes.append(process)

    def prune_dead_processes(self):
        for process in self.processes:
            if process.is_alive() or type(process) == Process:
                process.terminate()
                ndx = self.processes.index(process)
                del self.processes[ndx]

    def periodic(self):
        self.prune_dead_processes()
        if self.count_active_processes() == 0 and len(self.job_list) == 0:
            self.done = True
            print('All jobs completed!')
            self.end_time = time.time()
            self.total_time = self.end_time - self.start_time
            print('Took approximately {}.'.format(seconds_to_timecode(self.total_time)))
        else:
            while self.count_active_processes() < self.max_processes and len(self.job_list) > 0:
                self.start_job()

            Timer(self.refresh_interval, self.periodic).start()

    def add_job(self, job):
        if type(job) == MediaConverter:
            self.job_list.append(job)
        else:
            print('add_job(job) takes a MediaConverter object, received {}'.format(type(job)))
            print('\tQuitting now for safety...')
            exit()

    def add_jobs(self, jobs):
        for job in jobs:
            self.add_job(job)

    def jobs_done(self):
        if len(self.jobList) < 1:
            print("Job's done!")
        else:
            print('Next job is: ' + self.jobList[0].fileName)

    def job_cancelled(self):
        pass

    def write_log(self, logText):
        pass

    def open_log(self):
        pass