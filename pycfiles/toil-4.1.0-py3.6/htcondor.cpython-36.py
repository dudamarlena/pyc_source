# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/htcondor.py
# Compiled at: 2020-05-07 00:32:15
# Size of source mod 2**32: 14206 bytes
from __future__ import absolute_import
from builtins import str
import sys, os, logging, time, math
from toil.batchSystems.abstractGridEngineBatchSystem import AbstractGridEngineBatchSystem
import htcondor, classad
logger = logging.getLogger(__name__)

class HTCondorBatchSystem(AbstractGridEngineBatchSystem):

    class Worker(AbstractGridEngineBatchSystem.Worker):

        def createJobs(self, newJob):
            activity = False
            if newJob is not None:
                self.waitingJobs.append(newJob)
            while len(self.waitingJobs) > 0 and len(self.runningJobs) < int(self.boss.config.maxLocalJobs):
                activity = True
                jobID, cpu, memory, disk, jobName, command = self.waitingJobs.pop(0)
                submitObj = self.prepareSubmission(cpu, memory, disk, jobID, jobName, command)
                logger.debug('Submitting %r', submitObj)
                batchJobID = self.submitJob(submitObj)
                logger.debug('Submitted job %s', str(batchJobID))
                self.batchJobIDs[jobID] = (
                 batchJobID, None)
                self.runningJobs.add(jobID)

            return activity

        def prepareSubmission(self, cpu, memory, disk, jobID, jobName, command):
            cpu = int(math.ceil(cpu))
            memory = float(memory) / 1024
            disk = float(disk) / 1024
            stdoutfile = self.boss.formatStdOutErrPath(jobID, 'htcondor', '$(cluster)', 'std_output')
            stderrfile = self.boss.formatStdOutErrPath(jobID, 'htcondor', '$(cluster)', 'std_error')
            condorlogfile = self.boss.formatStdOutErrPath(jobID, 'htcondor', '$(cluster)', 'job_events')
            submit_parameters = {'executable':'/bin/sh', 
             'transfer_executable':'False', 
             'arguments':'"-c \'{0}\'"'.format(command).encode('utf-8'), 
             'environment':self.getEnvString(), 
             'getenv':'True', 
             'should_transfer_files':'Yes', 
             'output':stdoutfile, 
             'error':stderrfile, 
             'log':condorlogfile, 
             'request_cpus':'{0}'.format(cpu), 
             'request_memory':'{0:.3f}KB'.format(memory), 
             'request_disk':'{0:.3f}KB'.format(disk), 
             'leave_in_queue':'(JobStatus == 4)', 
             '+IsToilJob':'True', 
             '+ToilJobID':'{0}'.format(jobID), 
             '+ToilJobName':'"{0}"'.format(jobName), 
             '+ToilJobKilled':'False'}
            extra_parameters = os.getenv('TOIL_HTCONDOR_PARAMS')
            if extra_parameters is not None:
                logger.debug('Extra HTCondor parameters added to submit file from TOIL_HTCONDOR_PARAMS env. variable: {}'.format(extra_parameters))
                for parameter, value in [parameter_value.split('=', 1) for parameter_value in extra_parameters.split(';')]:
                    parameter = parameter.strip()
                    value = value.strip()
                    if parameter in submit_parameters:
                        raise ValueError('Some extra parameters are incompatible: {}'.format(extra_parameters))
                    submit_parameters[parameter] = value

            return htcondor.Submit(submit_parameters)

        def submitJob(self, submitObj):
            schedd = self.connectSchedd()
            with schedd.transaction() as (txn):
                batchJobID = submitObj.queue(txn)
            return batchJobID

        def getRunningJobIDs(self):
            requirements = '(JobStatus == 2) && (IsToilJob)'
            projection = ['ClusterId', 'ToilJobID', 'EnteredCurrentStatus']
            schedd = self.connectSchedd()
            ads = schedd.xquery(requirements=requirements, projection=projection)
            batchJobIDs = [batchJobID for batchJobID, task in self.batchJobIDs.values()]
            job_runtimes = {}
            for ad in ads:
                batchJobID = int(ad['ClusterId'])
                jobID = int(ad['ToilJobID'])
                if batchJobID not in batchJobIDs:
                    continue
                runtime = time.time() - ad['EnteredCurrentStatus']
                job_runtimes[jobID] = runtime

            return job_runtimes

        def killJob(self, jobID):
            batchJobID = self.batchJobIDs[jobID][0]
            logger.debug('Killing HTCondor job {0}'.format(batchJobID))
            schedd = self.connectSchedd()
            job_spec = '(ClusterId == {0})'.format(batchJobID)
            schedd.edit(job_spec, 'ToilJobKilled', 'True')

        def getJobExitCode(self, batchJobID):
            logger.debug('Getting exit code for HTCondor job {0}'.format(batchJobID))
            status = {1:'Idle', 
             2:'Running', 
             3:'Removed', 
             4:'Completed', 
             5:'Held', 
             6:'Transferring Output', 
             7:'Suspended'}
            requirements = '(ClusterId == {0})'.format(batchJobID)
            projection = ['JobStatus', 'ToilJobKilled', 'ExitCode',
             'HoldReason', 'HoldReasonSubCode']
            schedd = self.connectSchedd()
            ads = schedd.xquery(requirements=requirements, projection=projection)
            try:
                try:
                    ad = next(ads)
                except TypeError:
                    ad = ads.next()

            except StopIteration:
                logger.error('No HTCondor ads returned using constraint: {0}'.format(requirements))
                raise

            try:
                try:
                    next(ads)
                except TypeError:
                    ads.next()

            except StopIteration:
                pass
            else:
                logger.warning('Multiple HTCondor ads returned using constraint: {0}'.format(requirements))
            if ad['ToilJobKilled']:
                logger.debug('HTCondor job {0} was killed by Toil'.format(batchJobID))
                job_spec = 'ClusterId == {0}'.format(batchJobID)
                schedd.act(htcondor.JobAction.Remove, job_spec)
                return 1
            if status[ad['JobStatus']] == 'Completed':
                logger.debug('HTCondor job {0} completed with exit code {1}'.format(batchJobID, ad['ExitCode']))
                job_spec = 'ClusterId == {0}'.format(batchJobID)
                schedd.act(htcondor.JobAction.Remove, job_spec)
                return int(ad['ExitCode'])
            else:
                if status[ad['JobStatus']] == 'Held':
                    logger.error("HTCondor job {0} was held: '{1} (sub code {2})'".format(batchJobID, ad['HoldReason'], ad['HoldReasonSubCode']))
                    job_spec = 'ClusterId == {0}'.format(batchJobID)
                    schedd.act(htcondor.JobAction.Remove, job_spec)
                    return 1
                logger.debug('HTCondor job {0} has not completed (Status: {1})'.format(batchJobID, status[ad['JobStatus']]))
                return

        def connectSchedd(self):
            """Connect to HTCondor Schedd and return a Schedd object"""
            condor_host = os.getenv('TOIL_HTCONDOR_COLLECTOR')
            schedd_name = os.getenv('TOIL_HTCONDOR_SCHEDD')
            if condor_host and schedd_name:
                logger.debug('Connecting to HTCondor Schedd {0} using Collector at {1}'.format(schedd_name, condor_host))
                try:
                    schedd_ad = htcondor.Collector(condor_host).locate(htcondor.DaemonTypes.Schedd, schedd_name)
                except IOError:
                    logger.error('Could not connect to HTCondor Collector at {0}'.format(condor_host))
                    raise
                except ValueError:
                    logger.error('Could not find HTCondor Schedd with name {0}'.format(schedd_name))
                    raise

                schedd = htcondor.Schedd(schedd_ad)
            else:
                logger.debug('Connecting to HTCondor Schedd on local machine')
                schedd = htcondor.Schedd()
            try:
                schedd.xquery(limit=0)
            except RuntimeError:
                logger.error('Could not connect to HTCondor Schedd')
                raise

            return schedd

        def getEnvString(self):
            """Build an environment string that a HTCondor Submit object can use.

            For examples of valid strings, see:
            http://research.cs.wisc.edu/htcondor/manual/current/condor_submit.html#man-condor-submit-environment

            """
            env_items = []
            if self.boss.environment:
                for key, value in self.boss.environment.items():
                    env_string = key + '='
                    env_string += "'" + value.replace("'", "''").replace('"', '""') + "'"
                    env_items.append(env_string)

            return '"' + ' '.join(env_items) + '"'

    def issueBatchJob(self, jobNode):
        localID = self.handleLocalJob(jobNode)
        if localID:
            return localID
        else:
            self.checkResourceRequest(jobNode.memory, jobNode.cores, jobNode.disk)
            jobID = self.getNextJobID()
            self.currentJobs.add(jobID)
            self.newJobsQueue.put((jobID, jobNode.cores, jobNode.memory, jobNode.disk, jobNode.jobName, jobNode.command))
            logger.debug('Issued the job command: %s with job id: %s ', jobNode.command, str(jobID))
            return jobID

    @classmethod
    def obtainSystemConstants(cls):
        max_cpu = 4
        max_mem = 4000000000.0
        return (max_cpu, max_mem)