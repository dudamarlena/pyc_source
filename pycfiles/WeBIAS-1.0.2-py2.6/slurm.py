# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/scheduler/interfaces/slurm.py
# Compiled at: 2015-04-13 16:10:51
from subprocess import Popen, PIPE
import re
from . import *
from ... import config

def is_running(pid):
    squeue = config.get_default('Scheduler', 'squeue', 'squeue')
    query_res = Popen('%s -j %d' % (squeue, pid), shell=True, stdout=PIPE, stderr=PIPE)
    if re.match('slurm_load_jobs error: Invalid job id specified', str(query_res.stderr.read())):
        return False
    for x in query_res.stdout.readlines():
        (jobid, part, name, user, state, time, nodes, nodelist) = x.split()
        try:
            jobid = int(jobid)
        except ValueError:
            pass
        else:
            if jobid == pid:
                if str(state) not in ('CA', 'CD', 'F', 'TO'):
                    return True
                else:
                    return False

    return False


def queue_run(JOB_DIR):
    command_qsub = JOB_DIR + '/' + get_cmdfile() + '.sbatch'
    fh = open(JOB_DIR + '/' + get_cmdfile() + '.sbatch', 'w')
    fh.write('#!/bin/sh\n')
    fh.write('%s %s %s %s' % (config.runner, get_cmdfile(), get_errfile(), get_resfile()))
    fh.close()
    sbatch = config.get_default('Scheduler', 'sbatch', 'sbatch')
    cmd = '%s -D %s %s' % (sbatch, JOB_DIR, command_qsub)
    proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    out = proc.stdout.read()
    err = proc.stderr.read()
    pid = out.strip().split(' ')[(-1)]
    return int(pid)