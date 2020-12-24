# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/scheduler/interfaces/torque.py
# Compiled at: 2015-04-13 16:10:51
from subprocess import Popen, PIPE
import re
from . import *
from ... import config

def is_running(pid):
    torqout = Popen('qstat -f %d' % pid, shell=True, stdout=PIPE, stderr=PIPE)
    if re.match('qstat: Unknown Job Id', str(torqout.stderr.read())):
        return False
    for x in torqout.stdout.readlines():
        if re.match('job_state', str(x).strip().split(' ')[0]):
            state = str(x).strip().split(' ')[(-1)]
            if str(state) in ('R', 'Q'):
                return True
            return False


def queue_run(JOB_DIR):
    command_qsub = JOB_DIR + '/' + get_cmdfile() + '.qsub'
    fh = open(JOB_DIR + '/' + get_cmdfile() + '.qsub', 'w')
    fh.write('%s %s %s %s' % (config.runner, get_cmdfile(), get_errfile(), get_resfile()))
    fh.close()
    cmd = 'qsub -d %s %s' % (JOB_DIR, command_qsub)
    out = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE).stdout.read()
    pid = out.strip().split('.')[0]
    return int(pid)