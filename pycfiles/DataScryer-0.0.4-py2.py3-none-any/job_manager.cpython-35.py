# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\jobs\job_manager.py
# Compiled at: 2016-06-28 07:11:49
# Size of source mod 2**32: 2826 bytes
import logging
from copy import deepcopy
from datascryer.jobs.job import Job

class JobManager:

    def __init__(self):
        self._JobManager__jobs = {}

    def update_config(self, config):
        jobs_to_start = []
        job_to_stop = []
        for host, hv in config.items():
            for service, sv in hv.items():
                desc = (
                 host, service, dict(sv))
                if host not in self._JobManager__jobs:
                    jobs_to_start.append(desc)
                    self._JobManager__jobs[host] = {service: dict(sv)}
                else:
                    if host in self._JobManager__jobs and service not in self._JobManager__jobs[host]:
                        jobs_to_start.append(desc)
                        self._JobManager__jobs[host][service] = dict(sv)
                    elif host in self._JobManager__jobs and service in self._JobManager__jobs[host] and self._JobManager__jobs[host][service]['config'] != sv['config']:
                        logging.getLogger(__name__).debug('%s %s has a new config: %s\nold config: %s' % (
                         host, service, sv['config'], self._JobManager__jobs[host][service]['config']))
                        job_to_stop.append((host, service, self._JobManager__jobs[host][service]))
                        jobs_to_start.append(desc)
                        self._JobManager__jobs[host][service] = dict(sv)

        for host, hv in self._JobManager__jobs.items():
            for service, sv in hv.items():
                desc = (
                 host, service, dict(sv))
                if host not in config:
                    job_to_stop.append(desc)
                elif host in config and service not in config[host]:
                    job_to_stop.append(desc)

        self._JobManager__stop_jobs(job_to_stop)
        self._JobManager__start_jobs(jobs_to_start)

    @staticmethod
    def __stop_jobs(jobs):
        if not jobs:
            return
        for j in jobs:
            logging.getLogger(__name__).debug('Stopping job: %s %s' % (j[0], j[1]))
            j[2]['job'].stop()

    def __start_jobs(self, jobs):
        if not jobs:
            return
        for j in jobs:
            logging.getLogger(__name__).debug('Starting job: %s %s' % (j[0], j[1]))
            self._JobManager__jobs[j[0]][j[1]]['job'] = Job(deepcopy(j))
            self._JobManager__jobs[j[0]][j[1]]['job'].start()

    def stop(self):
        for host, hv in self._JobManager__jobs.items():
            for service, sv in hv.items():
                sv['job'].stop()