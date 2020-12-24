# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jobwrapper/slurm_wrapper.py
# Compiled at: 2018-09-07 05:20:19
# Size of source mod 2**32: 1338 bytes
import subprocess as sbp, time

def launch_job():
    jobID = sbp.check_output(['sbatch', '--parsable', 'LPPic2D'])
    jobID = jobID.decode('ascii')[:-1]
    print('Job launched with number : ', jobID)
    return jobID


def return_status(jobId):
    data = sbp.check_output(['sacct', '-j', str(jobId), '-n', '-o', 'state']).decode('ascii')
    lines = data.splitlines()
    if len(lines) < 1:
        print('job not found')
        print(jobId)
        print(lines)
        return -1
    else:
        jobstatus = lines[0].split()[0]
        print('the statis is: ', jobstatus)
        return jobstatus


def exist_job(jobID):
    """check if a job existe in the slurm queue"""
    data = sbp.check_output(['sacct', '-j', jobID, '-n', '-o', 'state'])
    data = data.decode('ascii')
    lines = data.splitlines()
    if len(lines) < 1:
        return False
    else:
        jobstatus = return_status(jobID)
        if jobstatus == 'PENDING' or jobstatus == 'RUNNING':
            return True
        return False


def kill_job(jobID):
    """kill a job"""
    print('~~~~~~~~~~~~~~~~~')
    if exist_job(jobID):
        print('Killing the job ')
        sbp.call(['scancel', jobID])
    else:
        print(f"the Job id={jobID} do not exist, we cannot kill it")
    time.sleep(1)