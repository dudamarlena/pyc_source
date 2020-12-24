# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/torque.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 10633 bytes
from __future__ import absolute_import
from __future__ import division
from builtins import str
from past.utils import old_div
import logging, os
from pipes import quote
import subprocess, time, math, sys, shlex, xml.etree.ElementTree as ET, tempfile
from toil.batchSystems import MemoryString
from toil.batchSystems.abstractGridEngineBatchSystem import AbstractGridEngineBatchSystem, UpdatedBatchJobInfo
logging.basicConfig(level=(logging.DEBUG))
logger = logging.getLogger(__name__)

class TorqueBatchSystem(AbstractGridEngineBatchSystem):

    class Worker(AbstractGridEngineBatchSystem.Worker):

        def __init__(self, newJobsQueue, updatedJobsQueue, killQueue, killedJobsQueue, boss):
            super(self.__class__, self).__init__(newJobsQueue, updatedJobsQueue, killQueue, killedJobsQueue, boss)
            self._version = self._pbsVersion()

        def _pbsVersion(self):
            """ Determines PBS/Torque version via pbsnodes
            """
            try:
                out = subprocess.check_output(['pbsnodes', '--version']).decode('utf-8')
                if 'PBSPro' in out:
                    logger.debug('PBS Pro proprietary Torque version detected')
                    self._version = 'pro'
                else:
                    logger.debug('Torque OSS version detected')
                    self._version = 'oss'
            except subprocess.CalledProcessError as e:
                if e.returncode != 0:
                    logger.error('Could not determine PBS/Torque version')

            return self._version

        def getRunningJobIDs(self):
            times = {}
            with self.runningJobsLock:
                currentjobs = dict((str(self.batchJobIDs[x][0].strip()), x) for x in self.runningJobs)
            logger.debug('getRunningJobIDs current jobs are: ' + str(currentjobs))
            if not currentjobs:
                return times
            else:
                jobids = sorted(list(currentjobs.keys()))
                if self._version == 'pro':
                    process = subprocess.Popen((['qstat', '-x'] + jobids), stdout=(subprocess.PIPE))
                else:
                    if self._version == 'oss':
                        process = subprocess.Popen((['qstat'] + jobids), stdout=(subprocess.PIPE))
                stdout, stderr = process.communicate()
                for currline in stdout.decode('utf-8').split('\n'):
                    items = currline.strip().split()
                    if items:
                        jobid = items[0].strip()
                        if jobid in currentjobs:
                            logger.debug('getRunningJobIDs job status for is: ' + items[4])
                        if jobid in currentjobs:
                            if items[4] == 'R':
                                walltime = items[3]
                                logger.debug('getRunningJobIDs qstat reported walltime is: ' + walltime)
                                if walltime == '0':
                                    walltime = time.mktime(time.strptime(walltime, '%S'))
                                else:
                                    walltime = time.mktime(time.strptime(walltime, '%H:%M:%S'))
                            times[currentjobs[jobid]] = walltime

                logger.debug('Job times from qstat are: ' + str(times))
                return times

        def getUpdatedBatchJob(self, maxWait):
            try:
                logger.debug('getUpdatedBatchJob: Job updates')
                item = self.updatedJobsQueue.get(timeout=maxWait)
                self.updatedJobsQueue.task_done()
                jobID, retcode = self.jobIDs[item.jobID], item.exitStatus
                self.currentjobs -= {self.jobIDs[item.jobID]}
            except Empty:
                logger.debug('getUpdatedBatchJob: Job queue is empty')
            else:
                return UpdatedBatchJobInfo(jobID=jobID, exitStatus=retcode, wallTime=None, exitReason=None)

        def killJob(self, jobID):
            subprocess.check_call(['qdel', self.getBatchSystemID(jobID)])

        def prepareSubmission(self, cpu, memory, jobID, command, jobName):
            return self.prepareQsub(cpu, memory, jobID) + [self.generateTorqueWrapper(command, jobID)]

        def submitJob(self, subLine):
            process = subprocess.Popen(subLine, stdout=(subprocess.PIPE))
            so, se = process.communicate()
            return so

        def getJobExitCode(self, torqueJobID):
            if self._version == 'pro':
                args = [
                 'qstat', '-x', '-f', str(torqueJobID).split('.')[0]]
            else:
                if self._version == 'oss':
                    args = [
                     'qstat', '-f', str(torqueJobID).split('.')[0]]
            process = subprocess.Popen(args, stdout=(subprocess.PIPE), stderr=(subprocess.STDOUT))
            for line in process.stdout:
                line = line.strip()
                if line.startswith('failed') or line.startswith('FAILED') and int(line.split()[1]) == 1:
                    return 1
                if line.startswith('exit_status') or line.startswith('Exit_status'):
                    status = line.split(' = ')[1]
                    logger.debug('Exit Status: ' + status)
                    return int(status)
                if 'unknown job id' in line.lower():
                    logger.debug('Batch system no longer remembers about job {}'.format(torqueJobID))
                    return 0

        def prepareQsub(self, cpu, mem, jobID):
            qsubline = [
             'qsub', '-S', '/bin/sh', '-V', '-N', 'toil_job_{}'.format(jobID)]
            if self.boss.environment:
                qsubline.append('-v')
                qsubline.append(','.join(k + '=' + quote(os.environ[k] if v is None else v) for k, v in self.boss.environment.items()))
            reqline = list()
            if mem is not None:
                memStr = str(old_div(mem, 1024)) + 'K'
                reqline.append('mem=' + memStr)
            if cpu is not None:
                if math.ceil(cpu) > 1:
                    reqline.append('nodes=1:ppn=' + str(int(math.ceil(cpu))))
            reqlineEnv = os.getenv('TOIL_TORQUE_REQS')
            if reqlineEnv is not None:
                logger.debug('Additional Torque resource requirements appended to qsub from TOIL_TORQUE_REQS env. variable: {}'.format(reqlineEnv))
                if 'mem=' in reqlineEnv or 'nodes=' in reqlineEnv or 'ppn=' in reqlineEnv:
                    raise ValueError("Incompatible resource arguments ('mem=', 'nodes=', 'ppn='): {}".format(reqlineEnv))
                reqline.append(reqlineEnv)
            if reqline:
                qsubline += ['-l', ','.join(reqline)]
            arglineEnv = os.getenv('TOIL_TORQUE_ARGS')
            if arglineEnv is not None:
                logger.debug('Native Torque options appended to qsub from TOIL_TORQUE_ARGS env. variable: {}'.format(arglineEnv))
                if 'mem=' in arglineEnv or 'nodes=' in arglineEnv or 'ppn=' in arglineEnv:
                    raise ValueError("Incompatible resource arguments ('mem=', 'nodes=', 'ppn='): {}".format(arglineEnv))
                qsubline += shlex.split(arglineEnv)
            return qsubline

        def generateTorqueWrapper(self, command, jobID):
            """
            A very simple script generator that just wraps the command given; for
            now this goes to default tempdir
            """
            stdoutfile = self.boss.formatStdOutErrPath(jobID, 'torque', '$PBS_JOBID', 'std_output')
            stderrfile = self.boss.formatStdOutErrPath(jobID, 'torque', '$PBS_JOBID', 'std_error')
            _, tmpFile = tempfile.mkstemp(suffix='.sh', prefix='torque_wrapper')
            fh = open(tmpFile, 'w')
            fh.write('#!/bin/sh\n')
            fh.write('#PBS -o {}\n'.format(stdoutfile))
            fh.write('#PBS -e {}\n'.format(stderrfile))
            fh.write('cd $PBS_O_WORKDIR\n\n')
            fh.write(command + '\n')
            fh.close
            return tmpFile

    @classmethod
    def obtainSystemConstants(cls):
        logger.debug('PBS/Torque does not need obtainSystemConstants to assess global cluster resources.')
        return (None, None)