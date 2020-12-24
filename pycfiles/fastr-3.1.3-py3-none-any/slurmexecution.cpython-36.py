# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/executionplugins/slurmexecution.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 10947 bytes
import json, os, re, shlex, subprocess, sys, threading, time, fastr
from fastr import exceptions
from fastr.plugins.executionplugin import ExecutionPlugin
from fastr.execution.job import JobState
from fastr.helpers.classproperty import classproperty
SBATCH_SCRIPT_TEMPLATE = '#!/bin/bash\n#SBATCH --nodes=1\n#SBATCH --ntasks=1\n#SBATCH --cpus-per-task {cores}\n{memory}\n{time}\n{partition}\n#SBATCH --output {stdout}\n#SBATCH --error {stderr}\n{depends}\n{hold}\n\n{command}\n'

class SlurmExecution(ExecutionPlugin):
    __doc__ = '\n    '
    SQUEUE_FORMAT = '{"id": %.18i, "status": "%.2t"}'
    STATUS_MAPPING = {'PD':JobState.queued, 
     ' R':JobState.running, 
     'CA':JobState.cancelled, 
     'CF':JobState.running, 
     'CG':JobState.running, 
     'CD':JobState.finished, 
     ' F':JobState.failed, 
     'TO':JobState.queued, 
     'NF':JobState.failed, 
     'RV':JobState.cancelled, 
     'SE':JobState.failed}
    SBATCH = 'sbatch'
    SCANCEL = 'scancel'
    SQUEUE = 'squeue'
    SCONTROL = 'scontrol'
    SUPPORTS_DEPENDENCY = True
    SUPPORTS_CANCEL = True
    SUPPORTS_HOLD_RELEASE = True

    def __init__(self, finished_callback=None, cancelled_callback=None):
        super(SlurmExecution, self).__init__(finished_callback, cancelled_callback)
        self.check_interval = fastr.config.slurm_job_check_interval
        self.partition = fastr.config.slurm_partition
        self.running = True
        self.job_translation_table = dict()
        self.job_lookup_table = dict()
        fastr.log.debug('Creating job status checker')
        self.job_checker = threading.Thread(name='SlurmJobChecker-0', target=(self.job_status_check), args=())
        self.job_checker.daemon = True
        fastr.log.debug('Starting job status checker')
        self.job_checker.start()

    @classproperty
    def configuration_fields(cls):
        return {'slurm_job_check_interval':(
          int, 30, 'The interval in which the job checker will startto check for stale jobs'), 
         'slurm_partition':(
          str, '', 'The slurm partition to use')}

    @classmethod
    def test(cls):
        try:
            subprocess.check_output([cls.SBATCH, '--help'], stderr=(subprocess.STDOUT))
        except OSError:
            raise exceptions.FastrExecutableNotFoundError(cls.SBATCH)

        try:
            subprocess.check_output([cls.SQUEUE, '--help'], stderr=(subprocess.STDOUT))
        except OSError:
            raise exceptions.FastrExecutableNotFoundError(cls.SQUEUE)

        try:
            subprocess.check_output([cls.SCONTROL, '--help'], stderr=(subprocess.STDOUT))
        except OSError:
            raise exceptions.FastrExecutableNotFoundError(cls.SCONTROL)

        try:
            subprocess.check_output([cls.SCANCEL, '--help'], stderr=(subprocess.STDOUT))
        except OSError:
            raise exceptions.FastrExecutableNotFoundError(cls.SCANCEL)

    def cleanup(self):
        self.running = False
        super(SlurmExecution, self).cleanup()

    def _job_finished(self, result):
        pass

    def _queue_job(self, job):
        command = [
         sys.executable,
         os.path.join(fastr.config.executionscript),
         job.commandfile]
        command = ' '.join(shlex.quote(item) for item in command)
        depends = ''
        if job.hold_jobs:
            depend_jobs = [self.job_lookup_table.get(j, None) for j in job.hold_jobs]
            depend_jobs = [str(x) for x in depend_jobs if x is not None]
            if depend_jobs:
                depends = '#SBATCH --dependency=afterok:{}'.format(','.join(depend_jobs))
        else:
            if job.required_memory:
                required_memory = '#SBATCH --mem {}M'.format(job.required_memory)
            else:
                required_memory = ''
            if job.required_time:
                required_time = '#SBATCH --time {}'.format(job.required_time)
            else:
                required_time = ''
            if self.partition:
                partition = '#SBATCH --partition {}'.format(self.partition)
            else:
                partition = ''
            if job.status == JobState.hold:
                hold = '--hold'
            else:
                hold = ''
            sbatch_script = SBATCH_SCRIPT_TEMPLATE.format(cores=(job.required_cores or 1),
              memory=required_memory,
              time=required_time,
              partition=partition,
              stdout=(job.stdoutfile),
              stderr=(job.stderrfile),
              command=command,
              depends=depends,
              hold=hold)
            if fastr.config.debug:
                fastr.log.debug('USING SBATCH SCRIPT:\n{}'.format(sbatch_script))
            sbatch = subprocess.Popen([
             self.SBATCH],
              stdin=(subprocess.PIPE),
              stdout=(subprocess.PIPE),
              stderr=(subprocess.PIPE))
            stdout, stderr = sbatch.communicate(sbatch_script)
            match = re.search('Submitted batch job (\\d+)', stdout)
            if match:
                cl_job_id = int(match.group(1))
            else:
                fastr.log.error('Could not submit job, sbatch returned:\n{}\n{}'.format(stdout, stderr))
                job.status = JobState.execution_failed
                self.job_finished(job, errors=['FastrSlurmSubmitError',
                 stderr,
                 __file__,
                 'unknown'])
                return
        self.job_translation_table[cl_job_id] = job
        self.job_lookup_table[job.id] = cl_job_id

    def _cancel_job(self, job):
        """
        Cancel a given job

        :param job:
        """
        try:
            slurm_job_id = self.job_lookup_table.pop(job.id)
        except KeyError:
            fastr.log.info('Job {} not found in SLURM lookup'.format(job.id))
            return
        else:
            scancel_process = subprocess.Popen([self.SCANCEL, str(slurm_job_id)])
            stdout, stderr = scancel_process.communicate()
            if stderr:
                fastr.log.warning('Encountered error when cancelling job: {}'.format(job.id))
            try:
                del self.job_translation_table[slurm_job_id]
            except KeyError:
                pass

    def _hold_job(self, job):
        slurm_job_id = self.job_lookup_table.get(job.id, None)
        if slurm_job_id:
            scontrol_process = subprocess.Popen([self.SCONTROL, 'hold', str(slurm_job_id)])
            stdout, stderr = scontrol_process.communicate()
            if stderr:
                fastr.log.warning('Encountered error when holding job: {}'.format(job.id))
        else:
            fastr.log.error('Cannot hold job {}, cannot find the slurm id!'.format(job.id))

    def _release_job(self, job):
        slurm_job_id = self.job_lookup_table.get(job.id, None)
        if slurm_job_id:
            scontrol_process = subprocess.Popen([self.SCONTROL, 'release', str(slurm_job_id)])
            stdout, stderr = scontrol_process.communicate()
            if stderr:
                fastr.log.warning('Encountered error when releasing job: {}'.format(job.id))
        else:
            fastr.log.error('Cannot release job {}, cannot find the slurm id!'.format(job.id))

    def job_status_check(self):
        last_update = time.time()
        while self.running:
            if time.time() - last_update < self.check_interval:
                time.sleep(1)
            else:
                fastr.log.debug('Running job status check')
                last_update = time.time()
                cluster_job_ids = set(self.job_lookup_table.values() + self.job_translation_table.keys())
                command = [
                 self.SQUEUE,
                 '-o', self.SQUEUE_FORMAT,
                 '-j', ','.join(str(x) for x in cluster_job_ids)]
                squeue = subprocess.Popen(command, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
                stdout, stderr = squeue.communicate()
                job_info = {}
                for line in stdout.splitlines()[1:]:
                    if line.strip() == '':
                        pass
                    else:
                        job = json.loads(line)
                        job_info[job['id']] = job['status']

                for job_id in cluster_job_ids:
                    if job_id not in job_info:
                        job = self.job_translation_table.pop(job_id, None)
                        if job is not None:
                            try:
                                del self.job_lookup_table[job.id]
                            except KeyError:
                                fastr.log.warning('Found an inconsistency in the job_lookup_table, cannot find job to remove')

                        self.job_finished(job)
                    else:
                        job = self.job_translation_table[job_id]
                        status = self.STATUS_MAPPING.get(job_info[job_id], None)
                        if status is None:
                            fastr.log.info('Found a job with unknown state: {}'.format(job_info[job_id]))
                        else:
                            job.status = status