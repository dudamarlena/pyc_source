# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/scheduler/interfaces/batch.py
# Compiled at: 2015-04-13 16:10:51
from subprocess import Popen, PIPE
from . import *
from ... import config
import sys

def is_running(pid):
    var = Popen('ps %s | wc -l' % pid, shell=True, stdout=PIPE).stdout.read().strip()
    if int(var) - 1 == 0:
        return False
    else:
        return True


def queue_run(JOB_DIR):
    pid = Popen([config.runner, get_cmdfile(), get_errfile(), get_resfile()], cwd=JOB_DIR).pid
    return pid