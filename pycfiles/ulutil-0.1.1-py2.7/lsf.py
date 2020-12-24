# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/ulutil/lsf.py
# Compiled at: 2014-12-19 21:46:45
import os, subprocess, time

def submit_to_LSF(queue, LSFopfile, duration, cmd_to_submit, mem_usage=None):
    cmd_to_submit = "'%s'" % cmd_to_submit.strip('"')
    LSF_params = {'LSFoutput': LSFopfile, 'queue': queue, 
       'duration': duration}
    LSF_cmd = 'rbsub -q%(queue)s -W %(duration)s -o%(LSFoutput)s' % LSF_params
    if mem_usage != None:
        LSF_cmd += ' -R "rusage[mem=%d]"' % mem_usage
    cmd = (' ').join([LSF_cmd, cmd_to_submit])
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    return p.stdout.read().split('<')[1].split('>')[0]


def parse_LSF_report(filename):
    jobID = -1
    finished = False
    succeeded = False
    ip = open(filename)
    for line in ip:
        if line.startswith('Subject:') and 'Job' in line:
            jobID = line.split()[2].rstrip(':')
            if 'Done' in line or 'Exited' in line:
                finished = True
        if 'TERM_REQUEUE_ADMIN' in line:
            finished = False
        if 'Successfully completed.' in line:
            succeeded = True

    ip.close()
    return (
     jobID, finished, succeeded)


def wait_for_LSF_jobs(jobIDs, logfiles, interval=120):
    while len(jobIDs) > 0:
        time.sleep(interval)
        for logfile in logfiles:
            if not os.path.exists(logfile):
                continue
            jobID, finished, succeeded = parse_LSF_report(logfile)
            if jobID != -1 and finished and succeeded:
                jobIDs.remove(jobID)
                logfiles.remove(logfile)
            elif jobID != -1 and finished and not succeeded:
                raise ValueError, 'Job %s failed' % jobID