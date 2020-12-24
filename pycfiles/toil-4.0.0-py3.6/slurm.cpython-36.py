# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/slurm.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 11518 bytes
from __future__ import absolute_import
from __future__ import division
from builtins import str
from past.utils import old_div
import logging, os
from pipes import quote
import subprocess, time, math
from six.moves.queue import Empty, Queue
from six import iteritems
from toil.batchSystems import MemoryString
from toil.batchSystems.abstractGridEngineBatchSystem import AbstractGridEngineBatchSystem
logger = logging.getLogger(__name__)

class SlurmBatchSystem(AbstractGridEngineBatchSystem):

    class Worker(AbstractGridEngineBatchSystem.Worker):

        def getRunningJobIDs(self):
            times = {}
            with self.runningJobsLock:
                currentjobs = dict((str(self.batchJobIDs[x][0]), x) for x in self.runningJobs)
            lines = subprocess.check_output(['squeue', '-h', '--format', '%i %t %M']).decode('utf-8').split('\n')
            for line in lines:
                values = line.split()
                if len(values) < 3:
                    continue
                slurm_jobid, state, elapsed_time = values
                if slurm_jobid in currentjobs and state == 'R':
                    seconds_running = self.parse_elapsed(elapsed_time)
                    times[currentjobs[slurm_jobid]] = seconds_running

            return times

        def killJob(self, jobID):
            subprocess.check_call(['scancel', self.getBatchSystemID(jobID)])

        def prepareSubmission(self, cpu, memory, jobID, command, jobName):
            return self.prepareSbatch(cpu, memory, jobID, jobName) + ['--wrap={}'.format(command)]

        def submitJob(self, subLine):
            try:
                output = subprocess.check_output(subLine, stderr=(subprocess.STDOUT)).decode('utf-8')
                result = int(output.strip().split()[(-1)])
                logger.debug('sbatch submitted job %d', result)
                return result
            except OSError as e:
                logger.error('sbatch command failed')
                raise e

        def getJobExitCode(self, slurmJobID):
            logger.debug('Getting exit code for slurm job %d', int(slurmJobID))
            state, rc = self._getJobDetailsFromSacct(slurmJobID)
            if rc == -999:
                state, rc = self._getJobDetailsFromScontrol(slurmJobID)
            logger.debug('s job state is %s', state)
            if state in ('PENDING', 'RUNNING', 'CONFIGURING', 'COMPLETING', 'RESIZING',
                         'SUSPENDED'):
                return
            else:
                return rc

        def _getJobDetailsFromSacct(self, slurmJobID):
            args = [
             'sacct',
             '-n',
             '-j', str(slurmJobID),
             '--format', 'State,ExitCode',
             '-P',
             '-S', '1970-01-01']
            process = subprocess.Popen(args, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
            rc = process.returncode
            if rc != 0:
                return (None, -999)
            for line in process.stdout:
                values = line.decode('utf-8').strip().split('|')
                if len(values) < 2:
                    continue
                state, exitcode = values
                logger.debug('sacct job state is %s', state)
                status, signal = [int(n) for n in exitcode.split(':')]
                if signal > 0:
                    status = 128 + signal
                logger.debug('sacct exit code is %s, returning status %d', exitcode, status)
                return (state, status)

            logger.debug('Did not find exit code for job in sacct output')

        def _getJobDetailsFromScontrol(self, slurmJobID):
            args = [
             'scontrol',
             'show',
             'job',
             str(slurmJobID)]
            process = subprocess.Popen(args, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
            job = dict()
            for line in process.stdout:
                values = line.decode('utf-8').strip().split()
                if len(values) > 0:
                    if values[0] == 'slurm_load_jobs':
                        return (None, None)
                for v in values:
                    bits = v.split('=')
                    job[bits[0]] = bits[1]

            state = job['JobState']
            try:
                exitcode = job['ExitCode']
                if exitcode is not None:
                    status, signal = [int(n) for n in exitcode.split(':')]
                    if signal > 0:
                        status = 128 + signal
                    logger.debug('scontrol exit code is %s, returning status %d', exitcode, status)
                    rc = status
                else:
                    rc = None
            except KeyError:
                rc = None

            return (state, rc)

        def prepareSbatch(self, cpu, mem, jobID, jobName):
            sbatch_line = [
             'sbatch', '-J', 'toil_job_{}_{}'.format(jobID, jobName)]
            if self.boss.environment:
                argList = []
                for k, v in self.boss.environment.items():
                    quoted_value = quote(os.environ[k] if v is None else v)
                    argList.append('{}={}'.format(k, quoted_value))

                sbatch_line.append('--export=' + ','.join(argList))
            if mem is not None:
                sbatch_line.append('--mem={}'.format(old_div(int(mem), 1048576)))
            if cpu is not None:
                sbatch_line.append('--cpus-per-task={}'.format(int(math.ceil(cpu))))
            stdoutfile = self.boss.formatStdOutErrPath(jobID, 'slurm', '%j', 'std_output')
            stderrfile = self.boss.formatStdOutErrPath(jobID, 'slurm', '%j', 'std_error')
            sbatch_line.extend(['-o', stdoutfile, '-e', stderrfile])
            nativeConfig = os.getenv('TOIL_SLURM_ARGS')
            if nativeConfig is not None:
                logger.debug('Native SLURM options appended to sbatch from TOIL_SLURM_ARGS env. variable: {}'.format(nativeConfig))
                if '--mem' in nativeConfig or '--cpus-per-task' in nativeConfig:
                    raise ValueError('Some resource arguments are incompatible: {}'.format(nativeConfig))
                sbatch_line.extend(nativeConfig.split())
            return sbatch_line

        def parse_elapsed(self, elapsed):
            total_seconds = 0
            try:
                elapsed = elapsed.replace('-', ':').split(':')
                elapsed.reverse()
                seconds_per_unit = [1, 60, 3600, 86400]
                for index, multiplier in enumerate(seconds_per_unit):
                    if index < len(elapsed):
                        total_seconds += multiplier * int(elapsed[index])

            except ValueError:
                pass

            return total_seconds

    @classmethod
    def getWaitDuration(cls):
        wait_duration_seconds = 1
        lines = subprocess.check_output(['scontrol', 'show', 'config']).decode('utf-8').split('\n')
        time_value_list = []
        for line in lines:
            values = line.split()
            if len(values) > 0:
                if values[0] == 'SchedulerTimeSlice' or values[0] == 'AcctGatherNodeFreq':
                    time_name = values[values.index('=') + 1:][1]
                    time_value = int(values[values.index('=') + 1:][0])
                    if time_name == 'min':
                        time_value *= 60
                time_value_list.append(math.ceil(time_value * 1.2))

        return max(time_value_list)

    @classmethod
    def obtainSystemConstants(cls):
        max_cpu = 0
        max_mem = MemoryString('0')
        lines = subprocess.check_output(['sinfo', '-Nhe', '--format', '%m %c']).decode('utf-8').split('\n')
        for line in lines:
            values = line.split()
            if len(values) < 2:
                continue
            mem, cpu = values
            max_cpu = max(max_cpu, int(cpu))
            max_mem = max(max_mem, MemoryString(mem + 'M'))

        if max_cpu == 0 or max_mem.byteVal() == 0:
            RuntimeError('sinfo did not return memory or cpu info')
        return (
         max_cpu, max_mem)