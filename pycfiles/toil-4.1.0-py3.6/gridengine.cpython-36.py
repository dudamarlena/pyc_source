# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/gridengine.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 8445 bytes
from __future__ import absolute_import
from __future__ import division
from builtins import map
from builtins import str
from builtins import range
from past.utils import old_div
import logging, os
from pipes import quote
from toil.lib.misc import call_command, CalledProcessErrorStderr
import time, math
from six.moves.queue import Empty, Queue
from six import iteritems
from toil.batchSystems import MemoryString
from toil.batchSystems.abstractGridEngineBatchSystem import AbstractGridEngineBatchSystem
logger = logging.getLogger(__name__)

class GridEngineBatchSystem(AbstractGridEngineBatchSystem):

    class Worker(AbstractGridEngineBatchSystem.Worker):
        __doc__ = '\n        Grid Engine-specific AbstractGridEngineWorker methods\n        '

        def getRunningJobIDs(self):
            times = {}
            with self.runningJobsLock:
                currentjobs = dict((str(self.batchJobIDs[x][0]), x) for x in self.runningJobs)
            stdout = call_command(['qstat'])
            for currline in stdout.split('\n'):
                items = currline.strip().split()
                if items and items[0] in currentjobs and items[4] == 'r':
                    jobstart = ' '.join(items[5:7])
                    jobstart = time.mktime(time.strptime(jobstart, '%m/%d/%Y %H:%M:%S'))
                    times[currentjobs[items[0]]] = time.time() - jobstart

            return times

        def killJob(self, jobID):
            call_command(['qdel', self.getBatchSystemID(jobID)])

        def prepareSubmission(self, cpu, memory, jobID, command, jobName):
            return self.prepareQsub(cpu, memory, jobID) + [command]

        def submitJob(self, subLine):
            stdout = call_command(subLine)
            output = stdout.split('\n')[0].strip()
            result = int(output)
            return result

        def getJobExitCode(self, sgeJobID):
            """
            Get job exist code, checking both qstat and qacct.  Return None if
            still running.  Higher level should retry on
            CalledProcessErrorStderr, for the case the job has finished and
            qacct result is stale.
            """
            job, task = sgeJobID, None
            if '.' in sgeJobID:
                job, task = sgeJobID.split('.', 1)
            elif not task is None:
                raise AssertionError('task ids not currently support by qstat logic below')
            try:
                call_command(['qstat', '-j', str(job)])
                return
            except CalledProcessErrorStderr as ex:
                if 'Following jobs do not exist' not in ex.stderr:
                    raise

            args = [
             'qacct', '-j', str(job)]
            if task is not None:
                args.extend(['-t', str(task)])
            stdout = call_command(args)
            for line in stdout.split('\n'):
                if line.startswith('failed'):
                    if int(line.split()[1]) == 1:
                        return 1
                    elif line.startswith('exit_status'):
                        logger.debug('Exit Status: %r', line.split()[1])
                        return int(line.split()[1])

        def prepareQsub(self, cpu, mem, jobID):
            qsubline = [
             'qsub', '-V', '-b', 'y', '-terse', '-j', 'y', '-cwd',
             '-N', 'toil_job_' + str(jobID)]
            if self.boss.environment:
                qsubline.append('-v')
                qsubline.append(','.join(k + '=' + quote(os.environ[k] if v is None else v) for k, v in self.boss.environment.items()))
            reqline = list()
            sgeArgs = os.getenv('TOIL_GRIDENGINE_ARGS')
            if mem is not None:
                memStr = str(old_div(mem, 1024)) + 'K'
                if not self.boss.config.manualMemArgs:
                    reqline += ['vf=' + memStr, 'h_vmem=' + memStr]
                elif self.boss.config.manualMemArgs:
                    if not sgeArgs:
                        raise ValueError('--manualMemArgs set to True, but TOIL_GRIDGENGINE_ARGS is not set.Please set TOIL_GRIDGENGINE_ARGS to specify memory allocation for your system.  Default adds the arguments: vf=<mem> h_vmem=<mem> to qsub.')
            if len(reqline) > 0:
                qsubline.extend(['-hard', '-l', ','.join(reqline)])
            if sgeArgs:
                sgeArgs = sgeArgs.split()
                for arg in sgeArgs:
                    if arg.startswith(('vf=', 'hvmem=', '-pe')):
                        raise ValueError('Unexpected CPU, memory or pe specifications in TOIL_GRIDGENGINE_ARGs: %s' % arg)

                qsubline.extend(sgeArgs)
            if os.getenv('TOIL_GRIDENGINE_PE') is not None:
                peCpu = int(math.ceil(cpu)) if cpu is not None else 1
                qsubline.extend(['-pe', os.getenv('TOIL_GRIDENGINE_PE'), str(peCpu)])
            else:
                if cpu is not None:
                    if cpu > 1:
                        raise RuntimeError('must specify PE in TOIL_GRIDENGINE_PE environment variable when using multiple CPUs. Run qconf -spl and your local documentation for possible values')
            stdoutfile = self.boss.formatStdOutErrPath(jobID, 'gridengine', '$JOB_ID', 'std_output')
            stderrfile = self.boss.formatStdOutErrPath(jobID, 'gridengine', '$JOB_ID', 'std_error')
            qsubline.extend(['-o', stdoutfile, '-e', stderrfile])
            return qsubline

    @classmethod
    def getWaitDuration(cls):
        return 1

    @classmethod
    def obtainSystemConstants(cls):
        lines = call_command(['qhost']).strip().split('\n')
        items = lines[0].strip().split()
        num_columns = len(items)
        cpu_index = None
        mem_index = None
        for i in range(num_columns):
            if items[i] == 'NCPU':
                cpu_index = i
            else:
                if items[i] == 'MEMTOT':
                    mem_index = i

        if cpu_index is None or mem_index is None:
            raise RuntimeError('qhost command does not return NCPU or MEMTOT columns')
        maxCPU = 0
        maxMEM = MemoryString('0')
        for line in lines[2:]:
            items = line.strip().split()
            if len(items) < num_columns:
                raise RuntimeError('qhost output has a varying number of columns')
            if items[cpu_index] != '-':
                if int(items[cpu_index]) > maxCPU:
                    maxCPU = int(items[cpu_index])
                if items[mem_index] != '-' and MemoryString(items[mem_index]) > maxMEM:
                    maxMEM = MemoryString(items[mem_index])

        if maxCPU is 0 or maxMEM is 0:
            raise RuntimeError('qhost returned null NCPU or MEMTOT info')
        return (
         maxCPU, maxMEM)