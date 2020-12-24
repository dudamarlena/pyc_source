# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/lsf.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 9767 bytes
from __future__ import absolute_import
from __future__ import division
from builtins import str
from builtins import range
from past.utils import old_div
import logging, math
from toil.lib.misc import call_command
import os
from dateutil.parser import parse
from dateutil.tz import tzlocal
from datetime import datetime
from toil.batchSystems import MemoryString
from toil.batchSystems.abstractGridEngineBatchSystem import AbstractGridEngineBatchSystem
from toil.batchSystems.lsfHelper import parse_memory_resource, parse_memory_limit, per_core_reservation
logger = logging.getLogger(__name__)

class LSFBatchSystem(AbstractGridEngineBatchSystem):

    class Worker(AbstractGridEngineBatchSystem.Worker):
        __doc__ = 'LSF specific AbstractGridEngineWorker methods.'

        def getRunningJobIDs(self):
            times = {}
            with self.runningJobsLock:
                currentjobs = dict((str(self.batchJobIDs[x][0]), x) for x in self.runningJobs)
            stdout = call_command(['bjobs', '-o', "jobid stat start_time delimiter='|'"])
            for curline in stdout.split('\n'):
                items = curline.strip().split('|')
                if items[0] in currentjobs and items[1] == 'RUN':
                    jobstart = parse((items[2]), default=(datetime.now(tzlocal())))
                    times[currentjobs[items[0]]] = datetime.now(tzlocal()) - jobstart

            return times

        def killJob(self, jobID):
            call_command(['bkill', self.getBatchSystemID(jobID)])

        def prepareSubmission(self, cpu, memory, jobID, command, jobName):
            return self.prepareBsub(cpu, memory, jobID) + [command]

        def submitJob(self, subLine):
            combinedEnv = self.boss.environment
            combinedEnv.update(os.environ)
            stdout = call_command(subLine, env=combinedEnv)
            line = stdout.split('\n')[0]
            result = int(line.strip().split()[1].strip('<>'))
            logger.debug('Got the job id: {}'.format(result))
            return result

        def getJobExitCode(self, lsfJobID):
            job, task = lsfJobID, None
            if '.' in lsfJobID:
                job, task = lsfJobID.split('.', 1)
            args = [
             'bjobs', '-l', str(job)]
            logger.debug('Checking job exit code for job via bjobs: {}'.format(job))
            stdout = call_command(args)
            output = stdout.replace('\n                     ', '')
            process_output = output.split('\n')
            started = 0
            for line in process_output:
                if 'Done successfully' in line or 'Status <DONE>' in line:
                    logger.debug('bjobs detected job completed for job: {}'.format(job))
                    return 0
                else:
                    if 'New job is waiting for scheduling' in line:
                        logger.debug('bjobs detected job pending scheduling for job: {}'.format(job))
                        return
                    else:
                        if 'PENDING REASONS' in line or 'Status <PEND>' in line:
                            logger.debug('bjobs detected job pending for job: {}'.format(job))
                            return
                        if 'Exited with exit code' in line:
                            exit = int(line[line.find('Exited with exit code ') + 22:].split('.')[0])
                            logger.error('bjobs detected job exit code {} for job {}'.format(exit, job))
                            return exit
                    if 'Completed <exit>' in line:
                        logger.error('bjobs detected job failed for job: {}'.format(job))
                        return 1
                if line.find('Started on ') > -1 or 'Status <RUN>' in line:
                    started = 1

            if started == 1:
                logger.debug('bjobs detected job started but not completed: {}'.format(job))
                return
            logger.debug('bjobs failed to detect job - trying bacct: {}'.format(job))
            args = [
             'bacct', '-l', str(job)]
            stdout = call_command(args)
            process_output = stdout.split('\n')
            for line in process_output:
                if line.find('Completed <done>') > -1 or line.find('<DONE>') > -1:
                    logger.debug('Detected job completed for job: {}'.format(job))
                    return 0
                if line.find('Completed <exit>') > -1 or line.find('<EXIT>') > -1:
                    logger.error('Detected job failed for job: {}'.format(job))
                    return 1

            logger.debug("Can't determine exit code for job or job still running: {}".format(job))

        def prepareBsub(self, cpu, mem, jobID):
            """
            Make a bsub commandline to execute.

            params:
              cpu: number of cores needed
              mem: number of bytes of memory needed
              jobID: ID number of the job
            """
            if mem:
                if per_core_reservation():
                    mem = float(mem) / 1073741824 / math.ceil(cpu)
                    mem_resource = parse_memory_resource(mem)
                    mem_limit = parse_memory_limit(mem)
                else:
                    mem = old_div(float(mem), 1073741824)
                    mem_resource = parse_memory_resource(mem)
                    mem_limit = parse_memory_limit(mem)
                bsubMem = ['-R',
                 'select[mem > {m}] rusage[mem={m}]'.format(m=mem_resource),
                 '-M', str(mem_limit)]
            else:
                bsubMem = []
            bsubCpu = [] if cpu is None else ['-n', str(math.ceil(cpu))]
            bsubline = ['bsub', '-cwd', '.', '-J', 'toil_job_{}'.format(jobID)]
            bsubline.extend(bsubMem)
            bsubline.extend(bsubCpu)
            stdoutfile = self.boss.formatStdOutErrPath(jobID, 'lsf', '%J', 'std_output')
            stderrfile = self.boss.formatStdOutErrPath(jobID, 'lsf', '%J', 'std_error')
            bsubline.extend(['-o', stdoutfile, '-e', stderrfile])
            lsfArgs = os.getenv('TOIL_LSF_ARGS')
            if lsfArgs:
                bsubline.extend(lsfArgs.split())
            return bsubline

    def getWaitDuration(self):
        """We give LSF a second to catch its breath (in seconds)"""
        return 8

    @classmethod
    def obtainSystemConstants(cls):
        stdout = call_command(['lshosts'])
        line = stdout.split('\n')[0]
        items = line.strip().split()
        num_columns = len(items)
        cpu_index = None
        mem_index = None
        for i in range(num_columns):
            if items[i] == 'ncpus':
                cpu_index = i
            else:
                if items[i] == 'maxmem':
                    mem_index = i

        if cpu_index is None or mem_index is None:
            raise RuntimeError('lshosts command does not return ncpus or maxmem columns')
        maxCPU = 0
        maxMEM = MemoryString('0')
        for line in stdout.split('\n')[1:]:
            items = line.strip().split()
            if not items:
                continue
            if len(items) < num_columns:
                raise RuntimeError('lshosts output has a varying number of columns')
            if items[cpu_index] != '-':
                if int(items[cpu_index]) > int(maxCPU):
                    maxCPU = int(items[cpu_index])
                if items[mem_index] != '-' and MemoryString(items[mem_index]) > maxMEM:
                    maxMEM = MemoryString(items[mem_index])

        if maxCPU is 0 or maxMEM is 0:
            raise RuntimeError('lshosts returns null ncpus or maxmem info')
        logger.debug('Got the maxMEM: {}'.format(maxMEM))
        logger.debug('Got the maxCPU: {}'.format(maxCPU))
        return (
         maxCPU, maxMEM)