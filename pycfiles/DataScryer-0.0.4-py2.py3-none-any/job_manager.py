# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Programmieren\dataScryer\datascryer\jobs\job_manager.py
# Compiled at: 2016-06-28 07:11:49
import logging
from copy import deepcopy
from datascryer.jobs.job import Job

class JobManager:

    def __init__(self):
        self.__jobs = {}

    def update_config(self, config):
        jobs_to_start = []
        job_to_stop = []
        for host, hv in config.items():
            for service, sv in hv.items():
                desc = (
                 host, service, dict(sv))
                if host not in self.__jobs:
                    jobs_to_start.append(desc)
                    self.__jobs[host] = {service: dict(sv)}
                elif host in self.__jobs and service not in self.__jobs[host]:
                    jobs_to_start.append(desc)
                    self.__jobs[host][service] = dict(sv)
                elif host in self.__jobs and service in self.__jobs[host] and self.__jobs[host][service]['config'] != sv['config']:
                    logging.getLogger(__name__).debug('%s %s has a new config: %s\nold config: %s' % (
                     host, service, sv['config'], self.__jobs[host][service]['config']))
                    job_to_stop.append((host, service, self.__jobs[host][service]))
                    jobs_to_start.append(desc)
                    self.__jobs[host][service] = dict(sv)

        for host, hv in self.__jobs.items():
            for service, sv in hv.items():
                desc = (
                 host, service, dict(sv))
                if host not in config:
                    job_to_stop.append(desc)
                elif host in config and service not in config[host]:
                    job_to_stop.append(desc)

        self.__stop_jobs(job_to_stop)
        self.__start_jobs(jobs_to_start)

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
            self.__jobs[j[0]][j[1]]['job'] = Job(deepcopy(j))
            self.__jobs[j[0]][j[1]]['job'].start()

    def stop(self):
        for host, hv in self.__jobs.items():
            for service, sv in hv.items():
                sv['job'].stop()